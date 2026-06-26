/**
 * SENSEN Multi-Agent Collaborator - Phase 4
 * 多Agent协作调度器
 * 
 * 支持：
 * 1. Sequential（顺序执行）：A → B → C
 * 2. Hierarchical（层级执行）：父任务拆分为多个子任务并行/串行
 * 3. 并行执行：多个Agent同时处理不同子任务
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// 协作目录
const COLLAB_DIR = path.join(__dirname, 'collaborations');

// 协作类型
const CollabType = {
  SEQUENTIAL: 'sequential',     // 顺序执行：A完成后B开始
  PARALLEL: 'parallel',        // 并行执行：多个Agent同时开始
  HIERARCHICAL: 'hierarchical'  // 层级执行：父任务拆分为多个子任务
};

// Agent状态
const AgentStatus = {
  IDLE: 'idle',
  WORKING: 'working',
  DONE: 'done',
  FAILED: 'failed',
  BLOCKED: 'blocked'
};

/**
 * 初始化协作目录
 */
function init() {
  if (!fs.existsSync(COLLAB_DIR)) {
    fs.mkdirSync(COLLAB_DIR, { recursive: true });
  }
}

/**
 * 创建协作任务
 * @param {Object} config - 协作配置
 */
function createCollaboration(config) {
  init();
  
  const id = `collab_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
  const now = new Date();
  
  const collaboration = {
    id,
    name: config.name || '未命名协作',
    type: config.type || CollabType.SEQUENTIAL,
    description: config.description || '',
    createdAt: now.toISOString(),
    updatedAt: now.toISOString(),
    status: 'pending',  // pending | running | done | failed
    tasks: config.tasks || [],  // 子任务列表
    results: {},        // 各Agent执行结果
    currentTaskIndex: 0,
    error: null,
    parentTaskId: config.parentTaskId || null  // 关联的父任务ID
  };
  
  // 初始化各任务状态
  for (let i = 0; i < collaboration.tasks.length; i++) {
    const task = collaboration.tasks[i];
    collaboration.tasks[i] = {
      id: `subtask_${i}`,
      agent: task.agent,
      description: task.description,
      status: AgentStatus.IDLE,
      result: null,
      error: null,
      startedAt: null,
      completedAt: null,
      dependsOn: task.dependsOn || []  // 依赖的其他任务索引
    };
  }
  
  saveCollaboration(collaboration);
  console.log(`[Collaborator] ✅ 创建协作: ${id} - ${collaboration.name}`);
  console.log(`  类型: ${collaboration.type}`);
  console.log(`  任务数: ${collaboration.tasks.length}`);
  
  return collaboration;
}

/**
 * 保存协作到文件
 */
function saveCollaboration(collab) {
  const filePath = path.join(COLLAB_DIR, `${collab.id}.json`);
  collab.updatedAt = new Date().toISOString();
  fs.writeFileSync(filePath, JSON.stringify(collab, null, 2), 'utf-8');
}

/**
 * 加载协作
 */
function loadCollaboration(id) {
  const filePath = path.join(COLLAB_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

/**
 * 获取所有协作
 */
function getAllCollaborations() {
  init();
  const files = fs.readdirSync(COLLAB_DIR).filter(f => f.endsWith('.json'));
  return files.map(f => {
    const content = JSON.parse(fs.readFileSync(path.join(COLLAB_DIR, f), 'utf-8'));
    return content;
  }).sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
}

/**
 * 检查任务依赖是否满足
 */
function checkDependencies(collab, taskIndex) {
  const task = collab.tasks[taskIndex];
  if (!task.dependsOn || task.dependsOn.length === 0) return true;
  
  return task.dependsOn.every(depIndex => {
    const depTask = collab.tasks[depIndex];
    return depTask && depTask.status === AgentStatus.DONE;
  });
}

/**
 * 获取下一个可执行的任务
 */
function getNextRunnableTask(collab) {
  for (let i = 0; i < collab.tasks.length; i++) {
    const task = collab.tasks[i];
    if (task.status !== AgentStatus.IDLE) continue;
    if (!checkDependencies(collab, i)) continue;
    return i;
  }
  return -1;
}

/**
 * 模拟执行单个任务（实际应该spawn sub-agent）
 * @param {Object} collab - 协作对象
 * @param {number} taskIndex - 任务索引
 */
async function executeTask(collab, taskIndex) {
  const task = collab.tasks[taskIndex];
  
  console.log(`\n[Collaborator] ⚡ 执行任务 ${taskIndex + 1}/${collab.tasks.length}`);
  console.log(`  Agent: @${task.agent}`);
  console.log(`  描述: ${task.description}`);
  
  task.status = AgentStatus.WORKING;
  task.startedAt = new Date().toISOString();
  saveCollaboration(collab);
  
  // 模拟执行（实际会spawn sub-agent）
  // 这里用setTimeout模拟，实际会用sessions_spawn
  const result = await simulateAgentTask(task.agent, task.description);
  
  task.status = AgentStatus.DONE;
  task.completedAt = new Date().toISOString();
  task.result = result;
  collab.results[task.agent] = result;
  
  saveCollaboration(collab);
  console.log(`[Collaborator] ✅ 任务完成: ${task.agent}`);
  
  return result;
}

/**
 * 模拟Agent执行（实际用sessions_spawn）
 */
function simulateAgentTask(agent, description) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        agent,
        description,
        output: `✅ ${agent} 已完成: ${description}`,
        executedAt: new Date().toISOString()
      });
    }, 500);
  });
}

/**
 * 执行协作流程
 * @param {string} collabId - 协作ID
 */
async function runCollaboration(collabId) {
  const collab = loadCollaboration(collabId);
  if (!collab) {
    console.error(`[Collaborator] ❌ 协作不存在: ${collabId}`);
    return null;
  }
  
  if (collab.status === 'done') {
    console.log(`[Collaborator] ⚠️ 协作已完成: ${collabId}`);
    return collab;
  }
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`🚀 开始执行协作: ${collab.name}`);
  console.log(`类型: ${collab.type}`);
  console.log(`${'='.repeat(60)}`);
  
  collab.status = 'running';
  saveCollaboration(collab);
  
  try {
    if (collab.type === CollabType.PARALLEL) {
      // 并行执行：所有任务同时开始
      console.log('\n[并行模式] 同时启动所有任务...');
      await Promise.all(
        collab.tasks.map((_, i) => executeTask(collab, i))
      );
    } else if (collab.type === CollabType.SEQUENTIAL) {
      // 顺序执行：一个完成后下一个
      console.log('\n[顺序模式] 依次执行任务...');
      while (true) {
        const nextIndex = getNextRunnableTask(collab);
        if (nextIndex === -1) break;
        await executeTask(collab, nextIndex);
        
        // 检查是否所有任务完成
        const allDone = collab.tasks.every(t => t.status === AgentStatus.DONE);
        if (allDone) break;
      }
    } else if (collab.type === CollabType.HIERARCHICAL) {
      // 层级执行：先执行父任务，再执行子任务
      console.log('\n[层级模式] 先父后子...');
      // 找到父任务（dependsOn为空或索引为0的顶级任务）
      const parentIndex = collab.tasks.findIndex(t => 
        !t.dependsOn || t.dependsOn.length === 0
      );
      if (parentIndex >= 0) {
        await executeTask(collab, parentIndex);
      }
      // 然后处理剩余任务
      while (true) {
        const nextIndex = getNextRunnableTask(collab);
        if (nextIndex === -1) break;
        await executeTask(collab, nextIndex);
        
        const allDone = collab.tasks.every(t => t.status === AgentStatus.DONE);
        if (allDone) break;
      }
    }
    
    collab.status = 'done';
    saveCollaboration(collab);
    
    console.log(`\n${'='.repeat(60)}`);
    console.log(`✅ 协作完成: ${collab.name}`);
    console.log(`${'='.repeat(60)}`);
    
  } catch (error) {
    collab.status = 'failed';
    collab.error = error.message;
    saveCollaboration(collab);
    console.error(`[Collaborator] ❌ 协作失败: ${error.message}`);
  }
  
  return collab;
}

/**
 * 打印协作状态
 */
function printCollaborationStatus(collab) {
  console.log(`\n📋 协作: ${collab.name} (${collab.id})`);
  console.log(`状态: ${collab.status}`);
  console.log(`类型: ${collab.type}`);
  console.log('─'.repeat(50));
  
  for (let i = 0; i < collab.tasks.length; i++) {
    const task = collab.tasks[i];
    const statusIcon = {
      [AgentStatus.IDLE]: '⭕',
      [AgentStatus.WORKING]: '⚡',
      [AgentStatus.DONE]: '✅',
      [AgentStatus.FAILED]: '❌',
      [AgentStatus.BLOCKED]: '🚫'
    }[task.status];
    
    const deps = task.dependsOn && task.dependsOn.length > 0 
      ? ` ← [${task.dependsOn.join(', ')}]` 
      : '';
    
    console.log(`  ${statusIcon} [${i}] @${task.agent}: ${task.description}${deps}`);
    if (task.result) {
      console.log(`       结果: ${task.result.output || task.result}`);
    }
    if (task.error) {
      console.log(`       错误: ${task.error}`);
    }
  }
}

/**
 * 获取协作统计
 */
function getCollabStats() {
  const collabs = getAllCollaborations();
  
  return {
    total: collabs.length,
    pending: collabs.filter(c => c.status === 'pending').length,
    running: collabs.filter(c => c.status === 'running').length,
    done: collabs.filter(c => c.status === 'done').length,
    failed: collabs.filter(c => c.status === 'failed').length
  };
}

/**
 * 清理指定时间的旧协作（可选）
 */
function cleanupOldCollaborations(daysToKeep = 7) {
  const collabs = getAllCollaborations();
  const cutoff = Date.now() - daysToKeep * 24 * 60 * 60 * 1000;
  
  let deleted = 0;
  for (const collab of collabs) {
    if (new Date(collab.updatedAt).getTime() < cutoff) {
      const filePath = path.join(COLLAB_DIR, `${collab.id}.json`);
      fs.unlinkSync(filePath);
      deleted++;
    }
  }
  
  console.log(`[Collaborator] 🧹 清理了 ${deleted} 个旧协作`);
  return deleted;
}

// 导出模块
module.exports = {
  CollabType,
  AgentStatus,
  createCollaboration,
  loadCollaboration,
  getAllCollaborations,
  runCollaboration,
  printCollaborationStatus,
  getCollabStats,
  cleanupOldCollaborations,
  COLLAB_DIR
};
