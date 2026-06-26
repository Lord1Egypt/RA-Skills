#!/usr/bin/env node
/**
 * Pre-flight: print credit balance and exit non-zero on auth failure or zero balance.
 * Usage: POWERLOOM_API_KEY=... node scripts/ensure-credits.mjs
 */

import { callTool } from "./lib/mcp.mjs";

async function main() {
  try {
    const out = await callTool("get_credit_balance", {});
    if (out.error) {
      console.error(String(out.error));
      process.exit(1);
    }
    const balance =
      out.balance ?? out.credits ?? out.credit_balance ?? out.remaining;
    const org = out.organization ?? out.org_id ?? out.org;
    console.log(
      JSON.stringify(
        {
          balance: balance ?? out,
          organization: org ?? null,
          rate_limits: out.rate_limits ?? out.rateLimits ?? null,
        },
        null,
        2
      )
    );
    const n = typeof balance === "number" ? balance : parseFloat(balance);
    if (Number.isFinite(n) && n <= 0) {
      console.error(
        "Zero credits — top up at https://bds-metering.powerloom.io/metering (free tier may still apply; check dashboard)."
      );
      process.exit(1);
    }
  } catch (e) {
    if (e.code === "HTTP_401" || e.code === "NO_API_KEY") {
      console.error(e.message);
      process.exit(1);
    }
    console.error(e.message || e);
    process.exit(1);
  }
}

main();
