#!/usr/bin/env node
/**
 * DataAgent OpenAPI CLI
 *
 * 通过命令行调用 DataPilot OpenAPI，支持以下能力：
 *   create-instance   — 创建 DataAgent 实例（namespace + agent 一步到位）
 *   ask               — 自然语言问数（SSE 流式对话）
 *   list-agents       — 列出所有 Agent（跨 namespace 汇总）
 *   knowledge-list    — 查看 Agent 知识库
 *   knowledge-upsert  — 新增/更新知识条目
 *   knowledge-get     — 获取单条知识详情
 *   knowledge-delete  — 删除知识条目
 *
 * 服务地址优先级：--base-url > 环境变量 DATAPILOT_API_URL > http://localhost:3000
 * 鉴权优先级：--token > --apiKey > 环境变量 DATAPILOT_API_KEY
 *
 * 用法：node dataagent_openapi_cli.mjs <command> [options]
 */

import { readFile, appendFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const LOG_FILE = join(__dirname, "dataagent_cli.log");

function sanitizeSecret(val) {
  if (typeof val === "string" && val.length > 4) return val.slice(0, 4) + "****";
  return val ? "****" : undefined;
}

function sanitizeArgs(args) {
  const safe = { ...args };
  for (const key of ["token", "apiKey"]) {
    if (safe[key]) safe[key] = sanitizeSecret(safe[key]);
  }
  return safe;
}

function getRelevantEnv() {
  return {
    DATAPILOT_API_URL: process.env.DATAPILOT_API_URL || undefined,
    DATAPILOT_API_KEY: sanitizeSecret(process.env.DATAPILOT_API_KEY),
  };
}

async function writeLog(entry) {
  const line = JSON.stringify({ timestamp: new Date().toISOString(), ...entry }) + "\n";
  try {
    await appendFile(LOG_FILE, line, "utf-8");
  } catch {
    // 日志写入失败不影响主流程
  }
}

// ─── CLI 参数解析 ────────────────────────────────────────────────────────────

/**
 * 将 process.argv 解析为键值对象。
 * 无值的 `--flag` 被设为 true，非 `--` 开头的参数收集到 `_` 数组。
 *
 * @param {string[]} argv - process.argv.slice(2)
 * @returns {{ _: string[], [key: string]: string | boolean | string[] }}
 */
function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

// ─── 鉴权与 HTTP 基础设施 ───────────────────────────────────────────────────

/**
 * 从 CLI 参数或环境变量中获取鉴权 Headers。
 * 优先级：--token > --apiKey > DATAPILOT_API_KEY
 *
 * @param {object} args - 解析后的 CLI 参数
 * @returns {{ Authorization: string, "X-Lang": string }}
 * @throws {Error} 未找到任何鉴权凭据时抛出
 */
function getAuthHeaders(args) {
  writeLog({ type: "getAuthHeaders", args: sanitizeArgs(args), keyenv: process.env.DATAPILOT_API_KEY });
  const auth = args.token || args.apiKey || process.env.DATAPILOT_API_KEY;
  if (!auth) {
    throw new Error("Missing auth. Provide --token/--apiKey or set DATAPILOT_API_KEY");
  }
  return {
    Authorization: `Bearer ${auth}`,
    "X-Lang": "zh",
  };
}

/**
 * 统一的 API 请求封装。
 * 自动拼接 baseUrl + /api + path，解析标准响应 { code, message, data }。
 *
 * @param {object} options
 * @param {string} options.baseUrl  - 服务根地址
 * @param {string} options.path     - API 路径（不含 /api 前缀）
 * @param {string} [options.method] - HTTP method，默认 GET
 * @param {object} [options.headers]
 * @param {string|FormData} [options.body]
 * @param {boolean} [options.raw]   - 为 true 时直接返回原始 Response（用于 SSE）
 * @returns {Promise<any>} 响应中的 data 字段
 * @throws {Error} HTTP 错误或 code !== 0 时抛出
 */
async function apiRequest({ baseUrl, path, method = "GET", headers = {}, body, raw = false }) {
  const url = `${baseUrl.replace(/\/+$/, "")}/api${path}`;
  const logEntry = { type: "api_request", method, url };

  try {
    const response = await fetch(url, { method, headers, body });

    if (raw) {
      await writeLog({ ...logEntry, status: response.status, raw: true });
      return response;
    }

    let payload;
    try {
      payload = await response.json();
    } catch {
      const text = await response.text();
      const err = new Error(`Invalid JSON response: ${text}`);
      await writeLog({ ...logEntry, status: response.status, error: err.message });
      throw err;
    }

    if (!response.ok || payload?.code !== 0) {
      const err = new Error(payload?.message || `HTTP ${response.status}`);
      await writeLog({ ...logEntry, status: response.status, error: err.message, responseCode: payload?.code });
      throw err;
    }

    await writeLog({ ...logEntry, status: response.status, success: true });
    return payload.data;
  } catch (err) {
    if (!err.message?.startsWith("Invalid JSON") && !err.message?.startsWith("HTTP ")) {
      await writeLog({ ...logEntry, error: err.message });
    }
    throw err;
  }
}

// ─── 数据源处理 ──────────────────────────────────────────────────────────────

/**
 * 从 CLI 参数加载数据源配置 JSON。
 * 支持两种方式：--datasource-json（内联字符串）或 --datasource-file（文件路径）。
 *
 * @param {object} args
 * @returns {Promise<object>} 数据源配置对象
 * @throws {Error} 两者均未提供时抛出
 */
async function loadDatasource(args) {
  if (args["datasource-json"]) {
    return JSON.parse(args["datasource-json"]);
  }
  if (args["datasource-file"]) {
    const text = await readFile(args["datasource-file"], "utf-8");
    return JSON.parse(text);
  }
  throw new Error("Missing datasource. Use --datasource-json or --datasource-file");
}

/**
 * 当数据源为 sqlite 且未提供 uri 时，上传 .db 文件并回填 uri。
 * 非 sqlite 或已有 uri 时原样返回。
 *
 * @param {object} options
 * @param {string} options.baseUrl
 * @param {object} options.headers
 * @param {object} options.datasource - 数据源配置
 * @param {object} options.args       - CLI 参数（含 --sqlite-file）
 * @returns {Promise<object>} 补全 uri 后的数据源配置
 */
async function uploadSqliteIfNeeded({ baseUrl, headers, datasource, args }) {
  if (datasource.type !== "sqlite" || datasource.uri) return datasource;

  const sqliteFile = args["sqlite-file"];
  if (!sqliteFile) {
    throw new Error("sqlite datasource requires --sqlite-file when uri is not provided");
  }

  const fileContent = await readFile(sqliteFile);
  const form = new FormData();
  form.append("file", new Blob([fileContent]), sqliteFile.split("/").pop() || "database.db");

  const data = await apiRequest({
    baseUrl,
    path: "/namespaces/sqlite-upload",
    method: "POST",
    headers,
    body: form,
  });
  return { ...datasource, uri: data.uri };
}

// ─── SSE 解析 ────────────────────────────────────────────────────────────────

/**
 * 解析 SSE 文本缓冲区，按 \n\n 分割事件，提取 data: 行并 JSON.parse。
 * 返回剩余未完成的 buffer 片段供下次拼接。
 *
 * @param {string} buffer    - 当前累积的 SSE 文本
 * @param {(event: object) => void} onEvent - 每解析出一个完整事件回调
 * @returns {string} 未消费完的 buffer 尾部
 */
function parseSSEChunk(buffer, onEvent) {
  const parts = buffer.split("\n\n");
  const rest = parts.pop() ?? "";
  for (const part of parts) {
    const dataLines = part
      .split("\n")
      .filter((line) => line.startsWith("data:"))
      .map((line) => line.replace(/^data:\s?/, ""));
    if (!dataLines.length) continue;
    const joined = dataLines.join("\n");
    try {
      onEvent(JSON.parse(joined));
    } catch {
      // 不完整或非 JSON 的 chunk，跳过
    }
  }
  return rest;
}

// ─── 命令实现：create-instance ───────────────────────────────────────────────

/**
 * 创建 DataAgent 实例：一步完成 namespace 创建 → 拉取表 → 创建 agent。
 * namespace 与 agent 使用相同的 name / description，对用户屏蔽拆分细节。
 *
 * 必填参数：--name, --datasource-file 或 --datasource-json
 * 可选参数：--description, --sqlite-file（sqlite 类型时）
 *
 * @param {object} args - CLI 参数
 * @returns {Promise<{namespaceId: string, agentId: string, name: string, description: string, tablesCount: number, datasourceType: string}>}
 */
async function createInstance(args) {
  const baseUrl = args["base-url"] || process.env.DATAPILOT_API_URL;
  const headers = getAuthHeaders(args);
  const name = args.name;
  if (!name) throw new Error("Missing --name");
  const description = args.description || "";

  // 1. 加载并预处理数据源（sqlite 需要先上传文件）
  let datasource = await loadDatasource(args);
  datasource = await uploadSqliteIfNeeded({ baseUrl, headers, datasource, args });

  // 2. 创建 namespace
  const namespace = await apiRequest({
    baseUrl,
    path: "/namespaces",
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ name, description, datasource }),
  });

  // 3. 拉取该 namespace 下所有表
  const tables = await apiRequest({
    baseUrl,
    path: `/namespaces/${namespace.namespaceId}/tables`,
    headers,
  });

  // 4. 创建 agent（默认关联全部表）
  const agent = await apiRequest({
    baseUrl,
    path: `/namespaces/${namespace.namespaceId}/agents`,
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      name,
      description,
      tables,
      metrics: [],
      sqls: [],
      suggestions: [],
    }),
  });

  return {
    namespaceId: namespace.namespaceId,
    agentId: agent.agentId,
    name: agent.name,
    description: agent.description || "",
    tablesCount: Array.isArray(tables) ? tables.length : 0,
    datasourceType: namespace.datasource?.type || datasource.type,
  };
}

