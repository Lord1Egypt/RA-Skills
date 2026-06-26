/**
 * Place orders on Polymarket CLOB.
 * Based on https://github.com/Alchemist-X/pm-PlaceOrder
 *
 * Usage:
 *   npx tsx place_order.ts --token-id <id> --side BUY --type GTC --price 0.068 --size 735
 *   npx tsx place_order.ts --token-id <id> --side BUY --type FOK --amount 50
 */

import dotenv from "dotenv";
dotenv.config({ path: ".env.aizen" });

import { ClobClient, OrderType, Side } from "@polymarket/clob-client";
import { Wallet } from "ethers";
import { performance } from "perf_hooks";
import { parseArgs } from "node:util";

const HOST = "https://clob.polymarket.com";
const CHAIN_ID = 137;

interface ClientEnv {
  privateKey: string;
  funderAddress: string;
  signatureType: number;
}

function loadEnv(): ClientEnv {
  const privateKey = process.env.PRIVATE_KEY ?? "";
  const funderAddress = process.env.FUNDER_ADDRESS ?? "";
  const signatureType = parseInt(process.env.SIGNATURE_TYPE ?? "1", 10);

  if (!privateKey || !funderAddress) {
    console.error(JSON.stringify({
      error: "Missing PRIVATE_KEY or FUNDER_ADDRESS in .env.aizen",
      status: "config_error",
    }));
    process.exit(1);
  }

  return { privateKey, funderAddress, signatureType };
}

async function initClient(env: ClientEnv): Promise<ClobClient> {
  const signer = new Wallet(env.privateKey);
  const temp = new ClobClient(HOST, CHAIN_ID, signer);
  const creds = await temp.createOrDeriveApiKey();
  return new ClobClient(HOST, CHAIN_ID, signer, creds, env.signatureType, env.funderAddress);
}

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
      type: { type: "string", default: "GTC" },
      price: { type: "string" },
      size: { type: "string" },
      amount: { type: "string" },
    },
    strict: false,
  });

  const tokenID = values["token-id"];
  const sideStr = (values.side ?? "BUY").toUpperCase();
  const typeStr = (values.type ?? "GTC").toUpperCase();
  const price = values.price ? parseFloat(values.price) : undefined;
  const size = values.size ? parseFloat(values.size) : undefined;
  const amount = values.amount ? parseFloat(values.amount) : undefined;

  if (!tokenID) {
    console.error(JSON.stringify({ error: "--token-id is required", status: "arg_error" }));
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
    if (typeStr === "FOK") {
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
        side: sideStr,
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
