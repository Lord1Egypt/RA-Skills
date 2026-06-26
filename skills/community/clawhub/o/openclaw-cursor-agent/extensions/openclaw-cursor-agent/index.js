import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PLUGIN_ID = "openclaw-cursor-agent";

const DEFAULTS = {
  toolkitRoot: "",
  defaultProjectPath: "",
  executionMode: process.platform === "win32" ? "wsl" : "direct",
  timeoutMs: 120000,
  shell: {
    executable: process.platform === "win32" ? "wsl.exe" : "bash",
    args: [],
    workingDirectory: "",
    wslDistro: "",
  },
};

const SPAWN_SCHEMA = {
  type: "object",
  required: ["taskName", "taskDescription"],
  properties: {
    taskName: { type: "string", description: "Short task label, for example feature-auth" },
    taskDescription: { type: "string", description: "The prompt that Cursor CLI should execute" },
    projectPath: { type: "string", description: "Optional project directory" },
    priority: { type: "string", description: "Task priority, for example low, normal, high" },
    eta: { type: "string", description: "Estimated duration, for example 45分钟" },
    taskFile: { type: "string", description: "Optional existing markdown task file" },
  },
};

const SESSION_SCHEMA = {
  type: "object",
  required: ["sessionQuery"],
  properties: {
    sessionQuery: { type: "string", description: "Full session name or task alias" },
  },
};

const SEND_SCHEMA = {
  type: "object",
  required: ["sessionQuery", "command"],
  properties: {
    sessionQuery: { type: "string", description: "Full session name or task alias" },
    command: { type: "string", description: "Instruction to send to the tmux session" },
  },
};

const KILL_SCHEMA = {
  type: "object",
  required: ["sessionQuery"],
  properties: {
    sessionQuery: { type: "string", description: "Full session name or task alias" },
    force: { type: "boolean", description: "Whether to force kill the session if graceful stop fails" },
    purge: { type: "boolean", description: "Whether to delete task, status, and log files after stop" },
  },
};

function asString(value, fallback = "") {
  return typeof value === "string" ? value : fallback;
}

function normalizeConfig(rawConfig) {
  const raw = rawConfig && typeof rawConfig === "object" ? rawConfig : {};
  const shell = raw.shell && typeof raw.shell === "object" ? raw.shell : {};
  const toolkitRootRaw = asString(raw.toolkitRoot || "").trim();
  const defaultProjectPathRaw = asString(raw.defaultProjectPath || "").trim();
  return {
    toolkitRoot: toolkitRootRaw ? path.resolve(toolkitRootRaw) : "",
    defaultProjectPath: defaultProjectPathRaw ? path.resolve(defaultProjectPathRaw) : "",
    executionMode: asString(raw.executionMode || DEFAULTS.executionMode || "direct").toLowerCase() === "wsl" ? "wsl" : "direct",
    timeoutMs: Number(raw.timeoutMs) > 0 ? Number(raw.timeoutMs) : DEFAULTS.timeoutMs,
    shell: {
      executable: asString(shell.executable || DEFAULTS.shell.executable),
      args: Array.isArray(shell.args) ? shell.args.map((x) => String(x)) : DEFAULTS.shell.args.slice(),
      workingDirectory: asString(shell.workingDirectory || DEFAULTS.shell.workingDirectory || ""),
      wslDistro: asString(shell.wslDistro || DEFAULTS.shell.wslDistro || ""),
    },
  };
}

function jsonResult(result, isError = false) {
  return {
    content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    details: result,
    isError,
  };
}

function textResult(text, details = {}, isError = false) {
  return {
    content: [{ type: "text", text }],
    details,
    isError,
  };
}

function ensureToolkitRoot(config) {
  if (!config.toolkitRoot) {
    throw new Error("未配置 toolkitRoot，请在 openclaw.json 中设置插件的 toolkitRoot。");
  }
  const scriptsDir = path.join(config.toolkitRoot, "scripts");
  if (!fs.existsSync(scriptsDir)) {
    throw new Error(`toolkitRoot 无效，找不到脚本目录: ${scriptsDir}`);
  }
}

