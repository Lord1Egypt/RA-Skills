#!/usr/bin/env node
/**
 * Hermes 项目共享系统 — CLI 管理工具
 * 
 * 用法:
 *   project list                   查看所有项目
 *   project show <id>             查看项目详情
 *   project add <id> --name ...   添加新项目
 *   project update <id> --status  更新项目状态
 *   project sync                  同步到记忆系统
 *   project template <id>         创建新项目模板
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = process.env.CLAWHUB_WORKDIR || path.join(__dirname, '..');
const JSON_PATH = path.join(WORKSPACE, 'projects_status.json');
const MD_PATH = path.join(WORKSPACE, 'PROJECT_STATUS.md');
const SCRIPT_PATH = path.join(WORKSPACE, 'scripts', 'update_project_status.js');

// ===== 辅助函数 =====

function readJSON() {
  try {
    return JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
  } catch (e) {
    console.error('❌ 读取 projects_status.json 失败:', e.message);
    process.exit(1);
  }
}

function writeJSON(data) {
  data.last_updated = new Date().toISOString();
  data.updated_by = process.env.AGENT_ID || 'agent:main:main';
  fs.writeFileSync(JSON_PATH, JSON.stringify(data, null, 2), 'utf8');
  regenerateMD();
  logToMemory(data);
}

function regenerateMD() {
  try {
    require(SCRIPT_PATH);
  } catch (e) {
    // 如果直接 require 失败，用子进程调用
    try {
      execSync(`node "${SCRIPT_PATH}"`, { stdio: 'inherit', cwd: WORKSPACE });
    } catch (e2) {
      console.error('⚠️  重新生成 PROJECT_STATUS.md 失败:', e2.message);
    }
  }
}

function logToMemory(data) {
  // 将项目更新记录到每日记忆文件
  const now = new Date();
  const dateStr = now.toISOString().substring(0, 10); // YYYY-MM-DD
  const timeStr = now.toISOString().substring(11, 19);
  const memDir = path.join(WORKSPACE, 'memory');
  const memFile = path.join(memDir, `${dateStr}.md`);

  if (!fs.existsSync(memDir)) {
    fs.mkdirSync(memDir, { recursive: true });
  }

  const entry = `\n## ${dateStr}T${timeStr}.000000\n项目共享系统: ${data.last_updated_by} 更新项目状态\n`;

  try {
    fs.appendFileSync(memFile, entry, 'utf8');
  } catch (e) {
    // 静默失败
  }
}

function truncate(s, len) {
  return s.length > len ? s.substring(0, len - 1) + '…' : s;
}

// ===== 命令处理 =====

function cmdList() {
  const data = readJSON();
  console.log('\n📋 项目共享系统 — 项目列表');
  console.log('='.repeat(60));
  console.log(`最后更新: ${data.last_updated} | 更新者: ${data.updated_by}`);
  console.log('-'.repeat(60));
  
  data.projects.forEach((p, i) => {
    const statusIcon = p.status === 'completed' ? '✅' : 
                      p.status === 'in_progress' ? '🔄' : '⏸️';
    const priorityIcon = p.priority === 'high' ? '🔴' : 
                        p.priority === 'medium' ? '🟡' : '🟢';
    console.log(`\n${i + 1}. ${statusIcon} ${priorityIcon} ${p.name}`);
    console.log(`   ID: ${p.id} | 状态: ${p.status} | 优先级: ${p.priority}`);
    console.log(`   ${truncate(p.current_task, 50)}`);
  });
  console.log(`\n${'='.repeat(60)}\n`);
}

function cmdShow(id) {
  const data = readJSON();
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.error(`❌ 未找到项目: ${id}`);
    console.log(`可用项目: ${data.projects.map(p => p.id).join(', ')}`);
    process.exit(1);
  }

  const statusIcon = project.status === 'completed' ? '✅' : 
                    project.status === 'in_progress' ? '🔄' : '⏸️';

  console.log(`\n${statusIcon} ${project.name}`);
  console.log('='.repeat(50));
  console.log(`  ID:         ${project.id}`);
  console.log(`  状态:       ${project.status}`);
  console.log(`  优先级:     ${project.priority}`);
  console.log(`  创建时间:   ${project.created_at}`);
  console.log(`  最后更新:   ${project.updated_at}`);
  console.log(`  描述:       ${project.description}`);
  console.log(`  当前任务:   ${project.current_task}`);
  console.log(`  涉及Agent:  ${project.agents_involved.join(', ')}`);
  
  if (project.history && project.history.length > 0) {
    console.log(`\n  📝 历史记录 (${project.history.length}条):`);
    project.history.slice(-5).forEach(h => {
      console.log(`    [${new Date(h.timestamp).toISOString().substring(11, 16)}] ${h.action}: ${truncate(h.description, 60)}`);
    });
  }
  
  if (project.errors && project.errors.length > 0) {
    console.log(`\n  ⚠️  问题记录 (${project.errors.length}条):`);
    project.errors.forEach(e => {
      console.log(`    ❌ ${truncate(e.error, 50)} → ${truncate(e.resolution, 40)}`);
    });
  }
  console.log('');
}

function cmdAdd(id, options) {
  const data = readJSON();
  
  if (data.projects.find(p => p.id === id)) {
    console.error(`❌ 项目已存在: ${id}`);
    process.exit(1);
  }

  const now = new Date().toISOString();
  const newProject = {
    id: id,
    name: options.name || id,
    description: options.desc || '',
    status: options.status || 'in_progress',
    priority: options.priority || 'medium',
    current_task: options.task || '项目初始化',
    agents_involved: [options.agent || 'agent:main:main'],
    created_at: now,
    updated_at: now,
    history: [{
      timestamp: now,
      agent: options.agent || 'agent:main:main',
      action: '项目开始',
      description: options.desc || `创建项目: ${options.name || id}`
    }],
    errors: []
  };

  data.projects.push(newProject);
  writeJSON(data);
  console.log(`✅ 项目创建成功: ${options.name || id} (${id})`);
}

function cmdUpdate(id, options) {
  const data = readJSON();
  const project = data.projects.find(p => p.id === id);
  if (!project) {
    console.error(`❌ 未找到项目: ${id}`);
    process.exit(1);
  }

  const now = new Date().toISOString();
  const changes = [];

  if (options.status) {
    const oldStatus = project.status;
    project.status = options.status;
    changes.push(`状态: ${oldStatus} → ${options.status}`);
  }
  if (options.task) {
    project.current_task = options.task;
    changes.push(`任务更新: ${options.task}`);
  }
  if (options.desc) {
    project.description = options.desc;
    changes.push(`描述更新`);
  }
  if (options.priority) {
    project.priority = options.priority;
    changes.push(`优先级: ${options.priority}`);
  }
  if (options.name) {
    const oldName = project.name;
    project.name = options.name;
    changes.push(`名称: ${oldName} → ${options.name}`);
  }

  project.updated_at = now;
  
  if (changes.length > 0) {
    project.history.push({
      timestamp: now,
      agent: options.agent || 'agent:main:main',
      action: options.action || '状态更新',
      description: changes.join('; ')
    });
  }

  writeJSON(data);
  console.log(`✅ 项目更新成功: ${project.name}`);
  changes.forEach(c => console.log(`   • ${c}`));
}

function cmdSync() {
  const data = readJSON();
  console.log('🔄 同步项目共享系统...');
  
  // 1. 更新时间戳
  data.last_updated = new Date().toISOString();
  data.updated_by = process.env.AGENT_ID || 'agent:main:main';
  
  // 2. 写入 JSON
  fs.writeFileSync(JSON_PATH, JSON.stringify(data, null, 2), 'utf8');
  console.log('✅ projects_status.json 已更新');
  
  // 3. 重新生成 Markdown
  regenerateMD();
  console.log('✅ PROJECT_STATUS.md 已更新');
  
  // 4. 记录到记忆
  logToMemory(data);
  console.log('✅ 记忆系统已记录');
  
  console.log('🎉 同步完成!');
  // 自动备份
  try {
    const { execSync } = require('child_process');
    const backupScript = path.join(__dirname, 'auto_backup.sh');
    if (require('fs').existsSync(backupScript)) {
      execSync('bash ' + backupScript, { stdio: 'inherit' });
    }
  } catch(e) { /* backup silently */ }
}

