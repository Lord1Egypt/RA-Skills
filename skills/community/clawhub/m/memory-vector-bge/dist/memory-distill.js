/**
 * 记忆蒸馏脚本 (Skill版) v2.0
 * 优化：
 * 1. 可配置 API - 支持环境变量
 * 2. 智能体主导蒸馏 - LLM 判断重要性
 * 3. 标签 + 重要性权重
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

// ============ 配置 (可配置 API) ============
const CONFIG = {
  // Embedding 服务配置
  embedding: {
    url: process.env.EMBEDDING_URL || 'http://localhost:11434/v1/embeddings',
    model: process.env.EMBEDDING_MODEL || 'bge-m3',
    apiKey: process.env.EMBEDDING_API_KEY || ''
  },
  // LLM 服务配置 (用于智能蒸馏)
  llm: {
    url: process.env.LLM_URL || 'http://localhost:11434/v1/chat/completions',
    model: process.env.LLM_MODEL || 'qwen2.5:7b',
    apiKey: process.env.LLM_API_KEY || ''
  },
  // 工作区
  workspace: process.cwd(),
  // 蒸馏参数
  distillDays: parseInt(process.env.DISTILL_DAYS) || 7,
  maxTokens: parseInt(process.env.MAX_TOKENS) || 500
};

// 路径
const WORKSPACE_DIR = CONFIG.workspace;
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');
const VECTOR_DIR = path.join(MEMORY_DIR, 'vector');
const MEMORIES_FILE = path.join(VECTOR_DIR, 'memories.json');
const MEMORY_FILE = path.join(WORKSPACE_DIR, 'MEMORY.md');

console.log('[蒸馏] 配置加载:');
console.log(`  Embedding: ${CONFIG.embedding.url} (${CONFIG.embedding.model})`);
console.log(`  LLM: ${CONFIG.llm.url} (${CONFIG.llm.model})`);
console.log(`  工作区: ${WORKSPACE_DIR}`);

// ============ 通用函数 ============

// HTTP 请求
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

// 获取 Embedding 向量
async function getEmbedding(text) {
  try {
    const result = await httpRequest(CONFIG.embedding.url, {
      model: CONFIG.embedding.model,
      input: text.substring(0, 1000)
    });
    return result.embedding || result.data?.[0]?.embedding;
  } catch (e) {
    console.error(`[蒸馏] Embedding 错误: ${e.message}`);
    return null;
  }
}

// ============ 智能体蒸馏 (NEW) ============

// LLM 判断记忆重要性
async function analyzeWithLLM(content) {
  console.log('[蒸馏] 使用 LLM 智能分析...');
  
  const prompt = `请分析以下对话记录，提取重要信息并打分。

要求输出 JSON 格式：
{
  "importance": 0.0-1.0 之间的分数,
  "keyInfo": ["关键信息1", "关键信息2"],
  "tags": ["标签1", "标签2"],
  "summary": "一句话总结"
}

对话内容：
${content.substring(0, 2000)}`;

  try {
    const result = await httpRequest(CONFIG.llm.url, {
      model: CONFIG.llm.model,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3
    }, 60000);
    
    const response = result.choices?.[0]?.message?.content || '';
    
    // 解析 JSON
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
  } catch (e) {
    console.error(`[蒸馏] LLM 分析失败: ${e.message}`);
  }
  
  // LLM 失败时回退到规则匹配
  return null;
}

// ============ 原有功能 ============

function getMemoryFiles(days = 7) {
  const files = [];
  const now = new Date();
  
  if (!fs.existsSync(MEMORY_DIR)) return files;
  
  const entries = fs.readdirSync(MEMORY_DIR);
  
  for (const entry of entries) {
    if (!entry.match(/^\d{4}-\d{2}-\d{2}\.md$/)) continue;
    
    const filePath = path.join(MEMORY_DIR, entry);
    const fileDate = new Date(entry.replace('.md', ''));
    const daysDiff = Math.floor((now - fileDate) / (1000 * 60 * 60 * 24));
    
    if (daysDiff <= days) {
      files.push({
        name: entry,
        date: fileDate.toISOString().split('T')[0],
        content: fs.readFileSync(filePath, 'utf-8')
      });
    }
  }
  
  return files.sort((a, b) => a.date.localeCompare(b.date));
}

// 过滤敏感信息
function filterSensitiveContent(content) {
  const patterns = [
    /api[_-]?key["']?\s*[:=]\s*["']?[a-zA-Z0-9_-]+["']?/gi,
    /sk-[a-zA-Z0-9]+/g,
    /token["']?\s*[:=]\s*["']?[a-zA-Z0-9_-]+["']?/gi,
    /password["']?\s*[:=]\s*["']?[^\s,"']+["']?/gi,
    /\d{10,}/g
  ];
  
  let filtered = content;
  for (const pattern of patterns) {
    filtered = filtered.replace(pattern, '[FILTERED]');
  }
  return filtered;
}

// 规则匹配 (回退方案)
function ruleBasedAnalysis(content) {
  const lines = content.split('\n');
  const keyPoints = [];
  const tags = new Set();
  
  const tagKeywords = {
    '通勤': ['通勤', '上班', '下班', '地铁'],
    '家庭': ['喜悦', '暖阳', '家人', '孩子'],
    '工作': ['工作', '上课', '讲义'],
    '娱乐': ['电影', '电视', '视频'],
    '配置': ['配置', 'API', '设置']
  };
  
  for (const line of lines) {
    if (line.startsWith('#') || !line.trim()) continue;
    
    // 检测关键词
    if (line.includes('记住') || line.includes('规则') || line.includes('重要')) {
      keyPoints.push(line.trim());
    }
    
    // 检测标签
    for (const [tag, keywords] of Object.entries(tagKeywords)) {
      if (keywords.some(k => content.includes(k))) {
        tags.add(tag);
      }
    }
  }
  
  // 计算重要性分数
  let importance = 0.3;
  if (keyPoints.length > 0) importance += 0.2;
  if (tags.size > 0) importance += 0.2;
  if (content.includes('杜老师')) importance += 0.1;
  if (content.length > 1000) importance += 0.2;
  importance = Math.min(importance, 1.0);
  
  return {
    importance,
    keyInfo: keyPoints.slice(0, 10),
    tags: [...tags],
    summary: content.substring(0, 100)
  };
}

// ============ 主函数 ============

async function distillMemory(days = 7) {
  console.log(`\n[蒸馏] 开始处理最近 ${days} 天的日志...`);
  
  const files = getMemoryFiles(days);
  console.log(`[蒸馏] 找到 ${files.length} 个日志文件`);
  
  if (files.length === 0) {
    console.log('[蒸馏] 没有需要处理的日志');
    return;
  }
  
  // 加载现有记忆
  let memories = { 
    version: '2.0', 
    updated: new Date().toISOString(), 
    memories: [], 
    index: { byTag: {}, byImportance: [] },
    config: CONFIG
  };
  
  if (fs.existsSync(MEMORIES_FILE)) {
    try {
      const existing = JSON.parse(fs.readFileSync(MEMORIES_FILE, 'utf-8'));
      // 迁移旧版本
      if (!existing.config) {
        memories.memories = existing.memories || [];
        memories.index = existing.index || { byTag: {}, byImportance: [] };
      } else {
        memories = existing;
      }
    } catch (e) {
      console.log('[蒸馏] 创建新的记忆库');
    }
  }
  
  // 处理每个文件
  let newCount = 0;
  
  for (const file of files) {
    console.log(`\n[蒸馏] 处理: ${file.name}`);
    
    if (memories.index[file.name]) {
      console.log(`  -> 已处理，跳过`);
      continue;
    }
    
    // 1. 智能分析 (优先) 或回退到规则
    let analysis = await analyzeWithLLM(file.content);
    if (!analysis) {
      console.log(`  -> 使用规则匹配分析`);
      analysis = ruleBasedAnalysis(file.content);
    } else {
      console.log(`  -> LLM 智能分析完成 (重要性: ${analysis.importance})`);
    }
    
    // 2. 生成向量
    console.log(`  -> 生成向量...`);
    const embedding = await getEmbedding(file.content);
    
    if (!embedding) {
      console.error(`  -> 向量生成失败，跳过`);
      continue;
    }
    
    // 3. 构建记忆对象
    const memory = {
      id: `${file.date}-${Date.now()}`,
      content: filterSensitiveContent(file.content).substring(0, 500),
      keyInfo: analysis.keyInfo || [],
      tags: analysis.tags || [],
      importance: analysis.importance || 0.5,  // NEW: 重要性权重
      summary: analysis.summary || file.content.substring(0, 100),
      embedding: embedding,
      source: file.name,
      created: new Date().toISOString()
    };
    
    memories.memories.push(memory);
    memories.index[file.name] = memory.id;
    
    // 4. 更新索引
    for (const tag of memory.tags) {
      if (!memories.index.byTag[tag]) memories.index.byTag[tag] = [];
      memories.index.byTag[tag].push(memory.id);
    }
    memories.index.byImportance.push({ id: memory.id, importance: memory.importance });
    
    // 按重要性排序
    memories.index.byImportance.sort((a, b) => b.importance - a.importance);
    
    console.log(`  -> 新增 [${memory.tags.join(', ')}] 重要性: ${memory.importance}`);
    newCount++;
  }
  
  // 保存
  if (newCount > 0) {
    memories.updated = new Date().toISOString();
    
    if (!fs.existsSync(VECTOR_DIR)) {
      fs.mkdirSync(VECTOR_DIR, { recursive: true });
    }
    
    fs.writeFileSync(MEMORIES_FILE, JSON.stringify(memories, null, 2));
    console.log(`\n[蒸馏] 已保存 ${newCount} 条新记忆`);
  }
  
  // 更新 MEMORY.md
  await updateMemoryCore(memories);
  
  console.log('\n[蒸馏] 完成!');
}

// 更新 MEMORY.md
async function updateMemoryCore(memories) {
  console.log('[蒸馏] 更新 MEMORY.md...');
  
  // 按重要性排序，取前10条
  const byImportance = memories.index?.byImportance || [];
  const topMemories = byImportance.slice(0, 10);
  
  let content = `# 杜老师核心记忆准则 (自动蒸馏 v2.0)

> 最后更新: ${new Date().toISOString().split('T')[0]}
> 记忆向量库: ${memories.memories.length} 条

---

## 🏠 家庭信息
- 喜悦 (6岁), 暖阳 (1岁)
- 家庭住址: 番禺区正太广场

## 🚇 通勤规则
- 纯地铁，不坐公交
- 起点: 正太广场 → 市桥站 → 汉溪长隆(换7号线) → 萝岗站

## 📌 重要记忆 (Top 10)
`;
  
  for (const item of topMemories) {
    const mem = memories.memories.find(m => m.id === item.id);
    if (mem) {
      content += `\n### ${mem.source} (重要性: ${(mem.importance * 100).toFixed(0)}%)\n`;
      content += `${mem.summary}\n`;
      content += `标签: ${mem.tags.join(', ')}\n`;
    }
  }
  
  content += `\n---\n*此文件由自动蒸馏生成，定期更新核心准则以控制 Token 消耗*`;
  
  fs.writeFileSync(MEMORY_FILE, content);
  console.log('[蒸馏] MEMORY.md 已更新');
}

// 运行
const days = parseInt(process.argv[2]) || CONFIG.distillDays;
distillMemory(days).catch(console.error);