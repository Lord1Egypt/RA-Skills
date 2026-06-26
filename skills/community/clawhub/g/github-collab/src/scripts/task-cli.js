#!/usr/bin/env node
/**
 * Task CLI - 任务管理命令行工具
 * 提供完整的任务管理功能
 */

const { 
  createTask, 
  getTaskById, 
  getAllTasks, 
  updateTask, 
  updateTaskStatus,
  completeTask,
  cancelTask,
  deleteTask,
  getTasksByAgent,
  getTasksByStatus,
  getTasksByPriority,
  assignTask
} = require('../db/task-manager');

const { 
  addDependency, 
  removeDependency, 
  getDependenciesForTask,
  getDependentTasks
} = require('../db/task-dependency-manager');

const {
  setTaskPriority,
  getHighPriorityTasks,
  getPriorityTasks
} = require('../db/task-priority-manager');

const {
  getAgentByName,
  getAllAgents
} = require('../db/agent-manager');

/**
 * 格式化任务显示
 */
function formatTask(task) {
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
  
  return {
    id: task.id,
    title: task.title,
    status: statusLabel,
    priority: priorityLabel,
    assignedTo: task.assigned_to || '未分配',
    createdAt: task.created_at,
    updatedAt: task.updated_at
  };
}

/**
 * 列出所有任务
 */
function listTasks(options = {}) {
  const { status, agent, priority, limit = 50 } = options;
  
  let tasks = [];
  
  if (status) {
    tasks = getTasksByStatus(status);
  } else if (agent) {
    tasks = getTasksByAgent(agent);
  } else if (priority) {
    tasks = getTasksByPriority(priority);
  } else {
    tasks = getAllTasks();
  }
  
  if (tasks.length > limit) {
    tasks = tasks.slice(0, limit);
  }
  
  if (tasks.length === 0) {
    console.log('📭 暂无任务');
    return;
  }
  
  console.log('\n=== 任务列表 ===\n');
  tasks.forEach((task, index) => {
    const formatted = formatTask(task);
    console.log(`${index + 1}. [${formatted.id}] ${formatted.title}`);
    console.log(`   状态：${formatted.status}`);
    console.log(`   优先级：${formatted.priority}`);
    console.log(`   分配给：${formatted.assignedTo}`);
    console.log(`   创建时间：${formatted.createdAt}`);
    console.log('');
  });
  
  console.log(`总计：${tasks.length} 个任务`);
}

/**
 * 创建任务
 */
function createNewTask(title, description, priority = 2, project_id = 'default') {
  try {
    const task = {
      title,
      description: description || undefined,
      priority: parseInt(priority),
      project_id
    };
    
    const created = createTask(task);
    console.log(`✅ 任务创建成功！`);
    console.log(`   ID: ${created.id}`);
    console.log(`   标题：${created.title}`);
    console.log(`   优先级：${priority === 1 ? '高' : priority === 2 ? '中' : '低'}`);
  } catch (error) {
    console.error('❌ 创建任务失败:', error.message);
  }
}

/**
 * 查看任务详情
 */
function viewTask(taskId) {
  try {
    const task = getTaskById(parseInt(taskId));
    
    if (!task) {
      console.error(`❌ 任务不存在：${taskId}`);
      return;
    }
    
    const formatted = formatTask(task);
    
    console.log('\n=== 任务详情 ===\n');
    console.log(`ID: ${task.id}`);
    console.log(`标题：${task.title}`);
    console.log(`描述：${task.description || '无'}`);
    console.log(`状态：${formatted.status}`);
    console.log(`优先级：${formatted.priority}`);
    console.log(`分配给：${formatted.assignedTo}`);
    console.log(`项目 ID: ${task.project_id}`);
    console.log(`创建时间：${task.created_at}`);
    console.log(`更新时间：${task.updated_at}`);
    
    if (task.completed_at) {
      console.log(`完成时间：${task.completed_at}`);
    }
    
    // 显示依赖关系
    const dependencies = getDependenciesForTask(task.id);
    if (dependencies.length > 0) {
      console.log(`\n依赖任务:`);
      dependencies.forEach(dep => {
        console.log(`  - [${dep.task_id}] 依赖 [${dep.dependent_task_id}]`);
      });
    }
    
    const dependentTasks = getDependentTasks(task.id);
    if (dependentTasks.length > 0) {
      console.log(`\n被依赖任务:`);
      dependentTasks.forEach(dep => {
        console.log(`  - [${dep.dependent_task_id}] 依赖 [${dep.task_id}]`);
      });
    }
  } catch (error) {
    console.error('❌ 获取任务详情失败:', error.message);
  }
}

