/**
 * doctor-check.js — Post-write openclaw doctor wrapper
 *
 * Runs `openclaw doctor` on a candidate config file.
 * Used after normalization or import to verify the config is valid.
 */

"use strict";

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const OPENCLAW_BIN = process.env.OPENCLAW_BIN || (() => {
  if (process.env.OPENCLAW_BIN) return process.env.OPENCLAW_BIN;
  return `${process.env.HOME}/.nvm/versions/node/v24.14.1/bin/openclaw`;
})();

// Patterns that indicate actual config failures (not advisory warnings)
const CONFIG_FAIL_PATTERNS = [
  /Cannot load.*config/i,
  /invalid.*json/i,
  /schema.*error/i,
  /config.*crash/i,
  /TypeError.*config/i,
  /SyntaxError/i,
  /JSON.*parse.*error/i,
  /openclaw\.json.*error/i,
];

function looksLikeConfigFailure(output) {
  return CONFIG_FAIL_PATTERNS.some((p) => p.test(output));
}

/**
 * Run openclaw doctor on a candidate config.
 * @param {string} configPath — path to openclaw.json candidate
 * @returns {{ ok: boolean, output: string, rc: number }}
 */
function runDoctor(configPath) {
  if (!fs.existsSync(configPath)) {
    return { ok: false, output: `Config file not found: ${configPath}`, rc: 2 };
  }

  const tmpDir = `${process.env.TMPDIR || "/tmp"}/openclaw-doctor-${process.pid}`;
  fs.mkdirSync(tmpDir, { recursive: true });
  const tmpConfig = path.join(tmpDir, "openclaw.json");
  fs.copyFileSync(configPath, tmpConfig);

  try {
    const output = execSync(`${OPENCLAW_BIN} doctor --non-interactive`, {
      cwd: tmpDir,
      timeout: 30000,
      encoding: "utf8",
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, OPENCLAW_CONFIG: tmpConfig },
    });
    return { ok: true, output, rc: 0 };
  } catch (err) {
    const out = err.stdout || err.stderr || err.message || "";
    // openclaw doctor exits 1 for warnings even when config is valid.
    // Only treat as failure if output contains actual config error patterns.
    if (looksLikeConfigFailure(out)) {
      return { ok: false, output: out, rc: err.status || 1 };
    }
    return { ok: true, output: out, rc: err.status || 1 };
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

/**
 * Restart the gateway after a config change.
 * @returns {{ ok: boolean, output: string }}
 */
function restartGateway() {
  try {
    const output = execSync(`openclaw gateway restart`, {
      timeout: 15000,
      encoding: "utf8",
      stdio: ["pipe", "pipe", "pipe"],
    });
    return { ok: true, output };
  } catch (err) {
    const out = err.stdout || err.stderr || err.message;
    return { ok: false, output: out, rc: err.status };
  }
}

/**
 * Check if the gateway is responsive.
 * @returns {boolean}
 */
function isGatewayUp() {
  try {
    execSync(`openclaw sessions`, { timeout: 10000, stdio: ["ignore", "ignore", "ignore"] });
    return true;
  } catch {
    return false;
  }
}

module.exports = { runDoctor, restartGateway, isGatewayUp };
