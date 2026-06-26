#!/usr/bin/env node
/**
 * Memory Classifier - 智能记忆分类器
 * 使用 LLM 自动将记忆分类为 6 种类型：
 * - profiles: 用户的角色、背景、身份信息
 * - preferences: 用户的偏好、习惯、风格
 * - entities: 人物、项目、概念等实体
 * - events: 发生的事件、对话、活动
 * - cases: 案例、经验、教训
 * - patterns: 模式、规律、方法论
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');

/**
 * 调用 LLM 进行分类
 */
async function classifyMemory(content) {
  const prompt = `你是一个记忆分类专家。请将以下记忆内容分类到最合适的类别中。

记忆内容：
${content}

类别定义：
- profiles: 用户的角色、背景、身份信息（例如："用户是产品经理"）
- preferences: 用户的偏好、习惯、风格（例如："用户偏好简洁直接的沟通"）
- entities: 人物、项目、概念等实体（例如："项目 X 使用 React 技术栈"）
- events: 发生的事件、对话、活动（例如："2026-03-30 讨论了记忆系统优化"）
- cases: 案例、经验、教训（例如："上次用 A 方案失败了，改用 B 方案成功"）
- patterns: 模式、规律、方法论（例如："用户习惯先做调研再动手"）

请以 JSON 格式返回分类结果：
{
  "category": "类别名称",
  "confidence": 0.95,
  "reasoning": "分类理由",
  "entities": ["提取的实体1", "实体2"],
  "importance": 0.8,
  "tags": ["标签1", "标签2"]
}

importance 评分标准（0-1）：
- 0.9-1.0: 核心身份信息、关键偏好、重要决策
- 0.7-0.9: 重要项目信息、有价值的经验
- 0.5-0.7: 一般性对话、常规事件
- 0.3-0.5: 琐碎信息、临时性内容
- 0.0-0.3: 噪音、无关信息

只返回 JSON，不要其他内容。`;

  try {
    // 使用 openclaw CLI 调用 LLM
    const result = execSync(
      `echo ${JSON.stringify(prompt)} | openclaw chat --model sonnet --format json`,
      { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 }
    );

    return JSON.parse(result.trim());
  } catch (error) {
    console.error('LLM 分类失败:', error.message);
    // Fallback: 基于关键词的简单分类
    return fallbackClassify(content);
  }
}

/**
 * Fallback 分类器（基于关键词）
 */
function fallbackClassify(content) {
  const lower = content.toLowerCase();

  // 关键词匹配
  const patterns = {
    profiles: ['我是', '用户是', '角色', '职业', '背景', '身份'],
    preferences: ['偏好', '喜欢', '习惯', '风格', '倾向', '不喜欢'],
    entities: ['项目', '技术栈', '工具', '框架', '系统', '产品'],
    events: ['讨论', '完成', '开始', '发生', '今天', '昨天'],
    cases: ['经验', '教训', '案例', '失败', '成功', '尝试'],
    patterns: ['模式', '规律', '方法', '流程', '习惯性', '通常']
  };

  let maxScore = 0;
  let category = 'events'; // 默认分类

  for (const [cat, keywords] of Object.entries(patterns)) {
    const score = keywords.filter(kw => lower.includes(kw)).length;
    if (score > maxScore) {
      maxScore = score;
      category = cat;
    }
  }

  return {
    category,
    confidence: maxScore > 0 ? 0.6 : 0.3,
    reasoning: 'Fallback 关键词匹配',
    entities: [],
    importance: 0.5,
    tags: []
  };
}

/**
 * 提取实体（人名、项目名、概念）
 */
