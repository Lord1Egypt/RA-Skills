#!/usr/bin/env node
/**
 * CLI Commands Manager - CLI 命令管理工具
 * 提供所有 CLI 命令的列表、说明和使用示例
 */

const { execSync } = require('child_process');
const path = require('path');

/**
 * CLI 命令列表
 */
const CLI_COMMANDS = {
  'init-db': {
    name: 'init-db',
    description: '数据库初始化脚本',
    file: 'scripts/init-db.js',
    usage: 'node scripts/init-db.js',
    examples: [
      'node scripts/init-db.js - 初始化数据库和默认 Agent'
    ]
  },
  'config-cli': {
    name: 'config-cli',
    description: '配置管理工具',
    file: 'scripts/config-cli.js',
    usage: 'node scripts/config-cli.js <command> [options]',
    commands: [
      { name: 'init', desc: '初始化配置表' },
      { name: 'set', desc: '设置配置', args: '<key> <value> [description]' },
      { name: 'get', desc: '获取配置', args: '<key>' },
      { name: 'list', desc: '列出所有配置' },
      { name: 'delete', desc: '删除配置', args: '<key>' },
      { name: 'backup', desc: '备份配置' },
      { name: 'restore', desc: '恢复配置', args: '<filename>' },
      { name: 'export', desc: '导出配置', args: '<filename>' },
      { name: 'import', desc: '导入配置', args: '<filename>' }
    ],
    examples: [
      'node scripts/config-cli.js init',
      'node scripts/config-cli.js set AGENT_MAIN qqbot:c2c:USER_ID "主 Agent 地址"',
      'node scripts/config-cli.js list',
      'node scripts/config-cli.js backup'
    ]
  },
  'update-agent': {
    name: 'update-agent',
    description: 'Agent 地址更新脚本',
    file: 'scripts/update-agent.js',
    usage: 'node scripts/update-agent.js <command> [options]',
    commands: [
      { name: 'list', desc: '列出所有 Agent' },
      { name: 'update', desc: '更新 Agent 地址', args: '<name> <address>' },
      { name: 'activate', desc: '激活 Agent', args: '<name>' },
      { name: 'deactivate', desc: '停用 Agent', args: '<name>' }
    ],
    examples: [
      'node scripts/update-agent.js list',
      'node scripts/update-agent.js update coder-agent qqbot:c2c:NEW_USER_ID',
      'node scripts/update-agent.js activate coder-agent'
    ]
  },
  'agent-assign': {
    name: 'agent-assign',
    description: 'Agent 任务分配脚本',
    file: 'scripts/agent-assign.js',
    usage: 'node scripts/agent-assign.js <command> [options]',
    commands: [
      { name: 'list-agents', desc: '列出所有 Agent' },
      { name: 'list-tasks', desc: '列出待分配任务' },
      { name: 'assign', desc: '分配任务', args: '<task_id> <agent_name>' },
      { name: 'status', desc: '查看任务状态', args: '<task_id>' },
      { name: 'auto-assign', desc: '自动分配任务' }
    ],
    examples: [
      'node scripts/agent-assign.js list-agents',
      'node scripts/agent-assign.js list-tasks',
      'node scripts/agent-assign.js assign 1 coder-agent',
      'node scripts/agent-assign.js status 1'
    ]
  },
  'task-breakdown': {
    name: 'task-breakdown',
    description: '任务拆解脚本',
    file: 'scripts/task-breakdown.js',
    usage: 'node scripts/task-breakdown.js <command> [options]',
    commands: [
      { name: 'show', desc: '显示拆解结果', args: '<title> <description>' },
      { name: 'create', desc: '创建拆解任务', args: '<title> <description>' },
      { name: 'list', desc: '列出所有拆解任务' }
    ],
    examples: [
      'node scripts/task-breakdown.js show "新功能" "实现新功能"',
      'node scripts/task-breakdown.js create "新功能" "实现新功能"'
    ]
  },
  'task-cli': {
    name: 'task-cli',
    description: '任务管理 CLI 工具',
    file: 'scripts/task-cli.js',
    usage: 'node scripts/task-cli.js <command> [options]',
    commands: [
      { name: 'list', desc: '列出任务', args: '[options]' },
      { name: 'create', desc: '创建任务', args: '<title> [description] [priority]' },
      { name: 'view', desc: '查看任务详情', args: '<task_id>' },
      { name: 'update', desc: '更新任务', args: '<task_id> [options]' },
      { name: 'status', desc: '更新任务状态', args: '<task_id> <status>' },
      { name: 'complete', desc: '完成任务', args: '<task_id>' },
      { name: 'cancel', desc: '取消任务', args: '<task_id> [reason]' },
      { name: 'assign', desc: '分配任务', args: '<task_id> <agent_name>' },
      { name: 'dependency', desc: '添加依赖', args: '<task_id> <depends_on_id>' },
      { name: 'priority', desc: '设置优先级', args: '<task_id> <priority>' }
    ],
    examples: [
      'node scripts/task-cli.js list',
      'node scripts/task-cli.js list --status=pending',
      'node scripts/task-cli.js create "新任务" "任务描述" 1',
      'node scripts/task-cli.js view 1',
      'node scripts/task-cli.js assign 1 coder-agent'
    ]
  },
  'project-manager': {
    name: 'project-manager',
    description: '项目管理工具',
    file: 'scripts/project-manager.js',
    usage: 'node scripts/project-manager.js <command> [options]',
    commands: [
      { name: 'list', desc: '列出所有项目' },
      { name: 'create', desc: '创建项目', args: '<title> [description]' },
      { name: 'view', desc: '查看项目详情', args: '<project_id>' },
      { name: 'progress', desc: '查看项目进度', args: '<project_id>' },
      { name: 'report', desc: '生成项目报告', args: '<project_id>' },
      { name: 'daily', desc: '生成每日报告' }
    ],
    examples: [
      'node scripts/project-manager.js list',
      'node scripts/project-manager.js create "新项目" "项目描述"',
      'node scripts/project-manager.js progress 1',
      'node scripts/project-manager.js daily'
    ]
  },
  'agent-queue': {
    name: 'agent-queue',
    description: 'Agent 工作队列查看工具',
    file: 'scripts/agent-queue.js',
    usage: 'node scripts/agent-queue.js <command> [options]',
    commands: [
      { name: 'list', desc: '列出所有 Agent 队列' },
      { name: 'view', desc: '查看指定 Agent 队列', args: '<agent_name>' },
      { name: 'stats', desc: '显示 Agent 统计' }
    ],
    examples: [
      'node scripts/agent-queue.js list',
      'node scripts/agent-queue.js view coder-agent',
      'node scripts/agent-queue.js stats'
    ]
  },
  'main': {
    name: 'main',
    description: '系统主入口',
    file: 'scripts/main.js',
    usage: 'node scripts/main.js',
    examples: [
      'node scripts/main.js - 启动系统'
    ]
  }
};