// ─── 命令实现：list-agents ───────────────────────────────────────────────────

/**
 * 列出所有 Agent：遍历全部 namespace，汇总每个 namespace 下的 agent。
 *
 * @param {object} args - CLI 参数
 * @returns {Promise<Array<{agentId: string, name: string, description: string, namespaceId: string, namespaceName: string, datasourceType: string, updatedAt: string}>>}
 */
async function listAgents(args) {
  const baseUrl = args["base-url"] || process.env.DATAPILOT_API_URL;
  const headers = getAuthHeaders(args);

  const namespaces = await apiRequest({ baseUrl, path: "/namespaces", headers });
  const result = [];

  for (const ns of namespaces) {
    const agents = await apiRequest({
      baseUrl,
      path: `/namespaces/${ns.namespaceId}/agents`,
      headers,
    });
    for (const a of agents) {
      result.push({
        agentId: a.agentId,
        name: a.name,
        description: a.description || "",
        namespaceId: a.namespaceId,
        namespaceName: ns.name,
        datasourceType: a.datasourceType || ns.datasource?.type || "",
        updatedAt: a.updatedAt,
      });
    }
  }

  return result;
}

// ─── 命令实现：ask ───────────────────────────────────────────────────────────

/**
 * 自然语言问数：通过 SSE 流式对话接口发送问题
 * 解析事件流，只返回最终回复文本、下载链接等结构化结果。
 *
 * 必填参数：--namespace-id, --agent-id, --input
 * 可选参数：--session-id（多轮对话），--role
 *
 * @param {object} args - CLI 参数
 * @returns {Promise<{sessionId: string, content: string, sql: string[], downloadUrls: string[], status: string}>}
 */
