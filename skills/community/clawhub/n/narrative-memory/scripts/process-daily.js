#!/usr/bin/env node

/**
 * 处理每日对话的脚本
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { loadConfig } from './utils/config-loader.js';

// 动态导入narrative.js以访问processText
import('./narrative.js').then(narrativeModule => {
  const processText = narrativeModule.processText;

  const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
  const DAILY_CONTEXT_PATH = join(WORKSPACE, '.soul', 'daily_context.json');
  const MEMORY_DIR = join(WORKSPACE, 'memory');

  async function main() {
    console.log('开始处理每日对话...');

    // 加载配置
    const config = loadConfig();

    // 处理每日上下文
    if (existsSync(DAILY_CONTEXT_PATH)) {
      try {
        const dailyContext = JSON.parse(readFileSync(DAILY_CONTEXT_PATH, 'utf-8'));
        console.log(`处理每日上下文: ${dailyContext.date}`);

        // 处理关键事件
        if (dailyContext.key_events && dailyContext.key_events.length > 0) {
          console.log(`发现${dailyContext.key_events.length}个关键事件`);
          for (const event of dailyContext.key_events) {
            console.log(`处理事件: ${event.substring(0, 50)}...`);
            const result = processText(event, config);
            if (result.narratives && result.narratives.length > 0) {
              console.log(`  创建叙事: ${result.narratives.length}个`);
            }
          }
        }

        // 处理总结
        if (dailyContext.summary) {
          console.log('处理每日总结...');
          processText(dailyContext.summary, config);
        }

      } catch (error) {
        console.error('处理每日上下文失败:', error.message);
      }
    } else {
      console.log('每日上下文文件不存在');
    }

    // 处理记忆文件（如果有）
    if (existsSync(MEMORY_DIR)) {
      console.log('检查记忆文件...');
      // 可以扩展：处理最近的memory文件
    }

    console.log('每日对话处理完成');
  }

  main().catch(error => {
    console.error('脚本执行失败:', error);
    process.exit(1);
  });
}).catch(error => {
  console.error('导入narrative.js失败:', error);
  process.exit(1);
});