/**
 * 显示所有命令列表
 */
function listAllCommands() {
  console.log('\n=== CLI 命令列表 ===\n');
  
  Object.values(CLI_COMMANDS).forEach((cmd, index) => {
    console.log(`${index + 1}. ${cmd.name}`);
    console.log(`   描述：${cmd.description}`);
    console.log(`   文件：${cmd.file}`);
    console.log(`   用法：${cmd.usage}`);
    console.log('');
  });
}

/**
 * 显示单个命令详情
 */
function showCommandDetail(commandName) {
  const cmd = CLI_COMMANDS[commandName];
  
  if (!cmd) {
    console.error(`❌ 命令不存在：${commandName}`);
    return;
  }
  
  console.log('\n=== 命令详情 ===\n');
  console.log(`名称：${cmd.name}`);
  console.log(`描述：${cmd.description}`);
  console.log(`文件：${cmd.file}`);
  console.log(`用法：${cmd.usage}`);
  console.log('');
  
  if (cmd.commands) {
    console.log('子命令:');
    cmd.commands.forEach(subCmd => {
      console.log(`  ${subCmd.name} ${subCmd.args || ''} - ${subCmd.desc}`);
    });
    console.log('');
  }
  
  if (cmd.examples) {
    console.log('示例:');
    cmd.examples.forEach(example => {
      console.log(`  ${example}`);
    });
    console.log('');
  }
}

/**
 * 搜索命令
 */
function searchCommands(keyword) {
  console.log(`\n=== 搜索：${keyword} ===\n`);
  
  const results = Object.values(CLI_COMMANDS).filter(cmd => 
    cmd.name.includes(keyword) || 
    cmd.description.toLowerCase().includes(keyword.toLowerCase())
  );
  
  if (results.length === 0) {
    console.log('未找到匹配的命令');
    return;
  }
  
  results.forEach(cmd => {
    console.log(`${cmd.name} - ${cmd.description}`);
  });
}

/**
 * 显示快速参考
 */
function showQuickReference() {
  console.log(`
=== 快速参考 ===

常用命令:
  初始化数据库：node scripts/init-db.js
  查看任务：node scripts/task-cli.js list
  创建任务：node scripts/task-cli.js create "标题" "描述"
  分配任务：node scripts/task-cli.js assign <id> <agent>
  查看项目：node scripts/project-manager.js list
  生成报告：node scripts/project-manager.js daily
  查看 Agent 队列：node scripts/agent-queue.js list

数据库配置:
  设置数据库类型：DB_TYPE=better-sqlite3
  设置数据库路径：DB_PATH=./db/mydb.db
  设置日志级别：LOG_LEVEL=DEBUG

环境变量:
  DB_TYPE - 数据库类型 (better-sqlite3, sqlite3, mysql, postgres)
  DB_PATH - 数据库路径
  DB_HOST - 数据库主机
  DB_PORT - 数据库端口
  DB_USER - 数据库用户
  DB_PASSWORD - 数据库密码
  DB_NAME - 数据库名称
  LOG_LEVEL - 日志级别 (DEBUG, INFO, WARN, ERROR)
  HEARTBEAT_INTERVAL - 心跳间隔 (分钟)
  SYNC_INTERVAL - 同步间隔 (分钟)
`);
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log(`
🚀 CLI Commands Manager - CLI 命令管理工具

用法:
  node scripts/cli-commands.js <command> [options]

命令:
  list                            列出所有命令
  show <command_name>             显示命令详情
  search <keyword>                搜索命令
  quick                          显示快速参考
  help                            显示帮助

示例:
  node scripts/cli-commands.js list
  node scripts/cli-commands.js show task-cli
  node scripts/cli-commands.js search task
  node scripts/cli-commands.js quick
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
      listAllCommands();
      break;
    
    case 'show':
      if (args.length < 2) {
        console.error('❌ 请提供命令名称');
        return;
      }
      showCommandDetail(args[1]);
      break;
    
    case 'search':
      if (args.length < 2) {
        console.error('❌ 请提供搜索关键词');
        return;
      }
      searchCommands(args[1]);
      break;
    
    case 'quick':
      showQuickReference();
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
  CLI_COMMANDS,
  listAllCommands,
  showCommandDetail,
  searchCommands,
  showQuickReference
};
