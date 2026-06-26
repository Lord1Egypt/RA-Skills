/**
 * Query on-chain positions from Polymarket CLOB.
 *
 * Usage:
 *   npx tsx positions.ts
 *   npx tsx positions.ts --address 0x...
 */

import { parseArgs } from "node:util";
import { loadEnv, initClient, ClobClient, HOST } from "./lib/client.js";

interface Position {
  token_id: string;
  size: number;
  avg_price: number;
  current_price: number;
  unrealized_pnl: number;
}

async function main() {
  const { values } = parseArgs({
    options: {
      address: { type: "string" },
    },
    strict: false,
  });

  const env = loadEnv();
  const walletAddress = (values.address as string | undefined) ?? env.eoaAddress;

  let client: ClobClient;
  try {
    client = await initClient(env);
  } catch (err: any) {
    console.log(JSON.stringify({ error: `Client init failed: ${err.message}`, status: "init_error" }));
    process.exit(1);
  }

  try {
    // Fetch positions via the data API
    const url = `${HOST}/positions?address=${walletAddress}`;
    const resp = await fetch(url);

    if (!resp.ok) {
      throw new Error(`Positions API returned ${resp.status}: ${resp.statusText}`);
    }

    const data = await resp.json() as any[];

    const positions: Position[] = [];

    for (const pos of data) {
      const tokenId = pos.asset ?? pos.token_id ?? "";
      const size = parseFloat(pos.size ?? "0");
      const avgPrice = parseFloat(pos.avg_price ?? pos.avgPrice ?? "0");

      if (size <= 0) continue;

      // Get current price from orderbook
      let currentPrice = avgPrice;
      try {
        const book = await client.getOrderBook(tokenId);
        const bids = (book as any)?.bids ?? [];
        const asks = (book as any)?.asks ?? [];
        if (bids.length > 0 && asks.length > 0) {
          currentPrice = (parseFloat(bids[0].price) + parseFloat(asks[0].price)) / 2;
        } else if (bids.length > 0) {
          currentPrice = parseFloat(bids[0].price);
        } else if (asks.length > 0) {
          currentPrice = parseFloat(asks[0].price);
        }
      } catch {
        /* use avg_price as fallback */
      }

      positions.push({
        token_id: tokenId,
        size: Math.round(size * 100) / 100,
        avg_price: Math.round(avgPrice * 10000) / 10000,
        current_price: Math.round(currentPrice * 10000) / 10000,
        unrealized_pnl: Math.round(size * (currentPrice - avgPrice) * 100) / 100,
      });
    }

    console.log(JSON.stringify({
      positions,
      count: positions.length,
      wallet_address: walletAddress,
      status: "ok",
    }));
  } catch (err: any) {
    console.log(JSON.stringify({
      error: err.message,
      status: "positions_error",
    }));
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ error: err.message, status: "fatal_error" }));
  process.exit(1);
});