async function ask(args) {
  const baseUrl = args["base-url"] || process.env.DATAPILOT_API_URL ;
  const headers = getAuthHeaders(args);
  const namespaceId = args["namespace-id"];
  const agentId = args["agent-id"];
  const input = args.input;
  if (!namespaceId || !agentId || !input) {
    throw new Error("Missing required params: --namespace-id --agent-id --input");
  }

  const response = await apiRequest({
    baseUrl,
    path: `/namespaces/${namespaceId}/agents/${agentId}/chat`,
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      input,
      sessionId: args["session-id"] || undefined,
      role: args.role || undefined,
    }),
    raw: true,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Chat failed: ${text || response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error("No SSE body");
  const decoder = new TextDecoder();
  let buffer = "";

  let resolvedSessionId = args["session-id"] || "";
  let content = "";
  const sqls = [];
  let status = "processing";

  const processEvent = (evt) => {
    switch (evt.event) {
      case "message_start":
        if (evt.session_id) resolvedSessionId = evt.session_id;
        break;

      case "block_delta":
        if (evt.block) {
          switch (evt.block.type) {
            case "text":
              if (typeof evt.block.text === "string") content += evt.block.text;
              break;
            case "sql":
              if (evt.block.statement) sqls.push(evt.block.statement);
              break;
            case "error":
              content = evt.block.message || "Unknown error";
              status = "failed";
              break;
          }
        }
        break;

      case "message_done":
        if (status !== "failed") status = "completed";
        break;

      case "error":
        content = evt.block?.message || "Unknown error";
        status = "failed";
        break;
    }
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    buffer = parseSSEChunk(buffer, processEvent);
  }
  if (buffer.trim()) {
    parseSSEChunk(`${buffer}\n\n`, processEvent);
  }

  const downloadPathPattern = /\/api\/sub-agents\/[^/\s]+\/download\/files\/[^\s"')]+/g;
  const downloadMatches = content.match(downloadPathPattern) || [];
  const downloadUrls = [...new Set(downloadMatches)].map(
    (p) => `${baseUrl.replace(/\/+$/, "")}${p}`
  );

  return {
    sessionId: resolvedSessionId,
    content: content.trim(),
    downloadUrls,
    status,
  };
}

// ─── 命令实现：knowledge-* ───────────────────────────────────────────────────

/**
 * 校验知识管理命令的公共必填参数。
 *
 * @param {object} args
 * @returns {{ baseUrl: string, headers: object, namespaceId: string, agentId: string }}
 * @throws {Error} 缺少 --namespace-id 或 --agent-id 时抛出
 */
function resolveKnowledgeContext(args) {
  const baseUrl = args["base-url"] || process.env.DATAPILOT_API_URL;
  const headers = getAuthHeaders(args);
  const namespaceId = args["namespace-id"];
  const agentId = args["agent-id"];
  if (!namespaceId || !agentId) {
    throw new Error("Missing --namespace-id or --agent-id");
  }
  return { baseUrl, headers, namespaceId, agentId };
}

/**
 * 查看知识库：列出指定 agent 的全部或按类型过滤的知识条目。
 *
 * 必填参数：--namespace-id, --agent-id
 * 可选参数：--knowledge-type（reference_sql / business_knowledge / analysis_template）
 *
 * @param {object} args
 * @returns {Promise<any>}
 */
async function knowledgeList(args) {
  const { baseUrl, headers, namespaceId, agentId } = resolveKnowledgeContext(args);
  const knowledgeType = args["knowledge-type"];
  const path = knowledgeType
    ? `/namespaces/${namespaceId}/agents/${agentId}/knowledge/${knowledgeType}`
    : `/namespaces/${namespaceId}/agents/${agentId}/knowledge`;
  return apiRequest({ baseUrl, path, headers });
}

/**
 * 新增或更新知识条目。同名条目会被覆盖。
 *
 * 必填参数：--namespace-id, --agent-id, --knowledge-type, --name, --content
 *
 * @param {object} args
 * @returns {Promise<any>}
 */
async function knowledgeUpsert(args) {
  const { baseUrl, headers, namespaceId, agentId } = resolveKnowledgeContext(args);
  const knowledgeType = args["knowledge-type"];
  const name = args.name;
  const content = args.content;
  if (!knowledgeType || !name || !content) {
    throw new Error("Missing required params: --knowledge-type, --name, --content");
  }
  return apiRequest({
    baseUrl,
    path: `/namespaces/${namespaceId}/agents/${agentId}/knowledge`,
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ knowledge_type: knowledgeType, name, content }),
  });
}

