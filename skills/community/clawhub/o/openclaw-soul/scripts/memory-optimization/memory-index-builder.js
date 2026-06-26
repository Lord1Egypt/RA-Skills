#!/usr/bin/env node
/**
 * Memory Index Builder - 渐进式披露索引构建器
 *
 * 三层索引结构（借鉴 claude-mem 和 OpenViking）：
 * - L0: 紧凑索引（~500 tokens）- 始终加载到 system prompt
 * - L1: 摘要层（~2000 tokens）- 相关时加载
 * - L2: 完整内容（~5000 tokens）- 明确请求时加载
 *
 * L0 内容：
 * - 用户基本信息（USER.md 摘要）
 * - 当前目标（GOALS.md 前3项）
 * - 最近3天的关键事件
 * - Core 层记忆索引（ID + 一句话描述）
 *
 * L1 内容：
 * - Working 层记忆摘要
 * - 相关项目的上下文
 * - 最近7天的对话摘要
 *
 * L2 内容：
 * - Peripheral 层记忆
 * - 完整对话记录
 * - 详细的项目文档
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.join(process.env.HOME, '.openclaw/workspace');
const MEMORY_INDEX = path.join(WORKSPACE, 'memory/metadata/memory-index.json');
const L0_INDEX = path.join(WORKSPACE, 'memory/metadata/L0-index.md');
const L1_INDEX = path.join(WORKSPACE, 'memory/metadata/L1-index.md');
const L2_INDEX = path.join(WORKSPACE, 'memory/metadata/L2-index.md');

/**
 * 生成 L0 索引（紧凑索引，始终加载）
 */
function buildL0Index() {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const coreMemories = index.tiers.core.map(id => index.memories[id]);

  let l0Content = `# L0 记忆索引（紧凑层）

> 此文件自动生成，包含最重要的记忆索引。
> 更新时间: ${new Date().toISOString()}

## 用户基本信息

`;

  // 读取 USER.md（如果存在）
  const userFile = path.join(WORKSPACE, 'USER.md');
  if (fs.existsSync(userFile)) {
    const userContent = fs.readFileSync(userFile, 'utf-8');
    // 提取前 200 字符作为摘要
    const userSummary = userContent.split('\n').slice(0, 5).join('\n');
    l0Content += userSummary + '\n\n';
  } else {
    l0Content += '（尚未建立用户档案）\n\n';
  }

  // 读取 GOALS.md（如果存在）
  l0Content += `## 当前目标\n\n`;
  const goalsFile = path.join(WORKSPACE, 'GOALS.md');
  if (fs.existsSync(goalsFile)) {
    const goalsContent = fs.readFileSync(goalsFile, 'utf-8');
    // 提取前 3 个目标
    const goals = goalsContent.split('\n').filter(line => line.trim().startsWith('-')).slice(0, 3);
    l0Content += goals.join('\n') + '\n\n';
  } else {
    l0Content += '（尚未设定目标）\n\n';
  }

  // Core 层记忆索引
  l0Content += `## 核心记忆（Core 层）\n\n`;
  if (coreMemories.length === 0) {
    l0Content += '（暂无核心记忆）\n\n';
  } else {
    coreMemories.forEach(mem => {
      const summary = mem.content.split('\n')[0].substring(0, 80);
      l0Content += `- [${mem.id}] ${summary}... (${mem.category}, 重要性: ${mem.importance.toFixed(2)})\n`;
    });
    l0Content += '\n';
  }

  // 最近 3 天的关键事件
  l0Content += `## 最近关键事件（3天内）\n\n`;
  const recentEvents = Object.values(index.memories)
    .filter(mem => {
      const daysSince = (new Date() - new Date(mem.timestamp)) / (1000 * 60 * 60 * 24);
      return mem.category === 'events' && daysSince <= 3;
    })
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .slice(0, 5);

  if (recentEvents.length === 0) {
    l0Content += '（暂无最近事件）\n\n';
  } else {
    recentEvents.forEach(mem => {
      const date = new Date(mem.timestamp).toISOString().split('T')[0];
      const summary = mem.content.split('\n')[0].substring(0, 60);
      l0Content += `- [${date}] ${summary}...\n`;
    });
    l0Content += '\n';
  }

  // Token 估算
  const tokenEstimate = Math.ceil(l0Content.length / 4);
  l0Content += `---\n\n*L0 索引大小: ~${tokenEstimate} tokens*\n`;

  fs.writeFileSync(L0_INDEX, l0Content);
  console.log(`✓ L0 索引已生成: ${L0_INDEX} (~${tokenEstimate} tokens)`);

  return { path: L0_INDEX, tokens: tokenEstimate };
}

