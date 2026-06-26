#!/usr/bin/env node

/**
 * vv 记忆语义搜索脚本
 * 
 * 功能：在 vv 的记忆系统中搜索相关内容
 * 支持：--user（个人记忆）、--repo（项目记忆）、--both（默认，全部搜索）
 * 
 * 用法：
 *   node search-memory.cjs [--user|--repo|--both] "搜索关键词"
 * 
 * 示例：
 *   node search-memory.cjs "昨天做了什么"
 *   node search-memory.cjs --repo "认证实现"
 *   node search-memory.cjs --user "编码偏好"
 */

const fs = require('fs');
const path = require('path');

// 配置
const WORKSPACE = process.env.WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const LEARNINGS_DIR = path.join(WORKSPACE, '.learnings');
const ARCHIVE_DIR = path.join(MEMORY_DIR, '.archive');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m'
};

function log(color, text) {
  console.log(`${color}${text}${colors.reset}`);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  let scope = 'both'; // user | repo | both
  let query = '';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--user') {
      scope = 'user';
    } else if (args[i] === '--repo') {
      scope = 'repo';
    } else if (args[i] === '--both') {
      scope = 'both';
    } else if (!args[i].startsWith('-')) {
      query = args[i];
    }
  }

  return { scope, query };
}

// 计算相关性分数
function calculateRelevance(content, query) {
  const queryTerms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
  const contentLower = content.toLowerCase();
  
  let score = 0;
  for (const term of queryTerms) {
    if (contentLower.includes(term)) {
      score++;
    }
  }
  
  // 标题匹配加分
  const titleMatch = content.split('\n')[0].toLowerCase();
  if (titleMatch.includes(query.toLowerCase())) {
    score += 3;
  }
  
  return score;
}

// 搜索文件
function searchFile(filePath, query) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const score = calculateRelevance(content, query);
    
    if (score > 0) {
      // 提取相关片段
      const lines = content.split('\n');
      const relevantLines = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.toLowerCase().includes(query.toLowerCase())) {
          // 获取上下文（前后各 2 行）
          const start = Math.max(0, i - 2);
          const end = Math.min(lines.length, i + 3);
          relevantLines.push({
            line: i + 1,
            context: lines.slice(start, end).join('\n')
          });
        }
      }
      
      return {
        file: filePath,
        score,
        matches: relevantLines,
        preview: content.substring(0, 200).replace(/\n/g, ' ') + '...'
      };
    }
  } catch (err) {
    // 忽略读取错误
  }
  
  return null;
}

// 搜索目录
function searchDirectory(dir, query, maxResults = 10) {
  const results = [];
  
  if (!fs.existsSync(dir)) {
    return results;
  }
  
  const files = fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .map(f => path.join(dir, f));
  
  for (const file of files) {
    const result = searchFile(file, query);
    if (result && result.score > 0) {
      results.push(result);
    }
    
    if (results.length >= maxResults) {
      break;
    }
  }
  
  // 按相关性排序
  return results.sort((a, b) => b.score - a.score);
}

// 主搜索函数
function searchMemory(query, scope) {
  log(colors.blue, '═══════════════════════════════════════');
  log(colors.cyan, `  vv 记忆搜索：${query}`);
  log(colors.blue, '═══════════════════════════════════════\n');
  
  const allResults = [];
  
  // 搜索范围
  const scopes = {
    user: [
      { dir: MEMORY_DIR, label: '📝 每日记忆' },
      { dir: LEARNINGS_DIR, label: '📚 学习记录' }
    ],
    repo: [
      { dir: path.join(WORKSPACE, 'projects'), label: '📁 项目记忆' }
    ],
    both: [
      { dir: MEMORY_DIR, label: '📝 每日记忆' },
      { dir: LEARNINGS_DIR, label: '📚 学习记录' },
      { dir: path.join(WORKSPACE, 'projects'), label: '📁 项目记忆' }
    ]
  };
  
  const searchTargets = scopes[scope] || scopes.both;
  
  for (const { dir, label } of searchTargets) {
    if (!fs.existsSync(dir)) continue;
    
    log(colors.yellow, `${label} (${dir})`);
    log(colors.gray, '───────────────────────────────────────');
    
    const results = searchDirectory(dir, query, 5);
    
    if (results.length === 0) {
      log(colors.gray, '  无匹配结果\n');
      continue;
    }
    
    for (const result of results) {
      const relPath = path.relative(WORKSPACE, result.file);
      log(colors.green, `  [${result.score}分] ${relPath}`);
      log(colors.gray, `    ${result.preview}\n`);
    }
    
    allResults.push(...results);
  }
  
  // 总结
  log(colors.blue, '═══════════════════════════════════════');
  log(colors.cyan, `  找到 ${allResults.length} 条相关记忆`);
  log(colors.blue, '═══════════════════════════════════════');
  
  return allResults;
}

// 执行
const { scope, query } = parseArgs();

if (!query) {
  console.error('用法：node search-memory.cjs [--user|--repo|--both] "搜索关键词"');
  console.error('示例：node search-memory.cjs "昨天做了什么"');
  process.exit(1);
}

searchMemory(query, scope);
