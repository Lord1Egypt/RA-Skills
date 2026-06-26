#!/usr/bin/env node
// notify-hub config.js — Read/write persistent skill configuration.
//
// Config file: ~/.config/notify-hub/config.json  (user-level, shared across workspaces)
//
// Supported fields:
//   rules          {array}    Routing rules. If omitted, DEFAULT_RULES are used.
//                             Each rule: { name, senderDomains, keywords, prefix }
//                             A matched rule always triggers immediate forwarding.
//                             Unmatched messages go to the daily summary.
//
// The recipient email is fetched via `mail-cli clawemail list --json` (data.userEmail).
// No manual configuration is needed.
//
// Usage (CLI):
//   node config.js get                 # print all config as JSON
//   node config.js get rules           # print rules array
//   node config.js set <key> <value>   # set a scalar field
//   node config.js unset <key>         # remove a field
//   node config.js rules-init          # merge default rules into config.json (then edit freely)
//   node config.js rules-reset         # overwrite rules with defaults

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Default routing rules
// ---------------------------------------------------------------------------

const DEFAULT_RULES = [
  {
    name: "stripe-payment",
    senderDomains: ["stripe.com", "emails.stripe.com"],
    keywords: "payment|charge|refund|payout",
    prefix: "💰 Stripe",
  },
  {
    name: "github-ci-failure",
    senderDomains: ["github.com", "noreply.github.com", "notifications.github.com"],
    keywords: "failed|broken|error",
    prefix: "🔴 GitHub CI",
  },
  {
    name: "urgent-catchall",
    senderDomains: null,
    keywords: "security|urgent|critical|outage|deploy",
    prefix: "🚨",
  },
];

// ---------------------------------------------------------------------------
// Paths
// ---------------------------------------------------------------------------
function getConfigDir() {
  const home = process.env.HOME || process.env.USERPROFILE || "~";
  return path.join(home, ".config", "notify-hub");
}

function getConfigPath() {
  return path.join(getConfigDir(), "config.json");
}

// ---------------------------------------------------------------------------
// Read / Write
// ---------------------------------------------------------------------------
function loadConfig() {
  const p = getConfigPath();
  if (!fs.existsSync(p)) return {};
  try {
    return JSON.parse(fs.readFileSync(p, "utf8"));
  } catch {
    return {};
  }
}

function saveConfig(cfg) {
  const dir = getConfigDir();
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(getConfigPath(), JSON.stringify(cfg, null, 2) + "\n");
}

// ---------------------------------------------------------------------------
// Exported API
// ---------------------------------------------------------------------------

/**
 * Get a config value. Returns undefined if not set.
 */
function getConfig(key) {
  return loadConfig()[key];
}

/**
 * Get routing rules from config. Falls back to DEFAULT_RULES if not configured.
 */
function getRules() {
  const cfg = loadConfig();
  return Array.isArray(cfg.rules) && cfg.rules.length > 0 ? cfg.rules : DEFAULT_RULES;
}

/**
 * Get the claw primary account email via mail-cli.
 * Exits with a descriptive error if mail-cli is unavailable or not configured.
 */
function getPrimaryEmail() {
  let raw;
  try {
    raw = execSync("mail-cli clawemail list --json", {
      encoding: "utf8",
      timeout: 15000,
      stdio: ["pipe", "pipe", "pipe"],
    });
  } catch {
    console.error(
      "\n[notify-hub] ❌ 无法调用 mail-cli，请确认已安装并配置：\n\n" +
      "  npm install -g @clawemail/mail-cli\n\n"
    );
    process.exit(1);
  }

  try {
    const data = JSON.parse(raw);
    const email = data?.data?.userEmail;
    if (!email) throw new Error("userEmail field missing");
    return email;
  } catch {
    console.error(
      "\n[notify-hub] ❌ 无法解析 mail-cli 返回的主账号信息，请检查 mail-cli 配置。\n"
    );
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// CLI entrypoint
// ---------------------------------------------------------------------------
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === "get") {
    const key = args[1];
    const cfg = loadConfig();
    if (key) {
      const val = cfg[key];
      if (val === undefined) {
        console.error(`Key "${key}" is not set.`);
        process.exit(1);
      }
      console.log(val);
    } else {
      if (Object.keys(cfg).length === 0) {
        console.log("(no configuration set)");
      } else {
        console.log(JSON.stringify(cfg, null, 2));
      }
    }
    process.exit(0);
  }

  if (cmd === "set") {
    const key = args[1];
    const value = args[2];
    if (!key || value === undefined) {
      console.error("Usage: node config.js set <key> <value>");
      process.exit(1);
    }
    const cfg = loadConfig();
    cfg[key] = value;
    saveConfig(cfg);
    console.log(`✅ ${key} = ${value}`);
    process.exit(0);
  }

  if (cmd === "unset") {
    const key = args[1];
    if (!key) {
      console.error("Usage: node config.js unset <key>");
      process.exit(1);
    }
    const cfg = loadConfig();
    delete cfg[key];
    saveConfig(cfg);
    console.log(`✅ ${key} unset`);
    process.exit(0);
  }

  if (cmd === "rules-init") {
    const cfg = loadConfig();
    const existing = Array.isArray(cfg.rules) ? cfg.rules : [];
    let added = 0;
    for (const def of DEFAULT_RULES) {
      if (!existing.find((r) => r.name === def.name)) {
        existing.push(def);
        added++;
      }
    }
    cfg.rules = existing;
    saveConfig(cfg);
    if (added > 0) {
      console.log(`✅ Merged ${added} default rule(s) into ${getConfigPath()}`);
    } else {
      console.log(`✅ All default rules already present in ${getConfigPath()}`);
    }
    console.log("Edit the file directly to add, remove or modify rules.");
    process.exit(0);
  }

  if (cmd === "rules-reset") {
    const cfg = loadConfig();
    cfg.rules = DEFAULT_RULES;
    saveConfig(cfg);
    console.log(`✅ Rules reset to defaults in ${getConfigPath()}`);
    process.exit(0);
  }

  if (cmd === "whoami") {
    console.log(getPrimaryEmail());
    process.exit(0);
  }

  console.error(`Unknown command: ${cmd}. Use get / set / unset / whoami / rules-init / rules-reset.`);
  process.exit(1);
}

module.exports = { getConfig, getRules, getPrimaryEmail, loadConfig, saveConfig, DEFAULT_RULES };
