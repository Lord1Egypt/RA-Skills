#!/usr/bin/env node
/**
 * memory-resume.js v1.0.0 — Zero-latency session recovery
 * Generates a <2000 token recovery summary after session reset.
 * 
 * Usage:
 *   node memory-resume.js [--workspace /path] [--max-chars 2000]
 * 
 * Output: compact recovery context for immediate session continuity
 *   1. Last session's final topic & status
 *   2. Recent 3 days' key entries (prioritized by tag)
 *   3. Active MEMORY.md sections
 */
const fs = require('fs'), path = require('path');

const DEFAULT_WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const args = process.argv.slice(2);
let workspace = DEFAULT_WORKSPACE, maxChars = 2000;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && args[i + 1]) workspace = args[++i];
  if (args[i] === '--max-chars' && args[i + 1]) maxChars = parseInt(args[++i]) || 2000;
}

const MEMORY_DIR = path.join(workspace, 'memory');
const MEMORY_MD = path.join(workspace, 'MEMORY.md');
const { getToday: _getToday } = require('./_timezone');
function getToday() { return _getToday(workspace); }

// Tag priority: higher = more important for recovery context
const TAG_PRIORITY = {
  'decision': 10, 'done': 9, 'blocked': 9, 'todo': 8, 'important': 10,
  'deploy': 8, 'error': 7, 'fix': 7, 'warning': 6, 'progress': 5,
  'note': 3, 'auto-extract': 4, 'flush': 4
};

function parseLogEntries(content) {
  const entries = [];
  for (const line of content.split('\n')) {
    const m = line.match(/^- (\d{2}:\d{2})\s*(?:\[([^\]]+)\])?\s*(.+)/);
    if (m) {
      const [, time, tag, text] = m;
      const priority = TAG_PRIORITY[tag] || 2;
      entries.push({ time, tag: tag || '', text: text.trim(), priority });
    }
  }
  return entries;
}

function getRecentLogs(days = 3) {
  if (!fs.existsSync(MEMORY_DIR)) return [];
  const today = getToday();
  const files = [];
  for (let i = 0; i < days; i++) {
    const d = new Date(today + 'T00:00:00');
    d.setDate(d.getDate() - i);
    const ds = d.toISOString().slice(0, 10);
    const fp = path.join(MEMORY_DIR, `${ds}.md`);
    if (fs.existsSync(fp)) {
      files.push({ date: ds, content: fs.readFileSync(fp, 'utf8') });
    }
  }
  return files;
}

