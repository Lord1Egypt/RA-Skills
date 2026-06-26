#!/usr/bin/env node
/**
 * MemoryRouter — Intelligent memory routing for OpenClaw agents
 * 
 * Modes:
 *   --tier     → Auto-tier MEMORY.md (with pre-tier backup + safety checks)
 *   --tier --dry-run  → Preview tiering without making changes
 *   --restore    → Restore MEMORY.md from latest backup
 *   --compact  → Generate smart memory manifest for next session
 *   --compact --query "text" → Query-aware manifest with entity resolution
 *   --compact --budget N     → Manifest filtered to stay within N tokens
 *   --audit    → Scan for duplicates/conflicts across memory files
 *   --status   → Show memory health overview
 *   --entity   → Manage entity index (add/list/search)
 *   --wal      → WAL protocol helpers
 */

const fs = require('fs');
const path = require('path');

// Detect workspace: check MM_WORKSPACE env, then walk up from __dirname
const WORKSPACE = (() => {
  if (process.env.MM_WORKSPACE) return process.env.MM_WORKSPACE;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..'); // fallback: 2 levels up
})();
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const CONFIG_PATH = path.join(__dirname, 'config.json');

// Max file size in bytes (10 MB default)
const MAX_FILE_SIZE = 10 * 1024 * 1024;

// Validate a filepath is within the workspace root
function validatePath(filepath) {
  const resolved = path.resolve(filepath);
  if (!resolved.startsWith(path.resolve(WORKSPACE) + path.sep) && resolved !== path.resolve(WORKSPACE)) {
    return { ok: false, reason: 'Path escapes workspace root' };
  }
  return { ok: true };
}

// Escape special regex characters
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// ─── Helpers ───────────────────────────────────────────────────────────────

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch {
    return {
      thresholds: { memoryMdMaxLines: 500, memoryMdMaxChars: 25000, tierArchiveMinAgeDays: 3, auditMaxFiles: 50 },
      tiering: { archiveDir: 'memory/active', retentionDays: 90, keepInMemory: ['identity', 'preferences', 'relationships', 'projects', 'patterns', 'boundaries', 'key_facts'] },
      manifest: { generateOnTier: true, manifestPath: 'memory/memory-manifest.json' },
      audit: { reportPath: 'memory/memory-audit-report.md', duplicateThreshold: 0.7, conflictKeywords: ['revised', 'updated', 'changed', 'no longer', 'actually', 'correction', 'mistake'] },
      tokenBudget: { enabled: false, defaultBudget: 30000, overhead: 5000 }
    };
  }
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function readSafe(filepath) {
  try {
    const resolved = path.resolve(filepath);
    // Symlink check
    const lstat = fs.lstatSync(resolved);
    if (lstat.isSymbolicLink()) {
      console.error(`[memory-router] Refusing to read symlink: ${filepath}`);
      return null;
    }
    // Size check
    const size = fs.statSync(resolved).size;
    if (size > MAX_FILE_SIZE) {
      console.error(`[memory-router] File too large (${size} bytes): ${filepath}`);
      return null;
    }
    return fs.readFileSync(resolved, 'utf8');
  } catch { return null; }
}

function writeSafe(filepath, content) {
  const resolved = path.resolve(filepath);

  // Path validation — reject paths outside workspace
  const validation = validatePath(filepath);
  if (!validation.ok) {
    console.error(`[memory-router] Refusing to write: ${validation.reason}`);
    return;
  }

  // Symlink check — must be before any file operations
  let fileExists = false;
  try {
    const lstat = fs.lstatSync(resolved);
    if (lstat.isSymbolicLink()) {
      console.error(`[memory-router] Refusing to write to symlink: ${filepath}`);
      return;
    }
    fileExists = true;
  } catch {
    // File doesn't exist yet — that's fine, we're creating it
  }

  // Size check
  if (content.length > MAX_FILE_SIZE) {
    console.error(`[memory-router] Content too large (${content.length} bytes) for ${filepath}`);
    return;
  }

  // Atomic write: write to temp file, then rename
  ensureDir(path.dirname(filepath));
  const tmpPath = resolved + '.tmp-' + process.pid;
  try {
    fs.writeFileSync(tmpPath, content, 'utf8');
    fs.renameSync(tmpPath, resolved);
  } catch (err) {
    // Clean up temp file on failure
    try { fs.unlinkSync(tmpPath); } catch {}
    console.error(`[memory-router] Write failed for ${filepath}: ${err.message}`);
  }
}

