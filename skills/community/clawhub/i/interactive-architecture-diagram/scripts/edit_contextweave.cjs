#!/usr/bin/env node
const { CWClient, printJson } = require("./cw_client.cjs");

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("-")) {
      continue;
    }
    const next = argv[i + 1];
    const value = next && !next.startsWith("-") ? next : "true";
    args[token] = value;
    if (value !== "true") {
      i += 1;
    }
  }
  return args;
}

function normalizeEditResult(result) {
  if (result.status === "error") {
    const message = String((result.error || {}).message || "");
    if (message.toLowerCase().includes("session")) {
      return {
        status: "error",
        error: {
          code: "SESSION_INVALID_OR_EXPIRED",
          message: message || "session_id 缺失、无效或已过期",
          recoverable: true,
          recovery_hint: "请先重新执行生成脚本获取新的 session_id，再重试编辑",
        },
      };
    }
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const sessionId = args["--session_id"] || args["-s"];
  const inputFile = args["--input_file"] || args["-i"];
  const mode = args["--mode"] || args["-m"] || "3";

  if (!sessionId || !inputFile) {
    printJson({
      status: "error",
      error: {
        code: "MISSING_REQUIRED_ARGS",
        message: "必须提供 session_id 和 input_file（为保证上下文完整，编辑操作强制要求使用文件）",
        recoverable: true,
        recovery_hint: "补充 input_file 参数后重试",
      },
    });
    process.exit(1);
  }

  const client = new CWClient();
  const result = normalizeEditResult(
    await client.runGeneration({
      inputFile,
      sessionId,
      mode,
    })
  );

  if (result.status === "ok" && result.cw_code) {
    const fs = require("fs");
    const path = require("path");
    // Use session_id as filename, fallback to 'diagram.cw' if missing
    const filename = result.session_id ? `${result.session_id}.cw` : "diagram.cw";
    const filePath = path.join(process.cwd(), filename);
    fs.writeFileSync(filePath, result.cw_code, "utf8");
    
    // Remove cw_code from the output to prevent polluting LLM context window
    delete result.cw_code;
    result.saved_cw_file = filePath;
  }

  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
