#!/usr/bin/env node
/*
Usage:
  Required env:
    PRIVATE_KEY=0x...
    LINKDROP_API_KEY=zpka_...
  Optional env:
    RPC_URL=...
    RPC_URL_POLYGON=...
    RPC_URL_BASE=...
    RPC_URL_ARBITRUM=...
    RPC_URL_OPTIMISM=...
    RPC_URL_AVALANCHE=...
    LINKDROP_BASE_URL=https://p2p.linkdrop.io
    LINKDROP_API_URL=https://escrow-api.linkdrop.io/v3

  Commands:
    node linkdrop-agent.js send --amount 0.01 [--token native|0xToken] [--chain polygon|base|arbitrum|optimism|avalanche]
    node linkdrop-agent.js claim --url "<claimUrl>" --to 0xRecipient [--chain polygon|base|arbitrum|optimism|avalanche]
    Default chain: base

  Positional fallback:
    node linkdrop-agent.js send <amount> [token] [chain]
    node linkdrop-agent.js claim <claimUrl> <to> [chain]
*/

const {
  claimTransfer,
  sendClaimableTransfer,
  serializeError,
} = require("./agentdrop-core");

const USAGE = [
  "linkdrop-agent.js",
  "Commands:",
  "  send --amount <decimal> [--token <native|0xERC20>] [--chain <polygon|base|arbitrum|optimism|avalanche>]",
  "  claim --url <claimUrl> --to <0xAddress> [--chain <polygon|base|arbitrum|optimism|avalanche>]",
  "  default chain: base",
  "Positional fallback:",
  "  send <amount> [token] [chain]",
  "  claim <claimUrl> <to> [chain]",
  "Required env:",
  "  PRIVATE_KEY",
  "  LINKDROP_API_KEY",
].join("\n");

let printed = false;

function printJson(payload) {
  if (printed) {
    return;
  }
  printed = true;
  process.stdout.write(`${JSON.stringify(payload)}\n`);
}

function fail(error, code) {
  const serialized = serializeError(error);
  printJson({
    ok: false,
    error: {
      code: code || serialized.details?.code || "UNKNOWN_ERROR",
      ...serialized,
    },
  });
  process.exitCode = 1;
}

process.on("unhandledRejection", (reason) => {
  fail(reason, "UNHANDLED_REJECTION");
});

process.on("uncaughtException", (error) => {
  fail(error, "UNCAUGHT_EXCEPTION");
});

function parseArgv(args) {
  const flags = {};
  const positionals = [];

  for (let index = 0; index < args.length; index += 1) {
    const token = args[index];
    if (!token.startsWith("--")) {
      positionals.push(token);
      continue;
    }

    const withoutPrefix = token.slice(2);
    if (withoutPrefix.length === 0) {
      continue;
    }

    const eqIndex = withoutPrefix.indexOf("=");
    if (eqIndex >= 0) {
      const key = withoutPrefix.slice(0, eqIndex);
      const value = withoutPrefix.slice(eqIndex + 1);
      flags[key] = value;
      continue;
    }

    const next = args[index + 1];
    if (next && !next.startsWith("--")) {
      flags[withoutPrefix] = next;
      index += 1;
    } else {
      flags[withoutPrefix] = true;
    }
  }

  return { flags, positionals };
}

function getHelpPayload() {
  return {
    ok: true,
    usage: USAGE,
    examples: [
      "node linkdrop-agent.js send --amount 0.01 --token native --chain base",
      "node linkdrop-agent.js send --amount 5 --token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --chain polygon",
      "node linkdrop-agent.js claim --url \"https://...\" --to 0x000000000000000000000000000000000000dead --chain base",
    ],
  };
}

async function runSendCommand(parsed) {
  const amountInput = parsed.flags.amount || parsed.positionals[0];
  const tokenInput = parsed.flags.token || parsed.positionals[1] || "native";
  const chainInput = parsed.flags.chain || parsed.positionals[2] || "base";
  return sendClaimableTransfer({
    amount: amountInput,
    token: tokenInput,
    chain: chainInput,
  });
}

async function runClaimCommand(parsed) {
  const claimUrl = parsed.flags.url || parsed.positionals[0];
  const destination = parsed.flags.to || parsed.positionals[1];
  const chainInput = parsed.flags.chain || parsed.positionals[2] || "base";
  return claimTransfer({
    claimUrl,
    to: destination,
    chain: chainInput,
  });
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length === 0 || argv.includes("--help") || argv[0] === "help") {
    printJson(getHelpPayload());
    return;
  }

  const command = String(argv[0]).toLowerCase();
  const parsed = parseArgv(argv.slice(1));
  if (command === "send") {
    const result = await runSendCommand(parsed);
    printJson(result);
    return;
  }

  if (command === "claim") {
    const result = await runClaimCommand(parsed);
    printJson(result);
    return;
  }

  throw new Error(`Unknown command '${command}'. Use 'send' or 'claim'.`);
}

main().catch((error) => {
  fail(error);
});
