#!/usr/bin/env node
/**
 * Project Manager - 项目管理工具
 * 提供项目管理、进度跟踪、报告生成功能
 */

const { 
  createProject, 
  getProjectById, 
  getAllProjects,
  updateProject,
  deleteProject
} = require('../db/project-manager');

const {
  getAllTasks,
  getTasksByProject,
  getTasksByStatus,
  getTasksByAgent
} = require('../db/task-manager');

const {
  getAllAgents,
  getAgentByName
} = require('../db/agent-manager');

const {
  getHealthyAgents
} = require('../db/agent-health-manager');

const fs = require('fs');
const path = require('path');

/**
 * 计算项目进度
 */
function calculateProjectProgress(projectId) {
  const tasks = getTasksByProject(projectId);
  
  if (tasks.length === 0) {
    return {
      total: 0,
      completed: 0,
      inProgress: 0,
      pending: 0,
      cancelled: 0,
      percentage: 0
    };
  }
  
  const completed = tasks.filter(t => t.status === 'completed').length;
  const inProgress = tasks.filter(t => t.status === 'in_progress').length;
  const pending = tasks.filter(t => t.status === 'pending').length;
  const cancelled = tasks.filter(t => t.status === 'cancelled').length;
  
  const percentage = Math.round((completed / tasks.length) * 100);
  
  return {
    total: tasks.length,
    completed,
    inProgress,
    pending,
    cancelled,
    percentage
  };
}

/**
 * 获取项目整体进度说明
 */
function getProjectProgressDescription(projectId) {
  const project = getProjectById(projectId);
  const progress = calculateProjectProgress(projectId);
  
  let description = `## ${project.title} 项目进度报告\n\n`;
  description += `生成时间：${new Date().toLocaleString('zh-CN')}\n\n`;
  description += `### 项目信息\n`;
  description += `- **标题**: ${project.title}\n`;
  description += `- **描述**: ${project.description || '无'}\n`;
  description += `- **创建时间**: ${project.created_at}\n\n`;
  
  description += `### 进度概览\n`;
  description += `- **总任务数**: ${progress.total}\n`;
  description += `- **已完成**: ${progress.completed} (${progress.percentage}%)\n`;
  description += `- **进行中**: ${progress.inProgress}\n`;
  description += `- **待分配**: ${progress.pending}\n`;
  description += `- **已取消**: ${progress.cancelled}\n\n`;
  
  // 进度条
  const barLength = 40;
  const filledLength = Math.round((progress.percentage / 100) * barLength);
  const bar = '█'.repeat(filledLength) + '░'.repeat(barLength - filledLength);
  
  description += `### 进度条\n`;
  description += `\`\`\`\n`;
  description += `[${bar}] ${progress.percentage}%\n`;
  description += `\`\`\`\n\n`;
  
  // 任务详情
  description += `### 任务详情\n\n`;
  
  const tasks = getTasksByProject(projectId);
  
  if (tasks.length > 0) {
    description += `| ID | 标题 | 状态 | 优先级 | 分配给 | 创建时间 |\n`;
    description += `|----|------|------|--------|--------|----------|\n`;
    
    tasks.forEach(task => {
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
      
      description += `| ${task.id} | ${task.title} | ${statusLabel} | ${priorityLabel} | ${task.assigned_to || '未分配'} | ${task.created_at} |\n`;
    });
  } else {
    description += `暂无任务\n`;
  }
  
  return description;
}

/**
 * 生成每日报告
 */
function generateDailyReport() {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  
  let report = `# 每日报告 - ${dateStr}\n\n`;
  report += `生成时间：${now.toLocaleString('zh-CN')}\n\n`;
  
  // 1. 项目概览
  report += `## 项目概览\n\n`;
  
  const projects = getAllProjects();
  
  if (projects.length === 0) {
    report += `暂无项目\n\n`;
  } else {
    projects.forEach(project => {
      const progress = calculateProjectProgress(project.id);
      report += `### ${project.title}\n`;
      report += `- **进度**: ${progress.percentage}%\n`;
      report += `- **总任务**: ${progress.total}\n`;
      report += `- **已完成**: ${progress.completed}\n`;
      report += `- **进行中**: ${progress.inProgress}\n`;
      report += `- **待分配**: ${progress.pending}\n\n`;
    });
  }
  
  // 2. 任务统计
  report += `## 任务统计\n\n`;
  
  const allTasks = getAllTasks();
  const todayTasks = allTasks.filter(t => 
    t.created_at.startsWith(dateStr) || t.completed_at?.startsWith(dateStr)
  );
  
  report += `- **总任务数**: ${allTasks.length}\n`;
  report += `- **今日新增**: ${todayTasks.filter(t => t.created_at.startsWith(dateStr)).length}\n`;
  report += `- **今日完成**: ${todayTasks.filter(t => t.completed_at?.startsWith(dateStr)).length}\n`;
  report += `- **待分配**: ${getTasksByStatus('pending').length}\n`;
  report += `- **进行中**: ${getTasksByStatus('in_progress').length}\n\n`;
  
  // 3. Agent 工作队列
  report += `## Agent 工作队列\n\n`;
  
  const agents = getAllAgents();
  
  agents.forEach(agent => {
    if (agent.is_active !== 1) return;
    
    const agentTasks = getTasksByAgent(agent.name);
    const inProgressTasks = agentTasks.filter(t => t.status === 'in_progress');
    
    report += `### ${agent.name}\n`;
    report += `- **角色**: ${agent.role}\n`;
    report += `- **当前任务**: ${inProgressTasks.length}\n`;
    
    if (inProgressTasks.length > 0) {
      report += `\n**当前任务列表**:\n\n`;
      inProgressTasks.forEach(task => {
        const priorityLabel = {
          1: '🔴 高',
          2: '🟡 中',
          3: '🟢 低'
        }[task.priority] || '⚪ 普通';
        
        report += `- [${task.id}] ${task.title} (${priorityLabel})\n`;
      });
    }
    
    report += `\n`;
  });
  
  // 4. 高优先级任务
  report += `## 高优先级任务\n\n`;
  
  const highPriorityTasks = allTasks.filter(t => t.priority === 1 && t.status !== 'completed');
  
  if (highPriorityTasks.length > 0) {
    highPriorityTasks.forEach(task => {
      const statusLabel = {
        pending: '⏳ 待分配',
        in_progress: '🔄 进行中',
        cancelled: '❌ 已取消'
      }[task.status] || '❓ 未知';
      
      report += `- [${task.id}] ${task.title} - ${statusLabel}\n`;
    });
  } else {
    report += `暂无高优先级任务\n`;
  }
  
  report += `\n`;
  
  // 5. 健康状态
  report += `## 系统健康状态\n\n`;
  
  const healthyAgents = getHealthyAgents();
  const totalAgents = agents.filter(a => a.is_active === 1).length;
  
  report += `- **活跃 Agent**: ${healthyAgents.length}/${totalAgents}\n`;
  report += `- **健康率**: ${Math.round((healthyAgents.length / totalAgents) * 100)}%\n\n`;
  
  return report;
}

