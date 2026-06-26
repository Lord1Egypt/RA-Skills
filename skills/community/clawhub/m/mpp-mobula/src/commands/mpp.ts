/**
 * MPP (Machine Payments Protocol) CLI.
 *
 * Pay-as-you-go Mobula API calls via Tempo (chainId 4217) USDC.e.
 * Each call costs ~$0.0004 and is settled directly from your wallet —
 * no subscription, no API key, no signup.
 */

import { tempoFetch, getTempoBalance, BRIDGE_URL } from "../mpp/tempo-client";
import {
  CLI_WALLET_FILE,
  createCliWallet,
  loadCliWallet,
  requireCliWallet,
} from "../cli-wallet";

function bridgeUrl(address: string): string {
  return `${BRIDGE_URL}?toAddress=${address}`;
}

export async function mppCommand(args: string[]): Promise<void> {
  const [subcommand, ...rest] = args;

  try {
    switch (subcommand) {
      case "wallet-create": {
        const w = await createCliWallet();
        console.log("✓ Wallet created");
        console.log(`Address: ${w.address}`);
        console.log(`Saved to: ${CLI_WALLET_FILE}`);
        console.log("\nNext: fund it with USDC.e on Tempo (chainId 4217):");
        console.log(`  ${bridgeUrl(w.address)}`);
        console.log("\nAny amount works — calls cost ~$0.0004 each.");
        break;
      }

      case "wallet-info":
      case "balance": {
        const w = await requireCliWallet();
        let usd = "?";
        try {
          const raw = await getTempoBalance(w.address);
          usd = (Number(raw) / 1_000_000).toFixed(4);
        } catch (e: any) {
          console.error("Could not fetch on-chain balance:", e.message);
        }
        console.log(`Address:   ${w.address}`);
        console.log(`USDC.e:    $${usd} (Tempo, chainId 4217)`);
        console.log(`Bridge:    ${bridgeUrl(w.address)}`);
        break;
      }

      case "price": {
        const [asset] = rest;
        if (!asset) {
          console.error("Usage: bun run start price <asset>");
          console.error("Example: bun run start price bitcoin");
          process.exit(1);
        }
        const w = await requireCliWallet();
        const data = await tempoFetch(
          "/api/2/token/price",
          { asset },
          w.privateKey,
        );
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case "wallet": {
        const [address] = rest;
        if (!address) {
          console.error("Usage: bun run start wallet <address>");
          process.exit(1);
        }
        const w = await requireCliWallet();
        const data = await tempoFetch(
          "/api/2/wallet/positions",
          { wallet: address },
          w.privateKey,
        );
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case "lighthouse": {
        const w = await requireCliWallet();
        const data = await tempoFetch(
          "/api/2/market/lighthouse",
          {},
          w.privateKey,
        );
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case "call": {
        const [path, ...kvs] = rest;
        if (!path) {
          console.error('Usage: bun run start call <path> [key=value ...]');
          console.error('Example: bun run start call /api/2/wallet/activity wallet=0xabc');
          process.exit(1);
        }
        const params: Record<string, string> = {};
        for (const kv of kvs) {
          const idx = kv.indexOf("=");
          if (idx > 0) params[kv.slice(0, idx)] = kv.slice(idx + 1);
        }
        const w = await requireCliWallet();
        const data = await tempoFetch(path, params, w.privateKey);
        console.log(JSON.stringify(data, null, 2));
        break;
      }

      case "subscribe":
      case "status":
      case "topup":
      case "key-create":
      case "key-revoke": {
        console.error(
          `The "${subcommand}" command is no longer supported.`,
        );
        console.error(
          `Mobula MPP currently only ships pay-as-you-go via Tempo (USDC.e).`,
        );
        console.error("");
        console.error("To get started:");
        console.error("  1. bun run start wallet-create");
        console.error(
          `  2. fund the wallet at ${BRIDGE_URL}?toAddress=<your-addr>`,
        );
        console.error("  3. bun run start price bitcoin");
        process.exit(1);
        break;
      }

      case "help":
      case undefined:
      default: {
        const wallet = await loadCliWallet();
        console.log(`
MPP — Pay-as-you-go Mobula API client (Tempo / USDC.e)

Setup:
  bun run start wallet-create      Generate a Tempo hot wallet
  bun run start balance            Show address + USDC.e balance + bridge link

Data calls (each costs ~$0.0004 from your USDC.e balance):
  bun run start price <asset>      Token price (e.g. bitcoin, ethereum, 0x...)
  bun run start wallet <address>   Wallet positions
  bun run start lighthouse         Trending tokens
  bun run start call <path> k=v..  Generic call (any /api/2/* endpoint)

Removed (subscription endpoints not available):
  subscribe, status, topup, key-create, key-revoke

Wallet location:
  ${CLI_WALLET_FILE}${wallet ? `\n  Address: ${wallet.address}` : "  (not yet created)"}

Docs: https://github.com/Flotapponnier/mpp-skill
        `.trim());
        break;
      }
    }
  } catch (error: any) {
    console.error("\n❌ Error:", error.message);
    process.exit(1);
  }
}