function charToTokens(chars) {
  // Rough estimate: ~4 chars per token for mixed markdown/English
  return Math.ceil(chars / 4);
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function daysSince(dateStr) {
  const d = new Date(dateStr);
  const now = new Date();
  return Math.floor((now - d) / (1000 * 60 * 60 * 24));
}

function extractSections(text) {
  const sections = [];
  const lines = text.split('\n');
  let currentSection = null;
  let currentContent = [];

  for (const line of lines) {
    const headerMatch = line.match(/^(#{1,3})\s+(.+)$/);
    if (headerMatch && currentSection !== null) {
      sections.push({ header: currentSection, content: currentContent.join('\n') });
      currentContent = [];
    }
    if (headerMatch) {
      currentSection = headerMatch[2].trim();
    } else if (currentSection !== null) {
      currentContent.push(line);
    }
  }
  if (currentSection && currentContent.length > 0) {
    sections.push({ header: currentSection, content: currentContent.join('\n') });
  }
  return sections;
}

function normalizeKeyword(kw) {
  return kw.toLowerCase().replace(/[_\-]/g, ' ').trim();
}

function classifySection(header, config) {
  const h = header.toLowerCase().trim();
  const keep = config.tiering.keepInMemory || [];
  
  for (const kw of keep) {
    const normalized = normalizeKeyword(kw);
    if (h === normalized || h.includes(normalized) || normalized.includes(h)) {
      return 'core';
    }
  }
  
  for (const kw of keep) {
    const normalized = normalizeKeyword(kw);
    const words = normalized.split(' ');
    for (const word of words) {
      if (word.length > 2 && h.includes(word)) {
        return 'core';
      }
    }
  }
  
  return 'archive';
}

function levenshtein(a, b) {
  const m = a.length, n = b.length;
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
    }
  }
  return dp[m][n];
}

function similarity(a, b) {
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - levenshtein(a, b) / maxLen;
}

// ─── Entity Index ──────────────────────────────────────────────────────────

function getEntityIndexPath() {
  return path.join(MEMORY_DIR, 'entity-index.json');
}

function loadEntityIndex() {
  const data = readSafe(getEntityIndexPath());
  if (!data) return { entities: {}, lastUpdated: getToday() };
  try { return JSON.parse(data); } catch { return { entities: {}, lastUpdated: getToday() }; }
}

function saveEntityIndex(index) {
  index.lastUpdated = getToday();
  writeSafe(getEntityIndexPath(), JSON.stringify(index, null, 2));
}

function entityAdd(name, entityType, files) {
  const index = loadEntityIndex();
  name = name.toLowerCase().trim();
  
  // Validate entity name
  if (!name || !/^[a-z0-9][a-z0-9_-]*$/.test(name)) {
    console.log('[memory-router] Entity name must be alphanumeric (with hyphens/underscores).');
    return null;
  }
  
  // Validate entityType
  if (!/^[a-z0-9][a-z0-9_-]*$/.test(entityType)) {
    console.log('[memory-router] Entity type must be alphanumeric (with hyphens/underscores).');
    return null;
  }
  
  if (!index.entities[name]) {
    index.entities[name] = { type: entityType, files: [], addedAt: getToday() };
  }
  
  // Merge files, deduplicate
  for (const f of files) {
    // Validate file path — must not escape workspace
    const validation = validatePath(f);
    if (!validation.ok) {
      console.log(`[memory-router] Skipping invalid file path: ${f} (${validation.reason})`);
      continue;
    }
    if (!index.entities[name].files.includes(f)) {
      index.entities[name].files.push(f);
    }
  }
  
  saveEntityIndex(index);
  console.log(`[memory-router] Entity added: "${name}" (${entityType}) → ${files.join(', ')}`);
  return index;
}

function entitySearch(query) {
  const index = loadEntityIndex();
  const queryLower = query.toLowerCase();
  const results = [];
  
  // Direct match
  if (index.entities[queryLower]) {
    results.push({ entity: queryLower, score: 1.0, ...index.entities[queryLower] });
  }
  
  // Fuzzy match (substring)
  for (const [name, data] of Object.entries(index.entities)) {
    if (queryLower.includes(name) || name.includes(queryLower)) {
      if (!results.find(r => r.entity === name)) {
        results.push({ entity: name, score: 0.8, ...data });
      }
    }
  }
  
  return results.sort((a, b) => b.score - a.score);
}

function entityList() {
  const index = loadEntityIndex();
  const entries = Object.entries(index.entities);
  console.log(`\nEntity Index (${entries.length} entities, last updated: ${index.lastUpdated})\n`);
  console.log(`${'Name'.padEnd(25)} ${'Type'.padEnd(15)} ${'Files'.padEnd(30)}`);
  console.log('-'.repeat(70));
  for (const [name, data] of entries) {
    console.log(`${name.padEnd(25)} ${data.type.padEnd(15)} ${data.files.join(', ').padEnd(30)}`);
  }
  console.log('');
  return index;
}

// ─── WAL Protocol ──────────────────────────────────────────────────────────

function walGetState() {
  const walPath = path.join(WORKSPACE, 'SESSION-STATE.md');
  const content = readSafe(walPath);
  if (!content) {
    console.log('[memory-router] No WAL state. Create with: wal init');
    return;
  }
  console.log(`[memory-router] WAL state: ${walPath}\n\n${content}`);
}

function walInit() {
  const walPath = path.join(WORKSPACE, 'SESSION-STATE.md');
  const template = `# SESSION-STATE.md — Active Working Memory

## Current Task
[What we're working on RIGHT NOW]

## Key Context
- User preference: 
- Decision made: 
- Blocker: 

## Pending Actions
- [ ] 

## Recent Decisions
[None yet]

---
*Last updated: ${getToday()}*
`;
  writeSafe(walPath, template);
  console.log(`[memory-router] WAL initialized: ${walPath}`);
}

function walUpdate(section, content) {
  const walPath = path.join(WORKSPACE, 'SESSION-STATE.md');
  const existing = readSafe(walPath);
  
  if (!existing) {
    console.log('[memory-router] No WAL state. Run "wal init" first.');
    return;
  }
  
  // Sanitize section name — prevent header injection
  const safeSection = section.replace(/[`$\\]/g, '').trim();
  if (!safeSection) {
    console.log('[memory-router] WAL update: section name is empty.');
    return;
  }
  
  // Sanitize content — prevent header injection
  const safeContent = content
    .replace(/^## /gm, '### ')   // prevent header injection
    .replace(/[`$\\]/g, '')      // prevent template literal / variable injection
    .substring(0, 50000);
  
  // Replace or append section
  const escaped = escapeRegex(safeSection);
  const sectionRegex = new RegExp(`## ${escaped}\\n([\\s\\S]*?)(?=\\n## |$)`);
  const match = existing.match(sectionRegex);
  
  if (match) {
    const newContent = existing.replace(sectionRegex, `## ${safeSection}\n${safeContent}`);
    const footerMatch = newContent.match(/---\n\*Last updated:.*\*\n$/);
    if (footerMatch) {
      writeSafe(walPath, newContent.replace(footerMatch[0], `---\n*Last updated: ${getToday()}*\n`));
    }
  } else {
    // Append section before footer
    const footerRegex = /---\n\*Last updated:.*\*\n$/;
    const lines = existing.split('\n');
    const footerIdx = lines.findIndex(l => l.startsWith('*Last updated:'));
    if (footerIdx > 0) {
      lines.splice(footerIdx, 0, '', `## ${safeSection}`, safeContent);
      writeSafe(walPath, lines.join('\n'));
    }
  }
  
  console.log(`[memory-router] WAL updated: ${section}`);
}

// ─── TIER MODE ─────────────────────────────────────────────────────────────

function tierMemory(dryRun = false) {
  const config = loadConfig();
  const memoryMdPath = path.join(WORKSPACE, 'MEMORY.md');
  const content = readSafe(memoryMdPath);

  if (!content) {
    console.log('[memory-router] No MEMORY.md found. Nothing to tier.');
    return null;
  }

  const lineCount = content.split('\n').length;
  const charCount = content.length;
  const maxLines = config.thresholds.memoryMdMaxLines;
  const maxChars = config.thresholds.memoryMdMaxChars;

  console.log(`[memory-router] MEMORY.md: ${lineCount} lines, ${charCount} chars`);

  if (lineCount <= maxLines && charCount <= maxChars) {
    console.log('[memory-router] Below thresholds. No tiering needed.');
    return null;
  }

  // ─── Safety: Check minimum core size ───
  const minCoreLines = config.tiering.minCoreLines || 20;
  const minCoreChars = config.tiering.minCoreChars || 1000;

  const sections = extractSections(content);
  const coreSections = [];
  const archiveSections = [];

  for (const s of sections) {
    if (classifySection(s.header, config) === 'core') {
      coreSections.push(s);
    } else {
      archiveSections.push(s);
    }
  }

  if (sections.length === 0) {
    const paragraphs = content.split(/\n\s*\n/).filter(p => p.trim());
    for (const p of paragraphs) {
      const firstLine = p.split('\n')[0].toLowerCase();
      const isCore = config.tiering.keepInMemory.some(kw => firstLine.includes(kw));
      if (isCore) {
        coreSections.push({ header: firstLine, content: p });
      } else {
        archiveSections.push({ header: firstLine, content: p });
      }
    }
  }

  // Safety check: if too few core sections, abort
  if (coreSections.length < minCoreLines || coreSections.reduce((sum, s) => sum + (s.content || '').length, 0) < minCoreChars) {
    console.error(`[memory-router] ⚠️ SAFETY: Only ${coreSections.length} core sections (${coreSections.reduce((sum, s) => sum + (s.content || '').length, 0)} chars) would remain. Aborting to prevent data loss.`);
    console.error('[memory-router] Increase minCoreLines (currently ' + minCoreLines + ') or minCoreChars (currently ' + minCoreChars + ') in config.json.');
    return null;
  }

  // ─── Dry run mode (BEFORE any file writes) ───
  if (dryRun) {
    const archiveFile = path.join(WORKSPACE, config.tiering.archiveDir, `MEMORY-archive-${getToday()}.md`);
    const coreLines = `# MEMORY.md - Long-Term Memory\n\n`.split('\n').length;
    const estimatedCoreLines = coreLines + coreSections.reduce((sum, s) => sum + (s.content || '').split('\n').length + 3, 0);
    
    console.log(`\n[memory-router] ── DRY RUN ──`);
    console.log(`[memory-router] Would archive: ${archiveFile}`);
    console.log(`[memory-router] Would reduce MEMORY.md from ${lineCount} lines to ~${estimatedCoreLines} lines`);
    console.log(`[memory-router] Core sections: ${coreSections.length}, Archive sections: ${archiveSections.length}`);
    console.log(`[memory-router] ✅ No files were modified.`);
    return { dryRun: true, coreSections: coreSections.length, archiveSections: archiveSections.length, estimatedCoreLines };
  }

  // ─── Safety: require --confirm for destructive write ───
  if (!args.includes('--confirm')) {
    console.error('[memory-router] ⚠️ TIER MODE requires --confirm flag for destructive writes.');
    console.error('[memory-router] Run --tier --dry-run first to preview changes.');
    console.error('[memory-router] When ready: --tier --confirm');
    return null;
  }

  // ─── Pre-tier backup (only after confirm, before actual tiering) ───
  const backupDir = path.join(WORKSPACE, config.tiering.backupDir || 'memory/backups');
  ensureDir(backupDir);
  const backupFile = path.join(backupDir, `MEMORY-backup-${getToday()}-${Date.now()}.md`);
  
  // Create backup with full content + unambiguous delimiter for safe restore
  const backupContent = `# MEMORY.md — Pre-Tier Backup

`;
  backupContent += `> Created ${getToday()} ${new Date().toISOString()} by memory-router skill
`;
  backupContent += `> Original: ${lineCount} lines, ${charCount} chars
`;
  backupContent += `> This is a full backup before tiering. Do NOT delete this file.
`;
  backupContent += `---
`;
  backupContent += `---END-METADATA---
`;
  backupContent += content;
  writeSafe(backupFile, backupContent);
  console.log(`[memory-router] ✅ Pre-tier backup: ${backupFile} (${lineCount} lines saved)`);

  // ─── Actual tiering ───
  const archiveDir = path.join(WORKSPACE, config.tiering.archiveDir);
  ensureDir(archiveDir);
  const archiveFile = path.join(archiveDir, `MEMORY-archive-${getToday()}.md`);
  
  let archiveContent = `# Archived Memory Sections\n\n`;
  archiveContent += `> Auto-archived on ${getToday()} by memory-router skill\n`;
  archiveContent += `> Original MEMORY.md had ${lineCount} lines. This archive contains ${archiveSections.length} sections.\n\n`;
  archiveContent += `---\n\n`;

  for (const s of archiveSections) {
    archiveContent += `## ${s.header}\n\n${s.content}\n\n---\n\n`;
  }

  writeSafe(archiveFile, archiveContent);

  let coreContent = `# MEMORY.md - Long-Term Memory\n\n`;
  coreContent += `> Auto-tiled on ${getToday()} by memory-router skill\n`;
  coreContent += `> ${archiveSections.length} sections archived. Core file reduced from ${lineCount} to ${coreSections.length} sections.\n\n`;
  coreContent += `---\n\n`;

  for (const s of coreSections) {
    coreContent += `## ${s.header}\n\n${s.content}\n\n---\n\n`;
  }

  writeSafe(memoryMdPath, coreContent);

  console.log(`[memory-router] ✅ Tiered: ${coreSections.length} core sections, ${archiveSections.length} archived to ${archiveFile}`);
  console.log(`[memory-router] MEMORY.md reduced from ${lineCount} lines to ${coreContent.split('\n').length} lines`);

  if (config.manifest.generateOnTier) {
    generateManifest(archiveDir);
  }
  
  return { coreSections: coreSections.length, archivedSections: archiveSections.length, archivedSize: archiveContent.length };
}

// ─── COMPACT MODE (Memory Manifest) ────────────────────────────────────────

function collectAllFiles() {
  const files = [];
  
  // Helper: safely list .md files in a directory
  function listMdFiles(dirPath, prefix) {
    if (!fs.existsSync(dirPath)) return;
    for (const f of fs.readdirSync(dirPath)) {
      if (f.endsWith('.md')) {
        const fullPath = path.join(dirPath, f);
        // Skip symlinks and non-regular files
        try {
          const stat = fs.lstatSync(fullPath);
          if (stat.isSymbolicLink()) continue;
          if (!stat.isFile()) continue;
        } catch {
          continue;
        }
        files.push({ path: `${prefix}/${f}`, size: fs.statSync(fullPath).size });
      }
    }
  }
  
  // MEMORY.md
  const mm = path.join(WORKSPACE, 'MEMORY.md');
  if (fs.existsSync(mm)) {
    files.push({ path: 'MEMORY.md', size: fs.statSync(mm).size });
  }
  
  // memory/
  listMdFiles(path.join(WORKSPACE, 'memory'), 'memory');
  
  // self-improving/
  listMdFiles(path.join(WORKSPACE, 'self-improving'), 'self-improving');
  
  // proactivity/
  listMdFiles(path.join(WORKSPACE, 'proactivity'), 'proactivity');
  
  // archives
  const config = loadConfig();
  const archiveDir = path.join(WORKSPACE, config.tiering.archiveDir);
  if (fs.existsSync(archiveDir)) {
    for (const f of fs.readdirSync(archiveDir)) {
      if (f.startsWith('MEMORY-archive-') && f.endsWith('.md')) {
        const fullPath = path.join(archiveDir, f);
        try {
          const stat = fs.lstatSync(fullPath);
          if (stat.isSymbolicLink()) continue;
          if (!stat.isFile()) continue;
        } catch {
          continue;
        }
        files.push({ path: `${config.tiering.archiveDir}/${f}`, size: fs.statSync(fullPath).size });
      }
    }
  }
  
  return files;
}

function generateManifest(archiveDir, query, budget) {
  const config = loadConfig();
  const manifest = {
    generated: getToday(),
    version: 2,
    query: query || null,
    budget: budget || null,
    files: []
  };

  const allFiles = collectAllFiles();
  const systemOverhead = config.tokenBudget?.overhead || 5000;
  
  // Always required
  const mmPath = path.join(WORKSPACE, 'MEMORY.md');
  if (fs.existsSync(mmPath)) {
    manifest.files.push({
      path: 'MEMORY.md',
      tier: 'core',
      reason: 'Primary memory file (core sections only)',
      required: true,
      size: fs.statSync(mmPath).size
    });
  }

  // Self-improving files
  const siDir = path.join(WORKSPACE, 'self-improving');
  if (fs.existsSync(siDir)) {
    for (const f of fs.readdirSync(siDir).filter(f => f.endsWith('.md'))) {
      const fp = path.join(siDir, f);
      manifest.files.push({
        path: `self-improving/${f}`,
        tier: 'domain',
        reason: 'Execution improvement memory',
        required: false,
        size: fs.statSync(fp).size
      });
    }
  }

  // Proactivity files
  const proDir = path.join(WORKSPACE, 'proactivity');
  if (fs.existsSync(proDir)) {
    for (const f of fs.readdirSync(proDir).filter(f => f.endsWith('.md'))) {
      const fp = path.join(proDir, f);
      manifest.files.push({
        path: `proactivity/${f}`,
        tier: 'domain',
        reason: 'Proactive boundary',
        required: false,
        size: fs.statSync(fp).size
      });
    }
  }

  // Recent memory files (last 14 days)
  const memoryDir = path.join(WORKSPACE, 'memory');
  if (fs.existsSync(memoryDir)) {
    const memoryFiles = fs.readdirSync(memoryDir)
      .filter(f => f.endsWith('.md') && f !== 'MEMORY.md')
      .sort()
      .slice(-14);

    for (const f of memoryFiles) {
      const filePath = path.join(memoryDir, f);
      const mtime = fs.statSync(filePath).mtime;
      const age = daysSince(mtime.toISOString());
      manifest.files.push({
        path: `memory/${f}`,
        tier: 'recent',
        ageDays: age,
        reason: age < 2 ? 'Very recent — load always' : 'Recent — load if relevant',
        required: age < 2,
        size: fs.statSync(filePath).size
      });
    }
  }

  // Archive files
  if (archiveDir && fs.existsSync(archiveDir)) {
    const archives = fs.readdirSync(archiveDir)
      .filter(f => f.startsWith('MEMORY-archive-') && f.endsWith('.md'))
      .sort()
      .reverse();

    for (const f of archives.slice(0, 5)) {
      const filePath = path.join(archiveDir, f);
      const mtime = fs.statSync(filePath).mtime;
      const age = daysSince(mtime.toISOString());
      manifest.files.push({
        path: `${config.tiering.archiveDir}/${f}`,
        tier: 'archive',
        ageDays: age,
        reason: 'Archived memory — load only on semantic match',
        required: false,
        size: fs.statSync(filePath).size
      });
    }
  }

  // ─── Feature: Entity-aware ranking ───
  if (query) {
    const entityIndex = loadEntityIndex();
    const entities = entitySearch(query);
    
    for (const entity of entities) {
      // Boost files that match the entity
      for (const f of entity.files) {
        const manifestFile = manifest.files.find(mf => mf.path === f);
        if (manifestFile) {
          manifestFile.entityMatch = entity.entity;
          manifestFile.entityScore = entity.score;
          manifestFile.boosted = true;
        }
      }
    }
    
    // Sort: required first, then boosted, then by recency, then by size
    manifest.files.sort((a, b) => {
      if (a.required !== b.required) return a.required ? -1 : 1;
      if (a.boosted !== b.boosted) return a.boosted ? -1 : 1;
      if (a.tier === 'recent' && b.tier !== 'recent') return -1;
      if (b.tier === 'recent' && a.tier !== 'recent') return 1;
      return (a.size || 0) - (b.size || 0);
    });
  }

  // ─── Feature: Token budget filtering ───
  if (budget) {
    const availableTokens = budget - systemOverhead;
    let loadedTokens = charToTokens(0);
    
    // First pass: count required files
    for (const f of manifest.files) {
      if (f.required) {
        loadedTokens += charToTokens(f.size || 0);
      }
    }
    
    // Second pass: add optional files until budget exhausted
    for (const f of manifest.files) {
      if (!f.required) {
        const fileTokens = charToTokens(f.size || 0);
        if (loadedTokens + fileTokens <= availableTokens) {
          f.load = true;
          loadedTokens += fileTokens;
        } else {
          f.load = false;
        }
      }
    }
    
    manifest.budgetUsed = loadedTokens;
    manifest.budgetTotal = budget;
    manifest.budgetEfficiency = ((1 - loadedTokens / budget) * 100).toFixed(1);
  }

  const manifestPath = path.join(WORKSPACE, config.manifest.manifestPath);
  writeSafe(manifestPath, JSON.stringify(manifest, null, 2));

  const required = manifest.files.filter(f => f.required).length;
  const optional = manifest.files.filter(f => !f.required).length;
  
  console.log(`[memory-router] Manifest generated: ${required} required, ${optional} optional files`);
  if (query) console.log(`[memory-router] Query-aware: "${query}"`);
  if (budget) {
    const efficiency = Math.max(0, parseFloat(manifest.budgetEfficiency));
    const warning = efficiency < 0 ? ' ⚠️ Budget insufficient — only core files loaded' : '';
    console.log(`[memory-router] Budget: ${manifest.budgetUsed}/${budget} tokens (${efficiency.toFixed(1)}% remaining)${warning}`);
  }
  console.log(`[memory-router] Manifest: ${manifestPath}`);

  return manifest;
}

function compact(query, budget) {
  const config = loadConfig();
  const archiveDir = path.join(WORKSPACE, config.tiering.archiveDir);
  return generateManifest(archiveDir, query, budget);
}

// ─── AUDIT MODE ────────────────────────────────────────────────────────────

function auditMemory() {
  const config = loadConfig();
  const workspace = WORKSPACE;
  const report = [];
  const duplicates = [];
  const conflicts = [];

  report.push(`# Memory Audit Report\n`);
  report.push(`> Generated: ${getToday()} by memory-router skill\n\n`);

  const memoryFiles = [];
  const filesToCheck = ['MEMORY.md', 'SOUL.md', 'AGENTS.md', 'USER.md', 'IDENTITY.md'];

  const memoryDir = path.join(workspace, 'memory');
  if (fs.existsSync(memoryDir)) {
    const dailyFiles = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md')).slice(-config.thresholds.auditMaxFiles);
    for (const f of dailyFiles) {
      filesToCheck.push(`memory/${f}`);
    }
  }

  const siDir = path.join(workspace, 'self-improving');
  if (fs.existsSync(siDir)) {
    const siFiles = fs.readdirSync(siDir).filter(f => f.endsWith('.md'));
    for (const f of siFiles) {
      filesToCheck.push(`self-improving/${f}`);
    }
  }

  const fileContents = [];
  for (const fp of filesToCheck) {
    const full = path.join(workspace, fp);
    const content = readSafe(full);
    if (content) {
      fileContents.push({ path: fp, content });
    }
  }

  report.push(`## Files Scanned: ${fileContents.length}\n\n`);

  report.push(`## Potential Duplicates\n\n`);
  for (let i = 0; i < fileContents.length; i++) {
    for (let j = i + 1; j < fileContents.length; j++) {
      const a = fileContents[i].content.toLowerCase().replace(/\s+/g, ' ').substring(0, 500);
      const b = fileContents[j].content.toLowerCase().replace(/\s+/g, ' ').substring(0, 500);
      const sim = similarity(a, b);
      if (sim > config.audit.duplicateThreshold) {
        duplicates.push({ files: [fileContents[i].path, fileContents[j].path], similarity: sim.toFixed(2) });
        report.push(`- **${fileContents[i].path}** ↔ **${fileContents[j].path}** (similarity: ${sim.toFixed(2)})\n`);
      }
    }
  }
  if (duplicates.length === 0) report.push('No high-similarity duplicates found.\n');

  report.push(`\n## Potential Conflicts\n\n`);
  for (const file of fileContents) {
    const content = file.content.toLowerCase();
    for (const kw of config.audit.conflictKeywords) {
      // Validate keyword — reject regex metacharacters
      if (/[.*+?^${}()|[\]\\]/.test(kw)) {
        console.warn(`[memory-router] Audit: skipping invalid keyword: ${kw} (contains regex metacharacters)`);
        continue;
      }
      if (content.includes(kw)) {
        const lineNum = content.split('\n').findIndex(l => l.includes(kw)) + 1;
        const line = content.split('\n')[lineNum - 1]?.trim() || '';
        conflicts.push({ file: file.path, keyword: kw, line, lineNum });
        report.push(`- **${file.path}:${lineNum}** — Found "${kw}": "${line}"\n`);
      }
    }
  }
  if (conflicts.length === 0) report.push('No revision keywords found.\n');

  report.push(`\n## Memory File Sizes\n\n`);
  for (const file of fileContents) {
    const size = file.content.length;
    const lines = file.content.split('\n').length;
    const status = size > config.thresholds.memoryMdMaxChars ? '⚠️ OVER' : '✅ OK';
    report.push(`- **${file.path}**: ${lines} lines, ${(size/1024).toFixed(1)} KB ${status}\n`);
  }

  // ─── Entity index summary ───
  const entityIndex = loadEntityIndex();
  const entityEntries = Object.entries(entityIndex.entities);
  report.push(`\n## Entity Index\n\n`);
  report.push(`- ${entityEntries.length} entities indexed\n`);
  if (entityEntries.length > 0) {
    report.push(`- Last updated: ${entityIndex.lastUpdated}\n`);
  }

  // ─── Token impact estimate ───
  const totalChars = fileContents.reduce((sum, f) => sum + f.content.length, 0);
  const totalTokens = charToTokens(totalChars + 3500);
  report.push(`\n## Token Impact Estimate\n\n`);
  report.push(`- Total content: ${totalChars.toLocaleString()} chars (~${totalTokens.toLocaleString()} tokens)\n`);
  report.push(`- All files loaded into context every session\n`);

  const reportPath = path.join(workspace, config.audit.reportPath);
  writeSafe(reportPath, report.join(''));

  console.log(`[memory-router] Audit complete: ${duplicates.length} duplicates, ${conflicts.length} conflicts found`);
  console.log(`[memory-router] Report: ${reportPath}`);

  return { duplicates, conflicts, fileCount: fileContents.length, totalTokens };
}

// ─── STATUS ────────────────────────────────────────────────────────────────

// ─── RESTORE MODE ────────────────────────────────────────────────────────

function restoreFromBackup() {
  const config = loadConfig();
  const backupDir = path.join(WORKSPACE, config.tiering.backupDir || 'memory/backups');
  
  if (!fs.existsSync(backupDir)) {
    console.log('[memory-router] No backup directory found. Nothing to restore.');
    return;
  }
  
  const backups = fs.readdirSync(backupDir)
    .filter(f => f.startsWith('MEMORY-backup-') && f.endsWith('.md'))
    .sort()
    .reverse(); // newest first
  
  if (backups.length === 0) {
    console.log('[memory-router] No backups found. Nothing to restore.');
    return;
  }
  
  const latestBackup = backups[0];
  const backupPath = path.join(backupDir, latestBackup);
  const backupContent = readSafe(backupPath);
  
  if (!backupContent) {
    console.log('[memory-router] Could not read backup file.');
    return;
  }
  
  // Extract header info
  const headerMatch = backupContent.match(/> Created (.+) by memory-router skill/);
  const originalMatch = backupContent.match(/> Original: (\d+) lines, (\d+) chars/);
  const created = headerMatch ? headerMatch[1] : 'unknown';
  const originalLines = originalMatch ? originalMatch[1] : 'unknown';
  const originalChars = originalMatch ? originalMatch[2] : 'unknown';
  
  // Require explicit confirmation via --force flag
  console.error(`[memory-router] ⚠️ RESTORE FROM BACKUP`);
  console.error(`[memory-router] Backup: ${latestBackup}`);
  console.error(`[memory-router] Created: ${created}`);
  console.error(`[memory-router] Original: ${originalLines} lines, ${originalChars} chars`);
  console.error(`[memory-router] This will OVERWRITE the current MEMORY.md.`);
  console.error(`[memory-router] ⛔ CONFIRMATION REQUIRED: Pass --force to proceed.`);
  
  if (!args.includes('--force')) {
    console.error(`[memory-router] ⛔ Aborted. Use --force to confirm restore.`);
    return;
  }
  
  const memoryMdPath = path.join(WORKSPACE, 'MEMORY.md');
  const currentContent = readSafe(memoryMdPath);
  const currentLines = currentContent ? currentContent.split('\n').length : 0;
  
  // Backup current before overwriting
  if (currentContent) {
    const currentBackup = path.join(backupDir, `MEMORY-current-before-restore-${Date.now()}.md`);
    writeSafe(currentBackup, `# Current MEMORY.md before restore\n\n> Saved at ${getToday()} ${new Date().toISOString()}\n\n${currentContent}`);
    console.log(`[memory-router] Current MEMORY.md backed up to: ${currentBackup}`);
  }
  
  // Extract only the original content using unambiguous delimiter
  const delimiter = '---END-METADATA---';
  const delimiterIdx = backupContent.indexOf(delimiter);
  
  if (delimiterIdx === -1) {
    console.error('[memory-router] ⚠️ Backup file missing delimiter. Cannot safely restore.');
    console.error('[memory-router] This backup may be from an older version. Manual recovery required.');
    return;
  }
  
  // Take everything after the delimiter (plus its length and the following newlines)
  let contentStart = delimiterIdx + delimiter.length;
  while (contentStart < backupContent.length && backupContent[contentStart] === '\n') contentStart++;
  let originalContent = backupContent.slice(contentStart);
  writeSafe(memoryMdPath, originalContent);
  
  console.log(`[memory-router] ✅ Restored MEMORY.md from ${latestBackup}`);
  console.log(`[memory-router] Restored: ${originalLines} lines, ${originalChars} chars`);
  
  // Regenerate manifest
  const archiveDir = path.join(WORKSPACE, config.tiering.archiveDir);
  generateManifest(archiveDir);
}

function showStatus() {
  const config = loadConfig();
  const workspace = WORKSPACE;

  console.log('=== MemoryRouter Status ===\n');

  const memoryMd = path.join(workspace, 'MEMORY.md');
  const memoryContent = readSafe(memoryMd);
  if (memoryContent) {
    const lines = memoryContent.split('\n').length;
    const chars = memoryContent.length;
    console.log(`MEMORY.md: ${lines} lines, ${(chars/1024).toFixed(1)} KB ${chars > config.thresholds.memoryMdMaxChars ? '⚠️ OVER' : '✅ OK'}`);
  } else {
    console.log('MEMORY.md: not found');
  }

  const memoryDir = path.join(workspace, 'memory');
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
    const totalSize = files.reduce((sum, f) => sum + (readSafe(path.join(memoryDir, f)) || '').length, 0);
    console.log(`memory/: ${files.length} files, ${(totalSize/1024).toFixed(1)} KB total`);
  } else {
    console.log('memory/: not found');
  }

  const siDir = path.join(workspace, 'self-improving');
  if (fs.existsSync(siDir)) {
    const siFiles = fs.readdirSync(siDir).filter(f => f.endsWith('.md'));
    console.log(`self-improving/: ${siFiles.length} files`);
  }

  const proDir = path.join(workspace, 'proactivity');
  if (fs.existsSync(proDir)) {
    const proFiles = fs.readdirSync(proDir).filter(f => f.endsWith('.md'));
    console.log(`proactivity/: ${proFiles.length} files`);
  }

  const archiveDir = path.join(workspace, config.tiering.archiveDir);
  if (fs.existsSync(archiveDir)) {
    const archives = fs.readdirSync(archiveDir).filter(f => f.startsWith('MEMORY-archive-'));
    console.log(`archives: ${archives.length} files`);
  }

  const manifestPath = path.join(workspace, config.manifest.manifestPath);
  const manifest = readSafe(manifestPath);
  if (manifest) {
    const m = JSON.parse(manifest);
    console.log(`manifest: generated ${m.generated}, ${m.files.length} files`);
  }

  const entityIndex = loadEntityIndex();
  console.log(`entity index: ${Object.keys(entityIndex.entities).length} entities`);

  const walPath = path.join(workspace, 'SESSION-STATE.md');
  if (fs.existsSync(walPath)) {
    console.log('WAL: active');
  } else {
    console.log('WAL: not initialized');
  }

  console.log('\n=== Commands ===');
  console.log('  --tier              → Auto-tier MEMORY.md (with pre-tier backup)');
  console.log('  --tier --dry-run    → Preview tiering without making changes');
  console.log('  --restore           → Restore MEMORY.md from latest backup');
  console.log('  --compact           → Generate memory manifest');
  console.log('  --compact --query   → Query-aware manifest with entity resolution');
  console.log('  --compact --budget  → Manifest filtered to token budget');
  console.log('  --audit             → Scan for duplicates/conflicts');
  console.log('  --status            → Show this overview');
  console.log('  --entity add/list/search');
  console.log('  --wal init/get/update');
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const mode = args.find(a => a.startsWith('--'))?.replace('--', '');
const subMode = args.find(a => a.startsWith('--') === false && a !== '--tier' && a !== '--compact' && a !== '--audit' && a !== '--status' && !a.startsWith('-')) || '';

// Parse flags
let query = null, budget = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--query' && i + 1 < args.length) query = args[i + 1];
  if (args[i] === '--budget' && i + 1 < args.length) budget = parseInt(args[i + 1]);
}

