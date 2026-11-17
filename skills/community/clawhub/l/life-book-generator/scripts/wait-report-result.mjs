#!/usr/bin/env node
import { parseArgs, printJson, requestMaybeJson, resolveBaseUrl, resolveTaskToken, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/wait-report-result.mjs --task-id <id> --task-token <token> [--poll-ms 5000] [--max-wait-ms 3600000]
`;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function positiveInteger(value, fallback, code) {
  const parsed = Number(value ?? fallback);
  if (!Number.isInteger(parsed) || parsed <= 0) throw new Error(code);
  return parsed;
}

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
  const pollMs = positiveInteger(args["poll-ms"], 5000, "POLL_MS_INVALID");
  const maxWaitMs = positiveInteger(args["max-wait-ms"], 3600000, "MAX_WAIT_MS_INVALID");
  const startedAt = Date.now();
  let lastBody = null;

  while (Date.now() - startedAt <= maxWaitMs) {
    const { response, body } = await requestMaybeJson(baseUrl, `/api/agent/report-tasks/${encodeURIComponent(taskId)}/result`, {
      method: "GET",
      headers: { authorization: `Bearer ${taskToken}` },
    }, timeoutMs);
    lastBody = body;
    if (!response.ok) {
      printJson({ ok: false, httpStatus: response.status, baseUrl, ...body });
      process.exit(1);
    }
    if (body?.task?.status === "ready" && body?.result) {
      printJson({ ok: true, httpStatus: response.status, baseUrl, waitedMs: Date.now() - startedAt, ...body });
      return;
    }
    if (body?.task?.status === "failed" || body?.task?.status === "canceled") {
      printJson({ ok: false, httpStatus: response.status, baseUrl, waitedMs: Date.now() - startedAt, ...body });
      process.exit(1);
    }
    await sleep(pollMs);
  }

  printJson({ ok: false, error: "REPORT_WAIT_TIMEOUT", baseUrl, waitedMs: Date.now() - startedAt, last: lastBody });
  process.exit(1);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "WAIT_REPORT_RESULT_FAILED"}\n`);
  process.exit(1);
});
