#!/usr/bin/env node
/**
 * memory-maintain.js v3.0.0 — Index stats, rebuild, prune, GC, and capacity management
 * 
 * v3.0: Auto-consolidation when MEMORY.md exceeds soft cap (5000 chars),
 *       snapshot before destructive GC, improved stale detection
 * 
 * Usage:
 *   node memory-maintain.js [--stats] [--reindex] [--prune-days 90]
 *   node memory-maintain.js --gc                # Analyze MEMORY.md for stale entries
 *   node memory-maintain.js --gc --apply        # Actually remove stale entries
 *   node memory-maintain.js --consolidate       # Merge similar entries to reduce size
 */
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const GLOBAL_MODULES = execSync('npm root -g', { encoding: 'utf8' }).trim();
const Database = require(path.join(GLOBAL_MODULES, 'better-sqlite3'));
const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');

const args = process.argv.slice(2);
const CORE_SOFT_CAP = 5000;  // Must match memory-write.js
let workspace = DEFAULT_WORKSPACE, showStats = false, reindex = false, pruneDays = 0, gc = false, gcApply = false, consolidate = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) workspace = args[++i];
  if (args[i] === '--stats') showStats = true;
  if (args[i] === '--reindex') reindex = true;
  if (args[i] === '--prune-days' && args[i + 1]) pruneDays = parseInt(args[++i]);
  if (args[i] === '--gc') gc = true;
  if (args[i] === '--apply') gcApply = true;
  if (args[i] === '--consolidate') consolidate = true;
}

const DB_PATH = path.join(workspace, '.memory', 'index.sqlite');
const SCRIPT_DIR = __dirname;

if (reindex) {
  console.log('[maintain] Full reindex...');
  console.log(execSync(`node "${path.join(SCRIPT_DIR, 'memory-index.js')}" --workspace "${workspace}" --force`, { encoding: 'utf8' }));
  process.exit(0);
}

if (!fs.existsSync(DB_PATH)) {
  console.log('[maintain] No index. Building...');
  console.log(execSync(`node "${path.join(SCRIPT_DIR, 'memory-index.js')}" --workspace "${workspace}"`, { encoding: 'utf8' }));
  process.exit(0);
}

const db = new Database(DB_PATH);

if (showStats || !pruneDays) {
  const total = db.prepare('SELECT COUNT(*) as c FROM files').get().c;
  const chunks = db.prepare('SELECT COUNT(*) as c FROM chunks').get().c;
  const core = db.prepare('SELECT COUNT(*) as c FROM files WHERE is_core = 1').get().c;
  const oldest = db.prepare('SELECT MIN(date) as d FROM files WHERE date IS NOT NULL').get().d;
  const newest = db.prepare('SELECT MAX(date) as d FROM files WHERE date IS NOT NULL').get().d;
  const memDir = path.join(workspace, 'memory');
  let disk = fs.existsSync(memDir) ? fs.readdirSync(memDir).filter(f => f.endsWith('.md')).length : 0;
  if (fs.existsSync(path.join(workspace, 'MEMORY.md'))) disk++;
  console.log(JSON.stringify({ status: 'ok', files: { total, core, daily: total - core, onDisk: disk }, chunks, dateRange: oldest && newest ? `${oldest} → ${newest}` : 'none', dbSizeKB: Math.round(fs.statSync(DB_PATH).size / 1024), needsSync: disk > total }));
}