/**
 * 生成 L1 索引（摘要层，相关时加载）
 */
function buildL1Index() {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const workingMemories = index.tiers.working.map(id => index.memories[id]);

  let l1Content = `# L1 记忆索引（摘要层）

> 此文件自动生成，包含 Working 层记忆摘要。
> 更新时间: ${new Date().toISOString()}

## Working 层记忆

`;

  if (workingMemories.length === 0) {
    l1Content += '（暂无 Working 层记忆）\n\n';
  } else {
    // 按类别分组
    const byCategory = {};
    workingMemories.forEach(mem => {
      if (!byCategory[mem.category]) {
        byCategory[mem.category] = [];
      }
      byCategory[mem.category].push(mem);
    });

    Object.entries(byCategory).forEach(([category, memories]) => {
      l1Content += `### ${category}\n\n`;
      memories.forEach(mem => {
        const summary = mem.content.substring(0, 150).replace(/\n/g, ' ');
        l1Content += `**[${mem.id}]** ${summary}...\n`;
        l1Content += `- 重要性: ${mem.importance.toFixed(2)} | 访问: ${mem.access_count}次 | 最后访问: ${new Date(mem.last_access).toISOString().split('T')[0]}\n\n`;
      });
    });
  }

  // 最近 7 天的对话摘要
  l1Content += `## 最近对话摘要（7天内）\n\n`;
  const transcriptsDir = path.join(WORKSPACE, 'memory/transcripts');
  if (fs.existsSync(transcriptsDir)) {
    const files = fs.readdirSync(transcriptsDir)
      .filter(f => f.endsWith('.md'))
      .sort()
      .reverse()
      .slice(0, 7);

    files.forEach(file => {
      const content = fs.readFileSync(path.join(transcriptsDir, file), 'utf-8');
      const firstLine = content.split('\n').find(line => line.trim().length > 0);
      l1Content += `- ${file.replace('.md', '')}: ${firstLine}\n`;
    });
    l1Content += '\n';
  } else {
    l1Content += '（暂无对话记录）\n\n';
  }

  // Token 估算
  const tokenEstimate = Math.ceil(l1Content.length / 4);
  l1Content += `---\n\n*L1 索引大小: ~${tokenEstimate} tokens*\n`;

  fs.writeFileSync(L1_INDEX, l1Content);
  console.log(`✓ L1 索引已生成: ${L1_INDEX} (~${tokenEstimate} tokens)`);

  return { path: L1_INDEX, tokens: tokenEstimate };
}

/**
 * 生成 L2 索引（完整内容，明确请求时加载）
 */
