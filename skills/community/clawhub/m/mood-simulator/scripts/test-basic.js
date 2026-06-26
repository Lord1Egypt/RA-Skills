/**
 * 基础功能测试
 */

import { loadConfig, getConfigSummary, getCurrentTimeWindow } from './utils/config-loader.js';
import fs from 'node:fs';
import path from 'node:path';

console.log('=== Mood Simulator 基础测试 ===\n');

// 测试1: 配置加载
console.log('1. 测试配置加载...');
try {
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   时间权重: ${config.timeFactorWeight}`);
  console.log(`   内容权重: ${config.contentFactorWeight}`);
  console.log(`   历史权重: ${config.historyFactorWeight}`);
  
  const summary = getConfigSummary();
  console.log(`   权重总和: ${summary.weights.total.toFixed(2)}`);
  console.log(`   时间窗口: ${summary.timeWindows}个`);
  console.log(`   情绪关键词: ${summary.emotionKeywords}个`);
} catch (error) {
  console.log('❌ 配置加载失败:', error.message);
}

// 测试2: 时间窗口
console.log('\n2. 测试时间窗口...');
try {
  const timeWindow = getCurrentTimeWindow();
  console.log(`✅ 当前时间窗口: ${timeWindow.name}`);
  console.log(`   基础能量: ${timeWindow.baseEnergy}`);
  console.log(`   时间段: ${timeWindow.start}:00-${timeWindow.end}:00`);
} catch (error) {
  console.log('❌ 时间窗口测试失败:', error.message);
}

// 测试3: 配置文件存在性
console.log('\n3. 测试配置文件存在性...');
try {
  const workspace = process.env.HOME ? path.join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
  const configPath = path.join(workspace, '.soul', 'mood-config.json');
  const statePath = path.join(workspace, '.soul', 'mood-state.json');
  const patternsPath = path.join(workspace, '.soul', 'mood-patterns.json');
  const historyPath = path.join(workspace, '.soul', 'mood-history.jsonl');
  
  console.log(`   配置文件: ${fs.existsSync(configPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   状态文件: ${fs.existsSync(statePath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   模式文件: ${fs.existsSync(patternsPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
  console.log(`   历史文件: ${fs.existsSync(historyPath) ? '✅ 存在' : 'ℹ️ 不存在（将创建）'}`);
} catch (error) {
  console.log('❌ 文件检查失败:', error.message);
}

// 测试4: 目录结构
console.log('\n4. 测试目录结构...');
try {
  const scriptFiles = [
    'simulator.js',
    'test-basic.js',
    'utils/config-loader.js',
    'utils/signal-manager.js'
  ];
  
  let allExist = true;
  for (const file of scriptFiles) {
    const filePath = path.join(process.cwd(), 'scripts', file);
    const exists = fs.existsSync(filePath);
    console.log(`   ${file}: ${exists ? '✅ 存在' : '❌ 缺失'}`);
    if (!exists) allExist = false;
  }
  
  if (allExist) {
    console.log('✅ 所有脚本文件就绪');
  } else {
    console.log('⚠️  部分脚本文件缺失');
  }
} catch (error) {
  console.log('❌ 目录结构测试失败:', error.message);
}

// 测试5: 配置验证
console.log('\n5. 测试配置验证...');
try {
  const issues = loadConfig().validateConfig ? loadConfig().validateConfig() : [];
  if (issues.length === 0) {
    console.log('✅ 配置验证通过');
  } else {
    console.log('⚠️  配置验证发现问题:');
    for (const issue of issues) {
      console.log(`   - ${issue}`);
    }
  }
} catch (error) {
  console.log('❌ 配置验证失败:', error.message);
}

// 测试6: 信号管理器
console.log('\n6. 测试信号管理器...');
try {
  const signalManagerPath = path.join(process.cwd(), 'scripts', 'utils', 'signal-manager.js');
  if (fs.existsSync(signalManagerPath)) {
    console.log('✅ 信号管理器文件存在');
    
    // 尝试导入（但不执行）
    const fileContent = fs.readFileSync(signalManagerPath, 'utf-8');
    const hasPublishFunction = fileContent.includes('publishSignal');
    const hasGetPendingFunction = fileContent.includes('getPendingSignals');
    
    console.log(`   包含发布函数: ${hasPublishFunction ? '✅' : '❌'}`);
    console.log(`   包含查询函数: ${hasGetPendingFunction ? '✅' : '❌'}`);
  } else {
    console.log('❌ 信号管理器文件缺失');
  }
} catch (error) {
  console.log('❌ 信号管理器测试失败:', error.message);
}

console.log('\n=== 测试完成 ===');
console.log('\n下一步建议:');
console.log('1. 运行 npm install 安装依赖');
console.log('2. 运行 npm test 进行完整测试');
console.log('3. 运行 node scripts/simulator.js --test 测试情绪评估');
console.log('4. 运行 node scripts/simulator.js --calculate-energy 测试能量计算');
console.log('5. 运行 node scripts/simulator.js --analyze-message "今天有点累" 测试内容分析');