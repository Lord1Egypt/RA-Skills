#!/usr/bin/env node
/**
 * Task Breakdown Script
 * 将复杂任务拆解为编码、测试、文档三类 TODO
 */

const { createTask, createProject, getAllTasks } = require('../db/task-manager');
const { addDependency, getDependenciesForTask } = require('../db/task-dependency-manager');

/**
 * 任务类型定义
 */
const TASK_TYPES = {
  CODE: 'code',
  TEST: 'test',
  DOC: 'doc'
};

/**
 * 任务优先级定义
 */
const PRIORITIES = {
  HIGH: 1,
  MEDIUM: 2,
  LOW: 3
};

/**
 * 将复杂任务拆解为子任务
 * @param {Object} task - 任务对象
 * @returns {Array} 子任务列表
 */
function breakdownTask(task) {
  const tasks = [];
  const { title, description, project_id } = task;
  
  // 1. 编码任务
  tasks.push({
    type: TASK_TYPES.CODE,
    title: `实现 ${title} 核心功能`,
    description: description ? `开发 ${title} 的核心功能模块：\n${description}` : `开发 ${title} 的核心功能模块`,
    priority: PRIORITIES.HIGH,
    project_id: project_id
  });
  
  // 2. 测试任务
  tasks.push({
    type: TASK_TYPES.TEST,
    title: `编写 ${title} 单元测试`,
    description: description ? `为核心功能编写测试用例：\n${description}` : `为核心功能编写测试用例，确保代码质量`,
    priority: PRIORITIES.MEDIUM,
    project_id: project_id
  });
  
  // 3. 文档任务
  tasks.push({
    type: TASK_TYPES.DOC,
    title: `编写 ${title} 项目文档`,
    description: '编写 README.md 和 API 文档',
    priority: PRIORITIES.MEDIUM,
    project_id: project_id
  });
  
  // 4. 操作手册
  tasks.push({
    type: TASK_TYPES.DOC,
    title: `编写 ${title} 操作手册`,
    description: '编写用户操作手册和部署指南',
    priority: PRIORITIES.LOW,
    project_id: project_id
  });
  
  return tasks;
}

/**
 * 创建任务并建立依赖关系
 * @param {Object} task - 任务对象
 */
function createBreakdownTasks(task) {
  const subTasks = breakdownTask(task);
  const createdTasks = [];
  
  // 创建所有子任务
  for (const subTask of subTasks) {
    try {
      const created = createTask(subTask);
      createdTasks.push(created);
      console.log(`✅ 创建任务：${created.title} (ID: ${created.id})`);
    } catch (error) {
      console.error(`❌ 创建任务失败 ${subTask.title}:`, error.message);
    }
  }
  
  // 建立依赖关系
  if (createdTasks.length >= 2) {
    // 测试任务依赖编码任务
    const codeTask = createdTasks[0];
    const testTask = createdTasks[1];
    
    try {
      addDependency(testTask.id, codeTask.id);
      console.log(`✅ 已建立依赖：${testTask.title} 依赖 ${codeTask.title}`);
    } catch (error) {
      console.error(`❌ 建立依赖失败:`, error.message);
    }
  }
  
  return createdTasks;
}

/**
 * 显示任务拆解结果
 */
function showBreakdown(task) {
  const tasks = breakdownTask(task);
  
  console.log('\n=== 任务拆解结果 ===\n');
  console.log(`原任务：${task.title}`);
  console.log(`描述：${task.description || '无'}`);
  console.log('─'.repeat(60));
  
  tasks.forEach((t, i) => {
    const typeLabel = {
      [TASK_TYPES.CODE]: '📝 编码',
      [TASK_TYPES.TEST]: '🧪 测试',
      [TASK_TYPES.DOC]: '📄 文档'
    }[t.type] || '📋 任务';
    
    const priorityLabel = {
      [PRIORITIES.HIGH]: '🔴 高',
      [PRIORITIES.MEDIUM]: '🟡 中',
      [PRIORITIES.LOW]: '🟢 低'
    }[t.priority] || '⚪ 普通';
    
    console.log(`\n${i + 1}. ${typeLabel} - ${t.title}`);
    console.log(`   优先级：${priorityLabel}`);
    console.log(`   描述：${t.description}`);
  });
  
  console.log('\n' + '─'.repeat(60));
  console.log(`总计：${tasks.length} 个子任务`);
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🚀 任务拆解工具\n');
    console.log('用法:');
    console.log('  node scripts/task-breakdown.js show <title> [description]     # 显示拆解结果');
    console.log('  node scripts/task-breakdown.js create <title> [description]  # 创建任务');
    console.log('\n示例:');
    console.log('  node scripts/task-breakdown.js show "用户登录功能" "实现 OAuth2 登录"');
    console.log('  node scripts/task-breakdown.js create "用户登录功能" "实现 OAuth2 登录"');
    console.log('');
    return;
  }
  
  const command = args[0];
  const title = args[1];
  const description = args.slice(2).join(' ');
  
  if (!title) {
    console.error('❌ 请提供任务标题');
    return;
  }
  
  const task = {
    title,
    description: description || undefined,
    project_id: 'default-project'
  };
  
  if (command === 'show') {
    showBreakdown(task);
  } else if (command === 'create') {
    console.log('\n🚀 开始创建任务...\n');
    createBreakdownTasks(task);
    console.log('\n✅ 任务创建完成！');
  } else {
    console.error('❌ 未知命令:', command);
    console.log('可用命令：show, create');
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = { breakdownTask, createBreakdownTasks, TASK_TYPES, PRIORITIES };