function cmdTemplate(id) {
  if (!id) {
    console.error('❌ 请指定项目 ID');
    process.exit(1);
  }
  
  console.log(`\n📋 项目模板: ${id}`);
  console.log('='.repeat(50));
  console.log(`
{
  "id": "${id}",
  "name": "项目名称",
  "description": "项目描述",
  "status": "in_progress",
  "priority": "medium",
  "current_task": "初始任务",
  "agents_involved": ["agent:main:main"],
  "created_at": "${new Date().toISOString()}",
  "updated_at": "${new Date().toISOString()}",
  "history": [{
    "timestamp": "${new Date().toISOString()}",
    "agent": "agent:main:main",
    "action": "项目开始",
    "description": "创建项目"
  }],
  "errors": []
}`);
  console.log('');
  console.log('快速创建:');
  console.log(`  project add ${id} --name "项目名称" --desc "描述" --priority high`);
}

// ===== 主入口 =====

function cmdSnapshot() {
  const data = readJSON();
  const now = new Date();
  const active = data.projects.filter(p => p.status === 'in_progress');
  const completed = data.projects.filter(p => p.status === 'completed');
  
  console.log('📋 项目状态快照');
  console.log('='.repeat(50));
  console.log(`生成时间: ${now.toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'})}`);
  console.log(`更新者: ${data.updated_by}\n`);
  
  console.log(`活跃项目 (${active.length}):`);
  active.forEach(p => console.log(`  🔄 ${p.name}: ${p.current_task}`));
  console.log();
  console.log(`已完成项目 (${completed.length}):`);
  completed.forEach(p => console.log(`  ✅ ${p.name}`));
  console.log();
  console.log(`总计: ${data.projects.length} 个项目`);
}

