#!/usr/bin/env node
/**
 * Milestone Execution - 状态管理工具
 * 
 * 用法:
 *   node state.js init --task "任务" --milestones "m1,m2,m3"
 *   node state.js status
 *   node state.js update --milestone 2 --status completed
 *   node state.js clear
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = '.milestone-state.json';

function loadState() {
  if (fs.existsSync(STATE_FILE)) {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  }
  return null;
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function initTask(task, milestones) {
  const state = {
    task,
    totalMilestones: milestones.length,
    currentMilestone: 1,
    milestones: milestones.map((m, i) => ({
      id: i + 1,
      task: m,
      status: 'pending',
      output: null,
      duration: null,
      error: null
    })),
    createdAt: new Date().toISOString(),
    lastUpdated: new Date().toISOString()
  };
  saveState(state);
  console.log('✅ 状态文件已创建:', STATE_FILE);
  console.log(JSON.stringify(state, null, 2));
}

function showStatus() {
  const state = loadState();
  if (!state) {
    console.log('❌ 未找到状态文件');
    return;
  }
  
  console.log(`\n📋 任务: ${state.task}`);
  console.log(`📊 进度: Milestone ${state.currentMilestone}/${state.totalMilestones}`);
  console.log('\n状态:');
  
  state.milestones.forEach(m => {
    const icon = m.status === 'completed' ? '✅' : 
                 m.status === 'running' ? '🔄' :
                 m.status === 'skipped' ? '⏭️' :
                 m.status === 'failed' ? '❌' : '⏳';
    console.log(`  ${icon} [${m.id}] ${m.task}`);
    if (m.output) console.log(`       输出: ${m.output}`);
    if (m.error) console.log(`       错误: ${m.error}`);
  });
  
  // 进度条
  const completed = state.milestones.filter(m => m.status === 'completed').length;
  const percent = Math.round((completed / state.totalMilestones) * 100);
  const bar = '█'.repeat(Math.floor(percent / 5)) + '░'.repeat(20 - Math.floor(percent / 5));
  console.log(`\n[${bar}] ${percent}%`);
  console.log(`\n最后更新: ${state.lastUpdated}`);
}

function updateMilestone(id, updates) {
  const state = loadState();
  if (!state) {
    console.log('❌ 未找到状态文件');
    return;
  }
  
  const m = state.milestones.find(m => m.id === id);
  if (!m) {
    console.log(`❌ 未找到 Milestone ${id}`);
    return;
  }
  
  Object.assign(m, updates);
  state.lastUpdated = new Date().toISOString();
  saveState(state);
  console.log(`✅ Milestone ${id} 已更新`);
}

function clearState() {
  if (fs.existsSync(STATE_FILE)) {
    fs.unlinkSync(STATE_FILE);
    console.log('🗑️ 状态文件已删除');
  } else {
    console.log('ℹ️ 没有状态文件需要删除');
  }
}

function rollback() {
  const state = loadState();
  if (!state) {
    console.log('❌ 未找到状态文件');
    return;
  }
  
  // 找到最后一个完成的 milestone
  const lastCompleted = [...state.milestones]
    .reverse()
    .find(m => m.status === 'completed');
  
  if (!lastCompleted) {
    console.log('❌ 没有可回滚的 milestone');
    return;
  }
  
  // 将当前和之后的 milestone 重置为 pending
  const rollbackId = lastCompleted.id;
  state.milestones.forEach(m => {
    if (m.id >= rollbackId) {
      m.status = 'pending';
      m.output = null;
      m.error = null;
    }
  });
  
  state.currentMilestone = rollbackId;
  state.lastUpdated = new Date().toISOString();
  saveState(state);
  console.log(`✅ 已回滚到 Milestone ${rollbackId}`);
}

const args = process.argv.slice(2);
const cmd = args[0];

if (cmd === 'init') {
  const taskIdx = args.indexOf('--task');
  const milIdx = args.indexOf('--milestones');
  if (taskIdx === -1 || milIdx === -1) {
    console.error('用法: node state.js init --task "任务" --milestones "m1,m2,m3"');
    process.exit(1);
  }
  initTask(args[taskIdx + 1], args[milIdx + 1].split(',').map(m => m.trim()));
} else if (cmd === 'status') {
  showStatus();
} else if (cmd === 'update') {
  const id = parseInt(args[args.indexOf('--milestone') + 1]);
  const status = args[args.indexOf('--status') + 1];
  updateMilestone(id, { status });
} else if (cmd === 'clear') {
  clearState();
} else if (cmd === 'rollback') {
  rollback();
} else {
  console.log('可用命令:');
  console.log('  init --task "任务" --milestones "m1,m2,m3"  初始化任务');
  console.log('  status                                          查看状态');
  console.log('  update --milestone N --status completed         更新状态');
  console.log('  rollback                                        回滚');
  console.log('  clear                                           清除状态');
}