function extractEntities(content) {
  // 简单的实体提取：大写开头的词、引号中的内容
  const entities = new Set();

  // 提取引号中的内容
  const quoted = content.match(/["「『]([^"」』]+)["」』]/g);
  if (quoted) {
    quoted.forEach(q => entities.add(q.replace(/["「『」』]/g, '')));
  }

  // 提取大写开头的词（可能是专有名词）
  const capitalized = content.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g);
  if (capitalized) {
    capitalized.forEach(c => entities.add(c));
  }

  return Array.from(entities);
}

/**
 * 处理单条记忆
 */
async function processMemory(memoryId, content, timestamp) {
  console.log(`\n处理记忆 ${memoryId}...`);

  // 调用 LLM 分类
  const classification = await classifyMemory(content);

  // 提取实体
  const entities = extractEntities(content);

  // 构建记忆元数据
  const metadata = {
    id: memoryId,
    content,
    timestamp,
    category: classification.category,
    confidence: classification.confidence,
    importance: classification.importance,
    entities: [...new Set([...classification.entities, ...entities])],
    tags: classification.tags,
    reasoning: classification.reasoning,

    // 衰减和晋升相关字段
    tier: classification.importance >= 0.8 ? 'core' :
          classification.importance >= 0.5 ? 'working' : 'peripheral',
    access_count: 0,
    last_access: timestamp,
    created_at: timestamp,
    decay_half_life: classification.importance >= 0.8 ? 90 : 30, // 天
  };

  console.log(`  分类: ${classification.category}`);
  console.log(`  重要性: ${classification.importance.toFixed(2)}`);
  console.log(`  层级: ${metadata.tier}`);
  console.log(`  实体: ${metadata.entities.join(', ') || '无'}`);

  return metadata;
}

/**
 * 批量处理记忆
 */
async function batchClassify(memories) {
  const results = [];

  for (const memory of memories) {
    try {
      const metadata = await processMemory(
        memory.id,
        memory.content,
        memory.timestamp
      );
      results.push(metadata);
    } catch (error) {
      console.error(`处理记忆 ${memory.id} 失败:`, error.message);
    }
  }

  return results;
}

/**
 * 更新记忆索引
 */
function updateMemoryIndex(memories) {
  let index = { memories: {}, tiers: { core: [], working: [], peripheral: [] }, categories: {} };

  if (fs.existsSync(MEMORY_INDEX)) {
    index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  }

  // 更新记忆
  memories.forEach(mem => {
    index.memories[mem.id] = mem;

    // 更新层级索引
    if (!index.tiers[mem.tier].includes(mem.id)) {
      index.tiers[mem.tier].push(mem.id);
    }

    // 更新分类索引
    if (!index.categories[mem.category]) {
      index.categories[mem.category] = [];
    }
    if (!index.categories[mem.category].includes(mem.id)) {
      index.categories[mem.category].push(mem.id);
    }
  });

  index.total_memories = Object.keys(index.memories).length;
  index.last_updated = new Date().toISOString();
  index.version = '2.0.0';

  fs.writeFileSync(MEMORY_INDEX, JSON.stringify(index, null, 2));
  console.log(`\n✓ 记忆索引已更新: ${index.total_memories} 条记忆`);
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: node memory-classifier.js <记忆文件路径>');
    console.log('或者: echo "记忆内容" | node memory-classifier.js --stdin');
    process.exit(1);
  }

  (async () => {
    if (args[0] === '--stdin') {
      // 从标准输入读取
      const content = fs.readFileSync(0, 'utf-8').trim();
      const memoryId = `M${Date.now()}`;
      const timestamp = new Date().toISOString();

      const metadata = await processMemory(memoryId, content, timestamp);
      updateMemoryIndex([metadata]);

      console.log('\n分类结果:');
      console.log(JSON.stringify(metadata, null, 2));
    } else {
      // 从文件读取
      const filePath = args[0];
      if (!fs.existsSync(filePath)) {
        console.error(`文件不存在: ${filePath}`);
        process.exit(1);
      }

      const content = fs.readFileSync(filePath, 'utf-8');
      const memories = JSON.parse(content); // 假设是 JSON 数组

      const results = await batchClassify(memories);
      updateMemoryIndex(results);

      console.log(`\n✓ 完成！共处理 ${results.length} 条记忆`);
    }
  })();
}

module.exports = { classifyMemory, processMemory, batchClassify, updateMemoryIndex };
