#!/usr/bin/env tsx

// src/cli/args.ts
import { parseArgs } from "util";
function parseCliInput() {
  const { positionals, values } = parseArgs({
    allowPositionals: true,
    options: {
      chains: { type: "string" },
      topic: { type: "string" },
      address: { type: "string" },
      message: { type: "string" },
      chain: { type: "string" },
      to: { type: "string" },
      data: { type: "string" },
      value: { type: "string" },
      gas: { type: "string" },
      gasPrice: { type: "string" },
      all: { type: "boolean" },
      clean: { type: "boolean" },
      open: { type: "boolean" },
      "no-simulate": { type: "boolean" },
      "debug-log-file": { type: "string" },
      help: { type: "boolean", short: "h" }
    }
  });
  return {
    command: positionals[0],
    help: Boolean(values.help),
    debugLogFile: values["debug-log-file"],
    args: {
      ...values,
      noSimulate: values["no-simulate"]
    }
  };
}

// src/cli/env.ts
import { existsSync, readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
function loadLocalEnv() {
  const envPath = resolve(dirname(fileURLToPath(import.meta.url)), "../../.env");
  if (!existsSync(envPath)) return;
  const content = readFileSync(envPath, "utf8");
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const normalized = line.startsWith("export ") ? line.slice("export ".length).trim() : line;
    const sep = normalized.indexOf("=");
    if (sep <= 0) continue;
    const key = normalized.slice(0, sep).trim();
    if (!key || process.env[key] !== void 0) continue;
    let value = normalized.slice(sep + 1).trim();
    if (value.startsWith('"') && value.endsWith('"') || value.startsWith("'") && value.endsWith("'")) {
      value = value.slice(1, -1);
    }
    process.env[key] = value;
  }
}

// src/cli/help.ts
function renderHelp(meta2) {
  return `${meta2.skillName} v${meta2.skillVersion}

Usage: dist/cli/cli.bundle.mjs <command> [options]

Commands:
  pair             Create pairing session (--chains eip155:56,eip155:1)
  status           Check session (--topic <topic> | --address <addr>)
  auth             Send consent sign (--topic <topic> | --address <addr>)
  sign             Sign message (--topic <topic> | --address <addr>) --message <msg>
  sign-typed-data  Sign EIP-712 typed data (--topic | --address) --data <json|@file> [--chain eip155:1]
  call             Raw contract call (--topic | --address) --to <contract> --data <calldata> [--value <wei|native-decimal>] [--gas <limit>] [--no-simulate]
  sessions         List all sessions (raw JSON)
  list-sessions    List sessions (human-readable)
  whoami           Show account info (--topic <topic> | --address <addr>)
  delete-session   Remove a saved session (--topic <topic> | --address <addr>)
  health           Ping session to check liveness (--topic | --address | --all) [--clean]
  version          Show version information

Options:
  --address <0x...>  Select session by wallet address (case-insensitive)
  --all              (health) Ping all sessions
  --clean            (health) Remove dead sessions from storage
  --open             (pair) Force open QR in system viewer (for agent environments)
  --no-simulate      (call) Skip transaction simulation (not recommended)
  --debug-log-file <path>  Append structured stdout/stderr logs to a file (jsonl)

Supported Chains:
  eip155:1      Ethereum Mainnet
  eip155:56     BSC (Lista Lending)`;
}

// src/cli/meta.ts
import { readFileSync as readFileSync2 } from "fs";
import { resolve as resolve2, dirname as dirname2 } from "path";
import { fileURLToPath as fileURLToPath2 } from "url";
function loadCliMeta() {
  const __dirname = dirname2(fileURLToPath2(import.meta.url));
  const pkgPath = resolve2(__dirname, "../../package.json");
  const pkg = JSON.parse(readFileSync2(pkgPath, "utf8"));
  return {
    skillVersion: pkg.version || "0.0.0",
    skillName: pkg.name || "@lista-dao/lista-wallet-connect-skill"
  };
}

// src/commands/pair.ts
import QRCode from "qrcode";
import { mkdirSync as mkdirSync3 } from "fs";
import { join as join3 } from "path";
import { execSync } from "child_process";
import { parseAccountId, parseChainId } from "@walletconnect/utils";

// src/client.ts
import { SignClient } from "@walletconnect/sign-client";
import { mkdirSync as mkdirSync2 } from "fs";
import { join as join2 } from "path";

// src/storage.ts
import { readFileSync as readFileSync3, writeFileSync, mkdirSync, existsSync as existsSync2 } from "fs";
import { join } from "path";
var SESSIONS_DIR = join(process.env.HOME || "/tmp", ".agent-wallet");
var SESSIONS_FILE = join(SESSIONS_DIR, "sessions.json");
function loadSessions() {
  if (!existsSync2(SESSIONS_FILE)) return {};
  try {
    return JSON.parse(readFileSync3(SESSIONS_FILE, "utf8"));
  } catch {
    return {};
  }
}
function saveSessions(sessions) {
  mkdirSync(SESSIONS_DIR, { recursive: true });
  writeFileSync(SESSIONS_FILE, JSON.stringify(sessions, null, 2));
}
function saveSession(topic, data) {
  const sessions = loadSessions();
  sessions[topic] = { ...data, updatedAt: (/* @__PURE__ */ new Date()).toISOString() };
  saveSessions(sessions);
}

