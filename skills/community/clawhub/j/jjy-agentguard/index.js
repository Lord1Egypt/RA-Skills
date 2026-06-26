/**
 * AgentGuard Plugin for OpenClaw
 *
 * 将 AgentGuard 安全引擎集成到 OpenClaw，代理所有工具调用：
 * - execute_command → 经 AgentGuard 规则引擎审核后执行
 * - read_file / write_file → 路径黑白名单 + 脱敏过滤
 * - list_directory → 目录访问控制
 * - http_request → 域名白名单过滤
 * - skill_check → Skill 白名单校验
 *
 * 所有操作记录到 AgentGuard 审计日志，Dashboard: http://127.0.0.1:19821
 *
 * Plugin 规范参考: https://docs.openclaw.ai/tools/plugin
 * Agent Tools 参考: https://docs.openclaw.ai/plugins/agent-tools
 */

import http from "http";

// --- 默认配置 (可被 openclaw.plugin.json configSchema 覆盖) ---
const DEFAULT_CONFIG = {
  daemonHost: "127.0.0.1",
  daemonPort: 19821,
  healthCheckInterval: 30,
  autoReconnect: true,
};

// --- 插件状态 ---
let pluginConfig = { ...DEFAULT_CONFIG };
let daemonConnected = false;
let healthCheckTimer = null;

// --- HTTP helper ---
function agRequest(method, path, body, customTimeout) {
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: pluginConfig.daemonHost,
      port: pluginConfig.daemonPort,
      path,
      method,
      timeout: customTimeout || (method === "GET" ? 5000 : 15000),
    };

    if (body) {
      opts.headers = {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(JSON.stringify(body)),
      };
    }

    const req = http.request(opts, (res) => {
      let chunks = "";
      res.on("data", (c) => (chunks += c));
      res.on("end", () => {
        try {
          const data = JSON.parse(chunks);
          // HTTP 4xx/5xx 视为业务错误
          if (res.statusCode >= 400) {
            resolve({ error: data.error || data.message || `HTTP ${res.statusCode}`, _status: res.statusCode });
          } else {
            resolve(data);
          }
        } catch {
          resolve({ raw: chunks, _status: res.statusCode });
        }
      });
    });
    req.on("error", reject);
    req.on("timeout", () => {
      req.destroy();
      reject(new Error("AgentGuard daemon 连接超时"));
    });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function agGet(path) {
  return agRequest("GET", path);
}
function agPost(path, body) {
  return agRequest("POST", path, body);
}

// --- AgentGuard tool proxy ---
async function callTool(toolName, params) {
  const res = await agPost("/api/tool/call", { tool: toolName, input: params });

  // If review required, return prompt for Agent to pause and retry
  if (res.review_required && res.audit_id) {
    const aid = res.audit_id;
    const timeout = res.timeout || 60;
    return {
      _needsApproval: true,
      text: [
        `⚠️ APPROVAL REQUIRED — 此操作需用户在 AgentGuard Dashboard 人工审批。`,
        ``,
        `📋 审批流程:`,
        `  1. 用户在 Dashboard 审批队列中 批准/拒绝 此操作`,
        `  2. 审批通过后，请使用完全相同的参数重新调用本工具，并额外添加参数 _audit_id: "${aid}"`,
        `  3. 若 ${timeout}s 内未审批则自动超时拒绝`,
        ``,
        `⏸️ 请暂停当前任务，告知用户需要审批，等用户确认后再重试。`,
        `Dashboard: http://${pluginConfig.daemonHost}:${pluginConfig.daemonPort}`,
      ].join('\n'),
    };
  }

  return res;
}

// --- Daemon 健康检查 ---
async function checkDaemonHealth(logger) {
  try {
    const status = await agGet("/api/status");
    if (status.version) {
      if (!daemonConnected) {
        daemonConnected = true;
        if (logger) logger.info(`[AgentGuard] daemon 已连接 v${status.version} mode=${status.mode}`);
      }
      return true;
    }
  } catch {
    if (daemonConnected) {
      daemonConnected = false;
      if (logger) logger.warn("[AgentGuard] daemon 连接断开");
    }
  }
  return false;
}

// --- 统一结果格式化 ---
function formatResult(res) {
  if (res.error) {
    return {
      content: [{ type: "text", text: `\ud83d\udeab AgentGuard \u62e6\u622a: ${res.error}` }],
      isError: true,
    };
  }
  if (res._needsApproval) {
    return { content: [{ type: "text", text: res.text }] };
  }
  const text = res.result || res.output || res.content || JSON.stringify(res, null, 2);
  return { content: [{ type: "text", text }] };
}

function formatError(e) {
  return {
    content: [{
      type: "text",
      text: `⚠️ AgentGuard daemon 未响应: ${e.message}\n` +
            `  启动命令: agentguard daemon start\n` +
            `  安装命令: 运行 skill 目录下的 setup.sh`,
    }],
    isError: true,
  };
}

