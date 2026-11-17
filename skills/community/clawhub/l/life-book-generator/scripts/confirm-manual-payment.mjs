#!/usr/bin/env node
import { parseArgs, printJson, requestJson, resolveBaseUrl, resolveTaskToken, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/confirm-manual-payment.mjs --task-id <id> --task-token <token> --channel alipay|wechat|evm

Use after the user says they have paid through the displayed manual payment QR/address.
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
  const channel = String(args.channel ?? "").trim();
  if (!["alipay", "wechat", "evm"].includes(channel)) throw new Error("MANUAL_PAYMENT_CHANNEL_INVALID");
  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const body = await requestJson(baseUrl, `/api/agent/report-tasks/${encodeURIComponent(taskId)}/payment-confirmations`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${taskToken}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ channel }),
  }, timeoutMs);
  printJson({ ok: true, baseUrl, ...body });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "CONFIRM_MANUAL_PAYMENT_FAILED"}\n`);
  process.exit(1);
});
