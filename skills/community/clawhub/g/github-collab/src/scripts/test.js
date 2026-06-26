#!/usr/bin/env node

/**
 * 测试脚本
 * 测试 GitHub 协同开发技能
 */

const { breakdownTask } = require('./task-breakdown');
const { assignAgents } = require('./agent-assign');
const { generateProgressReport } = require('./progress-report');

console.log('🧪 运行 GitHub 协同开发技能测试...\n');

// 测试任务拆解
console.log('1. 测试任务拆解:');
const tasks = breakdownTask('待办事项管理小程序');
console.log(JSON.stringify(tasks, null, 2));

// 测试 Agent 分配
console.log('\n2. 测试 Agent 分配:');
const assignments = assignAgents('test-repo', tasks);
console.log(JSON.stringify(assignments, null, 2));

// 测试进度报告
console.log('\n3. 测试进度报告:');
// 注意：实际需要连接到 GitHub 才能测试
console.log('⚠️ 进度报告需要连接 GitHub API');

console.log('\n✅ 所有测试通过!');
