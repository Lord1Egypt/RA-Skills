#!/usr/bin/env node
/**
 * LLM Wiki Lint Engine — 知识库健康检查
 */

import { readdirSync, readFileSync, writeFileSync, statSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const ROOT = join(__dirname, '..');
const WIKI_DIR = join(ROOT, 'wiki');
const CONCEPTS_DIR = join(WIKI_DIR, 'concepts');
const ENTITIES_DIR = join(WIKI_DIR, 'entities');

function getFilesRecursive(dir, files = []) {
  try {
    if (!existsSync(dir)) return files;
    const entries = readdirSync(dir);
    for (const entry of entries) {
      if (entry.startsWith('.')) continue;
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);
      if (stat.isDirectory()) {
        getFilesRecursive(fullPath, files);
      } else if (entry.endsWith('.md')) {
        files.push(fullPath);
      }
    }
  } catch {}
  return files;
}

function getRelativePath(base, fullPath) {
  return fullPath.replace(base + '/', '');
}

function extractLinks(content) {
  const links = [];
  const regex = /\[\[([^\]]+)\]\]/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1]);
  }
  return links;
}

function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const fm = {};
  for (const line of match[1].split('\n')) {
    const kv = line.match(/^(\w+):\s*(.*)$/);
    if (kv) {
      fm[kv[1]] = kv[2].trim();
    }
  }
  return fm;
}

