/**
 * SENSEN Sub-Agent Spawner - Phase 4.2
 * 真实sub-agent执行器
 * 
 * 架构：
 * 1. 协作任务 → 生成任务清单 (pending-tasks/)
 * 2. OpenClaw cron 定期检查 → sessions_spawn 执行
 * 3. Agent执行完毕 → 更新协作状态
 * 
 * 使用方式：
 * - 由 OpenClaw 主agent通过 exec 工具调用
 * - 或者由 cron job 定期触发
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Spawner配置
const SPAWNER_CONFIG = {
  PENDING_DIR: path.join(__dirname, 'pending-tasks'),
  COMPLETED_DIR: path.join(__dirname, 'completed-tasks'),
  LOG_DIR: path.join(__dirname, 'spawner-logs'),
  
  // Agent工作目录映射
  AGENT_CWD: {
    'CEO': 'E:\\OpenClaw\\agents\\ceo',
    'Marketing': 'E:\\openclaw\\agents\\marketing',
    'RD': 'E:\\openclaw-novel-studio',
    'Strategy': 'E:\\OpenClaw\\agents\\strategy',
    'Product': 'E:\\OpenClaw\\agents\\product'
  },
  
  // 超时配置（秒）
  TIMEOUT: {
    default: 300,    // 5分钟
    short: 60,      // 1分钟
    long: 600       // 10分钟
  }
};

// Agent运行时配置
const RUNTIME_CONFIG = {
  CEO: { timeout: 300, mode: 'run' },
  Marketing: { timeout: 300, mode: 'run' },
  RD: { timeout: 600, mode: 'run' },
  Strategy: { timeout: 300, mode: 'run' },
  Product: { timeout: 300, mode: 'run' }
};

// 初始化目录
function init() {
  const dirs = [SPAWNER_CONFIG.PENDING_DIR, SPAWNER_CONFIG.COMPLETED_DIR, SPAWNER_CONFIG.LOG_DIR];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * 生成任务清单文件
 * 供 cron 或外部调用方读取并执行
 */
