/**
 * Read orderbook and compute smart pricing from Polymarket CLOB.
 *
 * Usage:
 *   npx tsx orderbook.ts --token-id <id>
 *   npx tsx orderbook.ts --token-id <id> --side BUY --urgency medium --depth 5
 */

import { parseArgs } from "node:util";
import { loadEnv, initClient, ClobClient } from "./lib/client.js";

const URGENCY_FACTORS: Record<string, number> = {
  low: 0.2,
  medium: 0.3,
  high: 0.5,
};

async function main() {
  const { values } = parseArgs({
    options: {
      "token-id": { type: "string" },
      side: { type: "string" },
      urgency: { type: "string", default: "medium" },
      depth: { type: "string", default: "5" },
    },
    strict: false,
  });

  const tokenID = values["token-id"] as string | undefined;
  const sideStr = (values.side as string | undefined)?.toUpperCase();
  const urgency = ((values.urgency as string) ?? "medium").toLowerCase();
  const depth = parseInt((values.depth as string) ?? "5", 10);

  if (!tokenID) {
    console.log(JSON.stringify({ error: "--token-id is required", status: "arg_error" }));
    process.exit(1);
  }

  const urgencyFactor = URGENCY_FACTORS[urgency] ?? 0.3;

  const env = loadEnv();

  let client: ClobClient;
  try {
    client = await initClient(env);
  } catch (err: any) {
    console.log(JSON.stringify({ error: `Client init failed: ${err.message}`, status: "init_error" }));
    process.exit(1);
  }

  try {
    const book = await client.getOrderBook(tokenID);
    const bids: Array<{ price: string; size: string }> = (book as any)?.bids ?? [];
    const asks: Array<{ price: string; size: string }> = (book as any)?.asks ?? [];

    if (bids.length === 0 && asks.length === 0) {
      console.log(JSON.stringify({
        error: "Empty orderbook — no bids or asks",
        token_id: tokenID,
        status: "empty_book",
      }));
      process.exit(1);
    }

    const bestBid = bids.length > 0 ? parseFloat(bids[0].price) : 0;
    const bestAsk = asks.length > 0 ? parseFloat(asks[0].price) : 1;
    const spread = Math.round((bestAsk - bestBid) * 10000) / 10000;
    const spreadPct = bestBid > 0 ? Math.round((spread / bestBid) * 10000) / 100 : 0;

    // Smart price calculation
    let smartPrice: number | null = null;
    if (sideStr === "BUY") {
      smartPrice = Math.round((bestBid + spread * urgencyFactor) * 10000) / 10000;
    } else if (sideStr === "SELL") {
      smartPrice = Math.round((bestAsk - spread * urgencyFactor) * 10000) / 10000;
    }

    // Depth within 2% of best price
    const bidDepthLimit = bestBid * 0.98;
    const askDepthLimit = bestAsk * 1.02;

    let depthBidSize = 0;
    let depthBidUsd = 0;
    for (const b of bids) {
      const p = parseFloat(b.price);
      const s = parseFloat(b.size);
      if (p >= bidDepthLimit) {
        depthBidSize += s;
        depthBidUsd += s * p;
      }
    }

    let depthAskSize = 0;
    let depthAskUsd = 0;
    for (const a of asks) {
      const p = parseFloat(a.price);
      const s = parseFloat(a.size);
      if (p <= askDepthLimit) {
        depthAskSize += s;
        depthAskUsd += s * p;
      }
    }

    // Build level arrays (truncated to depth)
    const bidLevels = bids.slice(0, depth).map((b) => [b.price, b.size]);
    const askLevels = asks.slice(0, depth).map((a) => [a.price, a.size]);

    const result: any = {
      best_bid: bestBid,
      best_ask: bestAsk,
      spread,
      spread_pct: spreadPct,
      depth_2pct: {
        bid_size: Math.round(depthBidSize * 100) / 100,
        ask_size: Math.round(depthAskSize * 100) / 100,
        bid_usd: Math.round(depthBidUsd * 100) / 100,
        ask_usd: Math.round(depthAskUsd * 100) / 100,
      },
      levels: {
        bids: bidLevels,
        asks: askLevels,
      },
      status: "ok",
    };

    if (smartPrice !== null) {
      result.smart_price = smartPrice;
      result.urgency = urgency;
      result.urgency_factor = urgencyFactor;
    }

    console.log(JSON.stringify(result));
  } catch (err: any) {
    console.log(JSON.stringify({
      error: err.message,
      status: "orderbook_error",
    }));
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ error: err.message, status: "fatal_error" }));
  process.exit(1);
});
