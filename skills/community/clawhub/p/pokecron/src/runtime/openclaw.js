// OpenClaw runtime backend.
//
// Implements the poke runtime interface (see src/runtime/index.js) on top of
// the OpenClaw CLI: agent --local --deliver / agent --local / agents list.
// This is the only place that knows OpenClaw's flag grammar. If poke moves
// to a different harness, replace THIS file (or write a sibling) — nothing
// in reminders.js / scheduler.js / calendar.js should change.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { randomUUID } from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const SKILL_ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const DEFAULT_COMPAT_DIR = process.env.POKE_COMPAT_DIR || path.join(SKILL_ROOT_DIR, ".runtime", "openclaw-compat");
const DEFAULT_OPENCLAW_TIMEOUT_MS = 525_000;
const DEFAULT_OPENCLAW_RETRY_DELAY_MS = 10_000;
const TRANSIENT_OPENCLAW_ERROR_PATTERN =
  /gateway|ECONNREFUSED|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|socket hang up|fetch failed|network|temporar|timeout|timed out|502|503|504/i;

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function exists(filePath) {
  try { fs.accessSync(filePath, fs.constants.F_OK); return true; } catch { return false; }
}

function executable(filePath) {
  try { fs.accessSync(filePath, fs.constants.X_OK); return true; } catch { return false; }
}

function splitPathList(value) {
  return String(value || "").split(path.delimiter).map((entry) => entry.trim()).filter(Boolean);
}

function findExecutableInPath(name) {
  const names = process.platform === "win32"
    ? unique([name, `${name}.cmd`, `${name}.exe`, `${name}.bat`])
    : [name];
  for (const directory of splitPathList(process.env.PATH)) {
    for (const candidate of names) {
      const resolved = path.join(directory, candidate);
      if (executable(resolved)) return resolved;
    }
  }
  return null;
}

function makeCompatConfig(configPath, compatDir = DEFAULT_COMPAT_DIR) {
  fs.mkdirSync(compatDir, { recursive: true });
  const tempPath = path.join(compatDir, `poke-openclaw-${process.pid}-${Date.now()}.json`);
  const raw = fs.readFileSync(configPath, "utf8");
  const parsed = JSON.parse(raw);
  for (const channel of Object.values(parsed.channels || {})) {
    if (channel && typeof channel.streaming === "object" && typeof channel.streaming.mode === "string") {
      channel.streaming = channel.streaming.mode;
    }
  }
  fs.writeFileSync(tempPath, JSON.stringify(parsed, null, 2));
  return tempPath;
}

function cleanupTempFile(filePath) {
  if (!filePath) return;
  try { fs.unlinkSync(filePath); } catch {}
}

function parseJsonOrNull(value) {
  try { return JSON.parse(value); } catch { return null; }
}