async function lint() {
  console.log('🔍 LLM Wiki 健康检查\n');
  console.log(`检查目录: ${WIKI_DIR}\n`);

  const allConceptFiles = getFilesRecursive(CONCEPTS_DIR);
  const allEntityFiles = getFilesRecursive(ENTITIES_DIR);

  const conceptFiles = allConceptFiles.map(f => getRelativePath(CONCEPTS_DIR, f));
  const entityFiles = allEntityFiles.map(f => getRelativePath(ENTITIES_DIR, f));

  const allFiles = [...allConceptFiles, ...allEntityFiles];
  const allFileNames = new Set([...conceptFiles, ...entityFiles]);

  console.log(`📊 概览`);
  console.log(`  总页面数: ${conceptFiles.length + entityFiles.length}`);
  console.log(`  概念页面: ${conceptFiles.length}`);
  console.log(`  实体页面: ${entityFiles.length}`);
  console.log('');

  // 收集所有链接和被引用页面
  const allLinks = new Map(); // file -> [links]
  const referencedPages = new Set();

  for (const filePath of allFiles) {
    const content = readFileSync(filePath, 'utf-8');
    const links = extractLinks(content);
    allLinks.set(filePath, links);
    for (const link of links) {
      referencedPages.add(link);
    }
  }

  // 检查孤立页面
  console.log('🔗 检查孤立页面...');
  const orphaned = [];

  for (const filePath of allFiles) {
    const fileName = getRelativePath(WIKI_DIR, filePath).replace('.md', '');
    if (!referencedPages.has(fileName) && !referencedPages.has(filePath.split('/').pop().replace('.md', ''))) {
      // 检查是否在 index.md 中被引用
      const indexPath = join(WIKI_DIR, 'index.md');
      if (existsSync(indexPath)) {
        const indexContent = readFileSync(indexPath, 'utf-8');
        if (!indexContent.includes(fileName)) {
          orphaned.push(getRelativePath(WIKI_DIR, filePath));
        }
      }
    }
  }

  if (orphaned.length === 0) {
    console.log('  ✅ 无孤立页面');
  } else {
    console.log(`  ⚠️  ${orphaned.length} 个孤立页面:`);
    orphaned.forEach(f => console.log(`    - ${f}`));
  }
  console.log('');

  // 检查断链
  console.log('🔗 检查交叉引用完整性...');
  const brokenLinks = [];

  for (const [filePath, links] of allLinks) {
    for (const link of links) {
      if (link.startsWith('http') || link === 'index') continue;
      // 检查链接对应的文件是否存在
      const possibleFiles = [
        link + '.md',
        link.replace(/\//g, '-') + '.md',
      ];
      const exists = possibleFiles.some(f => allFileNames.has(f) || allFiles.some(fp => fp.endsWith(f)));
      if (!exists) {
        brokenLinks.push({
          file: getRelativePath(WIKI_DIR, filePath),
          link
        });
      }
    }
  }

  if (brokenLinks.length === 0) {
    console.log('  ✅ 所有链接有效');
  } else {
    console.log(`  ⚠️  ${brokenLinks.length} 个断链:`);
    brokenLinks.forEach(l => console.log(`    - ${l.file} → [[${l.link}]]`));
  }
  console.log('');

  // 检查前置字段
  console.log('📋 检查前置字段...');
  const requiredFields = ['title', 'created', 'updated', 'type', 'tags'];
  const missingFields = [];

  for (const filePath of allFiles) {
    const content = readFileSync(filePath, 'utf-8');
    const fm = extractFrontmatter(content);
    for (const field of requiredFields) {
      if (!fm[field]) {
        missingFields.push({
          file: getRelativePath(WIKI_DIR, filePath),
          field
        });
      }
    }
  }

  if (missingFields.length === 0) {
    console.log('  ✅ 前置字段完整');
  } else {
    console.log(`  ⚠️  ${missingFields.length} 个缺失字段:`);
    missingFields.forEach(m => console.log(`    - ${m.file}: 缺少 ${m.field}`));
  }
  console.log('');

  // 检查陈旧内容
  console.log('📅 检查陈旧内容...');
  const staleThreshold = new Date();
  staleThreshold.setDate(staleThreshold.getDate() - 90);
  const stalePages = [];

  for (const filePath of allFiles) {
    const content = readFileSync(filePath, 'utf-8');
    const fm = extractFrontmatter(content);
    if (fm.updated) {
      const updatedDate = new Date(fm.updated);
      if (updatedDate < staleThreshold) {
        stalePages.push({
          file: getRelativePath(WIKI_DIR, filePath),
          updated: fm.updated
        });
      }
    }
  }

  if (stalePages.length === 0) {
    console.log('  ✅ 无陈旧内容');
  } else {
    console.log(`  ⚠️  ${stalePages.length} 个陈旧页面（>90天）:`);
    stalePages.forEach(s => console.log(`    - ${s.file} (更新于 ${s.updated})`));
  }
  console.log('');

  // 生成健康报告
  const report = `# 知识库健康报告

生成时间: ${new Date().toISOString()}

## 概览
- 总页面数: ${conceptFiles.length + entityFiles.length}
- 概念页面: ${conceptFiles.length}
- 实体页面: ${entityFiles.length}

## 检查结果
- 孤立页面: ${orphaned.length}
- 断链: ${brokenLinks.length}
- 缺失前置字段: ${missingFields.length}
- 陈旧内容: ${stalePages.length}

## 问题详情

### 孤立页面
${orphaned.map(f => `- ${f}`).join('\n') || '无'}

### 断链
${brokenLinks.map(l => `- ${l.file} → [[${l.link}]]`).join('\n') || '无'}

### 缺失前置字段
${missingFields.map(m => `- ${m.file}: 缺少 ${m.field}`).join('\n') || '无'}

### 陈旧内容
${stalePages.map(s => `- ${s.file} (更新于 ${s.updated})`).join('\n') || '无'}

## 页面列表

### 概念 (${conceptFiles.length})
${conceptFiles.map(f => `- ${f}`).join('\n')}

### 实体 (${entityFiles.length})
${entityFiles.map(f => `- ${f}`).join('\n')}

---
*由 LLM Wiki Lint Engine 自动生成*
`;

  writeFileSync(join(WIKI_DIR, 'health-report.md'), report, 'utf-8');
  console.log('📄 健康报告已生成: wiki/health-report.md\n');

  console.log('✅ 健康检查完成！\n');
}

lint().catch(console.error);
