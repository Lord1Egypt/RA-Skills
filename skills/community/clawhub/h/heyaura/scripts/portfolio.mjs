#!/usr/bin/env node

import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import {
  appendPaymentIdentifierToExtensions,
  generatePaymentId,
  isValidPaymentId,
  PAYMENT_IDENTIFIER,
} from "@x402/extensions/payment-identifier";
import { wrapFetchWithPayment, x402Client, x402HTTPClient } from "@x402/fetch";
import { privateKeyToAccount } from "viem/accounts";

const API_ORIGIN = "https://aura.adex.network";
const API_PATH = "/api/x402/portfolio/balances";
const REQUEST_TIMEOUT_MS = 60_000;
const PRIVATE_KEY_ENV = "HEYAURA_EVM_PRIVATE_KEY";

const KNOWN_ASSETS = new Map([
  [
    "eip155:8453:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    { symbol: "USDC", decimals: 6 },
  ],
  [
    "eip155:1187947933:0x85889c8c714505e0c94b30fcfcf64fe3ac8fcb20",
    { symbol: "USDC", decimals: 6 },
  ],
]);

function usage() {
  return `Usage:
  portfolio.mjs status
  portfolio.mjs inspect --address <wallet-or-ens>
  portfolio.mjs pay --address <wallet-or-ens> --network <caip2> --asset <address> --amount <atomic> --pay-to <address> --confirm-payment YES [--payment-identifier <id>]

Payment environment:
  HEYAURA_EVM_PRIVATE_KEY  Local EVM payer key; required only by pay`;
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const args = {};

  for (let index = 0; index < rest.length; index += 1) {
    const flag = rest[index];
    if (!flag.startsWith("--")) {
      throw new Error(`Unexpected argument: ${flag}`);
    }

    const key = flag.slice(2);
    const value = rest[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }

    args[key] = value;
    index += 1;
  }

  return { command, args };
}

function requireArg(args, key) {
  const value = args[key];
  if (!value) {
    throw new Error(`Missing required --${key}`);
  }
  return value;
}

