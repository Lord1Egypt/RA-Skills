#!/usr/bin/env node
import { randomBytes } from "node:crypto";
import { spawn, spawnSync } from "node:child_process";
import {
  chmodSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmSync,
  writeFileSync
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";

// KokoChat product features only need read sessions/history and send messages.
// IMPORTANT: the current pairing flow uses OpenClaw's official `openclaw qr`
// device-pair flow, and that flow's actual device scopes are signed by the
// Gateway / OpenClaw version. The constants below are only for validating legacy
// KOKOCHAT_PAIRING_REQUEST payloads from old app builds; they are NOT passed to
// `openclaw qr` and do NOT constrain the final device token. Always inspect
// `openclaw devices list` after pairing.
const REQUIRED_SCOPES = [
  "operator.read",
  "operator.write"
];
const OPTIONAL_SCOPES = [];
const DEFAULT_SCOPES = [
  ...OPTIONAL_SCOPES,
  ...REQUIRED_SCOPES
];
const RELAY_STATE_FILE = "relay.json";
// Hosted relay behind deeply.plus Caddy (TLS-terminated, reverse-proxied to the
// loopback koko-relay on the same box). `wss://` = encrypted; the `/relay`
// prefix is stripped by Caddy so the relay sees /v1/gateway/* + /v1/connector/*.
// Override with KOKOCHAT_RELAY_URL for self-hosting.
const DEFAULT_RELAY_URL = "wss://deeply.plus/relay";
const RELAY_DAEMON_SERVICE = "kokochat-relay-connector.service";

const argInput = process.argv.slice(2).join(" ");
// Pairing now uses OpenClaw's official `openclaw qr` device-pair flow, which
// does NOT need a per-device pairing request. Older app builds may still pass
// KOKOCHAT_PAIRING_REQUEST (env or arg) — honor it for back-compat — but never
// block on stdin when there's nothing to read (that just hangs non-interactive
// shells, which is exactly what happened here).
const input = process.env.KOKOCHAT_PAIRING_REQUEST || argInput || "";

// The pairing request is still parsed (backward-compat with older app builds
// that send one), but pairing now goes through OpenClaw's OFFICIAL
// `openclaw qr` device-pair flow instead of self-signing a token:
//   - prepareRelayConnector still brings up the relay tunnel (NAT traversal).
//   - `openclaw qr --public-url <relay-tunnel-url>` asks the gateway to mint a
//     short-lived bootstrapToken setup code. The app completes the device-pair
//     handshake and the GATEWAY issues the real device token (read+write).
// We no longer call approveDevice()/write paired.json — that self-signing is
// exactly what a careful OpenClaw flags as a backdoor.
const request = input.trim().length > 0 ? parsePairingRequest(input) : null;
const stateDir = resolveStateDir();
const openclawEnv = readEnvFile(join(stateDir, "openclaw.env"));
const relay = prepareRelayConnector(stateDir, request);
const setupCode = generateOfficialSetupCode(relay.gatewayUrl);

process.stdout.write(`${setupCode}\n`);

function generateOfficialSetupCode(relayTunnelUrl) {
  const bin = process.env.OPENCLAW_BIN ?? "openclaw";
  const res = spawnSync(
    bin,
    ["qr", "--public-url", relayTunnelUrl, "--setup-code-only", "--no-ascii"],
    {
      encoding: "utf8",
      env: openclawCommandEnv()
    }
  );
  if (res.error) {
    throw new Error(`failed to run \`${bin} qr\`: ${res.error.message}`);
  }
  if (res.status !== 0) {
    throw new Error(`\`openclaw qr\` failed (exit ${res.status}): ${(res.stderr || res.stdout || "").trim()}`);
  }
  // `--setup-code-only` is supposed to print just the code, but OpenClaw still
  // writes a "Config warnings" banner to stdout (e.g. when a plugin is
  // misconfigured), and `--log-level silent` does NOT suppress it. The real
  // setup code is the only pure base64url line, so isolate the last such line
  // instead of concatenating all stdout (which corrupts the base64 / JSON).
  const qrCode =
    String(res.stdout ?? "")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => /^[A-Za-z0-9_-]{32,}$/.test(line))
      .pop() ?? "";
  if (qrCode.length === 0) {
    throw new Error("`openclaw qr` produced no setup code");
  }
  // `openclaw qr` keeps only the ORIGIN of --public-url and drops the path/query,
  // so its setup-code url loses the relay tunnel's /v1/gateway/<id>?secret=...
  // We keep the gateway-signed bootstrapToken but re-assemble the setup code with
  // the FULL relay tunnel url the app must dial to reach this gateway via relay.
  let bootstrapToken;
  try {
    const decoded = JSON.parse(
      Buffer.from(qrCode.replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8")
    );
    bootstrapToken = decoded?.bootstrapToken;
  } catch (err) {
    throw new Error(`could not decode \`openclaw qr\` setup code: ${err.message}`);
  }
  if (typeof bootstrapToken !== "string" || bootstrapToken.length === 0) {
    throw new Error("`openclaw qr` setup code had no bootstrapToken");
  }
  return encodeJson({
    url: relayTunnelUrl,
    bootstrapToken,
    relay: { mode: "gateway-tunnel" }
  });
}

function resolveStateDir() {
  const explicit =
    process.env.OPENCLAW_STATE_DIR ??
    process.env.OPENCLAW_CONFIG_DIR ??
    process.env.OPENCLAW_HOME;
  if (typeof explicit === "string" && explicit.trim().length > 0) {
    return resolve(explicit);
  }

  const inferred = inferInstalledStateDir();
  if (inferred !== null) return inferred;
  return join(homedir(), ".openclaw");
}

function inferInstalledStateDir() {
  // ClawHub installs this file at:
  //   <stateDir>/workspace/skills/kokochat-pairing/generate-kokochat-code.mjs
  // If we're running from there, infer <stateDir>. This matters for
  // `openclaw --profile ...`: without explicit env vars the child `openclaw qr`
  // would silently use the default ~/.openclaw gateway/port.
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const candidate = resolve(scriptDir, "..", "..", "..");
  if (existsSync(join(candidate, "openclaw.json"))) {
    return candidate;
  }
  return null;
}

function openclawCommandEnv() {
  return {
    ...openclawEnv,
    ...process.env,
    OPENCLAW_STATE_DIR: stateDir,
    OPENCLAW_CONFIG_PATH: join(stateDir, "openclaw.json")
  };
}

function parsePairingRequest(rawInput) {
  const candidates = [];
  const trimmed = String(rawInput ?? "").trim();
  if (trimmed) {
    candidates.push(trimmed);
  }
  for (const match of trimmed.matchAll(/[A-Za-z0-9_-]{80,}/g)) {
    candidates.push(match[0]);
  }

  for (const candidate of candidates) {
    const parsed = parseCandidate(candidate);
    if (parsed) {
      return validateRequest(parsed);
    }
  }
  throw new Error("No valid KokoChat pairing request found.");
}

function parseCandidate(candidate) {
  try {
    return JSON.parse(candidate);
  } catch {
    // Try base64url/base64 below.
  }

  try {
    return JSON.parse(Buffer.from(candidate, "base64url").toString("utf8"));
  } catch {
    return null;
  }
}

function validateRequest(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("KokoChat pairing request must decode to an object.");
  }
  if (value.type !== "kokochat.pairingRequest" || value.version !== 1) {
    throw new Error("Unsupported KokoChat pairing request type or version.");
  }
  const deviceId = stringField(value, "deviceId");
  const publicKey = stringField(value, "publicKey");
  if (!/^[0-9a-f]{64}$/.test(deviceId)) {
    throw new Error("KokoChat pairing request has an invalid deviceId.");
  }
  if (!/^[A-Za-z0-9_-]{32,}$/.test(publicKey)) {
    throw new Error("KokoChat pairing request has an invalid publicKey.");
  }
  const role = typeof value.role === "string" && value.role.trim() ? value.role.trim() : "operator";
  if (role !== "operator") {
    throw new Error(`Unsupported KokoChat role: ${role}`);
  }
  const requestedScopes = normalizeScopes(Array.isArray(value.scopes) ? value.scopes : DEFAULT_SCOPES);
  const scopes = DEFAULT_SCOPES.filter((scope) => requestedScopes.includes(scope));
  if (!REQUIRED_SCOPES.every((scope) => scopes.includes(scope))) {
    throw new Error("KokoChat pairing request is missing required operator scopes.");
  }
  const client = value.client && typeof value.client === "object" && !Array.isArray(value.client) ? value.client : {};
  return {
    deviceId,
    publicKey,
    role,
    scopes,
    displayName: stringField(client, "displayName", "KokoChat"),
    platform: stringField(client, "platform", "web"),
    deviceFamily: optionalStringField(client, "deviceFamily"),
    clientId: stringField(client, "id", "webchat"),
    clientMode: stringField(client, "mode", "webchat")
  };
}