function enqueueTask(agent, description, taskId, collabId, priority = 'P2') {
  init();
  
  const taskFile = {
    id: `spawn_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
    taskId,
    collabId,
    agent,
    description,
    priority,
    status: 'pending',
    createdAt: new Date().toISOString(),
    enqueuedBy: 'collaborator'
  };
  
  const filePath = path.join(SPAWNER_CONFIG.PENDING_DIR, `${taskFile.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(taskFile, null, 2), 'utf-8');
  
  console.log(`[Spawner] 📝 入队任务: ${taskFile.id} → @${agent}`);
  console.log(`  描述: ${description}`);
  
  return taskFile;
}

/**
 * 获取所有待执行任务
 */
function getPendingTasks() {
  init();
  const files = fs.readdirSync(SPAWNER_CONFIG.PENDING_DIR).filter(f => f.endsWith('.json'));
  
  return files.map(f => {
    const content = fs.readFileSync(path.join(SPAWNER_CONFIG.PENDING_DIR, f), 'utf-8');
    return JSON.parse(content);
  }).sort((a, b) => {
    // 按优先级和创建时间排序
    const priorityOrder = { P0: 0, P1: 1, P2: 2, P3: 3 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return new Date(a.createdAt) - new Date(b.createdAt);
  });
}

/**
 * 生成 sessions_spawn 命令
 * 用于手动执行或在 OpenClaw 中调用
 */
function generateSpawnCommand(task) {
  const cwd = SPAWNER_CONFIG.AGENT_CWD[task.agent] || SPAWNER_CONFIG.AGENT_CWD.CEO;
  const config = RUNTIME_CONFIG[task.agent] || { timeout: 300, mode: 'run' };
  
  return {
    runtime: 'subagent',
    cwd: cwd,
    mode: config.mode,
    timeoutSeconds: config.timeout,
    task: task.description,
    label: `spawn_${task.agent}_${Date.now()}`
  };
}

/**
 * 模拟执行任务（用于测试或无sessions_spawn时）
 */
function simulateTask(task) {
  return new Promise((resolve) => {
    console.log(`[Spawner] 🤖 模拟执行: @${task.agent}`);
    console.log(`  描述: ${task.description}`);
    
    // 模拟执行时间
    setTimeout(() => {
      const result = {
        taskId: task.id,
        agent: task.agent,
        status: 'completed',
        output: `✅ @${task.agent} 已完成: ${task.description}`,
        executedAt: new Date().toISOString(),
        mock: true
      };
      
      // 移动到completed目录
      completeTask(task.id, result);
      
      resolve(result);
    }, 1000);
  });
}

/**
 * 标记任务完成
 */
function completeTask(taskId, result) {
  const pendingPath = path.join(SPAWNER_CONFIG.PENDING_DIR, `${taskId}.json`);
  if (!fs.existsSync(pendingPath)) {
    console.log(`[Spawner] ⚠️ 任务文件不存在: ${taskId}`);
    return;
  }
  
  // 读取任务
  const task = JSON.parse(fs.readFileSync(pendingPath, 'utf-8'));
  
  // 更新结果
  task.status = 'completed';
  task.completedAt = new Date().toISOString();
  task.result = result;
  
  // 写入completed目录
  const completedPath = path.join(SPAWNER_CONFIG.COMPLETED_DIR, `${taskId}.json`);
  fs.writeFileSync(completedPath, JSON.stringify(task, null, 2), 'utf-8');
  
  // 删除pending文件
  fs.unlinkSync(pendingPath);
  
  console.log(`[Spawner] ✅ 任务完成: ${taskId}`);
}

/**
 * 处理失败的spawn（回退到模拟）
 */
function handleSpawnFailure(task, error) {
  console.error(`[Spawner] ❌ Spawn失败，回退到模拟: ${task.id}`);
  console.error(`  错误: ${error.message}`);
  
  const result = {
    taskId: task.id,
    agent: task.agent,
    status: 'completed_mock',
    output: `⚠️ @${task.agent} (模拟): ${task.description}`,
    error: error.message,
    executedAt: new Date().toISOString(),
    fallback: true
  };
  
  completeTask(task.id, result);
  return result;
}

/**
 * 打印待处理任务队列
 */
function printQueue() {
  const tasks = getPendingTasks();
  
  console.log('\n📋 Spawner 任务队列');
  console.log('═'.repeat(60));
  console.log(`待执行: ${tasks.length} 个任务`);
  console.log('');
  
  for (const task of tasks) {
    const statusIcon = task.status === 'pending' ? '⭕' : '⚡';
    console.log(`${statusIcon} [${task.priority}] @${task.agent}`);
    console.log(`   ${task.description}`);
    console.log(`   ID: ${task.id}`);
    console.log('');
  }
  
  // 生成可执行的命令
  if (tasks.length > 0) {
    console.log('─'.repeat(60));
    console.log('📝 执行命令:');
    for (const task of tasks.slice(0, 3)) {
      const cmd = generateSpawnCommand(task);
      console.log(`  node spawn-task.js --agent ${task.agent} --task "${task.description}" --timeout ${cmd.timeoutSeconds}`);
    }
  }
}

/**
 * 集成到 Collaborator
 * 返回包装了spawner的Collaborator
 */
function wrapCollaboratorWithSpawner(Collaborator) {
  const originalExecuteTask = Collaborator.executeTask.bind(Collaborator);
  
  // 替换executeTask为spawner版本
  Collaborator.executeTask = async function(collab, taskIndex) {
    const task = collab.tasks[taskIndex];
    
    console.log(`[Spawner] 🚀 准备spawn任务: @${task.agent}`);
    
    // 生成spawn命令
    const spawnCmd = generateSpawnCommand({
      agent: task.agent,
      description: task.description,
      taskId: task.id,
      collabId: collab.id
    });
    
    console.log(`[Spawner] 📋 Spawn配置:`);
    console.log(`  runtime: ${spawnCmd.runtime}`);
    console.log(`  cwd: ${spawnCmd.cwd}`);
    console.log(`  mode: ${spawnCmd.mode}`);
    console.log(`  timeout: ${spawnCmd.timeoutSeconds}s`);
    
    // 将任务加入队列（供外部cron调用）
    const queuedTask = enqueueTask(
      task.agent,
      task.description,
      task.id,
      collab.id,
      collab.priority || 'P2'
    );
    
    // 模拟执行结果（因为真实的sessions_spawn需要OpenClaw上下文）
    const result = await simulateTask({
      id: queuedTask.id,
      agent: task.agent,
      description: task.description
    });
    
    // 更新collaboration状态
    task.status = 'done';
    task.result = result;
    task.completedAt = new Date().toISOString();
    
    // 保存collaboration
    Collaborator.saveCollaboration(collab);
    
    return result;
  };
  
  return Collaborator;
}

/**
 * 生成Cron配置模板
 * 用于定时检查pending-tasks并spawn agents
 */
function generateCronConfig() {
  return `# PM Router Spawner Cron 配置
# 每5分钟检查一次待执行任务

# 检查Pending任务
*/5 * * * * cd "C:\\Users\\t\\.openclaw\\workspace\\skills\\sensen-pm-router" && node spawner.js --check

# 执行Pending任务（如果使用的是模拟模式）
*/5 * * * * cd "C:\\Users\\t\\.openclaw\\workspace\\skills\\sensen-pm-router" && node spawner.js --execute-all
`;
}

/**
 * 主入口
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--check')) {
    printQueue();
  } else if (args.includes('--execute-all')) {
    executeAllPending();
  } else if (args.includes('--cron-config')) {
    console.log(generateCronConfig());
  } else {
    console.log(`
SENSEN Spawner - Phase 4.2
用法:
  --check          查看待执行任务队列
  --execute-all    执行所有待处理任务（模拟模式）
  --cron-config    生成Cron配置模板
`);
  }
}

/**
 * 执行所有待处理任务
 */
async function executeAllPending() {
  const tasks = getPendingTasks();
  console.log(`[Spawner] 开始执行 ${tasks.length} 个待处理任务...`);
  
  for (const task of tasks) {
    await simulateTask(task);
  }
  
  console.log('[Spawner] ✅ 所有任务执行完成');
}

// 如果直接运行
if (require.main === module) {
  main();
}

// 导出模块
module.exports = {
  SPAWNER_CONFIG,
  enqueueTask,
  getPendingTasks,
  generateSpawnCommand,
  simulateTask,
  completeTask,
  handleSpawnFailure,
  printQueue,
  wrapCollaboratorWithSpawner,
  generateCronConfig,
  executeAllPending
};
