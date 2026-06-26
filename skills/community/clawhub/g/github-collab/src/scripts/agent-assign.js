#!/usr/bin/env node
/**
 * Agent Assignment Script
 * Agent 任务分配脚本
 */

const { getAgentByName, getAllAgents, getAgentAddress } = require('../db/agent-manager');
const { assignTask, getTaskById, getAllTasks, updateTaskStatus } = require('../db/task-manager');
const { getHealthyAgents } = require('../db/agent-health-manager');

/**
 * 列出所有可用 Agent
 */
function listAvailableAgents() {
  console.log('\n=== 可用 Agent 列表 ===\n');
  
  try {
    const agents = getAllAgents();
    
    if (agents.length === 0) {
      console.log('📭 暂无可用 Agent');
      return;
    }
    
    agents.forEach((agent, index) => {
      const status = agent.is_active === 1 ? '✅ 活跃' : '⏸️ 停用';
      console.log(`${index + 1}. ${agent.name}`);
      console.log(`   角色：${agent.role}`);
      console.log(`   地址：${agent.target}`);
      console.log(`   描述：${agent.description || '无'}`);
      console.log(`   状态：${status}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ 获取 Agent 列表失败:', error.message);
  }
}

/**
 * 列出所有待分配任务
 */
function listPendingTasks() {
  console.log('\n=== 待分配任务 ===\n');
  
  try {
    const tasks = getAllTasks();
    const pendingTasks = tasks.filter(t => t.status === 'pending');
    
    if (pendingTasks.length === 0) {
      console.log('📭 暂无待分配任务');
      return;
    }
    
    pendingTasks.forEach((task, index) => {
      const priorityLabel = {
        1: '🔴 高',
        2: '🟡 中',
        3: '🟢 低'
      }[task.priority] || '⚪ 普通';
      
      console.log(`${index + 1}. ${task.title} (ID: ${task.id})`);
      console.log(`   优先级：${priorityLabel}`);
      console.log(`   描述：${task.description || '无'}`);
      console.log(`   创建时间：${task.created_at}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ 获取任务列表失败:', error.message);
  }
}

/**
 * 分配任务给 Agent
 */
function assignTaskToAgent(taskId, agentName) {
  try {
    // 检查任务是否存在
    const task = getTaskById(taskId);
    if (!task) {
      console.error(`❌ 任务不存在：${taskId}`);
      return;
    }
    
    // 检查 Agent 是否存在
    const agent = getAgentByName(agentName);
    if (!agent) {
      console.error(`❌ Agent 不存在：${agentName}`);
      return;
    }
    
    // 检查 Agent 是否活跃
    if (agent.is_active !== 1) {
      console.error(`❌ Agent 未激活：${agentName}`);
      return;
    }
    
    // 分配任务
    const result = assignTask(taskId, agentName);
    
    if (result.changes > 0) {
      console.log(`✅ 任务已分配！`);
      console.log(`   任务：${task.title}`);
      console.log(`   Agent: ${agentName}`);
      console.log(`   状态：in_progress`);
    } else {
      console.error(`❌ 分配失败：任务可能已被分配`);
    }
  } catch (error) {
    console.error('❌ 分配失败:', error.message);
  }
}

/**
 * 智能分配任务
 */
function autoAssignTasks() {
  console.log('\n🤖 开始智能分配任务...\n');
  
  try {
    // 获取待分配任务
    const tasks = getAllTasks();
    const pendingTasks = tasks.filter(t => t.status === 'pending');
    
    if (pendingTasks.length === 0) {
      console.log('📭 暂无待分配任务');
      return;
    }
    
    // 获取健康的 Agent
    const healthyAgents = getHealthyAgents();
    
    if (healthyAgents.length === 0) {
      console.error('❌ 暂无健康的 Agent 可用');
      return;
    }
    
    console.log(`找到 ${pendingTasks.length} 个待分配任务`);
    console.log(`找到 ${healthyAgents.length} 个可用 Agent\n`);
    
    // 按优先级排序任务
    pendingTasks.sort((a, b) => a.priority - b.priority);
    
    // 分配任务
    let assignedCount = 0;
    for (const task of pendingTasks) {
      // 根据任务类型选择合适的 Agent
      let targetAgent = null;
      
      // 简单轮询分配
      targetAgent = healthyAgents[assignedCount % healthyAgents.length];
      
      if (targetAgent) {
        assignTaskToAgent(task.id, targetAgent.name);
        assignedCount++;
      }
    }
    
    console.log(`\n✅ 智能分配完成！已分配 ${assignedCount} 个任务`);
  } catch (error) {
    console.error('❌ 智能分配失败:', error.message);
  }
}

/**
 * 显示任务状态
 */
function showTaskStatus(taskId) {
  try {
    const task = getTaskById(taskId);
    
    if (!task) {
      console.error(`❌ 任务不存在：${taskId}`);
      return;
    }
    
    const statusLabel = {
      pending: '⏳ 待分配',
      in_progress: '🔄 进行中',
      completed: '✅ 已完成',
      cancelled: '❌ 已取消'
    }[task.status] || '❓ 未知';
    
    const priorityLabel = {
      1: '🔴 高',
      2: '🟡 中',
      3: '🟢 低'
    }[task.priority] || '⚪ 普通';
    
    console.log(`\n=== 任务详情 ===\n`);
    console.log(`ID: ${task.id}`);
    console.log(`标题：${task.title}`);
    console.log(`描述：${task.description || '无'}`);
    console.log(`状态：${statusLabel}`);
    console.log(`优先级：${priorityLabel}`);
    console.log(`分配给：${task.assigned_to || '未分配'}`);
    console.log(`创建时间：${task.created_at}`);
    console.log(`更新时间：${task.updated_at}`);
    
    if (task.completed_at) {
      console.log(`完成时间：${task.completed_at}`);
    }
  } catch (error) {
    console.error('❌ 获取任务状态失败:', error.message);
  }
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🚀 Agent 任务分配工具\n');
    console.log('用法:');
    console.log('  node scripts/agent-assign.js list-agents       # 列出所有 Agent');
    console.log('  node scripts/agent-assign.js list-tasks        # 列出待分配任务');
    console.log('  node scripts/agent-assign.js assign <task_id> <agent_name>  # 分配任务');
    console.log('  node scripts/agent-assign.js auto             # 智能分配');
    console.log('  node scripts/agent-assign.js status <task_id> # 查看任务状态');
    console.log('\n示例:');
    console.log('  node scripts/agent-assign.js list-agents');
    console.log('  node scripts/agent-assign.js assign 1 coder-agent');
    console.log('  node scripts/agent-assign.js auto');
    console.log('');
    return;
  }
  
  const command = args[0];
  
  switch (command) {
    case 'list-agents':
      listAvailableAgents();
      break;
    case 'list-tasks':
      listPendingTasks();
      break;
    case 'assign':
      if (args.length < 3) {
        console.error('❌ 用法：assign <task_id> <agent_name>');
        return;
      }
      assignTaskToAgent(args[1], args[2]);
      break;
    case 'auto':
      autoAssignTasks();
      break;
    case 'status':
      if (args.length < 2) {
        console.error('❌ 用法：status <task_id>');
        return;
      }
      showTaskStatus(args[1]);
      break;
    default:
      console.error('❌ 未知命令:', command);
      console.log('可用命令：list-agents, list-tasks, assign, auto, status');
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}