function stringField(value, key, fallback) {
  const raw = value?.[key];
  if (typeof raw === "string" && raw.trim()) {
    return raw.trim();
  }
  if (fallback !== undefined) {
    return fallback;
  }
  throw new Error(`KokoChat pairing request is missing ${key}.`);
}

function optionalStringField(value, key) {
  const raw = value?.[key];
  return typeof raw === "string" && raw.trim() ? raw.trim() : undefined;
}

function normalizeScopes(scopes) {
  return [...new Set(scopes.map((scope) => String(scope).trim()).filter(Boolean))].sort();
}

// Self-signed device approval (writing paired.json + minting our own operator
// token) has been removed: pairing now goes through OpenClaw's official
// `openclaw qr` device-pair flow, where the GATEWAY signs the token. That
// self-signing was exactly what a careful OpenClaw flags as a backdoor.

function readJsonObject(file) {
  try {
    const parsed = JSON.parse(readFileSync(file, "utf8"));
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  }
}

function writeJsonAtomic(file, value) {
  mkdirSync(dirname(file), { recursive: true, mode: 0o700 });
  const temp = `${file}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(temp, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  renameSync(temp, file);
}

function readEnvFile(file) {
  let raw;
  try {
    raw = readFileSync(file, "utf8");
  } catch {
    return {};
  }

  const out = {};
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const match = /^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/.exec(trimmed);
    if (!match) continue;
    out[match[1]] = unquoteEnvValue(match[2] ?? "");
  }
  return out;
}

function unquoteEnvValue(value) {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function envValue(key) {
  const value = process.env[key] ?? openclawEnv[key];
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function prepareRelayConnector(root, request) {
  const rawRelayUrl = envValue("KOKOCHAT_RELAY_URL") ?? DEFAULT_RELAY_URL;
  const relayUrl = normalizeWsUrl(rawRelayUrl).replace(/\/+$/, "");
  if (!/^wss?:\/\//.test(relayUrl)) {
    throw new Error("KOKOCHAT_RELAY_URL must start with ws:// or wss://");
  }

  const { relayId, relaySecret } = loadOrCreateRelayCredentials(root, relayUrl);
  const gatewayUrl = relayGatewayUrl(relayUrl, relayId, relaySecret);
  const localGatewayUrl = resolveLocalGatewayUrl(root);
  const configPath = writeRelayConnectorConfig(root, {
    relayUrl,
    relayId,
    relaySecret,
    gatewayUrl: localGatewayUrl
  });
  startRelayConnector(root, relayId, configPath);
  return { relayId, gatewayUrl };
}

function loadOrCreateRelayCredentials(root, relayUrl) {
  const dir = join(root, "kokochat-relay");
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const statePath = join(dir, RELAY_STATE_FILE);
  const existing = readJsonObject(statePath);
  if (
    existing.relayUrl === relayUrl &&
    isRelayId(existing.relayId) &&
    isRelaySecret(existing.relaySecret)
  ) {
    return {
      relayId: existing.relayId,
      relaySecret: existing.relaySecret
    };
  }

  const next = {
    relayUrl,
    relayId: randomBytes(18).toString("base64url"),
    relaySecret: randomBytes(32).toString("base64url"),
    createdAtMs: Date.now()
  };
  writeJsonAtomic(statePath, next);
  chmodSync(statePath, 0o600);
  return next;
}

function resolveLocalGatewayUrl(root) {
  const localGatewayUrl = envValue("KOKOCHAT_LOCAL_GATEWAY_URL");
  if (localGatewayUrl) {
    return normalizeWsUrl(localGatewayUrl);
  }
  const config = readJsonObject(join(root, "openclaw.json"));
  const port = Number(config.gateway?.port) || 18789;
  return `ws://127.0.0.1:${port}`;
}

