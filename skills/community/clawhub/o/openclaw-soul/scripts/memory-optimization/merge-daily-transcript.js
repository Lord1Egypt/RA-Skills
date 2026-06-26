#!/usr/bin/env node
/**
 * Merge Daily Transcript - 每日对话归档脚本（优化版）
 *
 * 新增功能：
 * 1. 智能分类：使用 LLM 自动分类记忆
 * 2. 智能去重：向量相似度 + LLM 语义决策
 * 3. 衰减和晋升：Weibull 衰减 + 三层晋升机制
 * 4. 渐进式索引：构建 L0/L1/L2 三层索引
 *
 * 工作流程：
 * 1. 读取 memory/daily/ 下的所有对话记录
 * 2. 提取关键信息（用户输入、AI 回复、工具调用）
 * 3. 调用 memory-classifier.js 进行智能分类
 * 4. 调用 memory-dedup.js 进行智能去重
 * 5. 更新记忆索引和衰减状态
 * 6. 构建三层索引（L0/L1/L2）
 * 7. 归档到 memory/transcripts/
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const DAILY_DIR = path.join(WORKSPACE, 'memory/daily');
const TRANSCRIPTS_DIR = path.join(WORKSPACE, 'memory/transcripts');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');

// 导入其他模块
const { classifyMemory, processMemory } = require('./memory-classifier.js');
const { deduplicateMemory } = require('./memory-dedup.js');
const { updateAllMemories } = require('./memory-decay.js');
const { buildAllIndexes } = require('./memory-index-builder.js');

/**
 * 提取对话中的关键信息
 */
function extractKeyInfo(dialogContent) {
  const lines = dialogContent.split('\n');
  const memories = [];

  let currentMemory = null;
  let inUserMessage = false;
  let inAssistantMessage = false;

  lines.forEach(line => {
    // 检测用户消息
    if (line.startsWith('User:') || line.startsWith('用户:')) {
      if (currentMemory) {
        memories.push(currentMemory);
      }
      currentMemory = {
        type: 'user_input',
        content: line.replace(/^(User:|用户:)\s*/, ''),
        timestamp: new Date().toISOString()
      };
      inUserMessage = true;
      inAssistantMessage = false;
    }
    // 检测 AI 回复
    else if (line.startsWith('Assistant:') || line.startsWith('AI:')) {
      if (currentMemory) {
        memories.push(currentMemory);
      }
      currentMemory = {
        type: 'assistant_response',
        content: line.replace(/^(Assistant:|AI:)\s*/, ''),
        timestamp: new Date().toISOString()
      };
      inUserMessage = false;
      inAssistantMessage = true;
    }
    // 继续累积内容
    else if (currentMemory && line.trim().length > 0) {
      currentMemory.content += '\n' + line;
    }
  });

  if (currentMemory) {
    memories.push(currentMemory);
  }

  return memories;
}

/**
 * 判断是否值得保存为长期记忆
 */
function isWorthSaving(content) {
  const lower = content.toLowerCase();

  // 过滤噪音
  const noisePatterns = [
    /^(hi|hello|hey|你好|嗨)/i,
    /^(ok|okay|好的|知道了|明白)/i,
    /^(thanks|thank you|谢谢)/i,
    /^(bye|goodbye|再见)/i
  ];

  if (noisePatterns.some(pattern => pattern.test(content.trim()))) {
    return false;
  }

  // 太短的内容不保存
  if (content.length < 20) {
    return false;
  }

  return true;
}

/**
 * 处理单个对话文件
 */
