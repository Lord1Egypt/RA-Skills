#!/usr/bin/env node
/**
 * obsidian-links.js — 分析 Vault 中的双向链接关系（跨平台）
 *
 * 用法:
 *   node obsidian-links.js              — 列出所有笔记和链接关系
 *   node obsidian-links.js <笔记名>     — 查找某笔记的相关笔记（一跳扩展）
 *   node obsidian-links.js --orphans    — 列出孤立笔记（无链接）
 *
 * 环境变量:
 *   OBSIDIAN_VAULT — Vault 路径（默认: ~/.obsidian-vault）
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const VAULT = process.env.OBSIDIAN_VAULT || path.join(os.homedir(), '.obsidian-vault');
const TARGET = process.argv[2] || null;

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

function extractLinks(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return [...new Set(content.match(/\[\[([^\]]+)\]\]/g) || [])];
  } catch {
    return [];
  }
}

function findFileBySlug(slug) {
  for (const dir of ['notes', 'references']) {
    const found = walkMd(path.join(VAULT, dir)).find(f => path.basename(f, '.md') === slug);
    if (found) return found;
  }
  return null;
}

// ─── 主逻辑 ──────────────────────────────────────────────────────────────────

if (!fs.existsSync(VAULT)) {
  console.log(`⚠️  Vault 目录不存在: ${VAULT}`);
  process.exit(1);
}

const allFiles = [
  ...walkMd(path.join(VAULT, 'notes')),
  ...walkMd(path.join(VAULT, 'references')),
];

if (TARGET === '--orphans') {
  console.log('=== 孤立笔记（无任何链接）===\n');
  for (const f of allFiles) {
    const links = extractLinks(f);
    const slug = path.basename(f, '.md');
    const linked = allFiles.some(other => {
      if (other === f) return false;
      const c = fs.readFileSync(other, 'utf-8');
      return c.includes(`[[${slug}]]`);
    });
    if (links.length === 0 && !linked) {
      console.log(`  📄 ${path.relative(VAULT, f)}`);
    }
  }

} else if (!TARGET) {
  console.log('=== Vault 链接图谱 ===\n');
  for (const f of allFiles) {
    const links = extractLinks(f);
    if (links.length > 0) {
      console.log(`📄 ${path.relative(VAULT, f)}`);
      for (const link of links) {
        console.log(`  └─→ ${link}`);
      }
      console.log('');
    }
  }

} else {
  console.log(`=== 与「${TARGET}」相关的笔记 ===\n`);

  const targetFile = findFileBySlug(TARGET);
  if (targetFile) {
    console.log(`📤 ${TARGET} → 链接到:`);
    const links = extractLinks(targetFile);
    for (const link of links) {
      const linkName = link.replace(/\[\[|\]\]/g, '');
      const linkFile = findFileBySlug(linkName);
      if (linkFile) {
        console.log(`  ✅ ${link} → ${path.relative(VAULT, linkFile)}`);
      } else {
        console.log(`  ⚠️  ${link} → (未找到笔记)`);
      }
    }
  }

  console.log('');
  console.log(`📥 链接到 ${TARGET}:`);
  for (const f of allFiles) {
    const content = fs.readFileSync(f, 'utf-8');
    if (content.includes(`[[${TARGET}]]`)) {
      console.log(`  ← ${path.relative(VAULT, f)}`);
    }
  }
}