function sleepSync(ms) {
  if (ms <= 0) return;
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

function errorOutput(err) {
  return [err?.message, err?.stdout, err?.stderr, ...(Array.isArray(err?.output) ? err.output : [])]
    .filter(Boolean)
    .map((entry) => Buffer.isBuffer(entry) ? entry.toString("utf8") : String(entry))
    .join("\n");
}

function shouldRetryOpenClawError(err) {
  return TRANSIENT_OPENCLAW_ERROR_PATTERN.test(errorOutput(err));
}

function sanitizeSessionFragment(value) {
  return String(value || "").trim().replace(/[^A-Za-z0-9_.-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 48);
}

function makeIsolatedSessionId(prefix, hint = "") {
  const safePrefix = sanitizeSessionFragment(prefix) || "poke";
  const safeHint = sanitizeSessionFragment(hint);
  const uuid = randomUUID().replace(/-/g, "").slice(0, 12);
  return [safePrefix, safeHint, uuid].filter(Boolean).join("-");
}

function resolveOpenClawPaths(options = {}) {
  const home =
    options.preferredHome ||
    process.env.POKE_SEND_HOME ||
    process.env.OPENCLAW_BRIDGE_HOME ||
    os.homedir();
  const stateDir =
    options.preferredStateDir ||
    process.env.POKE_SEND_STATE_DIR ||
    process.env.OPENCLAW_BRIDGE_STATE_DIR ||
    process.env.OPENCLAW_STATE_DIR ||
    path.join(home, ".openclaw");
  const configPath =
    options.preferredConfigPath ||
    process.env.POKE_SEND_CONFIG_PATH ||
    process.env.OPENCLAW_BRIDGE_CONFIG_PATH ||
    process.env.OPENCLAW_CONFIG_PATH ||
    path.join(stateDir, "openclaw.json");

  const binaryCandidates = unique([
    options.preferredBin,
    process.env.POKE_SEND_BIN,
    process.env.OPENCLAW_BRIDGE_BIN,
    process.env.OPENCLAW_BIN,
    findExecutableInPath("openclaw"),
    path.join(stateDir, "bin", process.platform === "win32" ? "openclaw.cmd" : "openclaw"),
    path.join(stateDir, "bin", "openclaw")
  ]);

  const bin = binaryCandidates.find((candidate) => candidate && executable(candidate));
  if (!bin) {
    throw new Error(
      "OpenClaw CLI not found. Set POKE_SEND_BIN, OPENCLAW_BRIDGE_BIN, OPENCLAW_BIN, or add openclaw to PATH."
    );
  }
  if (!exists(configPath)) {
    throw new Error(
      `OpenClaw config not found: ${configPath}. Set POKE_SEND_CONFIG_PATH, OPENCLAW_BRIDGE_CONFIG_PATH, or OPENCLAW_CONFIG_PATH.`
    );
  }

  return {
    home,
    stateDir,
    configPath,
    bin,
    compatDir: options.preferredCompatDir || process.env.POKE_COMPAT_DIR || DEFAULT_COMPAT_DIR
  };
}

function runOpenClawCli(paths, args, options = {}) {
  const compatConfig = makeCompatConfig(paths.configPath, paths.compatDir || DEFAULT_COMPAT_DIR);
  const timeoutMs = options.timeoutMs || DEFAULT_OPENCLAW_TIMEOUT_MS;
  const retryDelayMs = options.retryDelayMs || DEFAULT_OPENCLAW_RETRY_DELAY_MS;
  const deadline = Date.now() + timeoutMs;
  let lastError = null;
  try {
    while (true) {
      const remainingMs = deadline - Date.now();
      if (remainingMs <= 0) throw lastError || new Error("OpenClaw command timed out before it could start");
      try {
        return execFileSync(paths.bin, args, {
          encoding: "utf8",
          timeout: remainingMs,
          env: {
            ...process.env,
            HOME: paths.home,
            OPENCLAW_STATE_DIR: paths.stateDir,
            OPENCLAW_CONFIG_PATH: compatConfig
          },
          stdio: ["pipe", "pipe", "pipe"]
        });
      } catch (err) {
        lastError = err;
        const timeLeftAfterDelay = deadline - Date.now() - retryDelayMs;
        if (!shouldRetryOpenClawError(err) || timeLeftAfterDelay <= 0) throw err;
        sleepSync(retryDelayMs);
      }
    }
  } finally {
    cleanupTempFile(compatConfig);
  }
}

export function createOpenClawRuntime(options = {}) {
  const paths = resolveOpenClawPaths(options);

  return {
    id: "openclaw",
    home: paths.home,
    stateDir: paths.stateDir,
    configPath: paths.configPath,
    bin: paths.bin,
    compatDir: paths.compatDir,

    // Interface — see src/runtime/index.js for the spec.

    deliver({ agent, channel, target, prompt, thinking = "low", sessionId = "", sessionHint = "" }) {
      return runOpenClawCli(paths, [
        "agent", "--local",
        "--agent", agent,
        "--session-id", sessionId || makeIsolatedSessionId("poke-deliver", sessionHint || target || channel),
        "--message", prompt,
        "--deliver",
        "--channel", channel,
        "--reply-channel", channel,
        "--reply-to", target,
        "--thinking", thinking
      ]);
    },

    localAgent({ agent, prompt, thinking = "low", sessionId = "", sessionHint = "" }) {
      return runOpenClawCli(paths, [
        "agent", "--local",
        "--agent", agent,
        "--session-id", sessionId || makeIsolatedSessionId("poke-local", sessionHint),
        "--message", prompt,
        "--thinking", thinking
      ]);
    },

    defaultAgentId() {
      try {
        const output = runOpenClawCli(paths, ["agents", "list", "--json"], { timeoutMs: 30_000 });
        const parsed = parseJsonOrNull(output);
        if (!Array.isArray(parsed) || parsed.length === 0) return "";
        const selected = parsed.find((entry) => entry?.isDefault) || parsed[0];
        return selected?.id ? String(selected.id) : "";
      } catch {
        return "";
      }
    },

    // Escape hatch for tests and edge cases — direct CLI access.
    _rawCli(args, opts) { return runOpenClawCli(paths, args, opts); }
  };
}

export { DEFAULT_COMPAT_DIR, SKILL_ROOT_DIR };
