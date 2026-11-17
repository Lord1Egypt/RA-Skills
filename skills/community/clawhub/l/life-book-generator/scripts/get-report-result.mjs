#!/usr/bin/env node
import { parseArgs, printJson, requestMaybeJson, resolveBaseUrl, resolveTaskToken, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/get-report-result.mjs --task-id <id> --task-token <token>

Returns HTTP 202 with result:null until the report is ready.
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const taskId = String(args["task-id"] ?? "").trim();
  if (!taskId) throw new Error("TASK_ID_REQUIRED");
  const taskToken = resolveTaskToken(args);
  if (!taskToken) throw new Error("TASK_TOKEN_REQUIRED");
  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const { response, body } = await requestMaybeJson(baseUrl, `/api/agent/report-tasks/${encodeURIComponent(taskId)}/result`, {
    method: "GET",
    headers: { authorization: `Bearer ${taskToken}` },
  }, timeoutMs);
  printJson({ ok: response.ok, httpStatus: response.status, baseUrl, ...body });
  if (!response.ok) process.exit(1);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "GET_REPORT_RESULT_FAILED"}\n`);
  process.exit(1);
});