switch (mode) {
  case 'tier':
    const dryRun = args.includes('--dry-run');
    tierMemory(dryRun);
    break;
  case 'restore':
    restoreFromBackup();
    break;
  case 'compact': compact(query, budget); break;
  case 'audit': auditMemory(); break;
  case 'status': showStatus(); break;
  case 'entity':
    if (subMode === 'add') {
      // args: --entity add <name> <type> <files...>
      // name is at index 2 (args[0]=--entity, args[1]=add, args[2]=name)
      const name = args[2];
      const type = args[3];
      const files = args.slice(4);
      if (!name || !type) {
        console.log('Usage: memory-router.js --entity add <name> <type> <files...>');
      } else {
        entityAdd(name, type, files);
      }
    } else if (subMode === 'list') {
      entityList();
    } else if (subMode === 'search') {
      const searchQuery = args[2];
      if (searchQuery) {
        const results = entitySearch(searchQuery);
        console.log(`\nEntity search for "${searchQuery}":\n`);
        for (const r of results) {
          console.log(`  ${r.entity} (${r.type}) — score: ${r.score} — files: ${r.files.join(', ')}`);
        }
        if (results.length === 0) console.log('  No matches found.');
      } else {
        console.log('Usage: memory-router.js --entity search <query>');
      }
    } else {
      console.log('Usage: memory-router.js --entity add <name> <type> <files...>');
      console.log('       memory-router.js --entity list');
      console.log('       memory-router.js --entity search <query>');
    }
    break;
  case 'wal':
    if (subMode === 'init') walInit();
    else if (subMode === 'get') walGetState();
    else if (subMode === 'update') {
      const section = args[2];
      const contentIdx = args.indexOf('--content');
      const content = contentIdx >= 0 && contentIdx + 1 < args.length ? args[contentIdx + 1] : '';
      if (section) {
        walUpdate(section, content);
      } else {
        console.log('Usage: memory-router.js --wal update <section> --content "<text>"');
      }
    } else {
      console.log('Usage: memory-router.js --wal init');
      console.log('       memory-router.js --wal get');
      console.log('       memory-router.js --wal update <section> --content "<text>"');
    }
    break;
  default:
    console.log('MemoryRouter — Intelligent memory routing for OpenClaw agents');
    console.log('Usage: memory-router.js [--tier|--compact|--audit|--status|--entity|--wal]');
    showStatus();
}
