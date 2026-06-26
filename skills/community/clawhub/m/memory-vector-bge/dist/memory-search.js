/**
 * 记忆搜索脚本 (Skill版) v2.0
 * 优化：
 * 1. 可配置 API
 * 2. 支持按标签筛选
 * 3. 支持按重要性筛选
 * 4. 语义搜索 + 过滤
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

// ============ 配置 (可配置 API) ============
const CONFIG = {
  embedding: {
    url: process.env.EMBEDDING_URL || 'http://localhost:11434/v1/embeddings',
    model: process.env.EMBEDDING_MODEL || 'bge-m3',
    apiKey: process.env.EMBEDDING_API_KEY || ''
  }
};

// 路径
const WORKSPACE_DIR = process.cwd();
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');
const VECTOR_DIR = path.join(MEMORY_DIR, 'vector');
const MEMORIES_FILE = path.join(VECTOR_DIR, 'memories.json');

console.log('[搜索] 配置:');
console.log(`  Embedding: ${CONFIG.embedding.url} (${CONFIG.embedding.model})`);

// ============ 通用函数 ============

function httpRequest(url, data, timeout = 30000) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const isHttps = urlObj.protocol === 'https:';
    const lib = isHttps ? https : http;
    
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || (isHttps ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': CONFIG.embedding.apiKey ? `Bearer ${CONFIG.embedding.apiKey}` : ''
      },
      timeout
    };
    
    const req = lib.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => reject(new Error('Request timeout')));
    req.write(JSON.stringify(data));
    req.end();
  });
}

async function getEmbedding(text) {
  try {
    const result = await httpRequest(CONFIG.embedding.url, {
      model: CONFIG.embedding.model,
      input: text.substring(0, 1000)
    });
    return result.embedding || result.data?.[0]?.embedding;
  } catch (e) {
    console.error(`[搜索] Embedding 错误: ${e.message}`);
    return null;
  }
}

// 余弦相似度
function cosineSimilarity(a, b) {
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  
  for (let i = 0; i < a.length && i < b.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// ============ 搜索功能 ============

async function searchMemory(query, options = {}) {
  const {
    tag = null,           // 按标签筛选
    minImportance = 0,    // 最低重要性 0-1
    topK = 5,             // 返回数量
    debug = false
  } = options;
  
  console.log(`\n🔍 搜索: "${query}"`);
  console.log(`   标签: ${tag || '全部'}`);
  console.log(`   最低重要性: ${(minImportance * 100).toFixed(0)}%`);
  console.log('='.repeat(50));
  
  if (!fs.existsSync(MEMORIES_FILE)) {
    console.log('❌ 记忆库不存在');
    console.log('   运行: node memory-distill.js');
    return;
  }
  
  const memories = JSON.parse(fs.readFileSync(MEMORIES_FILE, 'utf-8'));
  
  console.log(`📚 记忆库: ${memories.memories.length} 条`);
  console.log(`🏷️ 可用标签: ${Object.keys(memories.index?.byTag || {}).join(', ')}\n`);
  
  // 获取查询向量
  const queryEmbedding = await getEmbedding(query);
  if (!queryEmbedding) {
    console.log('❌ 向量生成失败');
    return;
  }
  
  // 筛选 + 计算相似度
  const results = [];
  
  for (const memory of memories.memories) {
    if (!memory.embedding) continue;
    
    // 按标签筛选
    if (tag && (!memory.tags || !memory.tags.includes(tag))) {
      continue;
    }
    
    // 按重要性筛选
    if (memory.importance < minImportance) {
      continue;
    }
    
    // 计算语义相似度
    const similarity = cosineSimilarity(queryEmbedding, memory.embedding);
    
    // 综合评分 = 语义相似度 * 0.7 + 重要性 * 0.3
    const score = similarity * 0.7 + (memory.importance || 0.5) * 0.3;
    
    results.push({
      ...memory,
      similarity,
      score
    });
  }
  
  // 排序
  results.sort((a, b) => b.score - a.score);
  
  if (results.length === 0) {
    console.log('❌ 没有找到匹配的记录');
    return;
  }
  
  // 输出结果
  console.log(`\n📊 找到 ${results.length} 条相关记忆 (显示 Top ${topK}):\n`);
  
  for (let i = 0; i < Math.min(topK, results.length); i++) {
    const r = results[i];
    const importanceBar = '█'.repeat(Math.floor((r.importance || 0.5) * 10)) + '░'.repeat(10 - Math.floor((r.importance || 0.5) * 10));
    
    console.log(`┌─ ${i + 1}. ${r.source}`);
    console.log(`│  相似度: ${(r.similarity * 100).toFixed(1)}% | 重要性: ${importanceBar} (${(r.importance * 100).toFixed(0)}%)`);
    console.log(`│  标签: ${r.tags?.join(', ') || '无'}`);
    console.log(`│  摘要: ${r.summary?.substring(0, 60)}...`);
    if (r.keyInfo?.length > 0) {
      console.log(`│  关键: ${r.keyInfo[0].substring(0, 50)}`);
    }
    console.log(`└${'─'.repeat(48)}`);
  }
  
  console.log('\n' + '='.repeat(50));
  
  if (debug) {
    console.log('\n📋 原始数据:');
    console.log(JSON.stringify(results.slice(0, 2), null, 2));
  }
}

// ============ 命令行 ============

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  console.log(`
============================================
   记忆向量搜索 v2.0 (BGE-M3)
============================================

用法: node memory-search.js [选项] "搜索内容"

选项:
  --tag <标签>          按标签筛选 (如: 家庭, 工作)
  --min-importance <0-1>  最低重要性 (如: 0.5)
  --top <数量>          返回数量 (默认: 5)
  --debug               显示调试信息
  --tags                显示所有可用标签
  --list                列出所有记忆

示例:
  node memory-search.js "家庭信息"
  node memory-search.js "工作配置" --tag 工作
  node memory-search.js "重要的事情" --min-importance 0.7
  node memory-search.js --tags
  `);
  process.exit(1);
}

// 特殊命令
if (args[0] === '--tags') {
  if (fs.existsSync(MEMORIES_FILE)) {
    const memories = JSON.parse(fs.readFileSync(MEMORIES_FILE, 'utf-8'));
    const tags = Object.keys(memories.index?.byTag || {});
    console.log('\n🏷️ 可用标签:');
    console.log(tags.length ? tags.join(', ') : '无');
    
    // 统计每个标签的数量
    console.log('\n📊 标签统计:');
    for (const tag of tags) {
      const ids = memories.index.byTag[tag] || [];
      console.log(`  ${tag}: ${ids.length} 条`);
    }
  }
  process.exit(1);
}

if (args[0] === '--list') {
  if (fs.existsSync(MEMORIES_FILE)) {
    const memories = JSON.parse(fs.readFileSync(MEMORIES_FILE, 'utf-8'));
    console.log('\n📚 所有记忆:');
    for (const m of memories.memories) {
      const imp = (m.importance || 0.5) * 100;
      console.log(`  ${m.source} - ${m.tags?.join(', ') || '无'} - 重要性: ${imp.toFixed(0)}%`);
    }
  }
  process.exit(1);
}

// 解析选项和搜索词
let options = { topK: 5, minImportance: 0 };
let query = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--tag' && args[i + 1]) {
    options.tag = args[i + 1];
    i++;
  } else if (args[i] === '--min-importance' && args[i + 1]) {
    options.minImportance = parseFloat(args[i + 1]);
    i++;
  } else if (args[i] === '--top' && args[i + 1]) {
    options.topK = parseInt(args[i + 1]);
    i++;
  } else if (args[i] === '--debug') {
    options.debug = true;
  } else if (!args[i].startsWith('--')) {
    query = args[i];
  }
}

if (!query) {
  console.log('❌ 请输入搜索内容');
  console.log('   用法: node memory-search.js "搜索内容"');
  process.exit(1);
}

searchMemory(query, options).catch(console.error);