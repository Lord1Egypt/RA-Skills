/**
 * Place buy/sell orders on Polymarket CLOB.
 *
 * Usage:
 *   npx tsx trade.ts --token-id <id> --side BUY --order-type GTC --price 0.068 --size 735
 *   npx tsx trade.ts --token-id <id> --side BUY --order-type FOK --amount 50
 *   npx tsx trade.ts --token-id <id> --side SELL --order-type GTC --price 0.90 --size 100
 */

import { parseArgs } from "node:util";
import { performance } from "perf_hooks";
import { loadEnv, initClient, ClobClient, OrderType, Side } from "./lib/client.js";

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

async function pollOrderStatus(
  client: ClobClient,
  orderID: string,
  intervalMs: number = 100,
  timeoutMs: number = 15000,
): Promise<{ status: string; ms: number }> {
  const t0 = performance.now();
  const deadline = t0 + timeoutMs;
  while (performance.now() < deadline) {
    try {
      const order = await client.getOrder(orderID);
      const status = (order as any)?.status ?? "unknown";
      if (["live", "matched", "filled"].includes(status)) {
        return { status, ms: performance.now() - t0 };
      }
      if (["canceled", "cancelled"].includes(status)) {
        return { status: "cancelled", ms: performance.now() - t0 };
      }
    } catch {
      /* order not queryable yet */
    }
    await sleep(intervalMs);
  }
  return { status: "timeout", ms: -1 };
}

async function main() {
  const { values } = parseArgs({
    options: {
      "token-id": { type: "string" },
      side: { type: "string", default: "BUY" },
      "order-type": { type: "string", default: "GTC" },
      price: { type: "string" },
      size: { type: "string" },
      amount: { type: "string" },
    },
    strict: false,
  });

  const tokenID = values["token-id"] as string | undefined;
  const sideStr = ((values.side as string) ?? "BUY").toUpperCase();
  const orderTypeStr = ((values["order-type"] as string) ?? "GTC").toUpperCase();
  const price = values.price ? parseFloat(values.price as string) : undefined;
  const size = values.size ? parseFloat(values.size as string) : undefined;
  const amount = values.amount ? parseFloat(values.amount as string) : undefined;

  if (!tokenID) {
    console.log(JSON.stringify({ error: "--token-id is required", status: "arg_error" }));
    process.exit(1);
  }

  const side = sideStr === "SELL" ? Side.SELL : Side.BUY;
  const env = loadEnv();

  let client: ClobClient;
  try {
    client = await initClient(env);
  } catch (err: any) {
    console.log(JSON.stringify({ error: `Client init failed: ${err.message}`, status: "init_error" }));
    process.exit(1);
  }

  const t0 = performance.now();

  try {
    if (orderTypeStr === "FOK") {
      const orderAmount = amount ?? (size && price ? size * price : 0);
      if (!orderAmount || orderAmount <= 0) {
        console.log(JSON.stringify({ error: "FOK requires --amount or --size + --price", status: "arg_error" }));
        process.exit(1);
      }

      const resp = await (client as any).createAndPostMarketOrder(
        { tokenID, amount: orderAmount, side },
        undefined,
        OrderType.FOK,
      );

      const submitMs = performance.now() - t0;
      const orderID = resp.orderID ?? "";
      const postStatus = resp.status ?? "unknown";

      let finalStatus = postStatus;
      let pollMs = 0;
      if (postStatus === "delayed" && orderID) {
        const poll = await pollOrderStatus(client, orderID);
        finalStatus = poll.status;
        pollMs = poll.ms;
      }

      console.log(JSON.stringify({
        orderID,
        status: finalStatus,
        orderType: "FOK",
        side: sideStr,
        amount: orderAmount,
        latency_ms: Math.round((submitMs + pollMs) * 10) / 10,
      }));

    } else {
      // GTC order
      if (!price || !size) {
        console.log(JSON.stringify({ error: "GTC requires --price and --size", status: "arg_error" }));
        process.exit(1);
      }

      const resp = await client.createAndPostOrder(
        { tokenID, price, size, side },
        undefined,
        OrderType.GTC,
      );

      const submitMs = performance.now() - t0;
      const orderID = resp.orderID ?? "";
      const postStatus = resp.status ?? "unknown";

      if (!orderID) {
        console.log(JSON.stringify({
          error: "No orderID returned",
          postStatus,
          status: "order_failed",
          latency_ms: Math.round(submitMs * 10) / 10,
        }));
        process.exit(1);
      }

      const poll = await pollOrderStatus(client, orderID);

      console.log(JSON.stringify({
        orderID,
        status: poll.status,
        orderType: "GTC",
        side: sideStr as string,
        price,
        size,
        latency_ms: Math.round((submitMs + poll.ms) * 10) / 10,
      }));
    }
  } catch (err: any) {
    const elapsed = performance.now() - t0;
    console.log(JSON.stringify({
      error: err.message,
      status: "execution_error",
      latency_ms: Math.round(elapsed * 10) / 10,
    }));
    try {
      await client!.cancelAll();
    } catch { /* best effort cleanup */ }
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ error: err.message, status: "fatal_error" }));
  process.exit(1);
});
