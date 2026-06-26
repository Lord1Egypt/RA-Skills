/**
 * 基础功能测试
 */

import { loadConfig, getCurrentTimeWindow } from './utils/config-loader.js';
import { checkPluginAvailable } from './utils/openclaw-tools.js';
import fs from 'node:fs';
import path from 'node:path';

console.log('=== Proactive Trigger 基础测试 ===\n');

// 测试1: 配置加载
console.log('1. 测试配置加载...');
try {
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   每日最大触发: ${config.maxDailyTriggers}`);
  console.log(`   最小触发间隔: ${config.minTriggerIntervalHours}小时`);
  console.log(`   评分阈值: ${config.minTriggerScore}`);
} catch (error) {
  console.log('❌ 配置加载失败:', error.message);
}

// 测试2: 时间窗口
console.log('\n2. 测试时间窗口...');
try {
  const timeWindow = getCurrentTimeWindow();
  console.log(`✅ 当前时间窗口: ${timeWindow.name}`);
  console.log(`   权重: ${timeWindow.weight}`);
  console.log(`   允许类型: ${timeWindow.allowedTypes.join(', ') || '无'}`);
} catch (error) {
  console.log('❌ 时间窗口测试失败:', error.message);
}

// 测试3: 插件可用性
console.log('\n3. 测试OpenClaw插件可用性...');
try {
  const available = checkPluginAvailable();
  console.log(available ? '✅ 插件可用' : '⚠️ 插件不可用（某些功能受限）');
} catch (error) {
  console.log('❌ 插件测试失败:', error.message);
}

// 测试4: 状态文件
console.log('\n4. 测试状态文件...');
try {
  const statePath = path.join(process.env.HOME || '/tmp', '.openclaw/workspace/.soul/trigger-state.json');
  if (fs.existsSync(statePath)) {
    const state = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
    console.log('✅ 状态文件存在');
    console.log(`   今日触发次数: ${state.triggersToday || 0}`);
    console.log(`   上次触发时间: ${state.lastTriggerTime || '从未'}`);
  } else {
    console.log('ℹ️ 状态文件不存在（首次运行时会创建）');
  }
} catch (error) {
  console.log('❌ 状态文件测试失败:', error.message);
}

console.log('\n=== 测试完成 ===');
console.log('\n下一步建议:');
console.log('1. 运行 npm install 安装依赖');
console.log('2. 运行 npm test 进行完整测试');
console.log('3. 运行 node scripts/trigger.js --test "健康提醒" 测试触发评分');
console.log('4. 运行 node scripts/trigger.js --consume 测试信号处理');