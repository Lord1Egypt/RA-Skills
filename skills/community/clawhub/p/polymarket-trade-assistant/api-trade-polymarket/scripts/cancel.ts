/**
 * Cancel orders on Polymarket CLOB.
 *
 * Usage:
 *   npx tsx cancel.ts --order-id <id>
 *   npx tsx cancel.ts --all
 */

import { parseArgs } from "node:util";
import { loadEnv, initClient, ClobClient } from "./lib/client.js";

async function main() {
  const { values } = parseArgs({
    options: {
      "order-id": { type: "string" },
      all: { type: "boolean", default: false },
    },
    strict: false,
  });

  const orderID = values["order-id"] as string | undefined;
  const cancelAll = values.all ?? false;

  if (!orderID && !cancelAll) {
    console.log(JSON.stringify({ error: "--order-id <id> or --all is required", status: "arg_error" }));
    process.exit(1);
  }

  const env = loadEnv();

  let client: ClobClient;
  try {
    client = await initClient(env);
  } catch (err: any) {
    console.log(JSON.stringify({ error: `Client init failed: ${err.message}`, status: "init_error" }));
    process.exit(1);
  }

  try {
    if (cancelAll) {
      const resp = await client.cancelAll();
      // cancelAll may return cancelled order IDs or a success status
      const cancelled: string[] = Array.isArray(resp) ? resp : [];
      console.log(JSON.stringify({
        cancelled,
        count: cancelled.length,
        status: "ok",
      }));
    } else {
      await client.cancelOrder({ orderID: orderID! });
      console.log(JSON.stringify({
        cancelled: [orderID],
        count: 1,
        status: "ok",
      }));
    }
  } catch (err: any) {
    console.log(JSON.stringify({
      error: err.message,
      status: "cancel_error",
    }));
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ error: err.message, status: "fatal_error" }));
  process.exit(1);
});