function validatePortfolioAddress(value) {
  const isEvmAddress = /^0x[0-9a-fA-F]{40}$/.test(value);
  const isEnsName = /^(?=.{3,255}$)[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$/.test(value);
  if (!isEvmAddress && !isEnsName) {
    throw new Error("Address must be a 20-byte EVM address or an ENS-style name");
  }
}

function validateEvmAddress(value, label) {
  if (!/^0x[0-9a-fA-F]{40}$/.test(value)) {
    throw new Error(`${label} must be a 20-byte EVM address`);
  }
}

function validateAtomicAmount(value) {
  if (!/^[0-9]+$/.test(value) || BigInt(value) <= 0n) {
    throw new Error("Payment amount must be a positive atomic-unit integer");
  }
}

function validatePaymentIdentifier(value) {
  if (!isValidPaymentId(value)) {
    throw new Error(
      "Payment identifier must be 16-128 characters using only letters, numbers, hyphens, and underscores",
    );
  }
}

function buildUrl(address) {
  const url = new URL(API_PATH, API_ORIGIN);
  url.searchParams.set("address", address);
  return url;
}

function loadPayer() {
  const privateKey = process.env[PRIVATE_KEY_ENV];
  if (!privateKey) return null;
  if (!/^0x[0-9a-fA-F]{64}$/.test(privateKey)) {
    throw new Error(`${PRIVATE_KEY_ENV} must be a 32-byte 0x-prefixed private key`);
  }

  try {
    return privateKeyToAccount(privateKey);
  } catch {
    throw new Error(`${PRIVATE_KEY_ENV} is not a valid EVM private key`);
  }
}

function payerStatus() {
  const payer = loadPayer();
  return {
    payerConfigured: payer !== null,
    payerAddress: payer?.address ?? null,
  };
}

async function saveResult(result) {
  const directory = await mkdtemp(join(tmpdir(), "heyaura-portfolio-"));
  const resultFile = join(directory, "result.json");
  const json = `${JSON.stringify(result, null, 2)}\n`;
  await writeFile(resultFile, json, {
    encoding: "utf8",
    flag: "wx",
    mode: 0o600,
  });

  return {
    status: result.status,
    resultFile,
    resultBytes: Buffer.byteLength(json),
  };
}

function decodeBase64Json(value, headerName) {
  try {
    return JSON.parse(Buffer.from(value, "base64").toString("utf8"));
  } catch {
    throw new Error(`Invalid ${headerName} header returned by the API`);
  }
}

function formatUnits(amount, decimals) {
  const digits = amount.padStart(decimals + 1, "0");
  const integer = digits.slice(0, -decimals) || "0";
  const fraction = digits.slice(-decimals).replace(/0+$/, "");
  return fraction ? `${integer}.${fraction}` : integer;
}

function describeRequirement(requirement) {
  const asset = requirement.asset?.toLowerCase();
  const known = KNOWN_ASSETS.get(`${requirement.network}:${asset}`);
  return {
    scheme: requirement.scheme,
    network: requirement.network,
    amountAtomic: requirement.amount,
    amount: known ? formatUnits(requirement.amount, known.decimals) : null,
    symbol: known?.symbol ?? requirement.extra?.name ?? null,
    asset: requirement.asset,
    payTo: requirement.payTo,
    maxTimeoutSeconds: requirement.maxTimeoutSeconds,
  };
}

function describeExtensions(extensions) {
  const names = Object.keys(extensions ?? {}).sort();
  const paymentIdentifier = extensions?.[PAYMENT_IDENTIFIER];
  return {
    names,
    paymentIdentifier: {
      advertised: paymentIdentifier !== undefined,
      required: paymentIdentifier?.info?.required === true,
    },
  };
}

async function readBody(response) {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function inspect(address) {
  const response = await fetch(buildUrl(address), {
    method: "GET",
    headers: { Accept: "application/json" },
    redirect: "error",
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });

  if (response.status === 402) {
    const encoded = response.headers.get("payment-required");
    if (!encoded) {
      throw new Error("API returned 402 without a PAYMENT-REQUIRED header");
    }

    const challenge = decodeBase64Json(encoded, "PAYMENT-REQUIRED");
    if (challenge.x402Version !== 2 || !Array.isArray(challenge.accepts)) {
      throw new Error("Unsupported or malformed x402 payment challenge");
    }

    return {
      status: 402,
      paymentRequired: true,
      x402Version: challenge.x402Version,
      resource: challenge.resource,
      accepts: challenge.accepts.map(describeRequirement),
      extensions: describeExtensions(challenge.extensions),
    };
  }

  const body = await readBody(response);
  if (!response.ok) {
    throw new Error(`heyAura API returned HTTP ${response.status}: ${JSON.stringify(body)}`);
  }

  return { status: response.status, paymentRequired: false, data: body };
}

function createExactSelector(expected) {
  return (_version, accepts) => {
    const matches = accepts.filter(requirement =>
      requirement.scheme === "exact" &&
      requirement.network === expected.network &&
      requirement.asset?.toLowerCase() === expected.asset.toLowerCase() &&
      requirement.amount === expected.amount &&
      requirement.payTo?.toLowerCase() === expected.payTo.toLowerCase()
    );

    if (matches.length !== 1) {
      throw new Error("Live x402 terms do not exactly match the confirmed payment");
    }
    return matches[0];
  };
}

async function pay(address, expected) {
  const signer = loadPayer();
  if (!signer) {
    throw new Error(`${PRIVATE_KEY_ENV} is not configured`);
  }
  const selector = createExactSelector(expected);
  const paymentIdentifier = expected.paymentIdentifier ?? generatePaymentId("heyaura_");
  let paymentIdentifierApplied = false;
  const client = new x402Client(selector)
    .register(expected.network, new ExactEvmScheme(signer))
    .registerPolicy((_version, requirements) => requirements.filter(requirement =>
      requirement.scheme === "exact" &&
      requirement.network === expected.network &&
      requirement.asset?.toLowerCase() === expected.asset.toLowerCase() &&
      requirement.payTo?.toLowerCase() === expected.payTo.toLowerCase() &&
      requirement.amount === expected.amount
    ))
    .onBeforePaymentCreation(async context => {
      selector(context.paymentRequired.x402Version, [context.selectedRequirements]);
      const extensions = context.paymentRequired.extensions;
      if (extensions) {
        appendPaymentIdentifierToExtensions(extensions, paymentIdentifier);
        paymentIdentifierApplied =
          extensions[PAYMENT_IDENTIFIER]?.info?.id === paymentIdentifier;
      }
    });

  const fetchWithPayment = wrapFetchWithPayment(fetch, client);
  let response;
  try {
    response = await fetchWithPayment(buildUrl(address), {
      method: "GET",
      headers: { Accept: "application/json" },
      redirect: "error",
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });
  } catch (cause) {
    const message = cause instanceof Error ? cause.message : String(cause);
    const error = new Error(message, { cause });
    error.paymentIdentifier = paymentIdentifier;
    error.paymentIdentifierApplied = paymentIdentifierApplied;
    throw error;
  }
  const body = await readBody(response);

  let settlement = null;
  try {
    settlement = new x402HTTPClient(client).getPaymentSettleResponse(name =>
      response.headers.get(name),
    );
  } catch {
    settlement = null;
  }

  if (!response.ok) {
    const paymentState = settlement ? ` Settlement: ${JSON.stringify(settlement)}` : "";
    const error = new Error(
      `heyAura API returned HTTP ${response.status}: ${JSON.stringify(body)}.${paymentState}`,
    );
    error.paymentIdentifier = paymentIdentifier;
    error.paymentIdentifierApplied = paymentIdentifierApplied;
    throw error;
  }

  return {
    status: response.status,
    data: body,
    payment: {
      payer: signer.address,
      ...describeRequirement({ scheme: "exact", ...expected }),
      paymentIdentifier,
      paymentIdentifierApplied,
      settlement,
    },
  };
}

async function main() {
  const { command, args } = parseArgs(process.argv.slice(2));
  if (command !== "status" && command !== "inspect" && command !== "pay") {
    throw new Error(usage());
  }

  if (command === "status") {
    if (Object.keys(args).length > 0) {
      throw new Error("status does not accept arguments");
    }
    console.log(JSON.stringify(payerStatus(), null, 2));
    return;
  }

  const address = requireArg(args, "address");
  validatePortfolioAddress(address);

  if (command === "inspect") {
    const result = await inspect(address);
    const output = result.paymentRequired ? result : await saveResult(result);
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (requireArg(args, "confirm-payment") !== "YES") {
    throw new Error("Payment requires --confirm-payment YES after explicit user confirmation");
  }

  const expected = {
    network: requireArg(args, "network"),
    asset: requireArg(args, "asset"),
    amount: requireArg(args, "amount"),
    payTo: requireArg(args, "pay-to"),
    paymentIdentifier: args["payment-identifier"] ?? null,
  };
  if (!/^eip155:[0-9]+$/.test(expected.network)) {
    throw new Error("Payment network must be an EVM CAIP-2 identifier such as eip155:8453");
  }
  validateEvmAddress(expected.asset, "Payment asset");
  validateEvmAddress(expected.payTo, "Payment payee");
  validateAtomicAmount(expected.amount);
  if (expected.paymentIdentifier) {
    validatePaymentIdentifier(expected.paymentIdentifier);
  }

  console.log(JSON.stringify(await saveResult(await pay(address, expected)), null, 2));
}

main().catch(error => {
  const message = error instanceof Error ? error.message : String(error);
  const output = { error: message };
  if (error?.paymentIdentifier) {
    output.paymentIdentifier = error.paymentIdentifier;
    output.paymentIdentifierApplied = error.paymentIdentifierApplied;
  }
  console.error(JSON.stringify(output, null, 2));
  process.exitCode = 1;
});
