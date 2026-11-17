#!/usr/bin/env python3
/**
 * 测试友好的 API Key 提示功能
 */

const handler = require('./handler.js');

console.log('='.repeat(60));
console.log('🎯 kids-points 友好提示功能测试');
console.log('='.repeat(60));
console.log('');

// 测试 1: API Key 检查
console.log('📋 测试 1: API Key 检查');
console.log('-'.repeat(60));
const hasApiKey = handler.checkSenseApiKey();
console.log(`API Key 状态：${hasApiKey ? '✅ 已配置' : '⚠️ 未配置'}`);
console.log('');

// 测试 2: 提示文案
console.log('💡 测试 2: 提示文案展示');
console.log('-'.repeat(60));
console.log(handler.getApiKeyHint());
console.log('');

// 测试 3: 模拟音频消息处理（无 API Key 时）
console.log('🎤 测试 3: 模拟音频消息处理');
console.log('-'.repeat(60));
if (!hasApiKey) {
  const result = handler.handleAudioMessage('/tmp/test.ogg');
  console.log('返回消息:', result.message.substring(0, 300) + '...');
} else {
  console.log('⚠️  API Key 已配置，跳过此测试');
  console.log('💡 提示：临时移除 API Key 可测试此功能');
}
console.log('');

// 测试 4: 日报生成提示
console.log('📊 测试 4: 日报生成提示');
console.log('-'.repeat(60));
const report = handler.generateDailyReport();
console.log(report.message.substring(0, 300) + '...');
console.log('');

console.log('='.repeat(60));
console.log('✅ 测试完成！');
console.log('='.repeat(60));
