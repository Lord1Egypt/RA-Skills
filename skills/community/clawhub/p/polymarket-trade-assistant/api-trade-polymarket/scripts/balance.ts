/**
 * Query USDC balance and allowance on Polymarket.
 *
 * Usage:
 *   npx tsx balance.ts
 */

import { loadEnv, initClient, ClobClient } from "./lib/client.js";

async function main() {
  const env = loadEnv();

  let client: ClobClient;
  try {
    client = await initClient(env);
  } catch (err: any) {
    console.log(JSON.stringify({ error: `Client init failed: ${err.message}`, status: "init_error" }));
    process.exit(1);
  }

  try {
    const resp = await (client as any).getBalanceAllowance();
    // The API returns { balance: string, allowance: string } or similar
    const balance = parseFloat(resp?.balance ?? "0");
    const allowance = parseFloat(resp?.allowance ?? "0");

    console.log(JSON.stringify({
      usdc_balance: Math.round(balance * 100) / 100,
      allowance: Math.round(allowance * 100) / 100,
      wallet_address: env.eoaAddress,
      status: "ok",
    }));
  } catch (err: any) {
    console.log(JSON.stringify({
      error: err.message,
      status: "balance_error",
    }));
    process.exit(1);
  }
}

main().catch((err) => {
  console.log(JSON.stringify({ error: err.message, status: "fatal_error" }));
  process.exit(1);
});