async function processDialogFile(filePath) {
  console.log(`\n处理文件: ${path.basename(filePath)}`);

  const content = fs.readFileSync(filePath, 'utf-8');
  const keyInfo = extractKeyInfo(content);

  console.log(`  提取到 ${keyInfo.length} 条信息`);

  const processedMemories = [];

  for (const info of keyInfo) {
    // 过滤噪音
    if (!isWorthSaving(info.content)) {
      continue;
    }

    try {
      // 1. 智能分类
      const memoryId = `M${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const classified = await processMemory(memoryId, info.content, info.timestamp);

      // 2. 智能去重
      const dedupResult = await deduplicateMemory(classified);

      if (dedupResult.action === 'SKIP') {
        console.log(`  跳过重复记忆: ${memoryId}`);
        continue;
      }

      processedMemories.push(dedupResult.memory);

    } catch (error) {
      console.error(`  处理失败: ${error.message}`);
    }
  }

  return processedMemories;
}

/**
 * 更新记忆索引
 */
function updateMemoryIndex(memories) {
  let index = {
    memories: {},
    tiers: { core: [], working: [], peripheral: [] },
    categories: {
      profiles: [],
      preferences: [],
      entities: [],
      events: [],
      cases: [],
      patterns: []
    }
  };

  if (fs.existsSync(MEMORY_INDEX)) {
    index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  }

  // 更新记忆
  memories.forEach(mem => {
    index.memories[mem.id] = mem;

    // 更新层级索引
    if (!index.tiers[mem.tier]) {
      index.tiers[mem.tier] = [];
    }
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

/**
 * 生成对话摘要
 */
async function generateSummary(memories) {
  if (memories.length === 0) {
    return '（无有效对话）';
  }

  const content = memories.map(m => m.content).join('\n\n');

  const prompt = `请为以下对话生成一个简洁的摘要（1-2 句话）：

${content.substring(0, 2000)}

只返回摘要，不要其他内容。`;

  try {
    const summary = execSync(
      `echo ${JSON.stringify(prompt)} | openclaw chat --model sonnet`,
      { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 }
    );
    return summary.trim();
  } catch (error) {
    console.error('生成摘要失败:', error.message);
    return '（摘要生成失败）';
  }
}

/**
 * 归档到 transcripts
 */
async function archiveToTranscripts(date, memories) {
  if (!fs.existsSync(TRANSCRIPTS_DIR)) {
    fs.mkdirSync(TRANSCRIPTS_DIR, { recursive: true });
  }

  const transcriptFile = path.join(TRANSCRIPTS_DIR, `${date}.md`);

  // 生成摘要
  const summary = await generateSummary(memories);

  let content = `# ${date} 对话记录\n\n`;
  content += `**摘要**: ${summary}\n\n`;
  content += `**记忆数**: ${memories.length} 条\n\n`;
  content += `---\n\n`;

  // 按类别分组
  const byCategory = {};
  memories.forEach(mem => {
    if (!byCategory[mem.category]) {
      byCategory[mem.category] = [];
    }
    byCategory[mem.category].push(mem);
  });

  Object.entries(byCategory).forEach(([category, mems]) => {
    content += `## ${category}\n\n`;
    mems.forEach(mem => {
      content += `### [${mem.id}]\n\n`;
      content += `${mem.content}\n\n`;
      content += `- 重要性: ${mem.importance.toFixed(2)}\n`;
      content += `- 层级: ${mem.tier}\n`;
      if (mem.entities && mem.entities.length > 0) {
        content += `- 实体: ${mem.entities.join(', ')}\n`;
      }
      content += '\n';
    });
  });

  fs.writeFileSync(transcriptFile, content);
  console.log(`✓ 已归档到: ${transcriptFile}`);
}

/**
 * 主流程
 */
async function main() {
  console.log('=== 开始每日对话归档 ===\n');
  console.log(`时间: ${new Date().toISOString()}`);

  // 1. 检查 daily 目录
  if (!fs.existsSync(DAILY_DIR)) {
    console.log('daily 目录不存在，创建中...');
    fs.mkdirSync(DAILY_DIR, { recursive: true });
    console.log('✓ 目录已创建，但暂无对话记录');
    return;
  }

  const files = fs.readdirSync(DAILY_DIR).filter(f => f.endsWith('.md') || f.endsWith('.txt'));

  if (files.length === 0) {
    console.log('暂无对话记录需要归档');
    return;
  }

  console.log(`发现 ${files.length} 个对话文件\n`);

  // 2. 处理所有对话文件
  const allMemories = [];

  for (const file of files) {
    const filePath = path.join(DAILY_DIR, file);
    const memories = await processDialogFile(filePath);
    allMemories.push(...memories);
  }

  console.log(`\n共处理 ${allMemories.length} 条有效记忆`);

  if (allMemories.length === 0) {
    console.log('没有值得保存的记忆');
    return;
  }

  // 3. 更新记忆索引
  updateMemoryIndex(allMemories);

  // 4. 更新衰减状态
  console.log('\n更新衰减状态...');
  updateAllMemories();

  // 5. 构建三层索引
  console.log('\n构建三层索引...');
  buildAllIndexes();

  // 6. 归档到 transcripts
  const today = new Date().toISOString().split('T')[0];
  await archiveToTranscripts(today, allMemories);

  // 7. 清理 daily 目录
  console.log('\n清理 daily 目录...');
  files.forEach(file => {
    const filePath = path.join(DAILY_DIR, file);
    fs.unlinkSync(filePath);
    console.log(`  删除: ${file}`);
  });

  console.log('\n=== 归档完成 ===');
}

// 执行
if (require.main === module) {
  main().catch(error => {
    console.error('归档失败:', error);
    process.exit(1);
  });
}

module.exports = { main, processDialogFile, extractKeyInfo };
