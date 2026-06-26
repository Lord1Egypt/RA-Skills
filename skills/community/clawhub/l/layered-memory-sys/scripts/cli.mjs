#!/usr/bin/env node
// cli.mjs - 命令行入口 (v2.0)

import { Command } from 'commander';
import { initDatabase, migrateFromJSON } from '../src/db/database.mjs';
import { initEmbedding, search, refreshEmbeddings } from '../src/search/search-engine.mjs';
import { createMemory, listMemories, getStats, getDueReminders } from '../src/db/repository.mjs';
import { getConfig } from '../src/db/config-loader.mjs';
import dreamCycle from '../src/dream/dream-cycle-v2.mjs';

const program = new Command();
program.name('memory-sys').description('Layered Memory System v2.0');

// 初始化
program.command('init')
  .description('初始化数据库')
  .option('-m, --migrate', '从 JSON 迁移数据', false)
  .action(async (opts) => {
    const config = getConfig();
    await initDatabase(config);
    if (opts.migrate) migrateFromJSON(config);
    console.log('✅ 初始化完成');
  });

// 梦境模式
program.command('dream')
  .description('执行梦境模式')
  .action(async () => {
    const config = getConfig();
    await initDatabase(config);
    await dreamCycle(config);
  });

// 搜索
program.command('search <query>')
  .description('搜索记忆')
  .option('-l, --limit <n>', '结果数量', '10')
  .action(async (query, opts) => {
    const config = getConfig();
    await initDatabase(config);
    await initEmbedding(config);
    const results = await search(query, { limit: parseInt(opts.limit) });
    console.log(JSON.stringify(results, null, 2));
  });

// 列表
program.command('list')
  .description('列出记忆')
  .option('-l, --layer <layer>', '层级过滤')
  .option('-n, --limit <n>', '数量', '20')
  .action(async (opts) => {
    const config = getConfig();
    await initDatabase(config);
    const { memories, total } = listMemories({
      layer: opts.layer,
      limit: parseInt(opts.limit)
    });
    console.log(`总计 ${total} 条记忆\n`);
    memories.forEach(m => {
      console.log(`[${m.layer}] ${m.title} (${m.recall_count}次召回)`);
    });
  });

// 统计
program.command('stats')
  .description('显示统计')
  .action(async () => {
    const config = getConfig();
    await initDatabase(config);
    const stats = getStats();
    console.log(JSON.stringify(stats, null, 2));
  });

// 提醒检查
program.command('remind')
  .description('检查到期提醒')
  .action(async () => {
    const config = getConfig();
    await initDatabase(config);
    const reminders = getDueReminders();
    if (reminders.length === 0) {
      console.log('暂无到期提醒');
    } else {
      console.log(`${reminders.length} 条提醒到期：`);
      reminders.forEach(r => {
        console.log(`- ${r.title} (${r.remind_at})`);
      });
    }
  });

// 刷新 embedding
program.command('refresh-embeddings')
  .description('刷新所有记忆的 Embedding')
  .action(async () => {
    const config = getConfig();
    await initDatabase(config);
    await initEmbedding(config);
    const count = await refreshEmbeddings();
    console.log(`✅ 刷新了 ${count} 条记忆的 Embedding`);
  });

program.parse();
