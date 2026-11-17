#!/usr/bin/env node
import { parseArgs, printJson, requestJson, resolveBaseUrl, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/get-order.mjs --order-id <id>
`;

function canOpenPaymentStatus(order) {
  return order.provider !== "manual_qr" || order.awaitingReview || order.status === "paid";
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const orderId = String(args["order-id"] ?? "").trim();
  if (!orderId) throw new Error("ORDER_ID_REQUIRED");

  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const body = await requestJson(baseUrl, `/api/orders/${encodeURIComponent(orderId)}`, {
    method: "GET",
  }, timeoutMs);

  printJson({
    ok: true,
    baseUrl,
    orderId: body.orderId,
    orderNumber: body.orderNumber,
    status: body.status,
    provider: body.provider,
    awaitingReview: body.awaitingReview,
    reportId: body.reportId,
    reportEdition: body.reportEdition,
    amountFen: body.amountFen,
    manualPaymentChannel: body.manualPaymentChannel ?? null,
    paymentStatusUrl: `${baseUrl}/payment/success?order=${encodeURIComponent(body.orderId)}`,
    canOpenPaymentStatus: canOpenPaymentStatus(body),
  });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "GET_ORDER_FAILED"}\n`);
  process.exit(1);
});
