#!/usr/bin/env node
/**
 * Auto Memory Search - 自动触发记忆搜索（多维度增强版）
 * 用法：node auto-memory-search.js "用户消息"
 * 功能：检测消息类型，多维度搜索相关记忆
 *
 * 原为 auto-memory-search.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw', 'workspace');
const SESSION_STATE = path.join(WORKSPACE_DIR, 'SESSION-STATE.md');
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');
const MEMORY_MD = path.join(WORKSPACE_DIR, 'MEMORY.md');

// 检测消息类型
function detectType(msg) {
  const lowerMsg = msg.toLowerCase();

  if (/怎么|如何|为什么|什么|哪里|何时|谁|哪个|能否|可以吗|行不行|what|how|why|where|when|who/.test(lowerMsg)) return '疑问';
  if (/修复|bug|错误|问题|故障|解决|repair|fix|error|issue|debug/.test(lowerMsg)) return '修复';
  if (/规范|规则|标准|要求|必须|应该|spec|standard|rule|require/.test(lowerMsg)) return '规范';
  if (/特征|特点|特性|特色|feature|characteristic/.test(lowerMsg)) return '特征';
  if (/配置|设置|安装|部署|环境|config|setup|install|deploy|environment/.test(lowerMsg)) return '配置';
  if (/命令|指令|脚本|用法|example|command|script|usage/.test(lowerMsg)) return '命令';
  if (/\b(css|html|php|javascript|node|npm|tailwind|vite|thinkphp)\b/i.test(lowerMsg)) return '技术';
  return '普通';
}

// 提取搜索关键词
function extractKeywords(msg) {
  const enKeywords = (msg.match(/[A-Za-z0-9_]{2,}/g) || []).slice(0, 5);
  const cnWords = msg
    .split(/[\s,，.。!?！？;；:：]+/)
    .filter(w => w.length >= 2 && /[\u4e00-\u9fa5]/.test(w))
    .slice(0, 5);
  return [...new Set([...enKeywords, ...cnWords])];
}

// 关键词搜索（带上下文）
function searchByKeyword(keyword, file) {
  try {
    if (!fs.existsSync(file)) return '';
    const content = fs.readFileSync(file, 'utf8');
    const lines = content.split('\n');
    const results = [];
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].toLowerCase().includes(keyword.toLowerCase())) {
        const start = Math.max(0, i - 2);
        const end = Math.min(lines.length - 1, i + 2);
        results.push(`📌 "${keyword}" (行 ${i + 1}):\n---\n${lines.slice(start, end + 1).join('\n')}\n---`);
      }
    }
    return results.join('\n\n');
  } catch { return ''; }
}

// 类型标签搜索
function searchByType(msgType, file) {
  try {
    if (!fs.existsSync(file)) return '';
    const content = fs.readFileSync(file, 'utf8');
    const lines = content.split('\n');
    let typeTag = 'episodic';
    if (['修复', '问题', '错误'].includes(msgType)) typeTag = 'procedural';
    else if (['配置', '命令', '技术'].includes(msgType)) typeTag = 'semantic';

    const results = [];
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes(`[${typeTag}]`)) {
        const start = Math.max(0, i - 3);
        const end = Math.min(lines.length - 1, i + 3);
        results.push(`📌 类型标签 [${typeTag}] 相关:\n---\n${lines.slice(start, end + 1).join('\n')}\n---`);
      }
    }
    return results.join('\n\n');
  } catch { return ''; }
}

// 时间维度搜索
function searchByTime(keywords) {
  let results = [];

  // 今日记忆
  const today = new Date().toISOString().slice(0, 10);
  const todayFile = path.join(MEMORY_DIR, 'daily', `${today}.md`);
  if (fs.existsSync(todayFile)) {
    const content = fs.readFileSync(todayFile, 'utf8');
    for (const kw of keywords) {
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(kw.toLowerCase())) {
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length - 1, i + 2);
          results.push(`📍 今日记忆 "${kw}":\n---\n${lines.slice(start, end + 1).join('\n')}\n---`);
          break;
        }
      }
    }
  }

  // 昨日记忆
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const yesterdayFile = path.join(MEMORY_DIR, 'daily', `${yesterday}.md`);
  if (fs.existsSync(yesterdayFile)) {
    const content = fs.readFileSync(yesterdayFile, 'utf8');
    for (const kw of keywords) {
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(kw.toLowerCase())) {
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length - 1, i + 2);
          results.push(`📍 昨日记忆 "${kw}":\n---\n${lines.slice(start, end + 1).join('\n')}\n---`);
          break;
        }
      }
    }
  }

  // 长期记忆
  if (fs.existsSync(MEMORY_MD)) {
    const content = fs.readFileSync(MEMORY_MD, 'utf8');
    for (const kw of keywords) {
      const lines = content.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(kw.toLowerCase())) {
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length - 1, i + 2);
          results.push(`📍 长期记忆 "${kw}":\n---\n${lines.slice(start, end + 1).join('\n')}\n---`);
          break;
        }
      }
    }
  }

  return results.join('\n\n');
}

// 组合搜索
function searchCombined(keywords, file) {
  try {
    if (!fs.existsSync(file) || keywords.length === 0) return '';
    const content = fs.readFileSync(file, 'utf8');
    const lines = content.split('\n');
    const pattern = new RegExp(keywords.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'i');
    const results = [];
    for (let i = 0; i < lines.length; i++) {
      if (pattern.test(lines[i])) {
        const start = Math.max(0, i - 3);
        const end = Math.min(lines.length - 1, i + 3);
        results.push(lines.slice(start, end + 1).join('\n'));
      }
    }
    return results.length > 0 ? `📌 组合搜索结果:\n---\n${results.slice(0, 5).join('\n---\n')}\n---` : '';
  } catch { return ''; }
}

// 主逻辑
function main() {
  const userMessage = process.argv.slice(2).join(' ');
  if (!userMessage) {
    console.log('用法：node auto-memory-search.js "用户消息"');
    process.exit(1);
  }

  // 检查缓存是否存在，不存在则加载记忆
  if (!fs.existsSync(SESSION_STATE)) {
    const loaderPath = path.join(__dirname, 'memory-loader.js');
    if (fs.existsSync(loaderPath)) {
      try { execSync(`node "${loaderPath}"`, { stdio: 'pipe' }); } catch {}
    }
  }

  const msgType = detectType(userMessage);
  if (msgType === '普通') {
    console.log('ℹ️  普通消息，不自动搜索');
    process.exit(0);
  }

  console.log(`📋 消息类型：${msgType}`);

  const keywords = extractKeywords(userMessage);
  if (keywords.length === 0) {
    console.log('⚠️  未提取到关键词');
    process.exit(0);
  }
  console.log(`🔑 关键词：${keywords.join(', ')}`);

  // 多维度搜索
  let allResults = [];

  // 维度 1: 关键词搜索
  for (const kw of keywords) {
    const result = searchByKeyword(kw, SESSION_STATE);
    if (result) allResults.push(result);
  }

  // 维度 2: 类型标签搜索
  const typeResult = searchByType(msgType, SESSION_STATE);
  if (typeResult) allResults.push(typeResult);

  // 维度 3: 时间维度搜索
  const timeResult = searchByTime(keywords);
  if (timeResult) allResults.push(timeResult);

  // 维度 4: 组合搜索
  const combinedResult = searchCombined(keywords, SESSION_STATE);
  if (combinedResult) allResults.push(combinedResult);

  // 输出结果
  if (allResults.length === 0) {
    console.log('📭 未找到相关记忆');
  } else {
    console.log('\n✅ 多维度记忆搜索完成\n');
    console.log(allResults.join('\n\n'));
    console.log('\n---\n以上记忆供参考，根据情况决定是否引用');
  }
}

main();
