#!/usr/bin/env node
/**
 * memory-compact.js — Compress old daily logs into summaries
 * No AI needed — extracts headings + bullet points as summary.
 *
 * Usage:
 *   node memory-compact.js --older-than 30     # compact files >30 days old
 *   node memory-compact.js --older-than 30 --dry-run  # preview without writing
 *   node memory-compact.js --stats             # show compaction candidates
 */
const fs = require('fs'), path = require('path');
const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');

const args = process.argv.slice(2);
let workspace = DEFAULT_WORKSPACE, olderThan = 0, dryRun = false, showStats = false;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) { workspace = args[++i]; continue; }
  if (args[i] === '--older-than' && args[i + 1]) { olderThan = parseInt(args[++i]); continue; }
  if (args[i] === '--dry-run') { dryRun = true; continue; }
  if (args[i] === '--stats') { showStats = true; continue; }
}

const MEMORY_DIR = path.join(workspace, 'memory');
const ARCHIVE_DIR = path.join(workspace, 'memory', 'archive');

function getDailyFiles() {
  if (!fs.existsSync(MEMORY_DIR)) return [];
  return fs.readdirSync(MEMORY_DIR)
    .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
    .sort();
}

const { getToday: _getToday } = require('./_timezone');
function fileAgeDays(filename) {
  const dateStr = filename.replace('.md', '');
  const today = _getToday(workspace);
  return (new Date(today + 'T00:00:00').getTime() - new Date(dateStr + 'T00:00:00').getTime()) / 86400000;
}

function extractSummary(content, filename) {
  const lines = content.split('\n');
  const summary = [];
  const date = filename.replace('.md', '');

  // Extract: title, headings, bullet items with ✅/🎉/🔴/关键/重要
  for (const line of lines) {
    const trimmed = line.trim();
    // Keep headings
    if (/^#{1,3}\s/.test(trimmed)) {
      summary.push(trimmed);
      continue;
    }
    // Keep important bullets (completed tasks, key items, warnings)
    if (/^[-*]\s/.test(trimmed) && (
      /[✅🎉🔴❌⚠️]/.test(trimmed) ||
      /\b(完成|修复|创建|部署|发布|决策|重要|关键|milestone|done|fix|deploy|publish)\b/i.test(trimmed)
    )) {
      summary.push(trimmed);
      continue;
    }
    // Keep status lines
    if (/^(\*\*)?状态|status|结果|result/i.test(trimmed)) {
      summary.push(trimmed);
    }
  }

  // If summary is too short, just take first 5 bullet points
  if (summary.length < 3) {
    const bullets = lines.filter(l => /^[-*]\s/.test(l.trim())).slice(0, 5);
    return `# ${date} (compacted)\n\n${bullets.join('\n')}`;
  }

  return `# ${date} (compacted)\n\n${summary.join('\n')}`;
}

function main() {
  const files = getDailyFiles();

  if (showStats || !olderThan) {
    const candidates = files.filter(f => fileAgeDays(f) > (olderThan || 30));
    const recent = files.filter(f => fileAgeDays(f) <= (olderThan || 30));
    const totalSize = files.reduce((s, f) => s + fs.statSync(path.join(MEMORY_DIR, f)).size, 0);
    const candidateSize = candidates.reduce((s, f) => s + fs.statSync(path.join(MEMORY_DIR, f)).size, 0);

    console.log(JSON.stringify({
      status: 'ok',
      totalFiles: files.length,
      totalSizeKB: Math.round(totalSize / 1024),
      compactCandidates: candidates.length,
      candidateSizeKB: Math.round(candidateSize / 1024),
      recentFiles: recent.length,
      threshold: olderThan || 30,
      candidates: candidates.map(f => ({
        file: f,
        age: Math.round(fileAgeDays(f)),
        sizeKB: Math.round(fs.statSync(path.join(MEMORY_DIR, f)).size / 1024)
      }))
    }, null, 2));
    if (showStats) return;
  }

  if (!olderThan) {
    console.error('Usage: memory-compact.js --older-than <days> [--dry-run]');
    process.exit(1);
  }

  const candidates = files.filter(f => fileAgeDays(f) > olderThan);
  if (!candidates.length) {
    console.log(JSON.stringify({ status: 'ok', message: `No files older than ${olderThan} days`, compacted: 0 }));
    return;
  }

  if (!dryRun) {
    if (!fs.existsSync(ARCHIVE_DIR)) fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }

  let compacted = 0, savedBytes = 0;
  for (const file of candidates) {
    const fullPath = path.join(MEMORY_DIR, file);
    const content = fs.readFileSync(fullPath, 'utf8');
    const originalSize = content.length;
    const summary = extractSummary(content, file);
    const savings = originalSize - summary.length;

    if (dryRun) {
      console.log(`[dry-run] ${file}: ${originalSize} → ${summary.length} chars (save ${savings})`);
      console.log(summary.slice(0, 200) + (summary.length > 200 ? '…' : ''));
      console.log('---');
    } else {
      // Archive original (skip if already compacted)
      const content_header = content.slice(0, 50);
      if (content_header.includes('(compacted)')) { continue; } // already compacted
      const archivePath = path.join(ARCHIVE_DIR, file);
      if (!fs.existsSync(archivePath)) { fs.copyFileSync(fullPath, archivePath); }
      // Replace with summary
      fs.writeFileSync(fullPath, summary, 'utf8');
      compacted++;
      savedBytes += savings;
    }
  }

  if (!dryRun) {
    // Reindex after compaction
    const indexScript = path.join(__dirname, 'memory-index.js');
    if (fs.existsSync(indexScript)) {
      try { require('child_process').execSync(`node "${indexScript}" --workspace "${workspace}" --force`, { stdio: 'pipe' }); }
      catch (e) { /* non-fatal */ }
    }
    console.log(JSON.stringify({
      status: 'ok',
      compacted,
      savedKB: Math.round(savedBytes / 1024),
      archiveDir: 'memory/archive/',
      message: `Compacted ${compacted} files. Originals saved to memory/archive/`
    }));
  }
}
main();