// ── GC: analyze MEMORY.md for stale entries ──
if (gc) {
  const MEMORY_MD = path.join(workspace, 'MEMORY.md');
  if (!fs.existsSync(MEMORY_MD)) { console.log('[gc] No MEMORY.md found.'); process.exit(0); }
  const content = fs.readFileSync(MEMORY_MD, 'utf8');
  const lines = content.split('\n');
  
  // Detect stale patterns
  const stalePatterns = [
    // "当前版本" / "current version" entries older than 14 days
    { regex: /当前.*版本|current.*version|commit [a-f0-9]{7}/i, maxAgeDays: 14, reason: '版本信息可能过时' },
    // Completed TODOs still in memory
    { regex: /^\s*-\s*\[x\]/i, maxAgeDays: 0, reason: '已完成待办' },
    // Very old entries (>60 days)
    { regex: /_\((\d{4}-\d{2}-\d{2})\)_/, maxAgeDays: 60, reason: '超过60天的条目' },
  ];
  
  const { getToday: _gt } = require('./_timezone');
  const today = _gt(workspace);
  const todayMs = new Date(today + 'T00:00:00').getTime();
  
  const staleLines = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.match(/^- /)) continue; // Only check list entries
    
    for (const pat of stalePatterns) {
      if (pat.regex.test(line)) {
        // Extract date if present
        const dateMatch = line.match(/_\((\d{4}-\d{2}-\d{2})\)_/);
        if (dateMatch && pat.maxAgeDays > 0) {
          const entryMs = new Date(dateMatch[1] + 'T00:00:00').getTime();
          const ageDays = Math.floor((todayMs - entryMs) / 86400000);
          if (ageDays > pat.maxAgeDays) {
            staleLines.push({ lineNum: i + 1, text: line.trim(), reason: pat.reason, ageDays });
          }
        } else if (pat.maxAgeDays === 0) {
          staleLines.push({ lineNum: i + 1, text: line.trim(), reason: pat.reason, ageDays: 0 });
        }
      }
    }
  }

  // Detect duplicate entries (>80% similarity by simple char overlap)
  const listLines = lines.map((l, i) => ({ i, text: l })).filter(x => x.text.match(/^- /));
  for (let a = 0; a < listLines.length; a++) {
    for (let b = a + 1; b < listLines.length; b++) {
      const ta = listLines[a].text.replace(/\s*_\(\d{4}-\d{2}-\d{2}\)_\s*$/, '').toLowerCase();
      const tb = listLines[b].text.replace(/\s*_\(\d{4}-\d{2}-\d{2}\)_\s*$/, '').toLowerCase();
      if (ta === tb || (ta.length > 20 && tb.length > 20 && ta.includes(tb.slice(2, -2)))) {
        // b is the duplicate (later line), mark for removal
        if (!staleLines.find(s => s.lineNum === listLines[b].i + 1)) {
          staleLines.push({ lineNum: listLines[b].i + 1, text: listLines[b].text.trim(), reason: '重复条目', ageDays: 0 });
        }
      }
    }
  }

  if (staleLines.length === 0) {
    console.log(`[gc] MEMORY.md clean (${content.length} chars, ${listLines.length} entries). No stale entries.`);
  } else {
    console.log(`[gc] Found ${staleLines.length} potentially stale entries:`);
    for (const s of staleLines) {
      console.log(`  L${s.lineNum}: ${s.reason}${s.ageDays ? ` (${s.ageDays}d old)` : ''} → ${s.text.slice(0, 80)}`);
    }
    
    if (gcApply) {
      // Snapshot before destructive operation
      const snapshotDir = path.join(workspace, 'memory', 'snapshots');
      if (!fs.existsSync(snapshotDir)) fs.mkdirSync(snapshotDir, { recursive: true });
      const { getToday: _gt2, getTime: _gti2 } = require('./_timezone');
      const snapName = `MEMORY-${_gt2(workspace)}-pre-gc.md`;
      fs.copyFileSync(MEMORY_MD, path.join(snapshotDir, snapName));
      console.log(`[gc] Snapshot saved: memory/snapshots/${snapName}`);
      
      const removeSet = new Set(staleLines.map(s => s.lineNum - 1));
      const cleaned = lines.filter((_, i) => !removeSet.has(i)).join('\n');
      // Remove consecutive blank lines
      const tidied = cleaned.replace(/\n{3,}/g, '\n\n');
      fs.writeFileSync(MEMORY_MD, tidied, 'utf8');
      console.log(`[gc] Removed ${staleLines.length} entries. ${content.length} → ${tidied.length} chars (${Math.round(tidied.length/CORE_SOFT_CAP*100)}% cap).`);
    } else {
      console.log(`[gc] Run with --apply to remove. Preview only.`);
    }
  }
  process.exit(0);
}

