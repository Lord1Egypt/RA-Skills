#!/usr/bin/env node

/**
 * MIA-Trust Pipeline 一键执行入口
 * 
 * 用法: ./run.mjs "你的问题"
 * 
 * 完整流程: guard_blocked → Planner → evaluate_plan → 执行
 */

import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'fs';

const require = createRequire(import.meta.url);
const __dirname = dirname(fileURLToPath(import.meta.url));

// 默认配置
const DEFAULTS = {
  MIA_PLANNER_MODE: 'api',
  MIA_PLANNER_URL: process.env.MIA_PLANNER_URL || '',
  MIA_PLANNER_MODEL: process.env.MIA_PLANNER_MODEL || '',
  MIA_PLANNER_API_KEY: process.env.MIA_PLANNER_API_KEY || '',
  MIA_MEMORY_FILE: join(__dirname, 'memory/memory.jsonl'),
  MIA_FEEDBACK_FILE: join(__dirname, 'feedback/feedback.jsonl'),
  MIA_TRUST_EXPERIENCE_FILE: join(__dirname, 'trust/trust_experience.json'),
};

// 设置环境变量
Object.entries(DEFAULTS).forEach(([key, value]) => {
  if (!process.env[key] && value) {
    process.env[key] = value;
  }
});

const QUESTION = process.argv.slice(2).join(' ');
if (!QUESTION) {
  console.error('用法: ./run.mjs "你的问题"');
  process.exit(1);
}

console.log('=== MIA-Trust Pipeline ===');
console.log('问题:', QUESTION);
console.log('');

// ===== Step 1: guard_blocked =====
console.log('--- Step 1: guard_blocked ---');
const { execSync } = require('child_process');

let guardResult;
try {
  const output = execSync(
    `node ${join(__dirname, 'trust/mia-trust.mjs')} guard_blocked '{"query":"${QUESTION.replace(/"/g, '\\"')}"}'`,
    { encoding: 'utf-8', timeout: 60000 }
  );
  guardResult = JSON.parse(output);
} catch (e) {
  try {
    guardResult = JSON.parse(e.stdout || e.message);
  } catch {
    console.error('guard_blocked 执行失败');
    process.exit(1);
  }
}

console.log('结果:', JSON.stringify(guardResult, null, 2));

// 停止检查
if (guardResult.blocked || guardResult.risk_level === 'BLOCKED' || guardResult.safe === false) {
  console.log('');
  console.log('❌ 安全检查未通过，停止执行');
  console.log('建议:', guardResult.suggestion || guardResult.message);
  process.exit(1);
}

// ===== Step 2: Planner =====
console.log('');
console.log('--- Step 2: Planner ---');

let plannerResult;
try {
  const output = execSync(
    `node ${join(__dirname, 'planner/mia-planner.mjs')} "${QUESTION.replace(/"/g, '\\"')}"`,
    { encoding: 'utf-8', timeout: 60000 }
  );
  plannerResult = JSON.parse(output);
} catch (e) {
  try {
    plannerResult = JSON.parse(e.stdout || e.message);
  } catch {
    console.error('Planner 执行失败');
    process.exit(1);
  }
}

console.log('计划:', plannerResult.plan);
console.log('步骤:', plannerResult.steps);

// ===== Step 3: evaluate_plan =====
console.log('');
console.log('--- Step 3: evaluate_plan ---');

let evaluateResult;
try {
  const input = JSON.stringify({
    query: QUESTION,
    plan_draft: plannerResult.plan,
    memories: []
  }).replace(/"/g, '\\"');
  
  const output = execSync(
    `node ${join(__dirname, 'trust/mia-trust.mjs')} evaluate_plan '{"query":"${QUESTION.replace(/"/g, '\\"')}","plan_draft":"${plannerResult.plan.replace(/"/g, '\\"').replace(/\n/g, '\\n')}","memories":[]}'`,
    { encoding: 'utf-8', timeout: 90000 }
  );
  evaluateResult = JSON.parse(output);
} catch (e) {
  try {
    evaluateResult = JSON.parse(e.stdout || e.message);
  } catch {
    console.error('evaluate_plan 执行失败');
    process.exit(1);
  }
}

console.log('结���:', JSON.stringify(evaluateResult, null, 2));

// 执行检查
if (!evaluateResult.safe) {
  console.log('');
  console.log('❌ 计划审查未通过，停止执行');
  process.exit(1);
}

console.log('');
console.log('✅ Pipeline 执行完成');
console.log('');
console.log('--- 最终计划 ---');
console.log(evaluateResult.final_plan);

// ===== Step 4: 存储记忆 =====
console.log('');
console.log('--- Step 5: 存储记忆 ---');

const memoryRecord = {
  timestamp: new Date().toISOString(),
  question: QUESTION,
  plan: plannerResult.plan,
  execution: [],
  final_answer: evaluateResult
};

appendFileSync(
  DEFAULTS.MIA_MEMORY_FILE,
  JSON.stringify(memoryRecord) + '\n'
);

console.log('✅ 记忆已存储');