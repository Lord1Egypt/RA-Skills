#!/usr/bin/env node
import {
  parseArgs,
  printJson,
  readJsonInput,
  requestMaybeJson,
  resolveAgentApiKey,
  resolveBaseUrl,
  resolveTimeoutMs,
} from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/create-report-task.mjs --input-file <path> --edition lite|pro
  node skills/life-book-generator/scripts/create-report-task.mjs --input '{"version":"intake@1", ...}' --edition lite

Optional:
  --idempotency-key <key>
  --agent-api-key <key>     # or LIFE_BOOK_AGENT_API_KEY
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const edition = String(args.edition ?? "pro").trim();
  if (edition !== "lite" && edition !== "pro") throw new Error("REPORT_EDITION_INVALID");
  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const agentApiKey = resolveAgentApiKey(args);
  const intake = await readJsonInput(args);
  const headers = { "content-type": "application/json" };
  if (agentApiKey) headers.authorization = `Bearer ${agentApiKey}`;
  if (args["idempotency-key"]) headers["idempotency-key"] = String(args["idempotency-key"]);

  const { response, body } = await requestMaybeJson(baseUrl, "/api/agent/report-tasks", {
    method: "POST",
    headers,
    body: JSON.stringify({
      edition,
      idempotencyKey: args["idempotency-key"] ? String(args["idempotency-key"]) : undefined,
      intake,
    }),
  }, timeoutMs);

  printJson({
    ok: response.ok,
    httpStatus: response.status,
    baseUrl,
    ...body,
    taskStatusUrl: body?.task?.id ? `${baseUrl}/api/agent/report-tasks/${encodeURIComponent(body.task.id)}` : null,
    taskResultUrl: body?.task?.id ? `${baseUrl}/api/agent/report-tasks/${encodeURIComponent(body.task.id)}/result` : null,
    taskStreamUrl: body?.task?.id ? `${baseUrl}/api/agent/report-tasks/${encodeURIComponent(body.task.id)}/stream` : null,
  });
  if (!response.ok && response.status !== 402) process.exit(1);
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "CREATE_REPORT_TASK_FAILED"}\n`);
  process.exit(1);
});