function getActiveMemorySections() {
  if (!fs.existsSync(MEMORY_MD)) return '';
  const content = fs.readFileSync(MEMORY_MD, 'utf8');
  const lines = content.split('\n');
  
  // Extract section headers and their most recent entries
  const sections = [];
  let current = null;
  for (const line of lines) {
    if (line.match(/^## /)) {
      if (current) sections.push(current);
      current = { header: line.replace('## ', ''), entries: [] };
    } else if (current && line.match(/^- /)) {
      current.entries.push(line);
    }
  }
  if (current) sections.push(current);

  // Keep last 2 entries per section, skip empty sections
  return sections
    .filter(s => s.entries.length > 0)
    .map(s => `**${s.header}**: ${s.entries.slice(-2).map(e => e.replace(/^- /, '').replace(/\s*_\(\d{4}-\d{2}-\d{2}\)_\s*$/, '')).join(' | ')}`)
    .join('\n');
}

function checkAndExtractUnprocessedResets() {
  const sessDir = path.join(process.env.HOME, '.openclaw/agents/main/sessions');
  if (!fs.existsSync(sessDir)) return 0;
  
  const trackFile = path.join(workspace, '.memory', 'extracted-sessions.json');
  const tracked = fs.existsSync(trackFile) ? JSON.parse(fs.readFileSync(trackFile, 'utf8')) : {};
  
  const resetFiles = fs.readdirSync(sessDir).filter(f => f.includes('.reset.'));
  const unextracted = resetFiles.filter(f => !tracked[f]);
  
  if (unextracted.length === 0) return 0;
  
  console.error(`⚠️ ${unextracted.length} 个session未提取，正在恢复...`);
  
  // Try to use auto-extract for each
  const extractScript = path.join(__dirname, 'memory-auto-extract.js');
  if (fs.existsSync(extractScript)) {
    const { execSync } = require('child_process');
    for (const f of unextracted) {
      try {
        const fp = path.join(sessDir, f);
        execSync(`node "${extractScript}" --workspace "${workspace}" "${fp}"`, 
          { encoding: 'utf8', timeout: 30000, stdio: ['pipe', 'pipe', 'pipe'] });
        tracked[f] = { extractedAt: new Date().toISOString(), count: -1, source: 'resume' };
      } catch (e) {
        console.error(`  提取失败: ${f} — ${e.message.slice(0,80)}`);
      }
    }
    // Save tracking
    const memDir = path.join(workspace, '.memory');
    if (!fs.existsSync(memDir)) fs.mkdirSync(memDir, { recursive: true });
    fs.writeFileSync(trackFile, JSON.stringify(tracked, null, 2), 'utf8');
    
    // Reindex after extraction
    const indexScript = path.join(__dirname, 'memory-index.js');
    if (fs.existsSync(indexScript)) {
      try { execSync(`node "${indexScript}" --workspace "${workspace}"`, { timeout: 15000 }); } catch {}
    }
  }
  
  return unextracted.length;
}

function buildResumeSummary() {
  // P1: Check for unprocessed reset sessions FIRST, extract them before resuming
  const rescued = checkAndExtractUnprocessedResets();
  
  const recentLogs = getRecentLogs(3);
  
  if (recentLogs.length === 0 && !fs.existsSync(MEMORY_MD)) {
    console.log('[resume] No memory data found. Fresh start.');
    return;
  }

  let output = '## Session Recovery\n\n';
  if (rescued > 0) {
    output += `⚠️ 恢复了 ${rescued} 个未提取的session记忆\n\n`;
  }
  let charBudget = maxChars - output.length;

  // 1. Last session entries (most recent day, sorted by priority)
  if (recentLogs.length > 0) {
    const latest = recentLogs[0];
    const entries = parseLogEntries(latest.content);
    
    // Sort by priority desc, then by time desc (latest first)
    entries.sort((a, b) => b.priority - a.priority || b.time.localeCompare(a.time));
    
    // Last entry = most recent activity
    const lastEntry = entries.length > 0
      ? entries.reduce((a, b) => a.time > b.time ? a : b)
      : null;

    output += `**最后活动** (${latest.date}):\n`;
    if (lastEntry) {
      output += `> ${lastEntry.time} ${lastEntry.tag ? `[${lastEntry.tag}]` : ''} ${lastEntry.text}\n\n`;
    }

    // Top priority entries from today
    const topEntries = entries
      .filter(e => e.priority >= 5)
      .slice(0, 8);
    
    if (topEntries.length > 0) {
      output += `**关键记录** (${latest.date}):\n`;
      for (const e of topEntries) {
        const line = `- ${e.time} ${e.tag ? `[${e.tag}]` : ''} ${e.text}\n`;
        if (output.length + line.length > charBudget * 0.6) break;
        output += line;
      }
      output += '\n';
    }
  }

  // 2. Previous days' highlights (if budget allows)
  for (let i = 1; i < recentLogs.length && output.length < charBudget * 0.75; i++) {
    const log = recentLogs[i];
    const entries = parseLogEntries(log.content)
      .filter(e => e.priority >= 7)
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 3);
    
    if (entries.length > 0) {
      output += `**${log.date} 重点**:\n`;
      for (const e of entries) {
        const line = `- ${e.tag ? `[${e.tag}]` : ''} ${e.text}\n`;
        if (output.length + line.length > charBudget * 0.85) break;
        output += line;
      }
      output += '\n';
    }
  }

  // 3. Active memory sections (remaining budget)
  const memSections = getActiveMemorySections();
  if (memSections && output.length + memSections.length < charBudget) {
    output += '**长期记忆摘要**:\n' + memSections + '\n';
  }

  // Truncate if over budget
  if (output.length > maxChars) {
    output = output.slice(0, maxChars - 20) + '\n\n_(truncated)_';
  }

  console.log(output);
}

buildResumeSummary();