/**
 * 更新任务
 */
function updateTaskInfo(taskId, title, description, priority) {
  try {
    const updates = {};
    
    if (title) updates.title = title;
    if (description !== undefined) updates.description = description;
    if (priority) updates.priority = parseInt(priority);
    
    const result = updateTask(parseInt(taskId), updates);
    
    if (result.changes > 0) {
      console.log(`✅ 任务更新成功！`);
      console.log(`   修改项：${Object.keys(updates).join(', ')}`);
    } else {
      console.error(`❌ 任务不存在：${taskId}`);
    }
  } catch (error) {
    console.error('❌ 更新任务失败:', error.message);
  }
}

/**
 * 更新任务状态
 */
function updateTaskStatusCmd(taskId, status) {
  try {
    const result = updateTaskStatus(parseInt(taskId), status);
    
    if (result.changes > 0) {
      console.log(`✅ 任务状态更新成功！`);
      console.log(`   任务：${taskId}`);
      console.log(`   新状态：${status}`);
    } else {
      console.error(`❌ 任务不存在：${taskId}`);
    }
  } catch (error) {
    console.error('❌ 更新任务状态失败:', error.message);
  }
}

/**
 * 完成任务
 */
function completeTaskCmd(taskId) {
  try {
    const result = completeTask(parseInt(taskId));
    
    if (result.changes > 0) {
      console.log(`✅ 任务完成！`);
      console.log(`   任务：${taskId}`);
      console.log(`   完成时间：${new Date().toISOString()}`);
    } else {
      console.error(`❌ 任务不存在：${taskId}`);
    }
  } catch (error) {
    console.error('❌ 完成任务失败:', error.message);
  }
}

/**
 * 取消任务
 */
function cancelTaskCmd(taskId, reason) {
  try {
    const result = cancelTask(parseInt(taskId), reason);
    
    if (result.changes > 0) {
      console.log(`✅ 任务已取消！`);
      console.log(`   任务：${taskId}`);
      console.log(`   原因：${reason || '无'}`);
    } else {
      console.error(`❌ 任务不存在：${taskId}`);
    }
  } catch (error) {
    console.error('❌ 取消任务失败:', error.message);
  }
}

/**
 * 分配任务
 */
function assignTaskCmd(taskId, agentName) {
  try {
    const agent = getAgentByName(agentName);
    
    if (!agent) {
      console.error(`❌ Agent 不存在：${agentName}`);
      return;
    }
    
    if (agent.is_active !== 1) {
      console.error(`❌ Agent 未激活：${agentName}`);
      return;
    }
    
    const result = assignTask(parseInt(taskId), agentName);
    
    if (result.changes > 0) {
      console.log(`✅ 任务已分配！`);
      console.log(`   任务：${taskId}`);
      console.log(`   Agent: ${agentName}`);
    } else {
      console.error(`❌ 分配失败：任务可能已被分配`);
    }
  } catch (error) {
    console.error('❌ 分配任务失败:', error.message);
  }
}

/**
 * 添加依赖
 */
function addDependencyCmd(taskId, dependsOnId) {
  try {
    const result = addDependency(parseInt(taskId), parseInt(dependsOnId));
    
    if (result.changes > 0) {
      console.log(`✅ 依赖关系已建立！`);
      console.log(`   任务 [${taskId}] 依赖 [${dependsOnId}]`);
    } else {
      console.error(`❌ 添加依赖失败`);
    }
  } catch (error) {
    console.error('❌ 添加依赖失败:', error.message);
  }
}

/**
 * 设置优先级
 */
