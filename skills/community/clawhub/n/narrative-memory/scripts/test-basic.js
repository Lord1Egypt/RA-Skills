#!/usr/bin/env node

/**
 * 基础测试脚本
 */

import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadConfig } from './utils/config-loader.js';

const WORKSPACE = process.env.HOME ? join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = join(WORKSPACE, '.soul');

console.log('=== Narrative Memory 基础测试 ===\n');

// 1. 测试配置加载
console.log('1. 测试配置加载...');
try {
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   触发阈值: 决策=${config.decisionThreshold}, 价值判断=${config.valueJudgmentThreshold}`);
  console.log(`   积累阈值: 话题提及=${config.topicMentionThreshold}, 情感模式=${config.emotionalPatternThreshold}`);
} catch (error) {
  console.log('❌ 配置加载失败:', error.message);
}

// 2. 测试目录结构
console.log('\n2. 测试目录结构...');
try {
  if (!existsSync(SOUL_DIR)) {
    mkdirSync(SOUL_DIR, { recursive: true });
    console.log('ℹ️ 创建 .soul 目录');
  } else {
    console.log('✅ .soul 目录存在');
  }
  
  // 创建示例用户价值数据
  const userValuesPath = join(SOUL_DIR, 'user-values.json');
  if (!existsSync(userValuesPath)) {
    const sampleValues = {
      core_values: [
        {
          name: "家庭第一",
          description: "家庭永远是第一优先级",
          weight: 0.9,
          sources: ["USER.md"],
          value: "家庭永远是第一优先级"
        }
      ],
      work_principles: [],
      life_priorities: [],
      boundaries: {
        time: { start: 22, end: 7, enabled: true },
        energy: { threshold: 0.3, enabled: true },
        privacy: { topics: [], enabled: true },
        decision: { autonomy_level: "high", enabled: true }
      }
    };
    writeFileSync(userValuesPath, JSON.stringify(sampleValues, null, 2));
    console.log('ℹ️ 创建示例用户价值文件');
  } else {
    console.log('✅ 用户价值文件存在');
  }
  
  // 创建每日上下文
  const dailyContextPath = join(SOUL_DIR, 'daily_context.json');
  if (!existsSync(dailyContextPath)) {
    const dailyContext = {
      date: new Date().toISOString().split('T')[0],
      summary: "测试日",
      key_events: ["测试叙事记忆系统"],
      user_mood: "curious",
      open_todos: [],
      closed_todos: [],
      proactive_observations: []
    };
    writeFileSync(dailyContextPath, JSON.stringify(dailyContext, null, 2));
    console.log('ℹ️ 创建每日上下文文件');
  } else {
    console.log('✅ 每日上下文文件存在');
  }
} catch (error) {
  console.log('❌ 目录结构测试失败:', error.message);
}

// 3. 测试脚本文件
console.log('\n3. 测试脚本文件...');
const scriptFiles = [
  'scripts/narrative.js',
  'scripts/utils/config-loader.js',
  'scripts/test-basic.js'
];

let allFilesOk = true;
for (const file of scriptFiles) {
  const fullPath = join(process.env.HOME || '/', '.openclaw/skills/@soul-system/narrative-memory', file);
  if (existsSync(fullPath)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} 不存在`);
    allFilesOk = false;
  }
}

// 4. 测试配置验证
console.log('\n4. 测试配置验证...');
try {
  const config = loadConfig();
  const requiredFields = [
    'decisionThreshold', 'valueJudgmentThreshold', 'emotionalTurnThreshold',
    'milestoneThreshold', 'firstExperienceThreshold', 'reflectionThreshold',
    'topicMentionThreshold', 'emotionalPatternThreshold'
  ];
  
  let configValid = true;
  for (const field of requiredFields) {
    if (config[field] === undefined) {
      console.log(`❌ 配置缺少字段: ${field}`);
      configValid = false;
    }
  }
  
  if (configValid) {
    console.log('✅ 配置验证通过');
  }
} catch (error) {
  console.log('❌ 配置验证失败:', error.message);
}

// 5. 测试package.json
console.log('\n5. 测试package.json...');
try {
  const packagePath = join(process.env.HOME || '/', '.openclaw/skills/@soul-system/narrative-memory/package.json');
  if (existsSync(packagePath)) {
    const pkg = JSON.parse(readFileSync(packagePath, 'utf-8'));
    console.log(`✅ package.json 存在 (v${pkg.version})`);
    console.log(`   名称: ${pkg.name}`);
    console.log(`   脚本命令: ${Object.keys(pkg.scripts || {}).join(', ')}`);
  } else {
    console.log('❌ package.json 不存在');
  }
} catch (error) {
  console.log('❌ package.json测试失败:', error.message);
}

console.log('\n=== 测试完成 ===\n');
console.log('下一步建议:');
console.log('1. 运行 npm install 安装依赖');
console.log('2. 运行 npm test 进行完整测试');
console.log('3. 运行 node scripts/narrative.js --test 测试叙事检测');
console.log('4. 运行 node scripts/narrative.js --process-text "我决定放弃这个项目" 测试文本处理');
console.log('5. 运行 node scripts/narrative.js --timeline 查看时间线');