function relayGatewayUrl(relayUrl, relayId, relaySecret) {
  return `${relayUrl}/v1/gateway/${encodeURIComponent(relayId)}?secret=${encodeURIComponent(relaySecret)}`;
}

function writeRelayConnectorConfig(root, config) {
  const dir = join(root, "kokochat-relay");
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  const file = join(dir, `${config.relayId}.json`);
  writeJsonAtomic(file, config);
  chmodSync(file, 0o600);
  return file;
}

function startRelayConnector(root, relayId, configPath) {
  if (process.env.NODE_ENV === "test" && process.env.KOKOCHAT_SKIP_RELAY_CONNECTOR_START === "1") {
    return;
  }
  const pidFile = join(root, "kokochat-relay", `${relayId}.pid`);
  stopOtherRelayConnectors(root, relayId);

  // If the self-healing systemd daemon is managing the connector, don't spawn
  // a second one — two connectors on the same relay tunnel fight over it and
  // make the phone flap between connected/disconnected. The daemon
  // self-bootstraps from relay.json (which we just wrote), so a restart
  // picks up this pairing.
  //
  // Check whether the unit is installed, not just whether it is active. During
  // first pairing the unit may be inactive/restarting because relay.json did
  // not exist yet. Falling back to a detached connector in that moment creates
  // the exact duplicate-connector race we are trying to avoid.
  if (relayDaemonInstalled()) {
    stopExistingConnector(pidFile);
    stopDetachedRelayConnectors();
    restartRelayDaemon();
    return;
  }
  const connector = fileURLToPath(new URL("./relay/kokochat-relay-connector.mjs", import.meta.url));
  if (!existsSync(connector)) {
    throw new Error(`KokoChat relay connector is missing: ${connector}`);
  }

  if (isPidAlive(pidFile)) {
    return;
  }
  stopExistingConnector(pidFile);
  const child = spawn(process.execPath, [connector, "--config", configPath], {
    detached: true,
    stdio: "ignore",
    env: {
      ...openclawEnv,
      ...process.env,
      KOKOCHAT_RELAY_CONNECTOR_CONFIG: configPath
    }
  });
  child.unref();
  writeFileSync(pidFile, `${child.pid}\n`, { mode: 0o600 });
}

