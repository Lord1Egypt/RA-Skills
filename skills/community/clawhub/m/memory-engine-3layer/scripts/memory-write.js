#!/usr/bin/env node
/**
 * memory-write.js v6.0.0 — Write daily logs + MEMORY.md + USER.md + health check
 * 
 * v6.0: MEMORY.md soft cap (5000 chars), USER.md auto-update (1500 chars),
 *       capacity warnings, snapshot before compaction
 * 
 * Usage:
 *   node memory-write.js --today "event description" [--tag decision]
 *   node memory-write.js --core "durable fact" [--section projects]
 *   node memory-write.js --user "prefers concise answers"
 *   node memory-write.js --snapshot                    # snapshot MEMORY.md before compaction
 *   node memory-write.js --status
 */
const fs = require('fs'), path = require('path');
const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');

const args = process.argv.slice(2);
let workspace = DEFAULT_WORKSPACE, todayText = '', coreText = '', userText = '', tag = '', section = '', showStatus = false, doSnapshot = false;
// Capacity limits (inspired by Hermes Agent but more generous)
const CORE_SOFT_CAP = 5000;   // MEMORY.md soft limit (chars) — warn at 80%, block at 100%
const USER_SOFT_CAP = 1500;   // USER.md soft limit (chars)
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) { workspace = args[++i]; continue; }
  if (args[i] === '--today' && args[i + 1]) { todayText = args[++i]; continue; }
  if (args[i] === '--core' && args[i + 1]) { coreText = args[++i]; continue; }
  if (args[i] === '--user' && args[i + 1]) { userText = args[++i]; continue; }
  if (args[i] === '--tag' && args[i + 1]) { tag = args[++i]; continue; }
  if (args[i] === '--section' && args[i + 1]) { section = args[++i]; continue; }
  if (args[i] === '--status') { showStatus = true; continue; }
  if (args[i] === '--snapshot') { doSnapshot = true; continue; }
}

const MEMORY_DIR = path.join(workspace, 'memory');
const MEMORY_MD = path.join(workspace, 'MEMORY.md');
function ensureDir(dir) { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); }
const { getToday: _getToday, getTime: _getTime } = require('./_timezone');
function getToday() { return _getToday(workspace); }
function getTime() { return _getTime(workspace); }

// File lock using .lock file with retry
function withLock(filePath, fn) {
  const lockPath = filePath + '.lock';
  const maxRetries = 10, retryMs = 50;
  for (let i = 0; i < maxRetries; i++) {
    try {
      fs.writeFileSync(lockPath, String(process.pid), { flag: 'wx' });
      try { return fn(); } finally { try { fs.unlinkSync(lockPath); } catch(e) {} }
    } catch (e) {
      if (e.code === 'EEXIST') {
        // Check if lock is stale (>5s old)
        try { const s = fs.statSync(lockPath); if (Date.now() - s.mtimeMs > 5000) { fs.unlinkSync(lockPath); continue; } }
        catch(e2) { continue; }
        const jitter = Math.random() * retryMs;
        require('child_process').execSync(`sleep ${(retryMs + jitter) / 1000}`);
      } else throw e;
    }
  }
  // Fallback: just run without lock
  return fn();
}

function simpleNormalize(s) {
  return s.toLowerCase().replace(/[^\w\u4e00-\u9fff]/g, '').trim();
}

function isDuplicate(existing, newText) {
  // Check last 5 entries for >80% similarity
  const lines = existing.split('\n').filter(l => l.match(/^- \d{2}:\d{2}/)).slice(-5);
  const normNew = simpleNormalize(newText);
  if (normNew.length < 5) return false; // too short to deduplicate
  for (const line of lines) {
    const m = line.match(/^- \d{2}:\d{2}\s*(?:\[[^\]]+\])?\s*(.+)/);
    if (!m) continue;
    const normOld = simpleNormalize(m[1]);
    // Exact match after normalization
    if (normOld === normNew) return true;
    // One contains the other (>80% overlap)
    if (normOld.length > 15 && normNew.length > 15) {
      if (normOld.includes(normNew) || normNew.includes(normOld)) return true;
    }
  }
  return false;
}

function writeToday(text, tag) {
  ensureDir(MEMORY_DIR);
  const today = getToday(), fp = path.join(MEMORY_DIR, `${today}.md`), time = getTime(), tagStr = tag ? ` [${tag}]` : '';
  const result = withLock(fp, () => {
    let content = fs.existsSync(fp) ? fs.readFileSync(fp, 'utf8') : `# ${today} Daily Log\n\n`;
    // Dedup check: skip if very similar to recent entries
    if (isDuplicate(content, text)) {
      return { len: content.length, skipped: true };
    }
    content += `- ${time}${tagStr} ${text}\n`;
    fs.writeFileSync(fp, content, 'utf8');
    return { len: content.length, skipped: false };
  });
  if (result.skipped) {
    console.log(JSON.stringify({ status: 'ok', action: 'skipped_duplicate', file: `memory/${today}.md`, chars: result.len, note: 'Similar entry exists in last 5 entries' }));
  } else {
    console.log(JSON.stringify({ status: 'ok', action: 'append_daily', file: `memory/${today}.md`, chars: result.len }));
  }
}