// ====================================================
// Plugin entry point
// OpenClaw 插件标准接口: export default function(api)
// 参考: https://docs.openclaw.ai/plugins/agent-tools
// ====================================================
export default function (api) {
  // --- 读取插件配置 ---
  if (api.config) {
    pluginConfig = { ...DEFAULT_CONFIG, ...api.config };
  }
  const logger = api.logger || null;

  // --- 注册后台健康检查服务 ---
  // 参考: https://docs.openclaw.ai/tools/plugin#register-background-services
  if (api.registerService) {
    api.registerService({
      id: "agentguard-health",
      start: () => {
        if (logger) logger.info("[AgentGuard] 健康检查服务启动");
        checkDaemonHealth(logger);
        healthCheckTimer = setInterval(
          () => checkDaemonHealth(logger),
          (pluginConfig.healthCheckInterval || 30) * 1000
        );
      },
      stop: () => {
        if (healthCheckTimer) {
          clearInterval(healthCheckTimer);
          healthCheckTimer = null;
        }
        if (logger) logger.info("[AgentGuard] 健康检查服务停止");
      },
    });
  }

  // --- 注册 Gateway RPC 方法 ---
  // 允许其他插件或外部调用查询 AgentGuard 状态
  // 参考: https://docs.openclaw.ai/tools/plugin#register-gateway-rpc-methods
  if (api.registerGatewayMethod) {
    api.registerGatewayMethod("agentguard.status", async ({ respond }) => {
      try {
        const status = await agGet("/api/status");
        respond(true, { connected: true, ...status });
      } catch (e) {
        respond(false, { connected: false, error: e.message });
      }
    });

    api.registerGatewayMethod("agentguard.health", async ({ respond }) => {
      respond(true, { connected: daemonConnected, config: pluginConfig });
    });
  }

  // ============================================
  // 操作类工具 — 替代原生 exec/read/write
  // ============================================

  // Tool: ag_execute_command — 替代 exec / process
  api.registerTool({
    name: "ag_execute_command",
    description:
      "通过 AgentGuard 安全引擎执行 Shell 命令。命令经规则引擎审核，危险命令自动拦截，输出经脱敏引擎过滤敏感信息。替代原生 exec 工具。",
    parameters: {
      type: "object",
      properties: {
        command: { type: "string", description: "要执行的 Shell 命令" },
        cwd: { type: "string", description: "工作目录（可选）" },
        timeout: { type: "integer", description: "超时秒数，默认 30", default: 30 },
      },
      required: ["command"],
    },
    async execute(_id, params) {
      try {
        const res = await callTool("execute_command", {
          command: params.command,
          cwd: params.cwd || "",
          timeout: params.timeout || 30,
        });
        return formatResult(res);
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // Tool: ag_read_file — 替代 read
  api.registerTool({
    name: "ag_read_file",
    description:
      "通过 AgentGuard 安全引擎读取文件。敏感路径 (~/.ssh, /etc/shadow, 浏览器数据等) 自动拦截，文件内容经脱敏引擎过滤 API 凭证/认证令牌/SSH 密钥。替代原生 read 工具。",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string", description: "文件绝对路径或 ~ 开头路径" },
        offset: { type: "integer", description: "起始行号 (1-indexed)" },
        limit: { type: "integer", description: "读取行数" },
      },
      required: ["path"],
    },
    async execute(_id, params) {
      try {
        const input = { path: params.path };
        if (params.offset) input.offset = params.offset;
        if (params.limit) input.limit = params.limit;
        const res = await callTool("read_file", input);
        return formatResult(res);
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // Tool: ag_write_file — 替代 write / edit / apply_patch
  api.registerTool({
    name: "ag_write_file",
    description:
      "通过 AgentGuard 安全引擎写入文件。敏感路径自动拦截，写入内容经脱敏引擎检查防止泄露密钥。替代原生 write / edit / apply_patch 工具。",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string", description: "文件绝对路径" },
        content: { type: "string", description: "文件内容" },
      },
      required: ["path", "content"],
    },
    async execute(_id, params) {
      try {
        const res = await callTool("write_file", {
          path: params.path,
          content: params.content,
        });
        if (!res.error && !res.pending) {
          return { content: [{ type: "text", text: res.result || `✅ 文件已写入: ${params.path}` }] };
        }
        return formatResult(res);
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // Tool: ag_list_directory — 替代 read (目录)
  api.registerTool({
    name: "ag_list_directory",
    description:
      "通过 AgentGuard 安全引擎列出目录内容。受路径访问控制保护，敏感目录自动拦截。",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string", description: "目录路径" },
      },
      required: ["path"],
    },
    async execute(_id, params) {
      try {
        const res = await callTool("list_directory", { path: params.path });
        return formatResult(res);
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // Tool: ag_http_request — 替代 browser / 网络工具
  api.registerTool({
    name: "ag_http_request",
    description:
      "通过 AgentGuard 安全引擎发起 HTTP 请求。仅允许白名单域名，自动拦截未授权的外部请求，防止数据外泄。替代原生网络工具。",
    parameters: {
      type: "object",
      properties: {
        method: { type: "string", enum: ["GET", "POST", "PUT", "DELETE"], description: "HTTP 方法" },
        url: { type: "string", description: "请求 URL" },
        headers: { type: "object", description: "请求头" },
        body: { type: "string", description: "请求体" },
      },
      required: ["method", "url"],
    },
    async execute(_id, params) {
      try {
        const res = await callTool("http_request", {
          method: params.method,
          url: params.url,
          headers: params.headers,
          body: params.body,
        });
        return formatResult(res);
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // ============================================
  // 检查类工具
  // ============================================

  // Tool: ag_skill_check
  api.registerTool({
    name: "ag_skill_check",
    description:
      "检查指定 Skill/插件是否在 AgentGuard 安全白名单中。未通过白名单的 Skill 将被标记为不可信。",
    parameters: {
      type: "object",
      properties: {
        identifier: { type: "string", description: "Skill 标识符，例如 @anthropic/claude-code" },
        name: { type: "string", description: "Skill 名称（可选）" },
      },
      required: ["identifier"],
    },
    async execute(_id, params) {
      try {
        const res = await callTool("skill_check", {
          identifier: params.identifier,
          name: params.name || "",
        });
        if (res.error) {
          return {
            content: [{ type: "text", text: `🚫 Skill 未通过安全检查: ${res.error}` }],
            isError: true,
          };
        }
        return { content: [{ type: "text", text: res.result || `✅ Skill ${params.identifier} 在白名单中` }] };
      } catch (e) {
        return formatError(e);
      }
    },
  });

  // Tool: ag_status
  api.registerTool({
    name: "ag_status",
    description:
      "查看 AgentGuard 安全引擎状态：版本、运行模式、审计统计、Panic 状态。用户可以随时调用查看安全概况。",
    parameters: { type: "object", properties: {} },
    async execute() {
      try {
        const status = await agGet("/api/status");
        const modeLabel = { enforce: "强制拦截", supervised: "监督审批", permissive: "宽松放行" };
        const lines = [
          `🛡️ AgentGuard 安全引擎`,
          ``,
          `  版本:   v${status.version}`,
          `  模式:   ${modeLabel[status.mode] || status.mode}`,
          `  状态:   ${status.panic ? "🔴 已暂停 (Panic)" : "🟢 正常运行"}`,
          `  PID:    ${status.pid || "-"}`,
          ``,
          `  📊 审计统计`,
          `  总操作:  ${status.audit_total || 0}`,
          `  已拦截:  ${status.audit_denied || 0}`,
          ``,
          `  🔗 Dashboard: http://${pluginConfig.daemonHost}:${pluginConfig.daemonPort}`,
        ];
        return { content: [{ type: "text", text: lines.join("\n") }] };
      } catch (e) {
        return {
          content: [{
            type: "text",
            text: `⚠️ AgentGuard daemon 未运行\n\n` +
                  `  启动: agentguard daemon start\n` +
                  `  安装: 运行 skill 目录下的 setup.sh\n` +
                  `  文档: https://www.agentguard.site`,
          }],
          isError: true,
        };
      }
    },
  });

  // ============================================
  // 控制类工具
  // ============================================

  // Tool: ag_panic
  api.registerTool({
    name: "ag_panic",
    description:
      "🚨 紧急暂停 AgentGuard — 立即拒绝所有后续 Agent 操作。当发现异常或可疑行为时使用。",
    parameters: { type: "object", properties: {} },
    async execute() {
      try {
        await agPost("/api/panic", {});
        return {
          content: [{ type: "text", text: "🔴 AgentGuard 已紧急暂停，所有后续操作将被拦截。\n   恢复命令: 调用 ag_resume 或在 Dashboard 中恢复" }],
        };
      } catch (e) {
        return {
          content: [{ type: "text", text: `⚠️ Panic 操作失败: ${e.message}` }],
          isError: true,
        };
      }
    },
  });

  // Tool: ag_resume
  api.registerTool({
    name: "ag_resume",
    description:
      "恢复 AgentGuard 正常运行，解除 Panic 暂停状态。",
    parameters: { type: "object", properties: {} },
    async execute() {
      try {
        await agPost("/api/resume", {});
        const status = await agGet("/api/status");
        const modeLabel = { enforce: "强制拦截", supervised: "监督审批", permissive: "宽松放行" };
        return {
          content: [{
            type: "text",
            text: `🟢 AgentGuard 已恢复正常运行\n   当前模式: ${modeLabel[status.mode] || status.mode}`,
          }],
        };
      } catch (e) {
        return {
          content: [{ type: "text", text: `⚠️ Resume 操作失败: ${e.message}` }],
          isError: true,
        };
      }
    },
  });

  // --- 插件启动日志 ---
  if (logger) {
    logger.info(`[AgentGuard] 插件已加载 — daemon=${pluginConfig.daemonHost}:${pluginConfig.daemonPort}`);
  }
};
