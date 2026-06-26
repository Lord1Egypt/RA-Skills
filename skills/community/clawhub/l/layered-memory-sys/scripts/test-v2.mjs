#!/usr/bin/env node
// test-v2.mjs - v2.0 完整测试

import { initDatabase, migrateFromJSON } from '../src/db/database.mjs';
import { createMemory, listMemories, getStats, getEvents, getDueReminders } from '../src/db/repository.mjs';
import { initTokenizer, searchTFIDF, getStatus as getTokenizerStatus } from '../src/search/tokenizer.mjs';
import { search, indexAllMemories } from '../src/search/search-engine.mjs';
import { initEmbedder, cosineSimilarity, getStatus as getEmbedderStatus } from '../src/search/embedder.mjs';
import { execDreamCycle } from '../src/dream/dream-cycle.mjs';
import { effectiveRecallCount } from '../src/dream/consolidator.mjs';
import { loadConfig } from '../src/db/config-loader.mjs';

const config = loadConfig();

console.log('🧪 layered-memory-sys v2.0 测试');
console.log('=' .repeat(50));

// 1. 初始化数据库
console.log('\n📦 1. 初始化数据库...');
await initDatabase(config);

// 尝试迁移
migrateFromJSON(config);

// 2. 测试记忆 CRUD
console.log('\n📝 2. 测试记忆 CRUD...');
const testMem = {
  id: 'test-v2-' + Date.now(),
  title: '测试记忆 - 记忆系统架构优化',
  summary: '讨论了 v2.0 架构设计，包括 SQLite 存储、Embedding 搜索、Cron 调度器',
  content: '完整的设计文档已保存在 memory/v2-design.md',
  layer: 'active',
  ttl: 7,
  type: 'exploration',
  tags: ['记忆', '架构', '优化', 'SQLite', '搜索'],
  turns: 5,
  recall_count: 3,
  recall_days: [
    new Date(Date.now() - 86400000 * 1).toISOString().split('T')[0],
    new Date(Date.now() - 86400000 * 2).toISOString().split('T')[0],
    new Date().toISOString().split('T')[0],
  ],
  created_at: new Date(Date.now() - 86400000 * 5).toISOString().split('T')[0],
  last_active: new Date().toISOString().split('T')[0],
};

createMemory(testMem);
console.log('   ✅ 创建记忆成功');

// 3. 测试分词器
console.log('\n🔤 3. 测试分词器...');
await initTokenizer(config);
const tokens = searchTFIDF('记忆系统架构', { limit: 5, config });
console.log(`   分词器状态: ${JSON.stringify(getTokenizerStatus())}`);
console.log(`   TF-IDF 搜索 "记忆系统架构": ${tokens.length} 条结果`);
for (const t of tokens) {
  console.log(`   - ${t.title} (score: ${t.score.toFixed(3)})`);
}

// 4. 测试 Embedding
console.log('\n🧠 4. 测试 Embedding...');
await initEmbedder(config);
console.log(`   Embedding 状态: ${JSON.stringify(getEmbedderStatus())}`);

if (getEmbedderStatus().available) {
  const semantic = await search('记忆系统', { limit: 5, config });
  console.log(`   语义搜索 "记忆系统": ${semantic.length} 条结果`);
  for (const s of semantic) {
    console.log(`   - ${s.title} (${s.matchType}, score: ${s.score.toFixed(3)})`);
  }
} else {
  console.log('   ⚠️ Embedding 不可用（正常，本地模型需单独安装）');
  console.log('   提示: npm install @xenova/transformers');
}

// 5. 测试时间衰减
console.log('\n⏰ 5. 测试时间衰减...');
const recent = effectiveRecallCount([
  new Date().toISOString().split('T')[0],
  new Date(Date.now() - 86400000).toISOString().split('T')[0],
  new Date(Date.now() - 86400000 * 2).toISOString().split('T')[0],
]);
const old = effectiveRecallCount([
  new Date(Date.now() - 86400000 * 30).toISOString().split('T')[0],
  new Date(Date.now() - 86400000 * 60).toISOString().split('T')[0],
  new Date(Date.now() - 86400000 * 90).toISOString().split('T')[0],
]);
console.log(`   近3天召回3次: ${recent.toFixed(2)} (阈值 2.5 → ${recent >= 2.5 ? '升级' : '保持'})`);
console.log(`   3个月内召回3次: ${old.toFixed(2)} (阈值 2.5 → ${old >= 2.5 ? '升级' : '保持'})`);

// 6. 测试统计
console.log('\n📊 6. 测试统计...');
const stats = getStats();
console.log(`   记忆层级分布: ${JSON.stringify(stats.layers.map(l => `${l.layer}:${l.count}`))}`);
console.log(`   标签分布: ${stats.tags.slice(0, 5).map(t => `${t.tag}(${t.count})`).join(', ') || '无'}`);

// 7. 测试事件
console.log('\n📋 7. 测试事件...');
const events = getEvents({ limit: 5 });
console.log(`   最近事件: ${events.length} 条`);
for (const e of events.slice(0, 3)) {
  console.log(`   - [${e.eventType}] ${e.memoryId}`);
}

// 8. 测试梦境模式
console.log('\n💤 8. 测试梦境模式...');
const dreamStats = await execDreamCycle(config);
console.log(`   结果: 巩固${dreamStats.consolidate} 归档${dreamStats.archive} 遗忘${dreamStats.forget} 合并${dreamStats.merge} 自动写入${dreamStats.autowrite}`);

// 9. 最终统计
console.log('\n📊 9. 最终统计...');
const finalStats = getStats();
const total = finalStats.layers.reduce((s, l) => s + l.count, 0);
console.log(`   总记忆: ${total} 条`);
console.log(`   层级: ${finalStats.layers.map(l => `${l.layer}(${l.count})`).join(' / ')}`);

console.log('\n' + '=' .repeat(50));
console.log('✅ v2.0 测试完成！');