/**
 * 获取单条知识详情。
 *
 * 必填参数：--namespace-id, --agent-id, --knowledge-type, --name
 *
 * @param {object} args
 * @returns {Promise<any>}
 */
async function knowledgeGet(args) {
  const { baseUrl, headers, namespaceId, agentId } = resolveKnowledgeContext(args);
  const knowledgeType = args["knowledge-type"];
  const name = args.name;
  if (!knowledgeType || !name) {
    throw new Error("Missing required params: --knowledge-type, --name");
  }
  return apiRequest({
    baseUrl,
    path: `/namespaces/${namespaceId}/agents/${agentId}/knowledge/${knowledgeType}/${encodeURIComponent(name)}`,
    headers,
  });
}

/**
 * 删除一条知识。
 *
 * 必填参数：--namespace-id, --agent-id, --knowledge-type, --name
 *
 * @param {object} args
 * @returns {Promise<any>}
 */
async function knowledgeDelete(args) {
  const { baseUrl, headers, namespaceId, agentId } = resolveKnowledgeContext(args);
  const knowledgeType = args["knowledge-type"];
  const name = args.name;
  if (!knowledgeType || !name) {
    throw new Error("Missing required params: --knowledge-type, --name");
  }
  return apiRequest({
    baseUrl,
    path: `/namespaces/${namespaceId}/agents/${agentId}/knowledge/${knowledgeType}/${encodeURIComponent(name)}`,
    method: "DELETE",
    headers,
  });
}

