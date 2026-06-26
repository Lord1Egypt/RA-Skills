#!/usr/bin/env node
const { CWClient, printJson } = require("./cw_client.cjs");

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("-")) {
      continue;
    }
    const key = token;
    const next = argv[i + 1];
    const value = next && !next.startsWith("-") ? next : "true";
    args[key] = value;
    if (value !== "true") {
      i += 1;
    }
  }
  return args;
}

function normalizeGenerationResult(result) {
  if (result.status === "ok" && !result.session_id) {
    return {
      status: "error",
      error: {
        code: "MISSING_SESSION_ID",
        message: "生成成功响应缺少 session_id，无法用于后续编辑",
        recoverable: true,
        recovery_hint: "请重新执行生成；若仍失败请检查后端服务",
      },
      raw_result: result,
    };
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const userRequest = args["--user_request"] || args["-u"];
  const inputFile = args["--input_file"] || args["-i"];
  const sessionId = args["--session_id"] || args["-s"];
  const mode = args["--mode"] || args["-m"] || "3";
  const inputSequenceRaw = args["--input_sequence"];

  if (!userRequest && !inputFile) {
    printJson({
      status: "error",
      error: {
        code: "MISSING_INPUT",
        message: "必须至少提供 user_request 或 input_file",
        recoverable: true,
        recovery_hint: "补充生成请求文本或输入文件后重试",
      },
    });
    process.exit(1);
  }

  let inputSequence = null;
  if (inputSequenceRaw) {
    try {
      inputSequence = JSON.parse(inputSequenceRaw);
    } catch (error) {
      printJson({
        status: "error",
        error: {
          code: "INVALID_INPUT_SEQUENCE",
          message: "input_sequence 必须是合法 JSON",
          recoverable: true,
          recovery_hint: "按 JSON 数组格式传参后重试",
        },
      });
      process.exit(1);
    }
  }

  const client = new CWClient();
  const result = normalizeGenerationResult(
    await client.runGeneration({
      userRequest,
      inputFile,
      sessionId,
      mode,
      inputSequence,
    })
  );
  printJson(result);
  if (result.status === "error") {
    process.exit(1);
  }
}

main();
