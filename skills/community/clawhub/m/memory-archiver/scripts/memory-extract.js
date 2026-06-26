#!/usr/bin/env node
/**
 * Auto-Memory 提取脚本
 * 从对话内容中提取持久记忆，分类存储
 * 
 * 用法:
 *   node extract.js "<内容>" [--type <type>] [--tags <tag1,tag2>]
 *   node extract.js --scan "<目录>"  扫描目录中的文件提取记忆
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const MEMORY_DIR = WORKSPACE + '/memory/auto';
const MEMORY_INDEX = WORKSPACE + '/MEMORY.md';
const MAX_INDEX_LINES = 200;
const MAX_INDEX_BYTES = 25000;

const MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];

// 确保目录存在
function ensureDirs() {
  for (const type of MEMORY_TYPES) {
    const dir = path.join(MEMORY_DIR, type);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

// 生成记忆文件名
function generateFilename(type, title) {
  const slug = title
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, '_')
    .replace(/^_|_$/g, '')
    .substring(0, 50);
  const hash = crypto.randomBytes(4).toString('hex');
  return `${slug}_${hash}.md`;
}

// 计算内容 hash（用于去重）
function contentHash(content) {
  return crypto.createHash('md5').update(content.trim()).digest('hex');
}

// 去重检查
function isDuplicate(type, content) {
  const dir = path.join(MEMORY_DIR, type);
  if (!fs.existsSync(dir)) return false;
  
  const hash = contentHash(content);
  const hashFile = path.join(dir, '.hashes.json');
  
  let hashes = {};
  if (fs.existsSync(hashFile)) {
    try {
      hashes = JSON.parse(fs.readFileSync(hashFile, 'utf8'));
    } catch (e) {
      hashes = {};
    }
  }
  
  if (hashes[hash]) {
    console.log(`[去重] 发现重复内容，跳过: ${hash}`);
    return true;
  }
  
  return false;
}

// 记录 hash
function recordHash(type, content, filename) {
  const dir = path.join(MEMORY_DIR, type);
  const hashFile = path.join(dir, '.hashes.json');
  
  let hashes = {};
  if (fs.existsSync(hashFile)) {
    try {
      hashes = JSON.parse(fs.readFileSync(hashFile, 'utf8'));
    } catch (e) {}
  }
  
  hashes[contentHash(content)] = filename;
  fs.writeFileSync(hashFile, JSON.stringify(hashes, null, 2));
}

// 写入记忆文件
function writeMemory(type, title, content, tags = []) {
  ensureDirs();
  
  if (isDuplicate(type, content)) {
    return { success: false, reason: 'duplicate' };
  }
  
  const filename = generateFilename(type, title);
  const filepath = path.join(MEMORY_DIR, type, filename);
  
  const now = new Date().toISOString().split('T')[0];
  const memoryContent = `---
type: ${type}
created: ${now}
tags: [${tags.join(', ')}]
---

# ${title}

${content}
`;
  
  fs.writeFileSync(filepath, memoryContent, 'utf8');
  recordHash(type, content, filename);
  
  console.log(`[记忆写入] ${type}/${filename}`);
  return { success: true, type, filename, filepath };
}

// 更新 MEMORY.md 索引
function updateIndex() {
  if (!fs.existsSync(MEMORY_INDEX)) {
    fs.writeFileSync(MEMORY_INDEX, '# MEMORY.md - 长期记忆\n\n> 精选知识与模式\n\n---\n', 'utf8');
    return;
  }
  
  let content = fs.readFileSync(MEMORY_INDEX, 'utf8');
  
  // 查找索引部分
  const indexMarker = '## 记忆索引';
  let indexStart = content.indexOf(indexMarker);
  
  if (indexStart === -1) {
    // 添加索引标记
    content += '\n## 记忆索引\n\n_由 Auto-Memory 自动维护_\n\n';
    indexStart = content.indexOf('## 记忆索引');
  }
  
  // 重建索引
  const entries = [];
  for (const type of MEMORY_TYPES) {
    const dir = path.join(MEMORY_DIR, type);
    if (!fs.existsSync(dir)) continue;
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    if (files.length === 0) continue;
    
    entries.push(`### ${type}\n`);
    for (const file of files.slice(0, 10)) { // 每类型最多 10 条
      const filepath = path.join(dir, file);
      const fileContent = fs.readFileSync(filepath, 'utf8');
      const titleMatch = fileContent.match(/^# (.+)$/m);
      const tagsMatch = fileContent.match(/^tags: \[(.+?)\]$/m);
      const title = titleMatch ? titleMatch[1] : file;
      const tags = tagsMatch ? tagsMatch[1] : '';
      entries.push(`- [${title}](memory/auto/${type}/${file}) ${tags ? '`' + tags + '`' : ''}`);
    }
    entries.push('');
  }
  
  const newIndex = entries.join('\n');
  
  // 替换旧索引
  const nextSection = content.indexOf('\n## ', indexStart + 1);
  const beforeIndex = content.substring(0, indexStart);
  const afterIndex = nextSection !== -1 ? content.substring(nextSection) : '';
  
  content = beforeIndex + '## 记忆索引\n\n_由 Auto-Memory 自动维护_\n\n' + newIndex + afterIndex;
  
  // 检查大小限制
  const lines = content.split('\n');
  if (lines.length > MAX_INDEX_LINES) {
    content = lines.slice(0, MAX_INDEX_LINES).join('\n');
  }
  if (Buffer.byteLength(content, 'utf8') > MAX_INDEX_BYTES) {
    content = content.substring(0, MAX_INDEX_BYTES);
  }
  
  fs.writeFileSync(MEMORY_INDEX, content, 'utf8');
  console.log(`[索引更新] MEMORY.md 已更新`);
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法: node extract.js "<内容>" [--type <type>] [--tags <tag1,tag2>]');
    console.log('      node extract.js --update-index');
    process.exit(1);
  }
  
  if (args[0] === '--update-index') {
    updateIndex();
    return;
  }
  
  // 解析参数
  let content = '';
  let type = 'project'; // 默认类型
  let tags = [];
  let title = '';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--type' && i + 1 < args.length) {
      type = args[++i];
      if (!MEMORY_TYPES.includes(type)) {
        console.error(`错误: 未知类型 "${type}"，可选: ${MEMORY_TYPES.join(', ')}`);
        process.exit(1);
      }
    } else if (args[i] === '--tags' && i + 1 < args.length) {
      tags = args[++i].split(',').map(t => t.trim());
    } else if (args[i] === '--title' && i + 1 < args.length) {
      title = args[++i];
    } else {
      content += args[i] + ' ';
    }
  }
  
  content = content.trim();
  if (!content) {
    console.error('错误: 内容为空');
    process.exit(1);
  }
  
  if (!title) {
    title = content.substring(0, 30) + (content.length > 30 ? '...' : '');
  }
  
  const result = writeMemory(type, title, content, tags);
  
  if (result.success) {
    updateIndex();
    console.log(`✅ 记忆已保存: ${result.filepath}`);
  } else {
    console.log(`⏭️ 跳过: ${result.reason}`);
  }
}

main();
