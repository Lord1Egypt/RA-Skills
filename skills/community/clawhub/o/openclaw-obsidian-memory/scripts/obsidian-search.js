#!/usr/bin/env node
/**
 * obsidian-search.js — Obsidian Vault 智能检索（跨平台）
 *
 * 用法:
 *   node obsidian-search.js <关键词1> [关键词2] ... [--limit N] [--context N]
 *
 * 环境变量:
 *   OBSIDIAN_VAULT — Vault 路径（默认: ~/.obsidian-vault）
 *
 * 示例:
 *   node obsidian-search.js "obsidian 知识管理"
 *   node obsidian-search.js "bootstrap" --limit 5 --context 3
 *   OBSIDIAN_VAULT=/path/to/vault node obsidian-search.js "关键词"
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ─── 配置 ────────────────────────────────────────────────────────────────────

const VAULT = process.env.OBSIDIAN_VAULT || path.join(os.homedir(), '.obsidian-vault');
let LIMIT = 10;
let CONTEXT = 2;
const QUERY = [];

// ─── 解析参数 ────────────────────────────────────────────────────────────────

for (let i = 2; i < process.argv.length; i++) {
  const arg = process.argv[i];
  if (arg === '--limit') { LIMIT = parseInt(process.argv[++i], 10); }
  else if (arg === '--context') { CONTEXT = parseInt(process.argv[++i], 10); }
  else { QUERY.push(arg); }
}

if (QUERY.length === 0) {
  console.log('用法: node obsidian-search.js <关键词1> [关键词2] ... [--limit N] [--context N]');
  console.log('');
  console.log('环境变量:');
  console.log('  OBSIDIAN_VAULT — Vault 路径（默认: ~/.obsidian-vault）');
  process.exit(1);
}

if (!fs.existsSync(VAULT)) {
  console.log(`⚠️  Vault 目录不存在: ${VAULT}`);
  console.log('    请设置 OBSIDIAN_VAULT 环境变量或创建默认目录：');
  console.log('    mkdir -p "$HOME/.obsidian-vault"');
  process.exit(1);
}

// ─── 工具函数 ────────────────────────────────────────────────────────────────

const EXCLUDE_DIRS = new Set(['.obsidian', '_attachments', '.trash']);

function walkMd(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!EXCLUDE_DIRS.has(entry.name)) results.push(...walkMd(full));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

// ─── 收集文件 ───────────────────────────────────────────────────────────────

const SEARCH_DIRS = ['notes', 'references']
  .map(d => path.join(VAULT, d))
  .filter(d => fs.existsSync(d));

if (SEARCH_DIRS.length === 0) {
  console.log(`⚠️  Vault 中未找到 notes/ 或 references/ 目录: ${VAULT}`);
  process.exit(1);
}

let allFiles = [];
for (const dir of SEARCH_DIRS) allFiles.push(...walkMd(dir));

// ─── 多关键词匹配（AND → 退化 OR）────────────────────────────────────────────

function matchesKeyword(files, kw) {
  const lower = kw.toLowerCase();
  return files.filter(f => {
    try { return fs.readFileSync(f, 'utf-8').toLowerCase().includes(lower); }
    catch { return false; }
  });
}

let matched = allFiles;
for (const kw of QUERY) matched = matchesKeyword(matched, kw);

if (matched.length === 0) {
  const set = new Set();
  for (const kw of QUERY) matchesKeyword(allFiles, kw).forEach(f => set.add(f));
  matched = [...set];
}

// ─── 评分 ────────────────────────────────────────────────────────────────────

const scored = [];

for (const abs of matched) {
  const rel = path.relative(VAULT, abs);
  const name = path.basename(abs, '.md');
  let score = 0;

  // 标题匹配
  for (const kw of QUERY) {
    if (name.toLowerCase().includes(kw.toLowerCase())) score += 10;
  }

  // 内容匹配次数
  let content = '';
  try { content = fs.readFileSync(abs, 'utf-8'); } catch { /* skip */ }
  const lower = content.toLowerCase();
  for (const kw of QUERY) {
    const kl = kw.toLowerCase();
    let pos = 0, cnt = 0;
    while ((pos = lower.indexOf(kl, pos)) !== -1) { cnt++; pos += kl.length; }
    score += cnt * 2;
  }

  // 文件类型加权
  if (rel.includes(`${path.sep}areas${path.sep}`)) score += 5;
  else if (rel.includes(`${path.sep}projects${path.sep}`)) score += 3;
  else if (rel.includes(`${path.sep}daily${path.sep}`)) score += 1;
  else if (rel.includes(`${path.sep}ai-chats${path.sep}`)) score += 2;

  // 时间衰减
  let mtime = 0;
  try { mtime = fs.statSync(abs).mtimeMs; } catch { /* skip */ }
  const ageDays = (Date.now() - mtime) / 86400000;
  if (ageDays < 7) score += 5;
  else if (ageDays < 30) score += 3;
  else if (ageDays < 90) score += 1;

  scored.push({ score, rel, abs, content });
}

scored.sort((a, b) => b.score - a.score);

// ─── 输出 ────────────────────────────────────────────────────────────────────

const top = scored.slice(0, LIMIT);
const firstKw = QUERY[0].toLowerCase();

for (const { score, rel, abs, content } of top) {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📄 [${rel}] (score: ${score})`);
  console.log('');

  // 匹配行上下文
  const lines = content.split('\n');
  let matchCount = 0;
  for (let i = 0; i < lines.length && matchCount < 3; i++) {
    if (lines[i].toLowerCase().includes(firstKw)) {
      const start = Math.max(0, i - CONTEXT);
      const end = Math.min(lines.length - 1, i + CONTEXT);
      for (let j = start; j <= end; j++) {
        console.log(j === i ? `  → ${lines[j]}` : `    ${lines[j]}`);
      }
      console.log('');
      matchCount++;
    }
  }

  // 关联链接
  const links = [...new Set((content.match(/\[\[([^\]]+)\]\]/g) || []))].slice(0, 5);
  if (links.length > 0) {
    console.log(`  🔗 关联: ${links.join(' ')}`);
    console.log('');
  }
}