function writeCore(text, section) {
  const today = getToday();
  const result = withLock(MEMORY_MD, () => {
    let content = fs.existsSync(MEMORY_MD)
      ? fs.readFileSync(MEMORY_MD, 'utf8')
      : `# Long-Term Memory\n\n_Auto-created ${today}. Curated knowledge that persists across sessions._\n\n`;
    
    const newEntry = `- ${text} _(${today})_\n`;
    const projectedLen = content.length + newEntry.length + 5;
    
    // Capacity check
    if (projectedLen > CORE_SOFT_CAP) {
      const usage = Math.round((content.length / CORE_SOFT_CAP) * 100);
      return { 
        len: content.length, 
        blocked: true, 
        usage,
        message: `MEMORY.md at ${usage}% (${content.length}/${CORE_SOFT_CAP} chars). Adding ${newEntry.length} chars would exceed limit. Run: node memory-maintain.js --gc --apply to consolidate, or manually trim old entries.`
      };
    }
    
    if (section) {
      const hdr = `## ${section.charAt(0).toUpperCase() + section.slice(1)}`;
      const idx = content.indexOf(hdr);
      if (idx >= 0) {
        const after = content.indexOf('\n', idx);
        const next = content.indexOf('\n## ', after);
        const at = next >= 0 ? next : content.length;
        content = content.slice(0, at) + `\n` + newEntry + content.slice(at);
      } else {
        content += `\n${hdr}\n\n` + newEntry;
      }
    } else {
      content += `\n` + newEntry;
    }
    fs.writeFileSync(MEMORY_MD, content, 'utf8');
    const usage = Math.round((content.length / CORE_SOFT_CAP) * 100);
    return { len: content.length, blocked: false, usage };
  });
  
  if (result.blocked) {
    console.log(JSON.stringify({ status: 'warning', action: 'blocked_capacity', file: 'MEMORY.md', chars: result.len, usage: `${result.usage}%`, cap: CORE_SOFT_CAP, message: result.message }));
  } else {
    const output = { status: 'ok', action: 'append_core', file: 'MEMORY.md', section: section || 'root', chars: result.len, usage: `${result.usage}%` };
    if (result.usage >= 80) output.warning = `MEMORY.md at ${result.usage}% capacity — consider consolidating soon`;
    console.log(JSON.stringify(output));
  }
}

function writeUser(text) {
  const today = getToday();
  const USER_MD = path.join(workspace, 'USER.md');
  const result = withLock(USER_MD, () => {
    let content = fs.existsSync(USER_MD)
      ? fs.readFileSync(USER_MD, 'utf8')
      : `# USER.md - About Your Human\n\n`;
    
    const newEntry = `- ${text} _(${today})_\n`;
    const projectedLen = content.length + newEntry.length;
    
    if (projectedLen > USER_SOFT_CAP) {
      return { len: content.length, blocked: true, usage: Math.round((content.length / USER_SOFT_CAP) * 100) };
    }
    
    // Append to Context section (create if missing)
    const ctxHdr = '## Context';
    const idx = content.indexOf(ctxHdr);
    if (idx >= 0) {
      const after = content.indexOf('\n', idx);
      const next = content.indexOf('\n## ', after);
      const at = next >= 0 ? next : content.length;
      content = content.slice(0, at) + `\n` + newEntry + content.slice(at);
    } else {
      content += `\n${ctxHdr}\n\n` + newEntry;
    }
    fs.writeFileSync(USER_MD, content, 'utf8');
    return { len: content.length, blocked: false, usage: Math.round((content.length / USER_SOFT_CAP) * 100) };
  });
  
  if (result.blocked) {
    console.log(JSON.stringify({ status: 'warning', action: 'blocked_capacity', file: 'USER.md', chars: result.len, usage: `${result.usage}%`, cap: USER_SOFT_CAP }));
  } else {
    console.log(JSON.stringify({ status: 'ok', action: 'append_user', file: 'USER.md', chars: result.len, usage: `${result.usage}%` }));
  }
}

