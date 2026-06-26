#!/usr/bin/env node
// notify-hub summarize.js — Read today's daily log and send a digest email.
//
// Usage: node summarize.js [--date YYYY-MM-DD] [--dry-run]
//
// Recipient email is fetched automatically from the claw primary account via mail-cli.
// Reads:  os.tmpdir()/notify-hub-YYYY-MM-DD.jsonl
// Sends:  digest email to primary account
// Clears: the log file after a successful send

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { getPrimaryEmail } = require("./config");

// ---------------------------------------------------------------------------
// Arg parsing
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
let targetDate = new Date().toLocaleDateString("sv-SE"); // YYYY-MM-DD, default today
let dryRun = false;
let profileName = "notify";

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--date":
      targetDate = args[++i];
      break;
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

function getLogPath(dateStr) {
  return path.join(os.tmpdir(), `notify-hub-${dateStr}.jsonl`);
}

function readLogEntries(logPath) {
  if (!fs.existsSync(logPath)) return [];
  const lines = fs.readFileSync(logPath, "utf8").trim().split("\n").filter(Boolean);
  const entries = [];
  for (const line of lines) {
    try {
      entries.push(JSON.parse(line));
    } catch {
      // skip malformed lines
    }
  }
  return entries;
}

// Group entries by sender domain for a cleaner digest layout
function groupByDomain(entries) {
  const groups = {};
  for (const e of entries) {
    const match = (e.from || "").match(/@([\w.-]+)/);
    const domain = match ? match[1] : "unknown";
    if (!groups[domain]) groups[domain] = [];
    groups[domain].push(e);
  }
  return groups;
}

function buildDigestMarkdown(entries, dateStr) {
  const groups = groupByDomain(entries);
  const lines = [
    `# notify-hub 每日通知汇总`,
    ``,
    `**日期**: ${dateStr}`,
    `**通知总数**: ${entries.length} 封`,
    ``,
  ];

  for (const [domain, items] of Object.entries(groups)) {
    lines.push(`## ${domain} (${items.length} 封)`);
    lines.push(``);
    lines.push(`| 时间 | 主题 | 发件人 |`);
    lines.push(`|------|------|--------|`);
    for (const item of items) {
      const time = (item.time || "").replace("T", " ").slice(0, 16);
      const subject = (item.subject || "(no subject)").replace(/\|/g, "\\|");
      const from = (item.from || "").replace(/\|/g, "\\|");
      lines.push(`| ${time} | ${subject} | ${from} |`);
    }
    lines.push(``);
  }

  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const cli = findMailCli();
  const logPath = getLogPath(targetDate);

  // Run a final poll before reading the log to flush any emails that arrived
  // since the last scheduled poll (avoids the race condition where summarize
  // fires at the same time as router and misses recently-arrived messages).
  if (!dryRun) {
    const routerScript = path.join(__dirname, "router.js");
    console.log("Running final poll to flush pending emails...");
    try {
      // Use a longer timeout than the default run() helper (30s) because
      // router.js may need to process many messages with multiple network calls.
      execSync(`node "${routerScript}" --profile ${profileName}`, {
        encoding: "utf8",
        timeout: 120000,
        stdio: ["pipe", "pipe", "pipe"],
      });
    } catch {
      // Non-fatal: if the poll fails or times out, proceed with whatever
      // entries are already in the log rather than aborting the digest.
      console.warn("Warning: final poll did not complete cleanly; proceeding with existing log.");
    }
  }

  const entries = readLogEntries(logPath);

  if (entries.length === 0) {
    console.log(`Log: ${logPath}`);
    console.log("No entries — skipping digest.");
    return;
  }

  const digest = buildDigestMarkdown(entries, targetDate);
  const subject = `notify-hub 每日汇总 ${targetDate} — ${entries.length} 封通知`;

  console.log(`Log: ${logPath}`);
  console.log(`Entries: ${entries.length}`);
  console.log(`Subject: ${subject}`);

  if (dryRun) {
    console.log(`[DRY-RUN] Would send digest to ${mainEmail}`);
    console.log(`\n--- Digest ---\n${digest}\n--- End ---`);
    return;
  }

  // Write digest to a temp file to avoid shell escaping issues
  const tmpFile = path.join(os.tmpdir(), `notify-hub-digest-${Date.now()}.txt`);
  try {
    fs.writeFileSync(tmpFile, digest, "utf8");
    const escapedSubject = subject.replace(/"/g, '\\"');
    const result = run(
      `${cli} --profile ${profileName} compose send --to "${mainEmail}" --subject "${escapedSubject}" --body-file "${tmpFile}"`
    );
    if (result === null) {
      console.error("Failed to send digest email. Check mail-cli configuration.");
      process.exit(1);
    }
  } finally {
    if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
  }

  console.log(`Digest sent to ${mainEmail}`);

  // Clear the log after a successful send
  if (fs.existsSync(logPath)) {
    fs.unlinkSync(logPath);
    console.log(`Log cleared: ${logPath}`);
  }
}

try {
  main();
} catch (err) {
  console.error("Unexpected error:", err);
  process.exit(1);
}