function relayDaemonInstalled() {
  if (process.platform !== "linux") return false;
  const unitPaths = [
    `/etc/systemd/system/${RELAY_DAEMON_SERVICE}`,
    `/run/systemd/system/${RELAY_DAEMON_SERVICE}`,
    `/usr/lib/systemd/system/${RELAY_DAEMON_SERVICE}`,
    `/lib/systemd/system/${RELAY_DAEMON_SERVICE}`
  ];
  if (unitPaths.some((path) => existsSync(path))) return true;
  try {
    const result = spawnSync("systemctl", ["cat", RELAY_DAEMON_SERVICE], {
      stdio: "ignore"
    });
    return result.status === 0;
  } catch {
    return false;
  }
}

function restartRelayDaemon() {
  // The daemon self-bootstraps from relay.json, which this run just wrote.
  // Restart so it reconnects with the freshly-approved device immediately.
  try {
    spawnSync("systemctl", ["reset-failed", RELAY_DAEMON_SERVICE], { stdio: "ignore" });
    spawnSync("systemctl", ["restart", RELAY_DAEMON_SERVICE], { stdio: "ignore" });
  } catch {
    // Best effort; the daemon would also pick it up on its next reconnect.
  }
}

function relayDaemonMainPid() {
  if (process.platform !== "linux") return null;
  try {
    const result = spawnSync("systemctl", ["show", "-p", "MainPID", "--value", RELAY_DAEMON_SERVICE], {
      encoding: "utf8"
    });
    const pid = Number(result.stdout.trim());
    return Number.isInteger(pid) && pid > 0 ? pid : null;
  } catch {
    return null;
  }
}