// src/client.ts
var DEFAULT_WALLETCONNECT_PROJECT_ID = "c9e9af475f95d71b87da341e0b1e2237";
function getMetadata() {
  return {
    name: process.env.WC_METADATA_NAME || "Agent Wallet",
    description: process.env.WC_METADATA_DESCRIPTION || "AI Agent Wallet Connection",
    url: process.env.WC_METADATA_URL || "https://lista.org",
    icons: [process.env.WC_METADATA_ICON || "https://avatars.githubusercontent.com/u/258157775"]
  };
}
function findSessionByAddress(sessions, address) {
  const needle = address.toLowerCase();
  const matches = [];
  for (const [topic, session] of Object.entries(sessions)) {
    const hasMatch = (session.accounts || []).some((acct) => {
      const parts = acct.split(":");
      const addr = parts.slice(2).join(":");
      return addr.toLowerCase() === needle;
    });
    if (hasMatch) {
      matches.push({ topic, session });
    }
  }
  if (matches.length === 0) return null;
  matches.sort(
    (a, b) => (b.session.updatedAt || b.session.createdAt || "").localeCompare(
      a.session.updatedAt || a.session.createdAt || ""
    )
  );
  return matches[0];
}
async function getClient() {
  const projectId = process.env.WALLETCONNECT_PROJECT_ID || DEFAULT_WALLETCONNECT_PROJECT_ID;
  const dbPath = join2(SESSIONS_DIR, "wc-store");
  mkdirSync2(SESSIONS_DIR, { recursive: true });
  const debug = process.env.WC_DEBUG === "1";
  const t0 = Date.now();
  if (debug) console.error(`[WC] SignClient.init starting...`);
  const client = await SignClient.init({
    projectId,
    metadata: getMetadata(),
    storageOptions: {
      database: dbPath
    }
  });
  if (debug) console.error(`[WC] SignClient.init done in ${Date.now() - t0}ms`);
  return client;
}

// src/output.ts
function stringifyJson(payload) {
  return JSON.stringify(payload);
}
function printJson(payload) {
  console.log(stringifyJson(payload));
}
function printErrorJson(payload) {
  console.error(stringifyJson(payload));
}

