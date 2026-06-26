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

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const sessionId = args["--session_id"] || args["-s"];
  const formatName = args["--format"] || args["-f"];

  if (!sessionId || !formatName) {
    printJson({
      status: "error",
      error: {
        code: "MISSING_REQUIRED_ARGS",
        message: "必须提供 session_id 和 format",
        recoverable: true,
        recovery_hint: "补充参数后重试",
      },
    });
    process.exit(1);
  }

  if (!["svg", "pptx"].includes(formatName)) {
    printJson({
      status: "error",
      error: {
        code: "INVALID_FORMAT",
        message: "format 仅支持 svg 或 pptx",
        recoverable: true,
        recovery_hint: "修改 format 参数后重试",
      },
    });
    process.exit(1);
  }

  const client = new CWClient();
  let result = await client.exportSessionAsset(sessionId, formatName);
  if (result.status === "error") {
    const message = String((result.error || {}).message || "");
    if (message.toLowerCase().includes("session")) {
      result = {
        status: "error",
        error: {
          code: "SESSION_INVALID_OR_EXPIRED",
          message: message || "session_id 无效或已过期",
          recoverable: true,
          recovery_hint: "请先重新生成以获取新的 session_id",
        },
      };
    }
  }
  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