/**
 * 保存报告到文件
 */
function saveReport(report, filename) {
  const reportDir = path.join(__dirname, '..', 'reports');
  
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }
  
  const filepath = path.join(reportDir, filename);
  fs.writeFileSync(filepath, report, 'utf8');
  
  console.log(`✅ 报告已保存：${filepath}`);
}

/**
 * 列出项目
 */
function listProjects() {
  const projects = getAllProjects();
  
  if (projects.length === 0) {
    console.log('📭 暂无项目');
    return;
  }
  
  console.log('\n=== 项目列表 ===\n');
  
  projects.forEach((project, index) => {
    const progress = calculateProjectProgress(project.id);
    
    console.log(`${index + 1}. [${project.id}] ${project.title}`);
    console.log(`   描述：${project.description || '无'}`);
    console.log(`   进度：${progress.percentage}% (${progress.completed}/${progress.total})`);
    console.log(`   创建时间：${project.created_at}`);
    console.log('');
  });
}

/**
 * 创建项目
 */
function createProjectCmd(title, description) {
  try {
    const project = {
      title,
      description: description || undefined
    };
    
    const created = createProject(project);
    console.log(`✅ 项目创建成功！`);
    console.log(`   ID: ${created.id}`);
    console.log(`   标题：${created.title}`);
  } catch (error) {
    console.error('❌ 创建项目失败:', error.message);
  }
}

/**
 * 查看项目详情
 */
function viewProject(projectId) {
  const project = getProjectById(parseInt(projectId));
  
  if (!project) {
    console.error(`❌ 项目不存在：${projectId}`);
    return;
  }
  
  const progress = calculateProjectProgress(project.id);
  
  console.log('\n=== 项目详情 ===\n');
  console.log(`ID: ${project.id}`);
  console.log(`标题：${project.title}`);
  console.log(`描述：${project.description || '无'}`);
  console.log(`创建时间：${project.created_at}`);
  console.log('');
  console.log('=== 进度概览 ===');
  console.log(`总任务：${progress.total}`);
  console.log(`已完成：${progress.completed} (${progress.percentage}%)`);
  console.log(`进行中：${progress.inProgress}`);
  console.log(`待分配：${progress.pending}`);
  console.log(`已取消：${progress.cancelled}`);
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log(`
🚀 Project Manager - 项目管理工具

用法:
  node scripts/project-manager.js <command> [options]

命令:
  list                            列出所有项目
  create <title> [description]    创建项目
  view <project_id>               查看项目详情
  progress <project_id>           查看项目进度
  report <project_id>             生成项目报告
  daily                           生成每日报告
  help                            显示帮助

示例:
  node scripts/project-manager.js list
  node scripts/project-manager.js create "新项目" "项目描述"
  node scripts/project-manager.js view 1
  node scripts/project-manager.js progress 1
  node scripts/project-manager.js report 1
  node scripts/project-manager.js daily
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
      listProjects();
      break;
    
    case 'create':
      if (args.length < 2) {
        console.error('❌ 请提供项目标题');
        return;
      }
      createProjectCmd(args[1], args[2] || undefined);
      break;
    
    case 'view':
      if (args.length < 2) {
        console.error('❌ 请提供项目 ID');
        return;
      }
      viewProject(args[1]);
      break;
    
    case 'progress':
      if (args.length < 2) {
        console.error('❌ 请提供项目 ID');
        return;
      }
      const progressDesc = getProjectProgressDescription(parseInt(args[1]));
      console.log(progressDesc);
      break;
    
    case 'report':
      if (args.length < 2) {
        console.error('❌ 请提供项目 ID');
        return;
      }
      const report = getProjectProgressDescription(parseInt(args[1]));
      const filename = `project-${args[1]}-${new Date().toISOString().split('T')[0]}.md`;
      saveReport(report, filename);
      break;
    
    case 'daily':
      const dailyReport = generateDailyReport();
      const dailyFilename = `daily-report-${new Date().toISOString().split('T')[0]}.md`;
      saveReport(dailyReport, dailyFilename);
      console.log(dailyReport);
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
  calculateProjectProgress,
  getProjectProgressDescription,
  generateDailyReport,
  saveReport,
  listProjects,
  createProjectCmd,
  viewProject
};