function resolveScriptPath(config, scriptName) {
  ensureToolkitRoot(config);
  const scriptPath = path.join(config.toolkitRoot, "scripts", scriptName);
  if (!fs.existsSync(scriptPath)) {
    throw new Error(`脚本不存在: ${scriptPath}`);
  }
  return scriptPath;
}

function normalizeFsPath(value) {
  const text = asString(value).trim();
  if (!text) return "";
  return path.resolve(text);
}

function toWslPath(input) {
  const resolved = normalizeFsPath(input);
  const normalized = resolved.replace(/\\/g, "/");
  const match = normalized.match(/^([A-Za-z]):\/(.*)$/);
  if (!match) return normalized;
  return `/mnt/${match[1].toLowerCase()}/${match[2]}`;
}

function posixQuote(value) {
  const text = String(value);
  return `'${text.replace(/'/g, `'\\''`)}'`;
}

function parseJsonOutput(stdout) {
  const text = String(stdout || "").trim();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch (_) {
    const lines = text.split(/\r?\n/).filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i -= 1) {
      try {
        return JSON.parse(lines[i]);
      } catch (_) {
        continue;
      }
    }
  }
  return null;
}

async function runShellProbe(config, commandText) {
  const cwd = config.shell.workingDirectory || config.toolkitRoot || __dirname;
  const shellExecutable = config.shell.executable || (config.executionMode === "wsl" ? "wsl.exe" : "bash");
  const shellArgs = Array.isArray(config.shell.args) ? config.shell.args.slice() : [];
  let args = [];

  if (config.executionMode === "wsl") {
    args = shellArgs.slice();
    if (config.shell.wslDistro) {
      args.push("-d", config.shell.wslDistro);
    }
    args.push("--", "bash", "-c", commandText);
  } else {
    args = [...shellArgs, "-c", commandText];
  }

  return await new Promise((resolve) => {
    const child = spawn(shellExecutable, args, {
      cwd,
      env: process.env,
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";
    let finished = false;
    const timer = setTimeout(() => {
      if (finished) return;
      finished = true;
      child.kill();
      resolve({ ok: false, code: -1, stdout, stderr: `${stderr}\nprobe timeout`.trim() });
    }, Math.min(config.timeoutMs, 15000));

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", (error) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      resolve({ ok: false, code: -1, stdout, stderr: String(error) });
    });
    child.on("close", (code) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      resolve({
        ok: Number(code ?? 1) === 0,
        code: Number(code ?? 1),
        stdout,
        stderr,
      });
    });
  });
}

function summarizeProbe(result) {
  const stdout = asString(result?.stdout).trim();
  const stderr = asString(result?.stderr).trim();
  return stdout || stderr || "";
}

function boolAnd(items) {
  return items.every(Boolean);
}

function buildExecution(config, scriptName, args) {
  const scriptPath = resolveScriptPath(config, scriptName);
  const cwd = config.shell.workingDirectory || config.toolkitRoot || __dirname;

  if (config.executionMode === "wsl") {
    const shellExecutable = config.shell.executable || "wsl.exe";
    const shellArgs = Array.isArray(config.shell.args) ? config.shell.args.slice() : [];
    if (config.shell.wslDistro) {
      shellArgs.push("-d", config.shell.wslDistro);
    }
    shellArgs.push("--", "bash", toWslPath(scriptPath), ...args);
    return { executable: shellExecutable, args: shellArgs, cwd };
  }

  return {
    executable: config.shell.executable || "bash",
    args: [...(Array.isArray(config.shell.args) ? config.shell.args : []), scriptPath, ...args],
    cwd,
  };
}

async function runToolkitScript(config, scriptName, args) {
  const spec = buildExecution(config, scriptName, args);
  return await new Promise((resolve, reject) => {
    const child = spawn(spec.executable, spec.args, {
      cwd: spec.cwd,
      env: process.env,
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";
    let finished = false;

    const timeout = setTimeout(() => {
      if (finished) return;
      finished = true;
      child.kill();
      reject(new Error(`执行超时: ${scriptName}`));
    }, config.timeoutMs);

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("error", (error) => {
      if (finished) return;
      finished = true;
      clearTimeout(timeout);
      reject(error);
    });

    child.on("close", (code) => {
      if (finished) return;
      finished = true;
      clearTimeout(timeout);
      resolve({
        code: Number(code ?? 0),
        stdout,
        stderr,
        json: parseJsonOutput(stdout),
      });
    });
  });
}

async function diagnose(config) {
  const toolkitRoot = config.toolkitRoot || "(未配置)";
  const shellExecutable = config.shell.executable || "(未配置)";
  const scriptsDir = config.toolkitRoot ? path.join(config.toolkitRoot, "scripts") : "";
  const statusDir = config.toolkitRoot ? path.join(config.toolkitRoot, "status") : "";
  const tasksDir = config.toolkitRoot ? path.join(config.toolkitRoot, "tasks") : "";
  const logsDir = config.toolkitRoot ? path.join(config.toolkitRoot, "logs") : "";
  const scriptChecks = {
    spawn: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "spawn-cursor.sh")) : false,
    checkStatus: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "check-status.sh")) : false,
    attachSession: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "attach-session.sh")) : false,
    sendCommand: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "send-command.sh")) : false,
    killSession: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "kill-session.sh")) : false,
    common: config.toolkitRoot ? fs.existsSync(path.join(scriptsDir, "common.sh")) : false,
  };
  const scriptExists = boolAnd(Object.values(scriptChecks));
  const runtimeDirs = {
    status: config.toolkitRoot ? fs.existsSync(statusDir) : false,
    tasks: config.toolkitRoot ? fs.existsSync(tasksDir) : false,
    logs: config.toolkitRoot ? fs.existsSync(logsDir) : false,
  };
  const statusDirExists = runtimeDirs.status;
  const executableExists = shellExecutable ? (
    fs.existsSync(shellExecutable) || shellExecutable === "bash" || shellExecutable === "wsl.exe"
  ) : false;

  const shellRunner = executableExists
    ? await runShellProbe(config, "printf 'shell_ok'")
    : { ok: false, code: -1, stdout: "", stderr: "shell executable not found" };
  const pythonProbe = shellRunner.ok
    ? await runShellProbe(config, "command -v python3 && python3 --version")
    : { ok: false, code: -1, stdout: "", stderr: "shell unavailable" };
  const tmuxProbe = shellRunner.ok
    ? await runShellProbe(config, "command -v tmux && tmux -V")
    : { ok: false, code: -1, stdout: "", stderr: "shell unavailable" };
  const agentProbe = shellRunner.ok
    ? await runShellProbe(config, "if command -v agent >/dev/null 2>&1; then command -v agent && agent --version; elif command -v cursor-agent >/dev/null 2>&1; then command -v cursor-agent && cursor-agent --version; else exit 1; fi")
    : { ok: false, code: -1, stdout: "", stderr: "shell unavailable" };

  const dependencyChecks = {
    python3: {
      ok: pythonProbe.ok,
      detail: summarizeProbe(pythonProbe),
      code: pythonProbe.code,
    },
    tmux: {
      ok: tmuxProbe.ok,
      detail: summarizeProbe(tmuxProbe),
      code: tmuxProbe.code,
    },
    agent: {
      ok: agentProbe.ok,
      detail: summarizeProbe(agentProbe),
      code: agentProbe.code,
    },
  };

  const issues = [];
  if (!config.toolkitRoot) issues.push("未配置 toolkitRoot");
  if (!scriptExists) issues.push("工具脚本不完整");
  if (!runtimeDirs.status || !runtimeDirs.tasks || !runtimeDirs.logs) issues.push("运行目录未初始化");
  if (!executableExists) issues.push("shell.executable 不存在");
  if (!shellRunner.ok) issues.push("shell 运行器不可执行");
  if (!dependencyChecks.python3.ok) issues.push("缺少 python3");
  if (!dependencyChecks.tmux.ok) issues.push("缺少 tmux");
  if (!dependencyChecks.agent.ok) issues.push("缺少 agent 或 cursor-agent");

  return {
    ok: Boolean(
      config.toolkitRoot &&
      scriptExists &&
      runtimeDirs.status &&
      runtimeDirs.tasks &&
      runtimeDirs.logs &&
      executableExists &&
      shellRunner.ok &&
      dependencyChecks.python3.ok &&
      dependencyChecks.tmux.ok &&
      dependencyChecks.agent.ok
    ),
    pluginId: PLUGIN_ID,
    toolkitRoot,
    defaultProjectPath: config.defaultProjectPath || "",
    executionMode: config.executionMode,
    shellExecutable,
    shellArgs: config.shell.args,
    scriptExists,
    scriptsDir,
    scriptChecks,
    statusDirExists,
    runtimeDirs,
    executableExists,
    shellRunner: {
      ok: shellRunner.ok,
      code: shellRunner.code,
      detail: summarizeProbe(shellRunner) || "shell_ok",
    },
    dependencyChecks,
    issues,
  };
}

function summarizeSpawn(result) {
  const details = result?.json || {};
  return [
    "已提交 Cursor 后台任务。",
    `会话名: ${details.sessionName || "(未知)"}`,
    `状态: ${details.status || "(未知)"}`,
    `任务文件: ${details.taskFile || "(未知)"}`,
  ].join("\n");
}

function summarizeStatus(statusData) {
  const data = statusData?.status || {};
  const progress = data?.progress || {};
  return [
    `会话名: ${data.sessionName || statusData?.sessionName || "(未知)"}`,
    `状态: ${data.status || "(未知)"}`,
    `当前步骤: ${progress.currentStep || "(无)"}`,
    `进度估计: ${progress.estimatedProgress || "(无)"}`,
    `tmux 存活: ${statusData?.hasSession ? "是" : "否"}`,
  ].join("\n");
}

function summarizeSend(result) {
  const details = result?.json || {};
  const status = details?.status || {};
  return [
    `会话名: ${details.sessionName || "(未知)"}`,
    `是否送达: ${details.delivered ? "是" : "待确认"}`,
    `当前状态: ${status.status || "(未知)"}`,
    `当前步骤: ${status.progress?.currentStep || "(无)"}`,
  ].join("\n");
}

function summarizeKill(result) {
  const details = result?.json || {};
  return [
    `会话名: ${details.sessionName || "(未知)"}`,
    `最终状态: ${details.status || "(未知)"}`,
    `已清理文件: ${details.purged ? "是" : "否"}`,
  ].join("\n");
}

async function handleSpawnTool(config, params) {
  if (!params?.taskName || !params?.taskDescription) {
    return textResult("缺少 taskName 或 taskDescription。", {}, true);
  }
  const projectPath = normalizeFsPath(params.projectPath || config.defaultProjectPath || process.cwd());
  const args = [
    String(params.taskName),
    String(params.taskDescription),
    config.executionMode === "wsl" ? toWslPath(projectPath) : projectPath,
    "--json",
  ];
  if (params.priority) {
    args.push("--priority", String(params.priority));
  }
  if (params.eta) {
    args.push("--eta", String(params.eta));
  }
  if (params.taskFile) {
    const taskFilePath = normalizeFsPath(params.taskFile);
    args.push("--task-file", config.executionMode === "wsl" ? toWslPath(taskFilePath) : taskFilePath);
  }
  const result = await runToolkitScript(config, "spawn-cursor.sh", args);
  if (result.code !== 0 || !result.json) {
    return textResult(`启动失败。\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`, { code: result.code }, true);
  }
  return textResult(summarizeSpawn(result), result.json, false);
}

async function handleListTool(config) {
  const result = await runToolkitScript(config, "check-status.sh", ["--json"]);
  if (result.code !== 0 || !result.json) {
    return textResult(`列出任务失败。\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`, { code: result.code }, true);
  }
  const items = Array.isArray(result.json.items) ? result.json.items : [];
  const lines = items.length
    ? items.map((item) => `${item.sessionName} | ${item.status} | ${item.taskName || ""}`)
    : ["当前没有已记录任务。"];
  return textResult(lines.join("\n"), result.json, false);
}

async function handleStatusTool(config, sessionQuery) {
  if (!asString(sessionQuery).trim()) {
    return textResult("缺少 sessionQuery。", {}, true);
  }
  const result = await runToolkitScript(config, "check-status.sh", [String(sessionQuery), "--json"]);
  if (result.code !== 0 || !result.json) {
    return textResult(`查询状态失败。\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`, { code: result.code }, true);
  }
  return textResult(summarizeStatus(result.json), result.json, false);
}

async function handleSendTool(config, params) {
  if (!params?.sessionQuery || !params?.command) {
    return textResult("缺少 sessionQuery 或 command。", {}, true);
  }
  const result = await runToolkitScript(config, "send-command.sh", [String(params.sessionQuery), String(params.command), "--json"]);
  if (result.code !== 0 || !result.json) {
    return textResult(`发送指令失败。\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`, { code: result.code }, true);
  }
  return textResult(summarizeSend(result), result.json, !result.json.ok);
}

async function handleKillTool(config, params) {
  if (!params?.sessionQuery) {
    return textResult("缺少 sessionQuery。", {}, true);
  }
  const args = [String(params.sessionQuery), "--yes", "--json"];
  if (params.force) {
    args.push("--force");
  }
  if (params.purge) {
    args.push("--purge");
  }
  const result = await runToolkitScript(config, "kill-session.sh", args);
  if (result.code !== 0 && !result.json) {
    return textResult(`结束会话失败。\nSTDOUT:\n${result.stdout}\nSTDERR:\n${result.stderr}`, { code: result.code }, true);
  }
  return textResult(summarizeKill(result), result.json || { code: result.code }, result.code !== 0);
}

function registerTools(api, config) {
  api.registerTool({
    name: "cursor_agent_spawn_task",
    label: "Cursor Agent Spawn Task",
    description: "Start a long-running Cursor CLI coding task inside a tmux session through the cursor-agent-system toolkit.",
    parameters: SPAWN_SCHEMA,
    async execute(_toolCallId, params) {
      try {
        return await handleSpawnTool(config, params || {});
      } catch (error) {
        return textResult(`启动任务失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });

  api.registerTool({
    name: "cursor_agent_list_tasks",
    label: "Cursor Agent List Tasks",
    description: "List recorded Cursor task sessions managed by the cursor-agent-system toolkit.",
    parameters: { type: "object", properties: {} },
    async execute() {
      try {
        return await handleListTool(config);
      } catch (error) {
        return textResult(`列出任务失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });

  api.registerTool({
    name: "cursor_agent_check_status",
    label: "Cursor Agent Check Status",
    description: "Check task status, recent output, and tmux session information for a Cursor background task.",
    parameters: SESSION_SCHEMA,
    async execute(_toolCallId, params) {
      try {
        return await handleStatusTool(config, params?.sessionQuery);
      } catch (error) {
        return textResult(`查询状态失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });

  api.registerTool({
    name: "cursor_agent_send_command",
    label: "Cursor Agent Send Command",
    description: "Send additional instructions such as /pause, /resume, /status, or scope updates to a running Cursor tmux session.",
    parameters: SEND_SCHEMA,
    async execute(_toolCallId, params) {
      try {
        return await handleSendTool(config, params || {});
      } catch (error) {
        return textResult(`发送指令失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });

  api.registerTool({
    name: "cursor_agent_kill_session",
    label: "Cursor Agent Kill Session",
    description: "Gracefully stop or force kill a Cursor tmux session managed by the cursor-agent-system toolkit.",
    parameters: KILL_SCHEMA,
    async execute(_toolCallId, params) {
      try {
        return await handleKillTool(config, params || {});
      } catch (error) {
        return textResult(`结束会话失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });

  api.registerTool({
    name: "cursor_agent_doctor",
    label: "Cursor Agent Doctor",
    description: "Inspect plugin configuration, toolkit paths, and shell execution mode for the cursor-agent-system plugin.",
    parameters: { type: "object", properties: {} },
    async execute() {
      try {
        const report = await diagnose(config);
        return jsonResult(report, !report.ok);
      } catch (error) {
        return textResult(`诊断失败: ${error instanceof Error ? error.message : String(error)}`, {}, true);
      }
    },
  });
}

function registerCommands(api, config) {
  api.registerCommand({
    name: "cursor",
    description: "管理 OpenClaw Cursor Agent 后台任务（doctor/list/status/send/kill/spawn）",
    acceptsArgs: true,
    requireAuth: false,
    async handler(ctx) {
      const raw = asString(ctx.args || "").trim();
      if (!raw || raw === "help") {
        return {
          text: [
            "用法:",
            "/cursor doctor",
            "/cursor list",
            "/cursor status <会话名或任务别名>",
            "/cursor send <会话名或任务别名> <指令>",
            "/cursor kill <会话名或任务别名> [--force]",
            "/cursor spawn <任务名> || <任务描述> || [项目路径]",
          ].join("\n"),
        };
      }

      const [subcommand, ...rest] = raw.split(/\s+/);
      const tail = raw.slice(subcommand.length).trim();

      try {
        if (subcommand === "doctor") {
          const report = await diagnose(config);
          return { text: JSON.stringify(report, null, 2) };
        }
        if (subcommand === "list") {
          const result = await handleListTool(config);
          return { text: result.content[0].text };
        }
        if (subcommand === "status") {
          const result = await handleStatusTool(config, tail);
          return { text: result.content[0].text };
        }
        if (subcommand === "send") {
          const [sessionQuery, ...commandParts] = rest;
          const result = await handleSendTool(config, {
            sessionQuery,
            command: commandParts.join(" "),
          });
          return { text: result.content[0].text };
        }
        if (subcommand === "kill") {
          const force = rest.includes("--force");
          const sessionQuery = rest.filter((item) => item !== "--force")[0];
          const result = await handleKillTool(config, {
            sessionQuery,
            force,
            purge: false,
          });
          return { text: result.content[0].text };
        }
        if (subcommand === "spawn") {
          const parts = tail.split("||").map((item) => item.trim()).filter(Boolean);
          if (parts.length < 2) {
            return { text: "spawn 用法: /cursor spawn <任务名> || <任务描述> || [项目路径]" };
          }
          const [taskName, taskDescription, projectPath] = parts;
          const result = await handleSpawnTool(config, { taskName, taskDescription, projectPath });
          return { text: result.content[0].text };
        }
        return { text: "未知子命令。请使用 /cursor help 查看帮助。" };
      } catch (error) {
        return { text: `执行失败: ${error instanceof Error ? error.message : String(error)}` };
      }
    },
  });
}

function registerCli(api, config) {
  if (!api.registerCli) {
    return;
  }
  api.registerCli((ctx) => {
    ctx.program
      .command("cursor-agent-doctor")
      .description("检查 OpenClaw Cursor Agent 插件配置和工具目录")
      .action(async () => {
        const report = await diagnose(config);
        console.log(JSON.stringify(report, null, 2));
        if (!report.ok) {
          process.exitCode = 1;
        }
      });

    ctx.program
      .command("cursor-agent-list")
      .description("列出 Cursor 后台任务会话")
      .action(async () => {
        const result = await handleListTool(config);
        console.log(result.content[0].text);
      });
  }, { commands: ["cursor-agent-doctor", "cursor-agent-list"] });
}

const plugin = {
  id: PLUGIN_ID,
  name: "OpenClaw Cursor Agent",
  description: "Manage persistent Cursor CLI coding tasks through tmux.",
  register(api) {
    const config = normalizeConfig(api.pluginConfig);
    registerTools(api, config);
    if (api.registerCommand) {
      registerCommands(api, config);
    }
    registerCli(api, config);
  },
};

export default plugin;
