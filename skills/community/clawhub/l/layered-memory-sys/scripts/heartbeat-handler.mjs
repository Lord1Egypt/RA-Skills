#!/usr/bin/env node
// heartbeat-handler.mjs - 心跳触发入口（v2.0）
// 被心跳系统调用，执行梦境模式 + 提醒检查

import { loadConfig } from '../src/db/config-loader.mjs';
import { initDatabase } from '../src/db/database.mjs';
import { initTokenizer } from '../src/search/tokenizer.mjs';
import { initEmbedder } from '../src/search/embedder.mjs';
import { execDreamCycle } from '../src/dream/dream-cycle.mjs';
import { getDueReminders, updateMemory } from '../src/db/repository.mjs';
import { emit, EVENTS } from '../src/events/event-bus.mjs';

const config = loadConfig();

// 初始化
await initDatabase(config);
await initTokenizer(config);
await initEmbedder(config);

console.log('💓 心跳触发 v2.0...');

// 1. 检查提醒
const due = getDueReminders();
for (const reminder of due) {
  console.log(`🔔 提醒: ${reminder.title}`);
  console.log(`   ${reminder.summary}`);
  emit(EVENTS.REMINDER_TRIGGERED, reminder);
  updateMemory(reminder.id, { status: 'completed' });
}

// 2. 梦境模式（凌晨或空闲时）
const hour = new Date().getHours();
if (hour >= 2 && hour <= 5) {
  console.log('🌙 梦境模式触发...');
  const stats = await execDreamCycle(config);
  emit(EVENTS.DREAM_COMPLETED, stats);
}

console.log('✅ 心跳处理完成');