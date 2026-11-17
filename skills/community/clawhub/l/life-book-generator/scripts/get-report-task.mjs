#!/usr/bin/env node
import { parseArgs, printJson, requestJson, resolveBaseUrl, resolveTaskToken, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/get-report-task.mjs --task-id <id> --task-token <token>

You can also set LIFE_BOOK_TASK_TOKEN.
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
  const body = await requestJson(baseUrl, `/api/agent/report-tasks/${encodeURIComponent(taskId)}`, {
    method: "GET",
    headers: { authorization: `Bearer ${taskToken}` },
  }, timeoutMs);
  printJson({ ok: true, baseUrl, ...body });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "GET_REPORT_TASK_FAILED"}\n`);
  process.exit(1);
});