function snapshotCore() {
  if (!fs.existsSync(MEMORY_MD)) { console.log(JSON.stringify({ status: 'ok', action: 'snapshot_skipped', reason: 'no MEMORY.md' })); return; }
  const snapshotDir = path.join(workspace, 'memory', 'snapshots');
  ensureDir(snapshotDir);
  const today = getToday();
  const time = getTime().replace(':', '');
  const dest = path.join(snapshotDir, `MEMORY-${today}-${time}.md`);
  fs.copyFileSync(MEMORY_MD, dest);
  // Keep only last 10 snapshots
  const snaps = fs.readdirSync(snapshotDir).filter(f => f.startsWith('MEMORY-')).sort().reverse();
  for (const old of snaps.slice(10)) { try { fs.unlinkSync(path.join(snapshotDir, old)); } catch(e) {} }
  console.log(JSON.stringify({ status: 'ok', action: 'snapshot', file: dest, kept: Math.min(snaps.length, 10) }));
}

function healthCheck() {
  ensureDir(MEMORY_DIR);
  const today = getToday(), todayDate = new Date(today);
  const files = fs.readdirSync(MEMORY_DIR).filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/)).sort();
  const hasCore = fs.existsSync(MEMORY_MD), hasTodayLog = files.includes(`${today}.md`);
  const gaps = [];
  // Only count gaps since the earliest daily log (don't penalize days before system existed)
  const earliest = files.length > 0 ? files[0].replace('.md', '') : today;
  for (let i = 1; i < 14; i++) {
    const d = new Date(todayDate); d.setDate(d.getDate() - i);
    const ds = d.toISOString().slice(0, 10);
    if (ds < earliest) break; // don't count before system existed
    if (!files.includes(`${ds}.md`)) gaps.push(ds);
  }
  const totalChars = files.reduce((s, f) => s + fs.statSync(path.join(MEMORY_DIR, f)).size, 0);
  const coreChars = hasCore ? fs.statSync(MEMORY_MD).size : 0;
  const coreUsage = Math.round((coreChars / CORE_SOFT_CAP) * 100);
  const USER_MD = path.join(workspace, 'USER.md');
  const userChars = fs.existsSync(USER_MD) ? fs.statSync(USER_MD).size : 0;
  const userUsage = Math.round((userChars / USER_SOFT_CAP) * 100);
  const score = Math.max(0, 100 - gaps.length * 7 - (hasCore ? 0 : 20) - (hasTodayLog ? 0 : 15));
  const warnings = [];
  if (!hasCore) warnings.push('MEMORY.md missing — no long-term memory');
  if (!hasTodayLog) warnings.push(`No log for today (${today}) — session will be forgotten`);
  if (gaps.length > 3) warnings.push(`${gaps.length} gaps in last 14 days`);
  if (coreUsage >= 90) warnings.push(`MEMORY.md at ${coreUsage}% capacity (${coreChars}/${CORE_SOFT_CAP}) — consolidate now!`);
  else if (coreUsage >= 80) warnings.push(`MEMORY.md at ${coreUsage}% capacity — consider consolidating`);
  if (userUsage >= 90) warnings.push(`USER.md at ${userUsage}% capacity (${userChars}/${USER_SOFT_CAP})`);
  // Check snapshot count
  const snapDir = path.join(workspace, 'memory', 'snapshots');
  const snapCount = fs.existsSync(snapDir) ? fs.readdirSync(snapDir).filter(f => f.startsWith('MEMORY-')).length : 0;
  console.log(JSON.stringify({ status: 'ok', today, hasTodayLog, hasCoreMemory: hasCore, dailyFiles: files.length, totalDailyChars: totalChars, coreMemory: { chars: coreChars, cap: CORE_SOFT_CAP, usage: `${coreUsage}%` }, userProfile: { chars: userChars, cap: USER_SOFT_CAP, usage: `${userUsage}%` }, snapshots: snapCount, gapCount: gaps.length, healthScore: score, warnings }, null, 2));
}

function autoReindex() {
  const indexScript = path.join(__dirname, 'memory-index.js');
  if (fs.existsSync(indexScript)) {
    try { require('child_process').execSync(`node "${indexScript}" --workspace "${workspace}"`, { stdio: 'pipe' }); }
    catch (e) { /* index failure is non-fatal */ }
  }
}

if (showStatus) { healthCheck(); }
else if (doSnapshot) { snapshotCore(); }
else if (!todayText && !coreText && !userText) { console.error('Usage:\n  --today "text" [--tag t]  Append daily log\n  --core "text" [--section s]  Append MEMORY.md\n  --user "text"  Append USER.md\n  --snapshot  Snapshot MEMORY.md\n  --status  Health check'); process.exit(1); }
else { if (todayText) writeToday(todayText, tag); if (coreText) writeCore(coreText, section); if (userText) writeUser(userText); autoReindex(); }