function cmdSummary() {
  const data = readJSON();
  console.log('📊 项目摘要报告');
  console.log('='.repeat(50));
  console.log(`最后更新: ${data.last_updated}\n`);
  
  const statusCounts = {};
  const priorityCounts = {};
  
  data.projects.forEach(p => {
    statusCounts[p.status] = (statusCounts[p.status] || 0) + 1;
    priorityCounts[p.priority] = (priorityCounts[p.priority] || 0) + 1;
  });
  
  console.log('状态分布:');
  Object.entries(statusCounts).forEach(([k, v]) => {
    const icon = k === 'completed' ? '✅' : k === 'in_progress' ? '🔄' : '⏸️';
    console.log(`  ${icon} ${k}: ${v}`);
  });
  console.log();
  
  console.log('优先级分布:');
  Object.entries(priorityCounts).forEach(([k, v]) => {
    const icon = k === 'high' ? '🔴' : k === 'medium' ? '🟡' : '🟢';
    console.log(`  ${icon} ${k}: ${v}`);
  });
}

function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'help' || cmd === '--help') {
    console.log(`
📋 Hermes 项目共享系统 — CLI 管理工具

用法:
  project list                          查看所有项目
  project show <id>                     查看项目详情
  project add <id> [options]            添加新项目
  project update <id> [options]         更新项目状态
  project sync                          同步 JSON + MD + 记忆
  project template <id>                 生成项目模板

选项:
  --name <name>         项目名称
  --desc <desc>         项目描述
  --status <status>     状态: in_progress | completed | paused
  --priority <pri>      优先级: high | medium | low
  --task <task>         当前任务描述
  --action <action>     操作名称 (如: Phase 1 完成)
  --agent <agent>       Agent 标识

示例:
  project list
  project show hermes_agent_learning
  project add my_project --name "我的项目" --desc "项目描述" --priority high
  project update hermes_agent_learning --status completed --task "全部完成"
  project sync
`);
    return;
  }

  switch (cmd) {
    case 'list':
      cmdList();
      break;
    case 'show':
      cmdShow(args[1]);
      break;
    case 'add': {
      const idx = args.indexOf('--name');
      const name = idx !== -1 ? args[idx + 1] : undefined;
      const descIdx = args.indexOf('--desc');
      const desc = descIdx !== -1 ? args[descIdx + 1] : undefined;
      const statusIdx = args.indexOf('--status');
      const status = statusIdx !== -1 ? args[statusIdx + 1] : undefined;
      const priorityIdx = args.indexOf('--priority');
      const priority = priorityIdx !== -1 ? args[priorityIdx + 1] : undefined;
      const taskIdx = args.indexOf('--task');
      const task = taskIdx !== -1 ? args[taskIdx + 1] : undefined;
      const agentIdx = args.indexOf('--agent');
      const agent = agentIdx !== -1 ? args[agentIdx + 1] : undefined;
      cmdAdd(args[1], { name, desc, status, priority, task, agent });
      break;
    }
    case 'update': {
      const options = {};
      ['name', 'desc', 'status', 'priority', 'task', 'action', 'agent'].forEach(key => {
        const idx = args.indexOf(`--${key}`);
        if (idx !== -1) options[key] = args[idx + 1];
      });
      cmdUpdate(args[1], options);
      break;
    }
    case 'sync':
      cmdSync();
      break;
    case 'snapshot':
      cmdSnapshot();
      break;
    case 'summary':
      cmdSummary();
      break;
    case 'template':
      cmdTemplate(args[1]);
      break;
    default:
      console.error(`❌ 未知命令: ${cmd}`);
      console.log('可用命令: list, show, add, update, sync, snapshot, summary, template');
      process.exit(1);
  }
}

main();
