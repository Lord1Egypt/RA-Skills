#!/usr/bin/env node
/**
 * Notification Triage — Smart filtering and batching for agent notifications
 * 
 * Modes:
 *   --classify <message> <source>    → Classify notification by urgency
 *   --classify --force               → Classify without persisting auto-rule
 *   --batch <count>                  → Show pending batched notifications
 *   --batch --send <count>           → Flush batch to output
 *   --seen <id>                      → Mark notification as seen
 *   --seen --all                     → Mark all as seen
 *   --rules                          → List current rules
 *   --rules add <source> <level>     → Add rule (urgent|batch|ignore)
 *   --rules remove <source>          → Remove rule
 *   --rules clear                    → Wipe all rules
 *   --status                         → Triage status overview
 *
 * Behavior flags:
 *   --dir <path>                     → Override data directory (env: NOTIFY_TRIAGE_DIR)
 *   --force                          → Skip auto-rule creation; required for destructive ops
 *
 * Limits (hard caps, oldest dropped first on overflow):
 *   BATCH_MAX_ENTRIES    = 5000
 *   DROPPED_MAX_ENTRIES  = 1000
 *   DIGEST_MAX_ENTRIES   = 1000
 *
 * Atomic writes: every saveJSON uses a temp+rename pattern so a crash mid-write
 * cannot corrupt the JSON state files. Backups are NOT created — atomic rename
 * is sufficient because the rename is the only failure window.
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = (() => {
  if (process.env.NOTIFY_TRIAGE_DIR) return process.env.NOTIFY_TRIAGE_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'notification-triage');
const RULES_FILE = path.join(DATA_DIR, 'rules.json');
const SEEN_FILE = path.join(DATA_DIR, 'seen.json');
const BATCH_FILE = path.join(DATA_DIR, 'batch.json');
const DIGEST_FILE = path.join(DATA_DIR, 'digest.json');
const DROPPED_FILE = path.join(DATA_DIR, 'dropped.json');

// Hard caps to prevent unbounded growth from runaway classification
const BATCH_MAX_ENTRIES = 5000;
const DROPPED_MAX_ENTRIES = 1000;
const DIGEST_MAX_ENTRIES = 1000;

// Urgency levels
const LEVELS = { urgent: 3, batch: 2, ignore: 1 };

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// Atomic write: write to a temp file in the same directory, then rename.
// Rename within a single filesystem is atomic on POSIX, so a crash mid-write
// cannot leave a half-written JSON file behind.
function atomicWriteJSON(file, data) {
  ensureDir(path.dirname(file));
  const tmp = file + '.tmp.' + process.pid + '.' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
  fs.renameSync(tmp, file);
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  atomicWriteJSON(file, data);
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

// ─── CLASSIFY ──────────────────────────────────────────────────────────────

function classifyMessage(message, source, options = {}) {
  const { skipAutoRule = false } = options;
  const rules = loadRules();
  const msgLower = message.toLowerCase();
  
  // Check source-specific rules first
  if (rules[source]) {
    return { source, level: rules[source], rule: rules[source] };
  }
  
  // Keyword-based classification
  const urgentKeywords = ['urgent', 'critical', 'security', 'alert', 'error', 'fail', 'crash', 'down', 'breach', 'leak', 'hack', 'attack', 'payment', 'billing', 'deadline', 'immediate', 'asap', 'emergency', 'outage', 'incident'];
  const batchKeywords = ['update', 'summary', 'report', 'digest', 'newsletter', 'weekly', 'monthly', 'reminder', 'scheduled', 'notification'];
  
  let score = 0;
  for (const kw of urgentKeywords) {
    if (msgLower.includes(kw)) score += 2;
  }
  for (const kw of batchKeywords) {
    if (msgLower.includes(kw)) score -= 1;
  }
  
  // Check for time-sensitive content
  const timePatterns = ['today', 'tomorrow', 'now', 'immediately', 'before', 'by end', 'due', 'expires', 'final', 'last chance'];
  for (const tp of timePatterns) {
    if (msgLower.includes(tp)) score += 1;
  }
  
  // Determine level
  let level;
  if (score >= 3) level = 'urgent';
  else if (score >= 1) level = 'batch';
  else level = 'ignore';
  
  // Default rule for this source (unless --force is set, in which case the
  // classification is a one-off probe and no rule is persisted).
  if (!rules[source] && !skipAutoRule) {
    rules[source] = level;
    saveRules(rules);
  }
  
  return { source, level, rule: 'auto', score };
}

// ─── BATCH ─────────────────────────────────────────────────────────────────

function addNotification(id, message, source, level) {
  ensureDir(DATA_DIR);
  
  if (level === 'ignore') {
    console.log(`[notify-triage] Ignored: ${source}`);
    logDropped(source, message);
    return;
  }
  
  const batch = loadBatch();
  const now = new Date().toISOString();
  
  batch.push({
    id,
    source,
    message: message.substring(0, 500),
    level,
    timestamp: now,
    seen: false
  });
  
  // Enforce hard cap — drop oldest entries (preferring seen=true) if we exceed the limit
  if (batch.length > BATCH_MAX_ENTRIES) {
    const overflow = batch.length - BATCH_MAX_ENTRIES;
    // Drop seen first, then oldest unseen
    batch.sort((a, b) => {
      if (a.seen !== b.seen) return a.seen ? -1 : 1;
      return new Date(a.timestamp) - new Date(b.timestamp);
    });
    batch.splice(0, overflow);
    console.log(`[notify-triage] WARN: batch exceeded ${BATCH_MAX_ENTRIES} entries, dropped ${overflow} oldest`);
  }
  
  saveBatch(batch);
  console.log(`[notify-triage] Queued (${level}): ${source}`);
}

function getBatched(count = null) {
  const batch = loadBatch();
  const pending = batch.filter(n => !n.seen);
  
  if (count) {
    return pending.slice(0, count);
  }
  return pending;
}

function flushBatch(count = null) {
  const batch = loadBatch();
  const pending = batch.filter(n => !n.seen);
  const toFlush = count ? pending.slice(0, count) : pending;
  
  for (const n of toFlush) {
    n.seen = true;
    console.log(`[${n.level.toUpperCase()}] ${n.source}: ${n.message}`);
  }
  
  saveBatch(batch);
  console.log(`[notify-triage] Flushed ${toFlush.length} notifications`);
  return toFlush;
}

// ─── SEEN ──────────────────────────────────────────────────────────────────

function markSeen(id) {
  const batch = loadBatch();
  const found = batch.find(n => n.id === id);
  if (found) {
    found.seen = true;
    saveBatch(batch);
    const seenEntries = batch.filter(n => n.seen).map(n => ({ id: n.id, source: n.source, timestamp: n.timestamp }));
    atomicWriteJSON(SEEN_FILE, seenEntries);
    console.log(`[notify-triage] Marked as seen: ${found.source}`);
  } else {
    console.log(`[notify-triage] Not found: ${id}`);
  }
}

function markAllSeen() {
  const batch = loadBatch();
  let count = 0;
  for (const n of batch) {
    if (!n.seen) {
      n.seen = true;
      count++;
    }
  }
  saveBatch(batch);
  const seenEntries = batch.filter(n => n.seen).map(n => ({ id: n.id, source: n.source, timestamp: n.timestamp }));
  atomicWriteJSON(SEEN_FILE, seenEntries);
  console.log(`[notify-triage] Marked ${count} notifications as seen`);
}

// ─── DROPPED LOG ───────────────────────────────────────────────────────────

function logDropped(source, message) {
  const dropped = loadJSON(DROPPED_FILE, []);
  dropped.push({ source, message: message.substring(0, 200), timestamp: new Date().toISOString() });
  if (dropped.length > DROPPED_MAX_ENTRIES) dropped.splice(0, dropped.length - DROPPED_MAX_ENTRIES);
  atomicWriteJSON(DROPPED_FILE, dropped);
}

// ─── RULES ─────────────────────────────────────────────────────────────────

function loadRules() {
  return loadJSON(RULES_FILE, {});
}

function saveRules(rules) {
  ensureDir(path.dirname(RULES_FILE));
  atomicWriteJSON(RULES_FILE, rules);
}

function listRules() {
  const rules = loadRules();
  console.log('[notify-triage] Current rules:');
  for (const [source, level] of Object.entries(rules)) {
    console.log(`  ${source}: ${level}`);
  }
  if (Object.keys(rules).length === 0) {
    console.log('  (none — auto-classification active)');
  }
}

function addRule(source, level) {
  const rules = loadRules();
  if (!['urgent', 'batch', 'ignore'].includes(level)) {
    console.log('[notify-triage] Level must be: urgent, batch, or ignore');
    return;
  }
  rules[source] = level;
  saveRules(rules);
  console.log(`[notify-triage] Rule added: ${source} → ${level}`);
}

function removeRule(source) {
  const rules = loadRules();
  if (rules[source]) {
    delete rules[source];
    saveRules(rules);
    console.log(`[notify-triage] Rule removed: ${source}`);
  } else {
    console.log(`[notify-triage] No rule for: ${source}`);
  }
}

function clearAllRules() {
  saveRules({});
  console.log('[notify-triage] All rules cleared');
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function loadBatch() {
  return loadJSON(BATCH_FILE, []);
}

function saveBatch(batch) {
  atomicWriteJSON(BATCH_FILE, batch);
}

function showStatus() {
  const batch = loadBatch();
  const seen = loadJSON(SEEN_FILE, {});
  const rules = loadRules();
  
  const pending = batch.filter(n => !n.seen);
  const total = batch.length;
  
  console.log('[notify-triage] Status:');
  console.log(`  Pending: ${pending.length}`);
  console.log(`  Total processed: ${total}`);
  console.log(`  Rules configured: ${Object.keys(rules).length}`);
  console.log(`  Seen count: ${Object.keys(seen).length}`);
  console.log(`  Urgent pending: ${pending.filter(n => n.level === 'urgent').length}`);
  console.log(`  Batch pending: ${pending.filter(n => n.level === 'batch').length}`);
  console.log(`  Limits: batch≤${BATCH_MAX_ENTRIES}, dropped≤${DROPPED_MAX_ENTRIES}, digest≤${DIGEST_MAX_ENTRIES}`);
}

// ─── DIGEST MODE ───────────────────────────────────────────────────────────

function loadDigest() {
  return loadJSON(DIGEST_FILE, { entries: [], lastDigest: null });
}

function saveDigest(digest) {
  // Cap at DIGEST_MAX_ENTRIES
  if (digest.entries.length > DIGEST_MAX_ENTRIES) digest.entries = digest.entries.slice(-DIGEST_MAX_ENTRIES);
  atomicWriteJSON(DIGEST_FILE, digest);
}

function generateDigest(period = 'daily') {
  const digest = loadDigest();
  if (digest.entries.length === 0) {
    console.log('[notify-triage] No notifications to digest.');
    return;
  }
  
  // Group by source
  const bySource = {};
  for (const entry of digest.entries) {
    if (!bySource[entry.source]) bySource[entry.source] = [];
    bySource[entry.source].push(entry);
  }
  
  const dateStr = new Date().toISOString().split('T')[0];
  const icon = period === 'daily' ? '📬' : '📬';
  console.log(`${icon} ${period.charAt(0).toUpperCase() + period.slice(1)} Digest — ${dateStr}`);
  console.log('━'.repeat(40));
  
  let total = 0;
  for (const [source, entries] of Object.entries(bySource)) {
    console.log(`\n${source} (${entries.length} notifications)`);
    for (const e of entries.slice(-5)) {
      const time = new Date(e.timestamp).toLocaleTimeString();
      console.log(`  ${time} [${e.level}] ${e.message.substring(0, 80)}`);
    }
    if (entries.length > 5) console.log(`  ... and ${entries.length - 5} more`);
    total += entries.length;
  }
  
  console.log(`\n${'━'.repeat(40)}`);
  console.log(`📊 ${total} notifications batched`);
  
  // Clear digest store (not the batch queue — see SKILL.md "Digest Mode" section)
  saveDigest({ entries: [], lastDigest: new Date().toISOString() });
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let mode = 'status';
let rootDir = null, force = false;
let digestPeriod = 'daily';
let modeArgIndex = -1;

// First pass: identify mode (and the index of the mode arg) + collect flags
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--dir' && i + 1 < args.length) { rootDir = args[i + 1]; continue; }
  if (args[i] === '--force') { force = true; continue; }
  if (['--classify', '--batch', '--seen', '--rules', '--status', '--send', '--digest'].includes(args[i])) {
    mode = args[i].slice(2);
    if (mode === 'send') mode = 'flush';
    modeArgIndex = i;
  }
}

// After the mode is identified, collect positional args (anything that isn't
// a known flag and comes AFTER the mode arg). This lets `--force` appear in
// any position.
const positional = [];
if (modeArgIndex >= 0) {
  for (let i = modeArgIndex + 1; i < args.length; i++) {
    if (args[i] === '--force' || args[i] === '--all') continue; // already handled
    if (args[i].startsWith('--')) continue; // other flags
    positional.push(args[i]);
  }
}

(async () => {
switch (mode) {
  case 'classify': {
    const message = positional[0];
    const source = positional[1];
    if (!message || !source) {
      console.log('Usage: notification-triage.js --classify <message> <source> [--force]');
    } else {
      const result = classifyMessage(message, source, { skipAutoRule: force });
      addNotification(getToday() + '-' + Date.now(), message, source, result.level);
      console.log(`[notify-triage] Classified: ${result.level} (score: ${result.score || 'N/A'})${force ? ' [no auto-rule saved]' : ''}`);
    }
    break;
  }
  case 'batch': {
    const count = parseInt(positional[0]);
    if (isNaN(count)) {
      const pending = getBatched();
      console.log(`[notify-triage] ${pending.length} pending notifications:`);
      for (const n of pending) {
        console.log(`  [${n.level}] ${n.source}: ${n.message.substring(0, 80)}...`);
      }
    } else {
      getBatched(count).forEach(n => {
        console.log(`[${n.level}] ${n.source}: ${n.message.substring(0, 120)}`);
      });
    }
    break;
  }
  case 'flush': {
    const count = parseInt(positional[0]);
    flushBatch(isNaN(count) ? null : count);
    return;
  }
  case 'seen': {
    if (positional[0] === '--all' || args.includes('--all')) {
      markAllSeen();
    } else {
      markSeen(positional[0]);
    }
    break;
  }
  case 'rules': {
    if (positional[0] === 'add' && positional[1] && positional[2]) {
      addRule(positional[1], positional[2]);
    } else if (positional[0] === 'remove' && positional[1]) {
      removeRule(positional[1]);
    } else if (positional[0] === 'clear') {
      clearAllRules();
    } else {
      listRules();
    }
    break;
  }
  case 'digest': {
    generateDigest(positional[0] || 'daily');
    break;
  }
  default:
    showStatus();
    break;
}
})();
