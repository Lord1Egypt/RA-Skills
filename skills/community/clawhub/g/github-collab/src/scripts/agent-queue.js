#!/usr/bin/env node
/**
 * Agent Queue Viewer - Agent 工作队列查看工具
 * 查看每个 Agent 的工作队列和状态
 */

const {
  getAllAgents,
  getAgentByName,
  getAgentAddress
} = require('../db/agent-manager');

const {
  getTasksByAgent,
  getTasksByStatus
} = require('../db/task-manager');

const {
  getHealthyAgents,
  getLastHeartbeat
} = require('../db/agent-health-manager');

/**
 * 格式化时间差
 */
function formatTimeDiff(timestamp) {
  if (!timestamp) return '未知';
  
  const now = new Date();
  const last = new Date(timestamp);
  const diff = Math.floor((now - last) / 1000); // 秒
  
  if (diff < 60) {
    return `${diff}秒前`;
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}分钟前`;
  } else if (diff < 86400) {
    return `${Math.floor(diff / 3600)}小时前`;
  } else {
    return `${Math.floor(diff / 86400)}天前`;
  }
}

/**
 * 获取 Agent 工作队列
 */
function getAgentQueue(agentName) {
  const agent = getAgentByName(agentName);
  
  if (!agent) {
    return null;
  }
  
  const tasks = getTasksByAgent(agentName);
  const inProgressTasks = tasks.filter(t => t.status === 'in_progress');
  const pendingTasks = tasks.filter(t => t.status === 'pending');
  
  const lastHeartbeat = getLastHeartbeat(agentName);
  
  return {
    agent,
    inProgress: inProgressTasks,
    pending: pendingTasks,
    lastHeartbeat,
    isHealthy: lastHeartbeat && (new Date() - new Date(lastHeartbeat)) < 300000 // 5 分钟
  };
}

/**
 * 显示单个 Agent 队列
 */
function showAgentQueue(agentName) {
  const queue = getAgentQueue(agentName);
  
  if (!queue) {
    console.error(`❌ Agent 不存在：${agentName}`);
    return;
  }
  
  console.log('\n=== Agent 工作队列 ===\n');
  console.log(`Agent: ${queue.agent.name}`);
  console.log(`角色：${queue.agent.role}`);
  console.log(`地址：${queue.agent.target}`);
  console.log(`状态：${queue.isHealthy ? '✅ 健康' : '❌ 不健康'}`);
  console.log(`最后心跳：${formatTimeDiff(queue.lastHeartbeat)}`);
  console.log('');
  
  // 进行中任务
  console.log(`🔄 进行中任务 (${queue.inProgress.length}):`);
  if (queue.inProgress.length === 0) {
    console.log('  无');
  } else {
    queue.inProgress.forEach(task => {
      const priorityLabel = {
        1: '🔴 高',
        2: '🟡 中',
        3: '🟢 低'
      }[task.priority] || '⚪ 普通';
      
      console.log(`  - [${task.id}] ${task.title} (${priorityLabel})`);
      console.log(`    描述：${task.description || '无'}`);
      console.log(`    创建时间：${task.created_at}`);
    });
  }
  console.log('');
  
  // 待分配任务
  console.log(`⏳ 待分配任务 (${queue.pending.length}):`);
  if (queue.pending.length === 0) {
    console.log('  无');
  } else {
    queue.pending.forEach(task => {
      const priorityLabel = {
        1: '🔴 高',
        2: '🟡 中',
        3: '🟢 低'
      }[task.priority] || '⚪ 普通';
      
      console.log(`  - [${task.id}] ${task.title} (${priorityLabel})`);
    });
  }
}

/**
 * 显示所有 Agent 队列
 */
function showAllAgentQueues() {
  const agents = getAllAgents();
  const activeAgents = agents.filter(a => a.is_active === 1);
  
  if (activeAgents.length === 0) {
    console.log('📭 暂无活跃 Agent');
    return;
  }
  
  console.log('\n=== 所有 Agent 工作队列 ===\n');
  
  activeAgents.forEach(agent => {
    const queue = getAgentQueue(agent.name);
    
    console.log(`### ${agent.name} (${agent.role})`);
    console.log(`状态：${queue.isHealthy ? '✅ 健康' : '❌ 不健康'}`);
    console.log(`最后心跳：${formatTimeDiff(queue.lastHeartbeat)}`);
    console.log(`进行中：${queue.inProgress.length} | 待分配：${queue.pending.length}`);
    
    if (queue.inProgress.length > 0) {
      queue.inProgress.forEach(task => {
        const priorityLabel = {
          1: '🔴 高',
          2: '🟡 中',
          3: '🟢 低'
        }[task.priority] || '⚪ 普通';
        
        console.log(`  - [${task.id}] ${task.title} (${priorityLabel})`);
      });
    }
    
    console.log('');
  });
}

/**
 * 显示 Agent 统计
 */
function showAgentStats() {
  const agents = getAllAgents();
  const activeAgents = agents.filter(a => a.is_active === 1);
  const healthyAgents = getHealthyAgents();
  
  console.log('\n=== Agent 统计 ===\n');
  console.log(`总 Agent 数：${agents.length}`);
  console.log(`活跃 Agent: ${activeAgents.length}`);
  console.log(`健康 Agent: ${healthyAgents.length}`);
  console.log(`不健康 Agent: ${activeAgents.length - healthyAgents.length}`);
  console.log('');
  
  // 按角色统计
  const roleStats = {};
  activeAgents.forEach(agent => {
    if (!roleStats[agent.role]) {
      roleStats[agent.role] = { total: 0, healthy: 0 };
    }
    roleStats[agent.role].total++;
    if (healthyAgents.some(h => h.name === agent.name)) {
      roleStats[agent.role].healthy++;
    }
  });
  
  console.log('按角色统计:');
  Object.entries(roleStats).forEach(([role, stats]) => {
    console.log(`  ${role}: ${stats.healthy}/${stats.total} 健康`);
  });
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log(`
🚀 Agent Queue Viewer - Agent 工作队列查看工具

用法:
  node scripts/agent-queue.js <command> [options]

命令:
  list                            列出所有 Agent 队列
  view <agent_name>               查看指定 Agent 队列
  stats                           显示 Agent 统计
  help                            显示帮助

示例:
  node scripts/agent-queue.js list
  node scripts/agent-queue.js view coder-agent
  node scripts/agent-queue.js stats
`);
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    return;
  }
  
  const command = args[0];
  
  switch (command) {
    case 'list':
      showAllAgentQueues();
      break;
    
    case 'view':
      if (args.length < 2) {
        console.error('❌ 请提供 Agent 名称');
        return;
      }
      showAgentQueue(args[1]);
      break;
    
    case 'stats':
      showAgentStats();
      break;
    
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    
    default:
      console.error(`❌ 未知命令：${command}`);
      showHelp();
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = {
  getAgentQueue,
  showAgentQueue,
  showAllAgentQueues,
  showAgentStats
};