function stopDetachedRelayConnectors() {
  if (process.platform !== "linux") return;
  const mainPid = relayDaemonMainPid();
  let output = "";
  try {
    const result = spawnSync("pgrep", ["-f", "kokochat-relay-connector.mjs"], {
      encoding: "utf8"
    });
    output = result.stdout ?? "";
  } catch {
    return;
  }
  for (const line of output.split(/\r?\n/)) {
    const pid = Number(line.trim());
    if (!Number.isInteger(pid) || pid <= 0) continue;
    if (pid === process.pid || pid === mainPid) continue;
    terminatePid(pid);
  }
}

function stopOtherRelayConnectors(root, relayId) {
  const dir = join(root, "kokochat-relay");
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return;
  }
  for (const entry of entries) {
    if (!entry.endsWith(".pid") || entry === `${relayId}.pid`) {
      continue;
    }
    stopExistingConnector(join(dir, entry));
  }
}

function isPidAlive(pidFile) {
  if (!existsSync(pidFile)) {
    return false;
  }
  const pid = Number(readFileSync(pidFile, "utf8").trim());
  if (!Number.isInteger(pid) || pid <= 0) {
    return false;
  }
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function stopExistingConnector(pidFile) {
  if (!existsSync(pidFile)) {
    return;
  }
  const pid = Number(readFileSync(pidFile, "utf8").trim());
  if (!Number.isInteger(pid) || pid <= 0) {
    rmSync(pidFile, { force: true });
    return;
  }
  terminatePid(pid);
  rmSync(pidFile, { force: true });
}

function terminatePid(pid) {
  try {
    process.kill(pid, "SIGTERM");
  } catch {
    // The previous connector is already gone.
    return;
  }
  for (let i = 0; i < 10; i += 1) {
    if (!pidAlive(pid)) return;
    sleepMs(100);
  }
  try {
    process.kill(pid, "SIGKILL");
  } catch {
    // The process exited between the final liveness check and SIGKILL.
  }
}

function pidAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function sleepMs(ms) {
  spawnSync("sh", ["-c", `sleep ${Math.max(0, ms) / 1000}`], { stdio: "ignore" });
}

function normalizeWsUrl(url) {
  return String(url).replace(/^http:/, "ws:").replace(/^https:/, "wss:");
}

function encodeJson(value) {
  return Buffer.from(JSON.stringify(value)).toString("base64url");
}

function isRelayId(value) {
  return typeof value === "string" && /^[A-Za-z0-9_-]{16,160}$/.test(value);
}

function isRelaySecret(value) {
  return typeof value === "string" && /^[A-Za-z0-9_-]{32,256}$/.test(value);
}
