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
  const targetPath = args["--path"] || args["-p"] || "ContextWeave";

  if (!sessionId) {
    printJson({
      status: "error",
      error: {
        code: "MISSING_REQUIRED_ARGS",
        message: "必须提供 session_id",
        recoverable: true,
        recovery_hint: "补充参数后重试",
      },
    });
    process.exit(1);
  }

  const client = new CWClient();
  const result = await client.exportCode(sessionId, targetPath);
  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
