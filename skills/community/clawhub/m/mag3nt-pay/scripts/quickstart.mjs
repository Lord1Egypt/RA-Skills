#!/usr/bin/env node

/**
 * mag3nt-pay quickstart
 *
 * Verifies credentials, checks card balance, and confirms
 * which payment protocols are available.
 *
 * Usage:
 *   export MAG3NT_API_KEY=mag3nt_live_...
 *   export MAG3NT_CARD_ID=mag3nt_...
 *   export MAG3NT_CARD_TOKEN=tok_...
 *   node quickstart.mjs
 */

const requiredVars = ["MAG3NT_API_KEY", "MAG3NT_CARD_ID", "MAG3NT_CARD_TOKEN"];
const missing = requiredVars.filter((v) => !process.env[v]);

if (missing.length > 0) {
  console.error("[error] Missing environment variables:", missing.join(", "));
  console.error("        Set them and try again. Get credentials at https://mag3nt.com");
  process.exit(1);
}

const API_KEY = process.env.MAG3NT_API_KEY;
const CARD_ID = process.env.MAG3NT_CARD_ID;
const BASE_URL = "https://mag3nt.com";

async function main() {
  console.log("mag3nt-pay quickstart");
  console.log("---------------------\n");

  // List cards and find the matching card
  const res = await fetch(`${BASE_URL}/api/cards`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`[error] API returned ${res.status}: ${text}`);
    process.exit(1);
  }

  const data = await res.json();
  const cards = Array.isArray(data) ? data : data.cards || [];
  const card = cards.find((c) => c.id === CARD_ID);

  if (!card) {
    console.error(`[error] Card ${CARD_ID} not found. Found ${cards.length} card(s).`);
    if (cards.length > 0) {
      console.error("        Available card IDs:");
      cards.forEach((c) => console.error(`          - ${c.id} (${c.status})`));
    }
    process.exit(1);
  }

  const protocols = (card.accepted_protocols || "x402,mpp,ap2").split(",");

  console.log("  Card ID:      ", card.id);
  console.log("  Status:       ", card.status);
  console.log("  Limit:        ", card.limit_amount, "USDC");
  console.log("  Remaining:    ", card.remaining, "USDC");
  console.log("  Spent:        ", card.balance, "USDC");
  console.log("  Network:      ", card.funding_network || "not set");
  console.log("  Protocols:    ", protocols.join(", "));
  console.log("  Streaming:    ", card.streaming_enabled ? "enabled" : "disabled");
  console.log("");
  console.log("  Supported payment flows:");
  if (protocols.includes("x402"))  console.log("    - x402      single pay-per-request");
  if (protocols.includes("mpp"))   console.log("    - MPP       streaming micropayments");
  if (protocols.includes("ap2"))   console.log("    - AP2       mandate-based recurring");
  console.log("    - Pay Link  universal (always available)");
  console.log("");
  console.log("[ok] Agent card is ready. Call a 402-protected API to test.");
}

main().catch((err) => {
  console.error("[error]", err.message);
  process.exit(1);
});