function setPriorityCmd(taskId, priority) {
  try {
    const result = setTaskPriority(parseInt(taskId), parseInt(priority));
    
    if (result.changes > 0) {
      console.log(`✅ 优先级已更新！`);
      console.log(`   任务：${taskId}`);
      console.log(`   新优先级：${priority === 1 ? '高' : priority === 2 ? '中' : '低'}`);
    } else {
      console.error(`❌ 任务不存在：${taskId}`);
    }
  } catch (error) {
    console.error('❌ 设置优先级失败:', error.message);
  }
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
🚀 Task CLI - 任务管理命令行工具

用法:
  node scripts/task-cli.js <command> [options]

命令:
  list [options]              列出任务
    --status=<status>         按状态筛选 (pending, in_progress, completed, cancelled)
    --agent=<agent_name>      按 Agent 筛选
    --priority=<priority>     按优先级筛选 (1=高，2=中，3=低)
    --limit=<number>          限制显示数量 (默认：50)

  create <title> [description] [priority]  创建任务
  view <task_id>                    查看任务详情
  update <task_id> [options]        更新任务
    --title=<title>                更新标题
    --description=<desc>           更新描述
    --priority=<priority>          更新优先级

  status <task_id> <status>       更新任务状态
  complete <task_id>              完成任务
  cancel <task_id> [reason]       取消任务
  assign <task_id> <agent_name>   分配任务
  dependency <task_id> <depends_on_id>  添加依赖
  priority <task_id> <priority>   设置优先级

  help                            显示帮助

示例:
  node scripts/task-cli.js list
  node scripts/task-cli.js list --status=pending
  node scripts/task-cli.js list --agent=coder-agent
  node scripts/task-cli.js create "新任务" "任务描述" 1
  node scripts/task-cli.js view 1
  node scripts/task-cli.js update 1 --title="新标题" --priority=2
  node scripts/task-cli.js status 1 in_progress
  node scripts/task-cli.js complete 1
  node scripts/task-cli.js cancel 1 "原因"
  node scripts/task-cli.js assign 1 coder-agent
  node scripts/task-cli.js dependency 2 1
  node scripts/task-cli.js priority 1 1
`);
}

/**
 * 解析命令行参数
 */
function parseArgs(args) {
  const result = {
    command: null,
    options: {},
    args: []
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      showHelp();
      process.exit(0);
    }
    
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      result.options[key] = value;
    } else if (!result.command) {
      result.command = arg;
    } else {
      result.args.push(arg);
    }
  }
  
  return result;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const parsed = parseArgs(args);
  
  if (!parsed.command) {
    showHelp();
    return;
  }
  
  switch (parsed.command) {
    case 'list':
      listTasks(parsed.options);
      break;
    
    case 'create':
      if (parsed.args.length < 1) {
        console.error('❌ 请提供任务标题');
        return;
      }
      createNewTask(
        parsed.args[0],
        parsed.args[1] || undefined,
        parsed.args[2] || 2
      );
      break;
    
    case 'view':
      if (parsed.args.length < 1) {
        console.error('❌ 请提供任务 ID');
        return;
      }
      viewTask(parsed.args[0]);
      break;
    
    case 'update':
      if (parsed.args.length < 1) {
        console.error('❌ 请提供任务 ID');
        return;
      }
      updateTaskInfo(
        parsed.args[0],
        parsed.options.title,
        parsed.options.description,
        parsed.options.priority
      );
      break;
    
    case 'status':
      if (parsed.args.length < 2) {
        console.error('❌ 请提供任务 ID 和新状态');
        return;
      }
      updateTaskStatusCmd(parsed.args[0], parsed.args[1]);
      break;
    
    case 'complete':
      if (parsed.args.length < 1) {
        console.error('❌ 请提供任务 ID');
        return;
      }
      completeTaskCmd(parsed.args[0]);
      break;
    
    case 'cancel':
      if (parsed.args.length < 1) {
        console.error('❌ 请提供任务 ID');
        return;
      }
      cancelTaskCmd(parsed.args[0], parsed.args[1] || undefined);
      break;
    
    case 'assign':
      if (parsed.args.length < 2) {
        console.error('❌ 请提供任务 ID 和 Agent 名称');
        return;
      }
      assignTaskCmd(parsed.args[0], parsed.args[1]);
      break;
    
    case 'dependency':
      if (parsed.args.length < 2) {
        console.error('❌ 请提供任务 ID 和依赖的任务 ID');
        return;
      }
      addDependencyCmd(parsed.args[0], parsed.args[1]);
      break;
    
    case 'priority':
      if (parsed.args.length < 2) {
        console.error('❌ 请提供任务 ID 和优先级 (1=高，2=中，3=低)');
        return;
      }
      setPriorityCmd(parsed.args[0], parsed.args[1]);
      break;
    
    case 'help':
    case '--help':
    case '-h':
      showHelp();
      break;
    
    default:
      console.error(`❌ 未知命令：${parsed.command}`);
      showHelp();
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

module.exports = {
  listTasks,
  createNewTask,
  viewTask,
  updateTaskInfo,
  updateTaskStatusCmd,
  completeTaskCmd,
  cancelTaskCmd,
  assignTaskCmd,
  addDependencyCmd,
  setPriorityCmd
};