// ─── 帮助信息与入口 ──────────────────────────────────────────────────────────

/** 打印命令帮助信息 */
function printHelp() {
  console.log(`DataAgent OpenAPI CLI

Usage:
  node dataagent_openapi_cli.mjs <command> [options]

Commands:
  create-instance     Create a DataAgent instance (namespace + agent)
  ask                 Ask a question via SSE chat
  list-agents         List all agents across namespaces
  knowledge-list      List knowledge entries for an agent
  knowledge-upsert    Create or update a knowledge entry
  knowledge-get       Get a single knowledge entry
  knowledge-delete    Delete a knowledge entry

Common options:
  --base-url <url>    API server URL (env: DATAPILOT_API_URL, default: http://localhost:3000)
  --token <jwt>       Auth token (or --apiKey, or env DATAPILOT_API_KEY)
`);
}

/** 命令名 → 处理函数映射 */
const COMMAND_MAP = {
  "create-instance": createInstance,
  ask,
  "list-agents": listAgents,
  "knowledge-list": knowledgeList,
  "knowledge-upsert": knowledgeUpsert,
  "knowledge-get": knowledgeGet,
  "knowledge-delete": knowledgeDelete,
};

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command || command === "help" || command === "--help") {
    printHelp();
    process.exit(0);
  }

  const missing = [];
  if (!args["base-url"] && !process.env.DATAPILOT_API_URL) missing.push("DATAPILOT_API_URL (or --base-url)");
  if (!args.token && !args.apiKey && !process.env.DATAPILOT_API_KEY) missing.push("DATAPILOT_API_KEY (or --token/--apiKey)");
  if (missing.length) {
    throw new Error(`Missing required config: ${missing.join(", ")}. Set via environment variables or CLI options.`);
  }

  const handler = COMMAND_MAP[command];
  if (!handler) {
    const err = new Error(`Unknown command: ${command}. Run with --help to see available commands.`);
    await writeLog({ type: "command", command, error: err.message });
    throw err;
  }

  await writeLog({ type: "command_start", command, args: sanitizeArgs(args), env: getRelevantEnv() });
  const result = await handler(args);
  await writeLog({ type: "command_end", command, success: true });
  console.log(JSON.stringify({ ok: true, command, result }, null, 2));
}

main().catch(async (err) => {
  await writeLog({ type: "command_error", error: err.message, stack: err.stack });
  console.error(JSON.stringify({ ok: false, error: err.message }, null, 2));
  process.exit(1);
});
