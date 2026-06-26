#!/usr/bin/env node
/**
 * 记忆去重脚本
 * 检查内容是否已存在，支持模糊匹配
 * 
 * 用法: node dedup.js "<内容>" [类型]
 * 输出: {"duplicate": true, "existing": "文件名"} | {"duplicate": false}
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const MEMORY_DIR = WORKSPACE + '/memory/auto';

// 精确去重：MD5 hash
function exactHash(content) {
  return crypto.createHash('md5').update(content.trim()).digest('hex');
}

// 模糊去重：提取关键词后比较
function fuzzyMatch(content, type) {
  // 提取关键词（中文词组 + 英文单词）
  const keywords = content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/g) || [];
  if (keywords.length < 3) return null;
  
  const dir = path.join(MEMORY_DIR, type);
  if (!fs.existsSync(dir)) return null;
  
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
  
  for (const file of files) {
    const filepath = path.join(dir, file);
    const fileContent = fs.readFileSync(filepath, 'utf8');
    
    // 计算关键词重叠率
    const fileKeywords = fileContent.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/g) || [];
    const overlap = keywords.filter(k => fileKeywords.includes(k));
    const overlapRate = overlap.length / Math.max(keywords.length, fileKeywords.length);
    
    if (overlapRate > 0.7) {
      // 进一步检查核心内容相似度
      const titleMatch = fileContent.match(/^# (.+)$/m);
      return { file, title: titleMatch ? titleMatch[1] : file, overlapRate };
    }
  }
  
  return null;
}

function check(content, type = null) {
  const hash = exactHash(content);
  
  // 检查所有类型或指定类型
  const types = type ? [type] : ['user', 'feedback', 'project', 'reference'];
  
  for (const t of types) {
    const dir = path.join(MEMORY_DIR, t);
    const hashFile = path.join(dir, '.hashes.json');
    
    if (fs.existsSync(hashFile)) {
      try {
        const hashes = JSON.parse(fs.readFileSync(hashFile, 'utf8'));
        if (hashes[hash]) {
          return { duplicate: true, type: t, file: hashes[hash], method: 'exact' };
        }
      } catch (e) {}
    }
    
    // 模糊匹配
    const fuzzy = fuzzyMatch(content, t);
    if (fuzzy) {
      return { duplicate: true, type: t, file: fuzzy.file, title: fuzzy.title, method: 'fuzzy', overlapRate: fuzzy.overlapRate };
    }
  }
  
  return { duplicate: false };
}

function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.log('用法: node dedup.js "<内容>" [类型]');
    process.exit(1);
  }
  
  const content = args[0];
  const type = args[1] || null;
  
  const result = check(content, type);
  console.log(JSON.stringify(result, null, 2));
}

main();
