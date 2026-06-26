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
  const targetPath = args["--path"] || args["-p"] || "ContextWeave";

  const client = new CWClient();
  let result = await client.importCode(targetPath);
  if (result.status === "ok" && !result.session_id) {
    result = {
      status: "error",
      error: {
        code: "MISSING_SESSION_ID",
        message: "导入成功响应缺少 session_id",
        recoverable: true,
        recovery_hint: "请检查后端服务并重试导入",
      },
      raw_result: result,
    };
  }
  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
