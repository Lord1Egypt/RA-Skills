/**
 * SENSEN Collaboration Visualizer - P1-2
 * 协作流程可视化：生成 ASCII 时间线图
 * 
 * 支持：
 * 1. Timeline 视图 - 水平时间线显示执行顺序
 * 2. 状态面板 - 各任务状态一览
 * 3. 执行摘要 - 时间统计
 */

const {
  AgentStatus,
  getAllCollaborations,
  loadCollaboration
} = require('./sensen-collaborator');

// 本地状态控制，避免递归
let _suppressOutput = false;

/**
 * 格式化时长
 */
function formatDuration(ms) {
  if (!ms) return '-';
  const seconds = Math.floor(ms / 1000);
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
}

/**
 * 格式化时间
 */
function formatTime(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit' 
  });
}

/**
 * 计算任务耗时
 */
function getTaskDuration(task) {
  if (!task.startedAt || !task.completedAt) return null;
  return new Date(task.completedAt) - new Date(task.startedAt);
}

/**
 * 生成状态图标
 */
function getStatusIcon(status) {
  const icons = {
    [AgentStatus.IDLE]: '⭕',
    [AgentStatus.WORKING]: '🔄',
    [AgentStatus.DONE]: '✅',
    [AgentStatus.FAILED]: '❌',
    [AgentStatus.BLOCKED]: '🚫'
  };
  return icons[status] || '❓';
}

/**
 * 获取状态颜色代码（用于终端彩色输出）
 */
function getStatusColor(status) {
  const colors = {
    [AgentStatus.IDLE]: '\x1b[33m',    // 黄色
    [AgentStatus.WORKING]: '\x1b[36m',  // 青色
    [AgentStatus.DONE]: '\x1b[32m',     // 绿色
    [AgentStatus.FAILED]: '\x1b[31m',   // 红色
    [AgentStatus.BLOCKED]: '\x1b[35m'   // 紫色
  };
  return colors[status] || '\x1b[0m';
}

const RESET = '\x1b[0m';

/**
 * 生成单任务时间线
 */
function generateTaskTimeline(task, index, totalTasks, showDeps = true) {
  const statusIcon = getStatusIcon(task.status);
  const statusColor = getStatusColor(task.status);
  
  let line = `\n`;
  line += `${statusColor}${statusIcon}${RESET} [${index}] @${task.agent}\n`;
  line += `    任务: ${task.description}\n`;
  
  // 依赖关系
  if (showDeps && task.dependsOn && task.dependsOn.length > 0) {
    const depAgents = task.dependsOn.map(i => {
      return `[${i}]`;
    }).join(' → ');
    line += `    依赖: ${depAgents}\n`;
  }
  
  // 时间信息
  if (task.startedAt) {
    line += `    开始: ${formatTime(task.startedAt)}\n`;
  }
  if (task.completedAt) {
    line += `    结束: ${formatTime(task.completedAt)}\n`;
  }
  const duration = getTaskDuration(task);
  if (duration) {
    line += `    耗时: ${formatDuration(duration)}\n`;
  }
  
  // 结果/错误
  if (task.result && task.result.output) {
    const output = task.result.output.substring(0, 50);
    line += `    结果: ${output}${output.length > 50 ? '...' : ''}\n`;
  }
  if (task.error) {
    line += `    ${statusColor}❌ 错误: ${task.error}${RESET}\n`;
  }
  
  return line;
}

/**
 * 生成水平时间线视图
 */
