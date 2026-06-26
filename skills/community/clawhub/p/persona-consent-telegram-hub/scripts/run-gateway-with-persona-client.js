#!/usr/bin/env node
/**
 * Wrapper: start persona-client in the background, then run openclaw gateway.
 * Use this for the "install skill and it auto-runs" experience until OpenClaw
 * supports skill lifecycle hooks.
 *
 * Usage:
 *   node scripts/run-gateway-with-persona-client.js [--] [openclaw gateway args...]
 *
 * Reads ~/.openclaw/openclaw.json and uses skills.entries["persona-consent-telegram-hub"].env
 * for the persona-client. If PERSONA_SERVICE_URL and PERSONA_CLIENT_ID are not set,
 * only openclaw gateway is run.
 */

const { spawn } = require("node:child_process");
const path = require("node:path");
const fs = require("node:fs");

const SKILL_ID = "persona-consent-telegram-hub";
const configPath = process.env.OPENCLAW_CONFIG_PATH || path.join(process.env.HOME || process.env.USERPROFILE, ".openclaw", "openclaw.json");

function loadSkillEnv() {
  let raw;
  try {
    raw = fs.readFileSync(configPath, "utf8");
  } catch (e) {
    return null;
  }
  let config;
  try {
    config = JSON.parse(raw);
  } catch (e) {
    return null;
  }
  const entries = config?.skills?.entries;
  if (!entries || typeof entries !== "object") return null;
  const entry = entries[SKILL_ID];
  if (!entry || typeof entry.env !== "object") return null;
  return entry.env;
}

function main() {
  const skillEnv = loadSkillEnv();
  const personaUrl = skillEnv?.PERSONA_SERVICE_URL?.trim();
  const clientId = skillEnv?.PERSONA_CLIENT_ID?.trim();

  const skillDir = path.resolve(__dirname, "..");
  const scriptPath = path.join(skillDir, "scripts", "persona_client.sh");

  let argv = process.argv.slice(2);
  if (argv[0] === "--") argv = argv.slice(1);

  if (personaUrl && clientId && fs.existsSync(scriptPath)) {
    const childEnv = { ...process.env, ...skillEnv };
    const child = spawn("bash", [scriptPath], {
      cwd: skillDir,
      env: childEnv,
      stdio: "ignore",
      detached: true,
    });
    child.unref();
  }

  const openclaw = spawn("openclaw", ["gateway", ...argv], {
    stdio: "inherit",
    env: process.env,
  });
  process.exitCode = openclaw.exitCode ?? null;
  openclaw.on("exit", (code, sig) => {
    process.exit(code ?? (sig ? 128 + 1 : 0));
  });
}

main();