function buildL2Index() {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const peripheralMemories = index.tiers.peripheral.map(id => index.memories[id]);

  let l2Content = `# L2 记忆索引（完整层）

> 此文件自动生成，包含 Peripheral 层完整记忆。
> 更新时间: ${new Date().toISOString()}

## Peripheral 层记忆

`;

  if (peripheralMemories.length === 0) {
    l2Content += '（暂无 Peripheral 层记忆）\n\n';
  } else {
    // 按类别分组
    const byCategory = {};
    peripheralMemories.forEach(mem => {
      if (!byCategory[mem.category]) {
        byCategory[mem.category] = [];
      }
      byCategory[mem.category].push(mem);
    });

    Object.entries(byCategory).forEach(([category, memories]) => {
      l2Content += `### ${category}\n\n`;
      memories.forEach(mem => {
        l2Content += `#### [${mem.id}] ${mem.content.split('\n')[0]}\n\n`;
        l2Content += `${mem.content}\n\n`;
        l2Content += `**元数据:**\n`;
        l2Content += `- 重要性: ${mem.importance.toFixed(2)}\n`;
        l2Content += `- 访问: ${mem.access_count}次\n`;
        l2Content += `- 创建: ${new Date(mem.created_at).toISOString().split('T')[0]}\n`;
        l2Content += `- 最后访问: ${new Date(mem.last_access).toISOString().split('T')[0]}\n`;
        if (mem.entities && mem.entities.length > 0) {
          l2Content += `- 实体: ${mem.entities.join(', ')}\n`;
        }
        if (mem.tags && mem.tags.length > 0) {
          l2Content += `- 标签: ${mem.tags.join(', ')}\n`;
        }
        l2Content += '\n---\n\n';
      });
    });
  }

  // Token 估算
  const tokenEstimate = Math.ceil(l2Content.length / 4);
  l2Content += `*L2 索引大小: ~${tokenEstimate} tokens*\n`;

  fs.writeFileSync(L2_INDEX, l2Content);
  console.log(`✓ L2 索引已生成: ${L2_INDEX} (~${tokenEstimate} tokens)`);

  return { path: L2_INDEX, tokens: tokenEstimate };
}

/**
 * 生成所有层级的索引
 */
function buildAllIndexes() {
  console.log('开始构建三层索引...\n');

  const l0 = buildL0Index();
  const l1 = buildL1Index();
  const l2 = buildL2Index();

  console.log('\n=== 索引构建完成 ===');
  console.log(`L0 (紧凑层): ${l0.tokens} tokens`);
  console.log(`L1 (摘要层): ${l1.tokens} tokens`);
  console.log(`L2 (完整层): ${l2.tokens} tokens`);
  console.log(`总计: ${l0.tokens + l1.tokens + l2.tokens} tokens`);

  return { l0, l1, l2 };
}

/**
 * 获取指定记忆的详细内容（用于按需加载）
 */
function getMemoryDetail(memoryId) {
  const index = JSON.parse(fs.readFileSync(MEMORY_INDEX, 'utf-8'));
  const memory = index.memories[memoryId];

  if (!memory) {
    return null;
  }

  // 记录访问（强化记忆）
  const { recordAccess } = require('./memory-decay.js');
  recordAccess(memoryId);

  return memory;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0] || 'build';

  switch (command) {
    case 'build':
      // 构建所有索引
      buildAllIndexes();
      break;

    case 'l0':
      // 只构建 L0
      buildL0Index();
      break;

    case 'l1':
      // 只构建 L1
      buildL1Index();
      break;

    case 'l2':
      // 只构建 L2
      buildL2Index();
      break;

    case 'get':
      // 获取指定记忆的详细内容
      if (args.length < 2) {
        console.error('用法: node memory-index-builder.js get <记忆ID>');
        process.exit(1);
      }
      const memory = getMemoryDetail(args[1]);
      if (memory) {
        console.log(JSON.stringify(memory, null, 2));
      } else {
        console.error(`记忆 ${args[1]} 不存在`);
        process.exit(1);
      }
      break;

    default:
      console.log('用法:');
      console.log('  node memory-index-builder.js build    # 构建所有层级索引');
      console.log('  node memory-index-builder.js l0       # 只构建 L0 索引');
      console.log('  node memory-index-builder.js l1       # 只构建 L1 索引');
      console.log('  node memory-index-builder.js l2       # 只构建 L2 索引');
      console.log('  node memory-index-builder.js get <ID> # 获取指定记忆详情');
      process.exit(1);
  }
}

module.exports = { buildL0Index, buildL1Index, buildL2Index, buildAllIndexes, getMemoryDetail };