// ── Consolidate: merge similar entries within same section ──
if (consolidate) {
  const MEMORY_MD = path.join(workspace, 'MEMORY.md');
  if (!fs.existsSync(MEMORY_MD)) { console.log('[consolidate] No MEMORY.md found.'); process.exit(0); }
  const content = fs.readFileSync(MEMORY_MD, 'utf8');
  const usage = Math.round((content.length / CORE_SOFT_CAP) * 100);
  
  console.log(`[consolidate] MEMORY.md: ${content.length} chars (${usage}% of ${CORE_SOFT_CAP} cap)`);
  
  if (usage < 70 && !gcApply) {
    console.log(`[consolidate] Under 70% capacity — no consolidation needed.`);
    process.exit(0);
  }
  
  // Parse sections and find entries that can be merged
  const lines = content.split('\n');
  const sections = [];
  let currentSection = { header: '', entries: [], headerIdx: -1 };
  
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].match(/^## /)) {
      if (currentSection.header) sections.push(currentSection);
      currentSection = { header: lines[i], entries: [], headerIdx: i };
    } else if (lines[i].match(/^- /)) {
      currentSection.entries.push({ idx: i, text: lines[i] });
    }
  }
  if (currentSection.header) sections.push(currentSection);
  
  // Find merge candidates: entries with same date suffix in same section
  let mergeGroups = 0;
  for (const sec of sections) {
    // Group by date
    const byDate = {};
    for (const e of sec.entries) {
      const dm = e.text.match(/_\((\d{4}-\d{2}-\d{2})\)_/);
      const date = dm ? dm[1] : 'undated';
      if (!byDate[date]) byDate[date] = [];
      byDate[date].push(e);
    }
    // Flag groups with 3+ entries on same date
    for (const [date, entries] of Object.entries(byDate)) {
      if (entries.length >= 3) mergeGroups++;
    }
  }
  
  console.log(`[consolidate] ${sections.length} sections, ${mergeGroups} potential merge groups.`);
  
  if (!gcApply) {
    for (const sec of sections) {
      const entryChars = sec.entries.reduce((s, e) => s + e.text.length, 0);
      console.log(`  ${sec.header}: ${sec.entries.length} entries, ${entryChars} chars`);
    }
    console.log(`[consolidate] Run with --apply to execute. Tip: manually review MEMORY.md and merge related entries for best results.`);
  } else {
    // Snapshot first
    const snapshotDir = path.join(workspace, 'memory', 'snapshots');
    if (!fs.existsSync(snapshotDir)) fs.mkdirSync(snapshotDir, { recursive: true });
    const { getToday: _gt3 } = require('./_timezone');
    const snapName = `MEMORY-${_gt3(workspace)}-pre-consolidate.md`;
    fs.copyFileSync(MEMORY_MD, path.join(snapshotDir, snapName));
    console.log(`[consolidate] Snapshot saved: memory/snapshots/${snapName}`);
    
    // Remove exact duplicate entries (safest auto-consolidation)
    const seen = new Set();
    const dupeLines = new Set();
    for (const sec of sections) {
      for (const e of sec.entries) {
        const norm = e.text.replace(/\s*_\(\d{4}-\d{2}-\d{2}\)_\s*$/, '').toLowerCase().trim();
        if (seen.has(norm)) {
          dupeLines.add(e.idx);
        } else {
          seen.add(norm);
        }
      }
    }
    
    if (dupeLines.size > 0) {
      const cleaned = lines.filter((_, i) => !dupeLines.has(i)).join('\n').replace(/\n{3,}/g, '\n\n');
      fs.writeFileSync(MEMORY_MD, cleaned, 'utf8');
      console.log(`[consolidate] Removed ${dupeLines.size} duplicates. ${content.length} → ${cleaned.length} chars (${Math.round(cleaned.length/CORE_SOFT_CAP*100)}% cap).`);
    } else {
      console.log(`[consolidate] No exact duplicates found. Manual consolidation recommended for further reduction.`);
    }
  }
  process.exit(0);
}

if (pruneDays > 0) {
  const cutoff = new Date(); cutoff.setDate(cutoff.getDate() - pruneDays);
  const old = db.prepare('SELECT id, path FROM files WHERE date IS NOT NULL AND date < ? AND is_core = 0').all(cutoff.toISOString().slice(0, 10));
  if (!old.length) { console.log(`[maintain] Nothing older than ${pruneDays} days.`); }
  else {
    const dc = db.prepare('DELETE FROM chunks WHERE file_id = ?'), df = db.prepare('DELETE FROM files WHERE id = ?');
    db.transaction(() => { for (const f of old) { dc.run(f.id); df.run(f.id); } })();
    console.log(`[maintain] Pruned ${old.length} file(s).`);
  }
}
db.close();