function generateHorizontalTimeline(collab) {
  const lines = [];
  lines.push(`\n📊 时间线视图: ${collab.name}\n`);
  lines.push('═'.repeat(70));
  
  // 计算整体时间范围
  let earliestStart = null;
  let latestEnd = null;
  
  for (const task of collab.tasks) {
    if (task.startedAt) {
      const start = new Date(task.startedAt).getTime();
      if (!earliestStart || start < earliestStart) earliestStart = start;
    }
    if (task.completedAt) {
      const end = new Date(task.completedAt).getTime();
      if (!latestEnd || end > latestEnd) latestEnd = end;
    }
  }
  
  if (!earliestStart || !latestEnd) {
    lines.push('  (暂无时间数据)');
    return lines.join('\n');
  }
  
  const totalDuration = latestEnd - earliestStart;
  const timelineWidth = 50; // 时间线字符宽度
  
  // 绘制时间线
  for (let i = 0; i < collab.tasks.length; i++) {
    const task = collab.tasks[i];
    const statusIcon = getStatusIcon(task.status);
    
    let startPos = 0;
    let width = timelineWidth;
    
    if (task.startedAt && task.completedAt) {
      const start = new Date(task.startedAt).getTime();
      const end = new Date(task.completedAt).getTime();
      startPos = Math.floor(((start - earliestStart) / totalDuration) * timelineWidth);
      width = Math.max(1, Math.floor(((end - start) / totalDuration) * timelineWidth));
    } else if (task.startedAt) {
      const start = new Date(task.startedAt).getTime();
      startPos = Math.floor(((start - earliestStart) / totalDuration) * timelineWidth);
      width = timelineWidth - startPos;
    }
    
    // 生成任务条
    let bar = ' '.repeat(timelineWidth);
    const agentLabel = `@${task.agent.substring(0, 8)}`.padEnd(10);
    
    // 确定任务条字符
    const barChar = task.status === AgentStatus.DONE ? '█' :
                    task.status === AgentStatus.WORKING ? '▓' :
                    task.status === AgentStatus.FAILED ? '▒' : '░';
    
    // 边界检查
    const effectiveStart = Math.min(Math.max(0, startPos), timelineWidth - 1);
    const effectiveWidth = Math.max(0, Math.min(width, timelineWidth - effectiveStart));
    
    bar = bar.substring(0, effectiveStart) + 
          barChar.repeat(effectiveWidth) +
          bar.substring(effectiveStart + effectiveWidth);
    
    lines.push(`  ${statusIcon} ${agentLabel} |${bar}|`);
    
    // 显示时间戳
    if (task.startedAt) {
      lines.push(`             ${formatTime(task.startedAt)}`);
    }
  }
  
  // 时间轴
  lines.push('  ' + '─'.repeat(timelineWidth + 12));
  lines.push(`  开始: ${formatTime(new Date(earliestStart).toISOString())}`);
  lines.push(`  结束: ${formatTime(new Date(latestEnd).toISOString())}`);
  lines.push(`  总耗时: ${formatDuration(totalDuration)}`);
  
  return lines.join('\n');
}

/**
 * 生成详细状态面板
 */
function generateStatusPanel(collab) {
  const lines = [];
  
  lines.push(`\n📋 状态面板: ${collab.name}`);
  lines.push('═'.repeat(70));
  
  // 基本信息
  lines.push(`\n【基本信息】`);
  lines.push(`  ID: ${collab.id}`);
  lines.push(`  名称: ${collab.name}`);
  lines.push(`  类型: ${collab.type}`);
  lines.push(`  状态: ${collab.status}`);
  lines.push(`  创建: ${formatTime(collab.createdAt)}`);
  if (collab.updatedAt !== collab.createdAt) {
    lines.push(`  更新: ${formatTime(collab.updatedAt)}`);
  }
  
  // 统计
  const stats = {
    total: collab.tasks.length,
    done: collab.tasks.filter(t => t.status === AgentStatus.DONE).length,
    working: collab.tasks.filter(t => t.status === AgentStatus.WORKING).length,
    failed: collab.tasks.filter(t => t.status === AgentStatus.FAILED).length,
    idle: collab.tasks.filter(t => t.status === AgentStatus.IDLE).length
  };
  
  lines.push(`\n【执行统计】`);
  lines.push(`  总任务: ${stats.total}`);
  lines.push(`  ✅ 完成: ${stats.done}`);
  lines.push(`  🔄 进行: ${stats.working}`);
  lines.push(`  ❌ 失败: ${stats.failed}`);
  lines.push(`  ⭕ 等待: ${stats.idle}`);
  
  // 进度条
  const progress = stats.total > 0 ? stats.done / stats.total : 0;
  const barLength = 30;
  const filled = Math.round(progress * barLength);
  const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled);
  lines.push(`\n【进度】 [${bar}] ${Math.round(progress * 100)}%`);
  
  // 总耗时
  let totalDuration = 0;
  for (const task of collab.tasks) {
    const dur = getTaskDuration(task);
    if (dur) totalDuration += dur;
  }
  if (totalDuration > 0) {
    lines.push(`【总耗时】 ${formatDuration(totalDuration)}`);
  }
  
  return lines.join('\n');
}

