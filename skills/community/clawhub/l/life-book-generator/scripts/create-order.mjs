#!/usr/bin/env node
import { parseArgs, printJson, requestJson, resolveBaseUrl, resolveTimeoutMs } from "./_shared.mjs";

const HELP = `Usage:
  node skills/life-book-generator/scripts/create-order.mjs --intake-id <id> [--edition lite|pro]
`;

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(HELP);
    return;
  }
  const intakeId = String(args["intake-id"] ?? "").trim();
  if (!intakeId) throw new Error("INTAKE_ID_REQUIRED");
  const edition = String(args.edition ?? "pro").trim();
  if (edition !== "lite" && edition !== "pro") throw new Error("REPORT_EDITION_INVALID");

  const baseUrl = resolveBaseUrl(args);
  const timeoutMs = resolveTimeoutMs(args);
  const body = await requestJson(baseUrl, "/api/orders", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ intakeId, reportEdition: edition }),
  }, timeoutMs);

  printJson({
    ok: true,
    baseUrl,
    intakeId,
    edition,
    orderId: body.orderId,
    orderNumber: body.orderNumber,
    status: body.status,
    provider: body.provider,
    awaitingReview: body.awaitingReview,
    reportId: body.reportId,
    amountFen: body.amountFen,
    payUrl: body.payUrl ?? null,
    qrCodeUrl: body.qrCodeUrl ?? null,
    paymentStatusUrl: `${baseUrl}/payment/success?order=${encodeURIComponent(body.orderId)}`,
    checkoutUrl: `${baseUrl}/checkout/${encodeURIComponent(intakeId)}`,
  });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.message : "CREATE_ORDER_FAILED"}\n`);
  process.exit(1);
});
