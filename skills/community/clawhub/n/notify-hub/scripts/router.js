#!/usr/bin/env node
// notify-hub router.js — Poll the notify mailbox and route messages by urgency.
//
// Usage: node router.js [options]
//
// Options:
//   --profile <name>            mail-cli profile for the notify mailbox (default: notify)
//   --dry-run                   Print actions without sending mail or marking read
//
// Routing rules are loaded from ~/.config/notify-hub/config.json (rules array).
// Run `node scripts/config.js rules-init` to scaffold the default rules for editing.
//
// De-duplication: handled by marking processed messages as read.
// Log: daily JSONL in os.tmpdir()/notify-hub-YYYY-MM-DD.jsonl

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { getPrimaryEmail, getRules } = require("./config");

// ---------------------------------------------------------------------------
// Arg parsing
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
let profileName = "notify";
let dryRun = false;

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--profile":
      profileName = args[++i];
      break;
    case "--dry-run":
      dryRun = true;
      break;
    default:
      console.error(`Unknown option: ${args[i]}`);
      process.exit(1);
  }
}

// Fetch primary email from claw account via mail-cli
const mainEmail = getPrimaryEmail();

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function run(cmd) {
  try {
    return execSync(cmd, { encoding: "utf8", timeout: 30000, stdio: ["pipe", "pipe", "pipe"] });
  } catch {
    return null;
  }
}

function findMailCli() {
  const isWin = process.platform === "win32";
  const result = run(isWin ? "where mail-cli" : "which mail-cli");
  if (result && result.trim()) return "mail-cli";
  return "npx mail-cli";
}

function getDailyLogPath() {
  const dateStr = new Date().toLocaleDateString("sv-SE"); // YYYY-MM-DD
  return path.join(os.tmpdir(), `notify-hub-${dateStr}.jsonl`);
}

function appendDailyLog(entry) {
  const logPath = getDailyLogPath();
  fs.appendFileSync(logPath, JSON.stringify(entry) + "\n");
}

// ---------------------------------------------------------------------------
// Routing rules — loaded from config (falls back to DEFAULT_RULES)
// ---------------------------------------------------------------------------

/**
 * Load rules from config and compile the keywords string into a RegExp.
 * Invalid regex patterns are skipped with a warning so a single bad rule
 * doesn't break the whole run.
 */
function loadCompiledRules() {
  const rules = getRules();
  const result = [];
  for (const rule of rules) {
    let pattern;
    try {
      pattern = new RegExp(rule.keywords, "i");
    } catch {
      console.warn(`[WARN] Skipping rule "${rule.name}": invalid keywords regex "${rule.keywords}"`);
      continue;
    }
    result.push({ ...rule, keywords: pattern });
  }
  return result;
}

function matchSenderDomain(from, domains) {
  if (!domains) return true;
  const lower = (from || "").toLowerCase();
  return domains.some((d) => lower.includes(d));
}

function classifyMessage(msg, rules) {
  const subject = msg.subject || "";
  const from = msg.from || "";

  for (const rule of rules) {
    if (matchSenderDomain(from, rule.senderDomains) && rule.keywords.test(subject)) {
      return rule;
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// Actions
// ---------------------------------------------------------------------------
function forwardImmediately(cli, msg, rule, fid) {
  const newSubject = `[${rule.prefix}] ${msg.subject || "(no subject)"}`;
  const bodyLines = [
    `转发自: ${msg.from}`,
    `原始主题: ${msg.subject || "(no subject)"}`,
    `时间: ${msg.sentDate || msg.receivedDate || msg.date || ""}`,
    ``,
    `--- 邮件正文 ---`,
  ];

  const bodyRaw = run(`${cli} --profile ${profileName} read body --id "${msg.id}" --fid ${fid}`);
  if (bodyRaw) bodyLines.push(bodyRaw.trim());

  const body = bodyLines.join("\n");

  if (dryRun) {
    console.log(`[DRY-RUN] Would forward: "${newSubject}" -> ${mainEmail}`);
    return true;
  }

  // Write body to a temp file to avoid shell escaping issues (e.g. $ in amounts)
  const tmpFile = path.join(os.tmpdir(), `notify-hub-fwd-${Date.now()}.txt`);
  try {
    fs.writeFileSync(tmpFile, body, "utf8");
    const result = run(
      `${cli} --profile ${profileName} compose send --to "${mainEmail}" --subject "${newSubject.replace(/"/g, '\\"')}" --body-file "${tmpFile}"`
    );
    return result !== null;
  } finally {
    if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
  }
}

function appendToLog(msg) {
  const entry = {
    id: msg.id,
    from: msg.from,
    subject: msg.subject || "(no subject)",
    time: msg.sentDate || msg.receivedDate || msg.date || "",
  };
  if (dryRun) {
    console.log(`[DRY-RUN] Would append to daily log: ${JSON.stringify(entry)}`);
    return;
  }
  appendDailyLog(entry);
}

function markRead(cli, id, fid) {
  run(`${cli} --profile ${profileName} mail mark --ids "${id}" --read --fid ${fid}`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const cli = findMailCli();
  const compiledRules = loadCompiledRules();

  // 1. Get inbox folder ID
  const folderRaw = run(`${cli} --profile ${profileName} folder list --json`);
  if (!folderRaw) {
    console.error(`Failed to list folders for profile "${profileName}". Check your mail-cli configuration.`);
    process.exit(1);
  }

  let folders;
  try {
    const folderData = JSON.parse(folderRaw);
    folders = folderData.data || folderData;
  } catch {
    console.error("Failed to parse folder list output");
    process.exit(1);
  }

  const inbox = Array.isArray(folders)
    ? folders.find((f) => f.id === 1 || f.name === "INBOX" || f.name === "收件箱")
    : null;
  const fid = inbox ? inbox.id : 1;

  // 2. Fetch unread messages
  const listRaw = run(`${cli} --profile ${profileName} mail list --fid ${fid} --unread --json`);
  if (!listRaw) {
    console.log("No messages or failed to list mail.");
    return;
  }

  let messages;
  try {
    const listData = JSON.parse(listRaw);
    messages = Array.isArray(listData) ? listData : (listData.data || []);
  } catch {
    console.error("Failed to parse mail list output");
    process.exit(1);
  }

  if (messages.length === 0) {
    console.log("No unread messages.");
    return;
  }

  let forwarded = 0;
  let logged = 0;

  // 3. Process each message
  for (const msg of messages) {
    const id = String(msg.id || msg.msgId || "");
    if (!id) continue;

    const matchedRule = classifyMessage(msg, compiledRules);

    if (matchedRule) {
      const ok = forwardImmediately(cli, msg, matchedRule, fid);
      if (ok) {
        forwarded++;
        console.log(`[FORWARD] ${matchedRule.prefix} — ${msg.subject}`);
        if (!dryRun) markRead(cli, id, fid);
      }
    } else {
      appendToLog(msg);
      logged++;
      console.log(`[LOG] ${msg.subject}`);
      if (!dryRun) markRead(cli, id, fid);
    }
  }

  console.log(`Done. forwarded=${forwarded} logged=${logged}`);
}

try {
  main();
} catch (err) {
  console.error("Unexpected error:", err);
  process.exit(1);
}