// src/commands/pair.ts
function shouldAutoOpenQR(forceOpen) {
  if (forceOpen) return true;
  if (!process.stdout.isTTY) return false;
  if (process.env.CLAUDE_CODE || process.env.AGENT_MODE) return false;
  return true;
}
function openFile(filePath) {
  const platform = process.platform;
  try {
    if (platform === "darwin") {
      execSync(`open "${filePath}"`);
    } else if (platform === "win32") {
      execSync(`start "" "${filePath}"`);
    } else {
      execSync(`xdg-open "${filePath}"`);
    }
    return true;
  } catch {
    return false;
  }
}
function buildQrOpenCommands(qrPath) {
  return {
    macos: `open "${qrPath}"`,
    linux: `xdg-open "${qrPath}"`,
    windows: `start "" "${qrPath}"`
  };
}
var NAMESPACE_CONFIG = {
  eip155: {
    methods: ["personal_sign", "eth_sendTransaction", "eth_signTypedData_v4"],
    events: ["chainChanged", "accountsChanged"]
  }
};
function shortAddress(address) {
  if (!address || address.length < 10) return address;
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}
function buildPairSummary(accounts) {
  const parsed2 = accounts.map((account) => {
    try {
      const info = parseAccountId(account);
      return {
        chain: `${info.namespace}:${info.reference}`,
        address: info.address
      };
    } catch {
      return null;
    }
  }).filter((item) => item !== null);
  const chains = Array.from(new Set(parsed2.map((item) => item.chain)));
  const addresses = Array.from(new Set(parsed2.map((item) => item.address)));
  const primary = parsed2[0];
  return {
    chains,
    addresses,
    primaryAccount: primary ? {
      chain: primary.chain,
      address: primary.address,
      display: shortAddress(primary.address)
    } : void 0
  };
}
async function cmdPair(args) {
  const chains = args.chains ? args.chains.split(",") : ["eip155:56", "eip155:1"];
  const byNamespace = {};
  for (const chain of chains) {
    const { namespace } = parseChainId(chain);
    if (!NAMESPACE_CONFIG[namespace]) {
      printErrorJson({
        error: `Unsupported namespace: ${namespace}. Only EVM (eip155) is supported.`
      });
      process.exit(1);
    }
    if (!byNamespace[namespace]) byNamespace[namespace] = [];
    byNamespace[namespace].push(chain);
  }
  const requiredNamespaces = {};
  for (const [ns, nsChains] of Object.entries(byNamespace)) {
    requiredNamespaces[ns] = {
      chains: nsChains,
      ...NAMESPACE_CONFIG[ns]
    };
  }
  const debug = process.env.WC_DEBUG === "1";
  const t0 = Date.now();
  const client = await getClient();
  if (debug) console.error(`[WC] getClient() done in ${Date.now() - t0}ms`);
  const t1 = Date.now();
  const { uri, approval } = await client.connect({ requiredNamespaces });
  if (debug) console.error(`[WC] client.connect() done in ${Date.now() - t1}ms`);
  const qrPath = join3(SESSIONS_DIR, `qr-${Date.now()}.png`);
  mkdirSync3(SESSIONS_DIR, { recursive: true });
  await QRCode.toFile(qrPath, uri, { width: 400, margin: 2 });
  const qrMarkdown = `![WalletConnect QR](${qrPath})`;
  const qrOpenCommands = buildQrOpenCommands(qrPath);
  const openclawMediaDirective = `MEDIA:${qrPath}`;
  const autoOpen = shouldAutoOpenQR(args.open);
  let openedBySystem = false;
  if (autoOpen) {
    openedBySystem = openFile(qrPath);
  }
  const output = {
    status: "waiting_for_approval",
    interactionRequired: true,
    userReminder: "Wallet pairing is waiting for your confirmation. Please open your wallet app and approve or reject the request.",
    message: "Scan and approve this WalletConnect request in your wallet app.",
    qrPath,
    qrMarkdown,
    uri,
    deliveryPlan: {
      preferred: ["image_attachment", "markdown_image"],
      fallback: "wc_uri",
      fallbackWhen: [
        "image_not_supported",
        "image_render_failed",
        "image_delivery_failed"
      ],
      image: {
        qrPath,
        qrMarkdown,
        qrOpenCommands
      },
      wcUri: {
        uri
      }
    },
    deliveryHint: "Primary delivery is QR image (qrPath/qrMarkdown). Use wc URI only when image rendering or image delivery is not supported.",
    openclaw: {
      mediaDirective: openclawMediaDirective,
      fallbackUri: uri,
      rule: "For OpenClaw channel delivery, emit mediaDirective as a standalone line first. Only use fallbackUri when media delivery is unsupported or fails."
    }
  };
  if (!autoOpen || !openedBySystem) {
    output.note = "If QR image preview is unavailable, try opening qrPath with a system image viewer first. Use the wc URI only if image rendering/delivery is not supported.";
    output.qrOpenCommands = qrOpenCommands;
  }
  if (autoOpen && !openedBySystem) {
    output.openFailed = true;
  }
  printJson(output);
  try {
    const session = await approval();
    const accounts = Object.values(session.namespaces).flatMap((ns) => ns.accounts || []);
    const walletName = session.peer?.metadata?.name || "Unknown Wallet";
    const pairedAt = (/* @__PURE__ */ new Date()).toISOString();
    const summary = buildPairSummary(accounts);
    saveSession(session.topic, {
      accounts,
      chains,
      peerName: walletName,
      createdAt: pairedAt
    });
    printJson({
      status: "paired",
      message: `Wallet connected successfully (${walletName}).`,
      topic: session.topic,
      accounts,
      peerName: walletName,
      pairedAt,
      summary: {
        chainCount: summary.chains.length,
        accountCount: accounts.length,
        chains: summary.chains,
        primaryAccount: summary.primaryAccount
      },
      nextActions: [
        "Use whoami/status to verify the active session.",
        "Use auth if a consent signature is required before operations."
      ]
    });
  } catch (err) {
    printJson({ status: "rejected", error: err.message });
  }
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/commands/auth.ts
import { randomBytes } from "crypto";

// src/helpers.ts
import { parseAccountId as parseAccountId2 } from "@walletconnect/utils";
import { normalize } from "viem/ens";
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";
function findAccount(accounts, chainHint) {
  if (!chainHint) return accounts[0] || null;
  const exact = accounts.find((a) => a.startsWith(chainHint + ":") || a.startsWith(chainHint));
  if (exact) return exact;
  const ns = chainHint.split(":")[0];
  return accounts.find((a) => a.startsWith(ns + ":")) || null;
}
function parseAccount(accountStr) {
  const parsed2 = parseAccountId2(accountStr);
  return {
    ...parsed2,
    chainId: `${parsed2.namespace}:${parsed2.reference}`,
    address: parsed2.address
  };
}
function redactAddress(address, keep = 7) {
  if (!address) return address;
  if (address.startsWith("0x")) {
    const hex = address.slice(2);
    if (hex.length <= keep * 2) return address;
    return `0x${hex.slice(0, keep)}...${hex.slice(-keep)}`;
  }
  if (address.length <= keep * 2) return address;
  return `${address.slice(0, keep)}...${address.slice(-keep)}`;
}
function encodeEvmMessage(message) {
  return "0x" + Buffer.from(message, "utf8").toString("hex");
}
function requireSession(sessions, topic) {
  const data = sessions[topic];
  if (!data) {
    printErrorJson({ error: "Session not found", topic });
    process.exit(1);
  }
  return data;
}
function requireAccount(sessionData, chainHint, label = "matching") {
  const account = findAccount(sessionData.accounts, chainHint);
  if (!account) {
    printErrorJson({ error: `No ${label} account found`, chainHint });
    process.exit(1);
  }
  return account;
}
async function resolveAddress(addressOrEns) {
  if (!addressOrEns.endsWith(".eth")) return addressOrEns;
  const client = createPublicClient({ chain: mainnet, transport: http() });
  const resolved = await client.getEnsAddress({ name: normalize(addressOrEns) });
  if (!resolved) throw new Error(`Could not resolve ENS name: ${addressOrEns}`);
  return resolved;
}
async function requestWithTimeout(client, requestParams, {
  timeoutMs = 3e5,
  phase = "wallet_request",
  context,
  emitStdoutHeartbeat
} = {}) {
  const start = Date.now();
  const shouldEmitStdout = emitStdoutHeartbeat ?? (!process.stdout.isTTY || process.env.WC_STDOUT_HEARTBEAT === "1");
  const userReminder = "Wallet confirmation is pending. Please open your wallet app and approve or reject the request to continue.";
  const emitHeartbeat = () => {
    const elapsed = Date.now() - start;
    const heartbeat = {
      status: "waiting_for_approval",
      phase,
      elapsedMs: elapsed,
      timeoutMs,
      interactionRequired: true,
      userReminder,
      ...context || {}
    };
    process.stderr.write(`${stringifyJson(heartbeat)}
`);
    if (shouldEmitStdout) {
      printJson(heartbeat);
    }
  };
  emitHeartbeat();
  return Promise.race([
    client.request(requestParams),
    new Promise((_, reject) => {
      setTimeout(
        () => reject(new Error("Request timed out after 5 minutes -- user did not respond")),
        timeoutMs
      );
    })
  ]);
}

// src/commands/auth.ts
async function cmdAuth(args) {
  if (!args.topic) {
    printErrorJson({ error: "--topic required" });
    process.exit(1);
  }
  const client = await getClient();
  const sessionData = requireSession(loadSessions(), args.topic);
  const evmAccountStr = requireAccount(sessionData, "eip155", "EVM");
  const { chainId, address } = parseAccount(evmAccountStr);
  const nonce = randomBytes(16).toString("hex");
  const timestamp = (/* @__PURE__ */ new Date()).toISOString();
  const display = redactAddress(address);
  const message = [
    "AgentWallet Authentication",
    "",
    `I authorize this AI agent to request transactions on my behalf.`,
    "",
    `Address: ${display}`,
    `Nonce: ${nonce}`,
    `Timestamp: ${timestamp}`
  ].join("\n");
  try {
    const signature = await requestWithTimeout(client, {
      topic: args.topic,
      chainId,
      request: {
        method: "personal_sign",
        params: [encodeEvmMessage(message), address]
      }
    }, {
      phase: "auth",
      context: {
        command: "auth",
        topic: args.topic,
        chainId,
        address: display
      }
    });
    saveSession(args.topic, {
      ...sessionData,
      authenticated: true,
      authAddress: address,
      authNonce: nonce,
      authSignature: signature,
      authTimestamp: timestamp
    });
    printJson({
      status: "authenticated",
      address: display,
      signature,
      nonce,
      message
    });
  } catch (err) {
    printJson({ status: "rejected", error: err.message });
  }
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/commands/sign.ts
async function cmdSign(args) {
  if (!args.topic || !args.message) {
    printErrorJson({ error: "--topic and --message required" });
    process.exit(1);
  }
  const client = await getClient();
  const sessionData = requireSession(loadSessions(), args.topic);
  const chainHint = args.chain;
  const account = findAccount(
    sessionData.accounts,
    chainHint?.startsWith("eip155") ? chainHint : "eip155"
  );
  if (!account) {
    printErrorJson({ error: "No EVM account found", chainHint });
    process.exit(1);
  }
  const { chainId, address } = parseAccount(account);
  const signature = await requestWithTimeout(client, {
    topic: args.topic,
    chainId,
    request: {
      method: "personal_sign",
      params: [encodeEvmMessage(args.message), address]
    }
  }, {
    phase: "sign",
    context: {
      command: "sign",
      topic: args.topic,
      chainId,
      address
    }
  });
  const result = { status: "signed", address, signature, chain: chainId };
  printJson(result);
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/commands/sign-typed-data.ts
import { readFileSync as readFileSync4 } from "fs";
function parseTypedData(raw) {
  let json;
  if (raw.startsWith("@")) {
    const filePath = raw.slice(1);
    try {
      json = JSON.parse(readFileSync4(filePath, "utf8"));
    } catch (err) {
      throw new Error(
        `Failed to read typed data from file "${filePath}": ${err.message}`
      );
    }
  } else {
    try {
      json = JSON.parse(raw);
    } catch {
      throw new Error("--data must be valid JSON or a @file path");
    }
  }
  if (!json || typeof json !== "object" || Array.isArray(json)) {
    throw new Error("Typed data must be a JSON object");
  }
  const obj = json;
  const missing = ["domain", "types", "message"].filter((k) => !(k in obj));
  if (missing.length > 0) {
    throw new Error(`Typed data missing required field(s): ${missing.join(", ")}`);
  }
  if (typeof obj.types !== "object" || Array.isArray(obj.types)) {
    throw new Error("Typed data 'types' must be an object");
  }
  return obj;
}
function inferPrimaryType(types) {
  const candidates = Object.keys(types).filter((k) => k !== "EIP712Domain");
  if (candidates.length === 0) {
    throw new Error(
      "Cannot infer primaryType: no types defined besides EIP712Domain \u2014 provide it explicitly"
    );
  }
  return candidates[0];
}
async function cmdSignTypedData(args) {
  if (!args.topic || !args.data) {
    printErrorJson({ error: "--topic (or --address) and --data required" });
    process.exit(1);
  }
  let typedData;
  try {
    typedData = parseTypedData(args.data);
  } catch (err) {
    printErrorJson({ error: err.message });
    process.exit(1);
  }
  const primaryType = typedData.primaryType ?? (() => {
    try {
      return inferPrimaryType(typedData.types);
    } catch (err) {
      printErrorJson({ error: err.message });
      process.exit(1);
    }
  })();
  const client = await getClient();
  const sessionData = requireSession(loadSessions(), args.topic);
  const account = findAccount(
    sessionData.accounts,
    args.chain?.startsWith("eip155") ? args.chain : "eip155"
  );
  if (!account) {
    printErrorJson({
      error: "No EVM (eip155) account found in session \u2014 EIP-712 is EVM-only"
    });
    process.exit(1);
  }
  const { chainId, address } = parseAccount(account);
  const payload = { ...typedData, primaryType };
  const signature = await requestWithTimeout(client, {
    topic: args.topic,
    chainId,
    request: {
      method: "eth_signTypedData_v4",
      params: [address, JSON.stringify(payload)]
    }
  }, {
    phase: "sign_typed_data",
    context: {
      command: "sign-typed-data",
      topic: args.topic,
      chainId,
      address,
      primaryType
    }
  });
  printJson({ status: "signed", address, signature, chain: chainId, primaryType });
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/rpc.ts
import { existsSync as existsSync3, readFileSync as readFileSync5 } from "fs";
import { homedir } from "os";
import { join as join4 } from "path";
var LENDING_CONFIG_FILE = join4(homedir(), ".agent-wallet", "lending-config.json");
var DEFAULT_EVM_RPCS = {
  "eip155:1": [
    "https://eth.llamarpc.com",
    "https://cloudflare-eth.com",
    "https://rpc.ankr.com/eth"
  ],
  "eip155:56": [
    "https://bsc-dataseed.binance.org",
    "https://bsc-dataseed1.binance.org",
    "https://bsc-dataseed2.binance.org"
  ]
};
function loadSharedRpcOverrides() {
  try {
    if (!existsSync3(LENDING_CONFIG_FILE)) return {};
    const raw = readFileSync5(LENDING_CONFIG_FILE, "utf8");
    const parsed2 = JSON.parse(raw);
    if (!parsed2 || typeof parsed2 !== "object" || !parsed2.rpcUrls) {
      return {};
    }
    return parsed2.rpcUrls;
  } catch {
    return {};
  }
}
function getRpcCandidatesForChain(chainId) {
  const overrides = loadSharedRpcOverrides();
  const override = overrides[chainId];
  const candidates = [];
  const seen = /* @__PURE__ */ new Set();
  if (typeof override === "string" && override.trim().length > 0) {
    const normalized = override.trim();
    if (!seen.has(normalized)) {
      seen.add(normalized);
      candidates.push({ rpcUrl: normalized, source: "shared_config" });
    }
  }
  for (const rpcUrl of DEFAULT_EVM_RPCS[chainId]) {
    const normalized = rpcUrl.trim();
    if (!normalized || seen.has(normalized)) continue;
    seen.add(normalized);
    candidates.push({ rpcUrl: normalized, source: "default" });
  }
  return candidates;
}

// src/commands/call/constants.ts
import { mainnet as mainnet2, bsc } from "viem/chains";
var EXPLORER_URLS = {
  "eip155:1": "https://etherscan.io/tx/",
  "eip155:56": "https://bscscan.com/tx/"
};
var CHAIN_CONFIG = {
  "eip155:1": { chain: mainnet2 },
  "eip155:56": { chain: bsc }
};

// src/commands/call/parse.ts
import { parseUnits } from "viem";
function parseValue(value) {
  if (!value || value === "0") return void 0;
  if (value.startsWith("0x")) return value;
  if (value.includes(".")) {
    const wei = parseUnits(value, 18);
    return "0x" + wei.toString(16);
  }
  return "0x" + BigInt(value).toString(16);
}
function parseGas(value) {
  if (!value) return void 0;
  if (value.startsWith("0x")) return value;
  return "0x" + BigInt(value).toString(16);
}
function buildCallTransaction(from, to, args) {
  const tx = {
    from,
    to
  };
  if (args.data) {
    tx.data = args.data.startsWith("0x") ? args.data : "0x" + args.data;
  }
  const value = parseValue(args.value);
  if (value) tx.value = value;
  const gas = parseGas(args.gas);
  if (gas) tx.gas = gas;
  const gasPrice = parseGas(args.gasPrice);
  if (gasPrice) tx.gasPrice = gasPrice;
  return tx;
}

// src/commands/call/simulate.ts
import { createPublicClient as createPublicClient2, http as http2 } from "viem";
var FOURBYTE_API = "https://www.4byte.directory/api/v1/signatures/";
var selectorSignatureCache = /* @__PURE__ */ new Map();
function toMessage(value) {
  if (value instanceof Error) {
    const errLike = value;
    return errLike.message || errLike.shortMessage || errLike.details || String(value);
  }
  if (typeof value === "string") return value;
  return String(value);
}
function extractRevertData(message) {
  const patterns = [
    /Execution reverted with reason:\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i,
    /execution reverted:?\s*[^\n]*?(0x[0-9a-fA-F]{8,})/i
  ];
  for (const pattern of patterns) {
    const match = message.match(pattern);
    const candidate = match?.[1];
    if (!candidate) continue;
    if (candidate.length < 10) continue;
    if (candidate.length % 2 !== 0) continue;
    return candidate.toLowerCase();
  }
  return void 0;
}
function extractTextReason(message) {
  const normalize2 = (value) => {
    const cleaned = value.trim().replace(/\.+$/, "");
    if (/^0x$/i.test(cleaned)) return void 0;
    return cleaned || void 0;
  };
  const withReasonMatch = message.match(/Execution reverted with reason:\s*([^\n]+)/i);
  if (withReasonMatch?.[1]) {
    const reason = withReasonMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
    return normalize2(reason);
  }
  const revertedMatch = message.match(/execution reverted:?\s*([^\n]+)/i);
  if (revertedMatch?.[1]) {
    const reason = revertedMatch[1].replace(/:\s*0x[0-9a-fA-F]{8,}\.?$/i, "");
    return normalize2(reason);
  }
  return void 0;
}
function extractSelectorFromReason(reason) {
  if (!reason) return void 0;
  const cleaned = reason.trim().replace(/\.+$/, "");
  if (!/^0x[0-9a-fA-F]{8}$/.test(cleaned)) return void 0;
  return cleaned.toLowerCase();
}
async function lookupSelectorSignature(selector) {
  const normalized = selector.toLowerCase();
  if (selectorSignatureCache.has(normalized)) {
    return selectorSignatureCache.get(normalized);
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 2500);
  try {
    const url = `${FOURBYTE_API}?hex_signature=${encodeURIComponent(normalized)}`;
    const response = await fetch(url, {
      method: "GET",
      signal: controller.signal,
      headers: { accept: "application/json" }
    });
    if (!response.ok) {
      selectorSignatureCache.set(normalized, void 0);
      return void 0;
    }
    const payload = await response.json();
    const signature = payload.results?.[0]?.text_signature;
    if (typeof signature === "string" && signature.length > 0) {
      selectorSignatureCache.set(normalized, signature);
      return signature;
    }
    selectorSignatureCache.set(normalized, void 0);
    return void 0;
  } catch {
    return void 0;
  } finally {
    clearTimeout(timeout);
  }
}
async function simulateTransaction(chainId, tx, rpcCandidates) {
  const config = CHAIN_CONFIG[chainId];
  const attempts = [];
  for (const candidate of rpcCandidates) {
    const client = createPublicClient2({
      chain: config.chain,
      transport: http2(candidate.rpcUrl)
    });
    try {
      await client.call({
        account: tx.from,
        to: tx.to,
        data: tx.data,
        value: tx.value ? BigInt(tx.value) : void 0
      });
      return {
        success: true,
        rpcUrl: candidate.rpcUrl,
        rpcSource: candidate.source
      };
    } catch (err) {
      const message = toMessage(err);
      const isRevert = /revert/i.test(message);
      const revertData = extractRevertData(message);
      const textReason = extractTextReason(message);
      const selectorFromReason = extractSelectorFromReason(textReason);
      const revertSelector = revertData ? revertData.slice(0, 10) : selectorFromReason;
      const signature = revertSelector ? await lookupSelectorSignature(revertSelector) : void 0;
      attempts.push({
        rpcUrl: candidate.rpcUrl,
        source: candidate.source,
        error: message
      });
      if (isRevert || revertData) {
        return {
          success: false,
          error: message,
          revertReason: signature || textReason || "Contract execution reverted",
          revertData,
          revertSelector,
          attempts
        };
      }
    }
  }
  return {
    success: false,
    error: attempts.length > 0 ? attempts.map((a) => `[${a.source}] ${a.rpcUrl}: ${a.error}`).join(" | ") : "Simulation failed with no RPC candidates",
    attempts
  };
}

// src/commands/call.ts
function resolveSupportedChain(chain) {
  if (chain === "eip155:1" || chain === "eip155:56") {
    return chain;
  }
  return null;
}
async function cmdCall(args) {
  if (!args.topic) {
    printErrorJson({ error: "--topic required" });
    process.exit(1);
  }
  if (!args.to) {
    printErrorJson({ error: "--to (contract address) required" });
    process.exit(1);
  }
  const evmChain = resolveSupportedChain(args.chain || "eip155:56");
  if (!evmChain) {
    printErrorJson({
      error: `Unsupported chain: ${args.chain}. Only eip155:1 (ETH) and eip155:56 (BSC) are supported.`
    });
    process.exit(1);
  }
  const client = await getClient();
  const sessionData = requireSession(loadSessions(), args.topic);
  const accountStr = requireAccount(sessionData, evmChain, "EVM");
  const { address: from } = parseAccount(accountStr);
  const resolvedTo = await resolveAddress(args.to);
  if (resolvedTo !== args.to) {
    printErrorJson({ ens: args.to, resolved: resolvedTo });
  }
  const tx = buildCallTransaction(from, resolvedTo, args);
  process.stderr.write(
    `${stringifyJson({
      action: "sending_raw_tx",
      chain: evmChain,
      from,
      to: resolvedTo,
      data: tx.data ? `${tx.data.slice(0, 10)}...` : void 0,
      value: tx.value,
      gas: tx.gas
    })}
`
  );
  if (!args.noSimulate) {
    const rpcCandidates = getRpcCandidatesForChain(evmChain);
    process.stderr.write(
      `${stringifyJson({
        action: "simulating_tx",
        rpcCandidates: rpcCandidates.map((candidate) => ({
          rpcUrl: candidate.rpcUrl,
          rpcSource: candidate.source
        }))
      })}
`
    );
    const simResult = await simulateTransaction(
      evmChain,
      { from, to: resolvedTo, data: tx.data, value: tx.value },
      rpcCandidates
    );
    if (!simResult.success) {
      printJson({
        status: "simulation_failed",
        error: simResult.error,
        revertReason: simResult.revertReason,
        revertData: simResult.revertData,
        revertSelector: simResult.revertSelector,
        attempts: simResult.attempts,
        hint: "Transaction would revert on-chain. Use --no-simulate to force send (not recommended)."
      });
      await client.core.relayer.transportClose().catch(() => {
      });
      process.exit(1);
    }
    process.stderr.write(
      `${stringifyJson({
        action: "simulation_passed",
        rpcUrl: simResult.rpcUrl,
        rpcSource: simResult.rpcSource
      })}
`
    );
  }
  try {
    const txHash = await requestWithTimeout(client, {
      topic: args.topic,
      chainId: evmChain,
      request: {
        method: "eth_sendTransaction",
        params: [tx]
      }
    }, {
      phase: "call",
      context: {
        command: "call",
        topic: args.topic,
        chain: evmChain,
        from,
        to: resolvedTo
      }
    });
    const explorerUrl = EXPLORER_URLS[evmChain] || "";
    printJson({
      status: "sent",
      txHash,
      chain: evmChain,
      from,
      to: resolvedTo,
      ...resolvedTo !== args.to ? { ens: args.to } : {},
      data: tx.data,
      value: tx.value,
      explorer: explorerUrl ? `${explorerUrl}${txHash}` : void 0
    });
  } catch (err) {
    printJson({ status: "rejected", error: err.message });
  }
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/commands/health.ts
var PING_TIMEOUT_MS = 15e3;
async function pingSession(client, topic) {
  try {
    await Promise.race([
      client.ping({ topic }),
      new Promise(
        (_, reject) => setTimeout(() => reject(new Error("ping timeout")), PING_TIMEOUT_MS)
      )
    ]);
    return { alive: true };
  } catch (err) {
    return { alive: false, error: err.message };
  }
}
async function cmdHealth(args) {
  const sessions = loadSessions();
  let topics = [];
  if (args.all) {
    topics = Object.keys(sessions);
    if (topics.length === 0) {
      printJson({ status: "no_sessions", message: "No sessions found" });
      process.exit(0);
    }
  } else if (args.topic) {
    if (!sessions[args.topic]) {
      printErrorJson({ error: "Session not found", topic: args.topic });
      process.exit(1);
    }
    topics = [args.topic];
  } else if (args.address) {
    const match = findSessionByAddress(sessions, args.address);
    if (!match) {
      printErrorJson({ error: "No session found for address", address: args.address });
      process.exit(1);
    }
    topics = [match.topic];
  } else {
    printErrorJson({ error: "--topic, --address, or --all required for health command" });
    process.exit(1);
  }
  const client = await getClient();
  const results = [];
  const deadTopics = [];
  for (const topic of topics) {
    const session = sessions[topic];
    const accounts = session.accounts || [];
    const peerName = session.peerName || "unknown";
    process.stderr.write(`${stringifyJson({ pinging: topic, peer: peerName })}
`);
    const { alive, error } = await pingSession(client, topic);
    const shortAddresses = accounts.map((a) => {
      const parts = a.split(":");
      return redactAddress(parts.slice(2).join(":"));
    });
    const entry = {
      topic: topic.slice(0, 16) + "...",
      fullTopic: topic,
      peerName,
      accounts: shortAddresses,
      alive,
      ...error && { error }
    };
    results.push(entry);
    if (!alive) {
      deadTopics.push(topic);
    }
  }
  let cleaned = 0;
  if (args.clean && deadTopics.length > 0) {
    const updated = { ...sessions };
    for (const t of deadTopics) {
      delete updated[t];
    }
    saveSessions(updated);
    cleaned = deadTopics.length;
  }
  const output = {
    checked: results.length,
    alive: results.filter((r) => r.alive).length,
    dead: results.filter((r) => !r.alive).length,
    ...args.clean && { cleaned },
    sessions: results
  };
  printJson(output);
  await client.core.relayer.transportClose().catch(() => {
  });
  process.exit(0);
}

// src/chains.ts
var CHAIN_LABELS = {
  "eip155:1": "Ethereum",
  "eip155:56": "BSC"
};
function getChainLabel(chainId) {
  return CHAIN_LABELS[chainId] || chainId;
}
function formatChainDisplay(chainId) {
  return getChainLabel(chainId);
}

// src/commands/sessions.ts
function resolveAddress2(args) {
  if (args.address && !args.topic) {
    const sessions = loadSessions();
    const match = findSessionByAddress(sessions, args.address);
    if (!match) {
      printErrorJson({ error: "No session found for address", address: args.address });
      process.exit(1);
    }
    args.topic = match.topic;
  }
  return args;
}
async function cmdStatus(args) {
  args = resolveAddress2(args);
  if (!args.topic) {
    printErrorJson({ error: "--topic or --address required" });
    process.exit(1);
  }
  const sessions = loadSessions();
  const session = sessions[args.topic];
  if (!session) {
    printJson({ status: "not_found", topic: args.topic });
    return;
  }
  printJson({ status: "active", ...session });
}
async function cmdSessions() {
  const sessions = loadSessions();
  printJson(sessions);
}
async function cmdListSessions() {
  const sessions = loadSessions();
  const entries = Object.entries(sessions);
  if (entries.length === 0) {
    console.log("No saved sessions.");
    return;
  }
  for (const [topic, s] of entries) {
    const accounts = (s.accounts || []).map((a) => {
      const parts = a.split(":");
      const chain = parts.slice(0, 2).join(":");
      const addr = parts.slice(2).join(":");
      return `  ${formatChainDisplay(chain)}: ${addr}`;
    });
    const auth = s.authenticated ? " authenticated" : "";
    const date = s.createdAt ? new Date(s.createdAt).toISOString().slice(0, 16) : "unknown";
    console.log(`Topic: ${topic.slice(0, 12)}...`);
    console.log(`  Peer: ${s.peerName || "unknown"}${auth}`);
    console.log(`  Created: ${date}`);
    console.log(`  Accounts:`);
    accounts.forEach((a) => console.log(`  ${a}`));
    console.log();
  }
}
async function cmdWhoami(args) {
  args = resolveAddress2(args);
  const sessions = loadSessions();
  if (args.topic) {
    const session2 = sessions[args.topic];
    if (!session2) {
      printErrorJson({ error: "Session not found", topic: args.topic });
      process.exit(1);
    }
    printJson({
      topic: args.topic,
      peerName: session2.peerName,
      accounts: session2.accounts,
      authenticated: session2.authenticated || false,
      createdAt: session2.createdAt
    });
    return;
  }
  const entries = Object.entries(sessions);
  if (entries.length === 0) {
    printJson({ error: "No sessions found" });
    return;
  }
  entries.sort(
    (a, b) => (b[1].updatedAt || b[1].createdAt || "").localeCompare(
      a[1].updatedAt || a[1].createdAt || ""
    )
  );
  const [topic, session] = entries[0];
  printJson({
    topic,
    peerName: session.peerName,
    accounts: session.accounts,
    authenticated: session.authenticated || false,
    createdAt: session.createdAt
  });
}
async function cmdDeleteSession(args) {
  args = resolveAddress2(args);
  if (!args.topic) {
    printErrorJson({ error: "--topic or --address required" });
    process.exit(1);
  }
  const sessions = loadSessions();
  if (!sessions[args.topic]) {
    printJson({ status: "not_found", topic: args.topic });
    return;
  }
  const { peerName, accounts } = sessions[args.topic];
  delete sessions[args.topic];
  saveSessions(sessions);
  printJson({ status: "deleted", topic: args.topic, peerName, accounts });
}

// src/cli/router.ts
function resolveAddress3(args) {
  if (args.address && !args.topic) {
    const sessions = loadSessions();
    const match = findSessionByAddress(sessions, args.address);
    if (!match) {
      printErrorJson({ error: "No session found for address", address: args.address });
      process.exit(1);
    }
    args.topic = match.topic;
  }
  return args;
}
async function runCommand(command, args, meta2) {
  const commands = {
    pair: cmdPair,
    status: cmdStatus,
    auth: (a) => cmdAuth(resolveAddress3(a)),
    sign: (a) => cmdSign(resolveAddress3(a)),
    "sign-typed-data": (a) => cmdSignTypedData(resolveAddress3(a)),
    call: (a) => cmdCall(resolveAddress3(a)),
    sessions: cmdSessions,
    "list-sessions": cmdListSessions,
    whoami: cmdWhoami,
    "delete-session": cmdDeleteSession,
    health: cmdHealth,
    version: async () => {
      printJson({
        skill: meta2.skillName,
        version: meta2.skillVersion,
        hint: "If version mismatch, run: npm install && npm run build"
      });
    }
  };
  if (!commands[command]) {
    console.error(`Unknown command: ${command}`);
    process.exit(1);
  }
  await commands[command](args);
}

// src/cli/debug-log.ts
import { appendFileSync, mkdirSync as mkdirSync4 } from "fs";
import { dirname as dirname3, resolve as resolve3 } from "path";
function writeRecord(filePath, record) {
  try {
    appendFileSync(filePath, `${JSON.stringify(record)}
`, "utf8");
  } catch {
  }
}
function toText(chunk, encoding) {
  if (typeof chunk === "string") return chunk;
  if (chunk instanceof Uint8Array) {
    return Buffer.from(chunk).toString(encoding || "utf8");
  }
  return String(chunk);
}
function normalizeWriteArgs(encodingOrCb, cb) {
  if (typeof encodingOrCb === "function") {
    return { encoding: void 0, callback: encodingOrCb };
  }
  return { encoding: encodingOrCb, callback: cb };
}
function parseJsonIfPossible(line) {
  try {
    return JSON.parse(line);
  } catch {
    return void 0;
  }
}
function isStructuredJson(value) {
  return Array.isArray(value) || typeof value === "object" && value !== null;
}
function patchWriteStream(streamName, stream, filePath, skill) {
  const originalWrite = stream.write.bind(stream);
  let buffer = "";
  const emitLine = (line) => {
    if (!line) return;
    const parsed2 = parseJsonIfPossible(line);
    const record = {
      ts: (/* @__PURE__ */ new Date()).toISOString(),
      pid: process.pid,
      skill,
      stream: streamName,
      line
    };
    if (isStructuredJson(parsed2)) {
      record.json = parsed2;
    }
    writeRecord(filePath, record);
  };
  const flushBuffer = () => {
    if (!buffer) return;
    emitLine(buffer.replace(/\r$/, ""));
    buffer = "";
  };
  stream.write = ((chunk, encodingOrCb, cb) => {
    const { encoding, callback } = normalizeWriteArgs(encodingOrCb, cb);
    const text = toText(chunk, encoding);
    buffer += text;
    let index = buffer.indexOf("\n");
    while (index >= 0) {
      const line = buffer.slice(0, index).replace(/\r$/, "");
      emitLine(line);
      buffer = buffer.slice(index + 1);
      index = buffer.indexOf("\n");
    }
    if (encoding !== void 0 && callback) {
      return originalWrite(chunk, encoding, callback);
    }
    if (encoding !== void 0) {
      return originalWrite(chunk, encoding);
    }
    if (callback) {
      return originalWrite(chunk, callback);
    }
    return originalWrite(chunk);
  });
  return flushBuffer;
}
function setupDebugLogFile(skill, cliLogFile) {
  const requested = cliLogFile || process.env.SKILL_DEBUG_LOG_FILE || process.env.DEBUG_LOG_FILE;
  if (!requested) return null;
  const filePath = resolve3(requested);
  try {
    mkdirSync4(dirname3(filePath), { recursive: true });
  } catch {
  }
  process.env.SKILL_DEBUG_LOG_FILE = filePath;
  const flushStdout = patchWriteStream("stdout", process.stdout, filePath, skill);
  const flushStderr = patchWriteStream("stderr", process.stderr, filePath, skill);
  const flushAll = () => {
    flushStdout();
    flushStderr();
  };
  process.on("beforeExit", flushAll);
  process.on("exit", flushAll);
  writeRecord(filePath, {
    ts: (/* @__PURE__ */ new Date()).toISOString(),
    pid: process.pid,
    skill,
    stream: "stderr",
    line: "debug_log_enabled",
    config: {
      filePath,
      argv: process.argv.slice(2)
    }
  });
  return filePath;
}

// src/cli.ts
var parsed = parseCliInput();
setupDebugLogFile("@lista-dao/lista-wallet-connect-skill", parsed.debugLogFile);
loadLocalEnv();
var meta = loadCliMeta();
var SKILL_VERSION = meta.skillVersion;
var SKILL_NAME = meta.skillName;
if (!parsed.command || parsed.help) {
  console.log(renderHelp(meta));
  process.exit(0);
}
runCommand(parsed.command, parsed.args, meta).catch((err) => {
  printErrorJson({ error: err.message });
  process.exit(1);
});
export {
  SKILL_NAME,
  SKILL_VERSION
};