/**
 * 生成任务详情列表
 */
function generateTaskList(collab) {
  const lines = [];
  
  lines.push(`\n📝 任务详情`);
  lines.push('─'.repeat(70));
  
  for (let i = 0; i < collab.tasks.length; i++) {
    lines.push(generateTaskTimeline(collab.tasks[i], i, collab.tasks.length));
  }
  
  return lines.join('\n');
}

/**
 * 生成完整可视化报告
 */
function generateFullReport(collabId) {
  const collab = loadCollaboration(collabId);
  if (!collab) {
    return { error: `协作 ${collabId} 不存在` };
  }
  
  const report = {
    summary: generateStatusPanel(collab),
    timeline: generateHorizontalTimeline(collab),
    tasks: generateTaskList(collab)
  };
  
  return report;
}

/**
 * 打印完整可视化报告
 */
function printVisualReport(collabId) {
  const report = generateFullReport(collabId);
  
  if (report.error) {
    console.error(report.error);
    return;
  }
  
  console.log(report.summary);
  console.log(report.timeline);
  console.log(report.tasks);
}

/**
 * 打印最近协作状态概览
 */
function printRecentCollabsOverview(count = 5) {
  const collabs = getAllCollaborations().slice(0, count);
  
  console.log(`\n📊 最近 ${collabs.length} 个协作概览`);
  console.log('═'.repeat(70));
  console.log(' ID                    名称                      状态   任务  耗时');
  console.log('─'.repeat(70));
  
  for (const collab of collabs) {
    const id = collab.id.substring(0, 20).padEnd(20);
    const name = (collab.name || '未命名').substring(0, 20).padEnd(20);
    const status = (collab.status || '-').padEnd(6);
    const taskCount = `${collab.tasks.length}个`.padEnd(5);
    
    // 计算耗时
    let totalDuration = 0;
    for (const task of collab.tasks) {
      const dur = getTaskDuration(task);
      if (dur) totalDuration += dur;
    }
    const duration = totalDuration > 0 ? formatDuration(totalDuration) : '-';
    
    console.log(` ${id} ${name} ${status} ${taskCount} ${duration}`);
  }
  
  console.log('─'.repeat(70));
}

/**
 * 打印实时进度（紧凑视图）
 */
function printProgressCompact(collab) {
  const done = collab.tasks.filter(t => t.status === AgentStatus.DONE).length;
  const total = collab.tasks.length;
  const progress = total > 0 ? Math.round(done / total * 100) : 0;
  
  // 进度条
  const barLength = 20;
  const filled = Math.round(progress / 100 * barLength);
  const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled);
  
  const statusIcon = collab.status === 'running' ? '🔄' :
                     collab.status === 'done' ? '✅' :
                     collab.status === 'failed' ? '❌' : '⭕';
  
  console.log(`\r${statusIcon} [${bar}] ${progress}% (${done}/${total}) ${collab.name}`);
}

// 导出
module.exports = {
  getStatusIcon,
  getStatusColor,
  formatDuration,
  formatTime,
  getTaskDuration,
  generateTaskTimeline,
  generateHorizontalTimeline,
  generateStatusPanel,
  generateTaskList,
  generateFullReport,
  printVisualReport,
  printRecentCollabsOverview,
  printProgressCompact
};
