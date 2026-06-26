import { walletAddress } from "./setup-gateway.js";
import { GatewayClient } from "./gateway-client.js";

///////////////////////////////////////////////////////////////////////////////
// Check Gateway info and unified USDC balance
// This script queries the Gateway API to show:
// 1. Which chains are supported (wallet + minter contracts)
// 2. Your unified USDC balance across all chains

const gatewayClient = new GatewayClient();

console.log("═══════════════════════════════════════════════");
console.log("  Nexwave Gateway — Balance Check");
console.log("═══════════════════════════════════════════════");
console.log(`Account: ${walletAddress}\n`);

// Fetch supported chain info
console.log("📡 Fetching Gateway API info...");
const info = await gatewayClient.info();
console.log(`   API Version: ${info.version}`);
console.log("   Supported chains:");
for (const domain of info.domains) {
  const hasWallet = "walletContract" in domain;
  const hasMinter = "minterContract" in domain;
  console.log(
    `   • ${domain.chain} ${domain.network} — wallet: ${hasWallet ? "✅" : "❌"}, minter: ${hasMinter ? "✅" : "❌"}`
  );
}

// Check unified balance
console.log("\n💰 Checking unified USDC balance...");
const { balances } = await gatewayClient.balances("USDC", walletAddress);

let totalBalance = 0;
for (const balance of balances) {
  const chainName =
    GatewayClient.CHAINS[balance.domain] || `Domain ${balance.domain}`;
  const amount = parseFloat(balance.balance);
  totalBalance += amount;
  console.log(`   • ${chainName}: ${balance.balance} USDC`);
}

console.log(`\n   📊 Total unified balance: ${totalBalance.toFixed(6)} USDC`);
console.log("\n═══════════════════════════════════════════════");

process.exit(0);
