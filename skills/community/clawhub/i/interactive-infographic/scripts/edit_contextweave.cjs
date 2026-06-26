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
  const userRequest = args["--user_request"] || args["-u"];
  const mode = args["--mode"] || args["-m"] || "3";

  if (!sessionId || !userRequest) {
    printJson({
      status: "error",
      error: {
        code: "MISSING_REQUIRED_ARGS",
        message: "必须提供 session_id 和 user_request",
        recoverable: true,
        recovery_hint: "补充参数后重试",
      },
    });
    process.exit(1);
  }

  const client = new CWClient();
  const result = normalizeEditResult(
    await client.runGeneration({
      userRequest,
      sessionId,
      mode,
    })
  );
  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
