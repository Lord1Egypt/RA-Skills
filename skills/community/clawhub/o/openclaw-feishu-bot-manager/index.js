#!/usr/bin/env node
/**
 * feishu-bot-manager
 * 飞书多账户机器人配置管理 Skill
 * 
 * 支持的路由绑定方案：
 * 1. 账户级绑定 - 该飞书账户的所有消息路由到指定 Agent
 * 2. 群聊级绑定 - 特定群聊的消息路由到指定 Agent
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const {
  validateAppId,
  validateAccountId,
  validateChatId,
  validateConfig
} = require('./lib/validator');

// 配置路径
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw', 'openclaw.json');
const BACKUP_DIR = path.join(process.env.HOME, '.openclaw', 'backups');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
  bold: '\x1b[1m'
};

const log = {
  info: (msg) => console.log(`${colors.cyan}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  preview: (msg) => console.log(`${colors.gray}${msg}${colors.reset}`),
  bold: (msg) => console.log(`${colors.bold}${msg}${colors.reset}`)
};

function loadConfig() {
  try {
    const content = fs.readFileSync(CONFIG_PATH, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    log.error(`读取配置失败: ${err.message}`);
    process.exit(1);
  }
}

function cloneConfig(config) {
  return JSON.parse(JSON.stringify(config));
}

function saveConfig(config) {
  try {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf8');
    return true;
  } catch (err) {
    log.error(`保存配置失败: ${err.message}`);
    return false;
  }
}

function createBackup() {
  try {
    if (!fs.existsSync(BACKUP_DIR)) {
      fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(BACKUP_DIR, `openclaw.json.${timestamp}`);
    fs.copyFileSync(CONFIG_PATH, backupPath);
    return backupPath;
  } catch (err) {
    log.error(`创建备份失败: ${err.message}`);
    return null;
  }
}

function findConflicts(config, { mode, accountId, chatid, agentid }) {
  const conflicts = [];
  const bindings = config.bindings || [];

  bindings.forEach((binding, index) => {
    const match = binding.match || {};

    if (mode === 'account' && match.accountId === accountId) {
      conflicts.push(`binding[${index}] 已使用 accountId=${accountId}，当前绑定到 agent=${binding.agentId}`);
    }

    if (mode === 'group' && match.peer?.kind === 'group' && match.peer?.id === chatid) {
      conflicts.push(`binding[${index}] 已使用 chatId=${chatid}，当前绑定到 agent=${binding.agentId}`);
    }

    if (agentid && binding.agentId === agentid) {
      if (mode === 'account' && match.accountId && match.accountId !== accountId) {
        conflicts.push(`binding[${index}] 中 agent=${agentid} 已绑定其他账户 ${match.accountId}`);
      }
      if (mode === 'group' && match.peer?.kind === 'group' && match.peer?.id !== chatid) {
        conflicts.push(`binding[${index}] 中 agent=${agentid} 已绑定其他群 ${match.peer.id}`);
      }
    }
  });

  return conflicts;
}

function previewConfigChange(before, after, accountId) {
  const beforeAccounts = Object.keys(before.channels?.feishu?.accounts || {});
  const afterAccounts = Object.keys(after.channels?.feishu?.accounts || {});
  const beforeBindings = before.bindings || [];
  const afterBindings = after.bindings || [];

  console.log('\n配置变更预览:');
  console.log(`  账户数: ${beforeAccounts.length} -> ${afterAccounts.length}`);
  console.log(`  bindings: ${beforeBindings.length} -> ${afterBindings.length}`);
  if (!beforeAccounts.includes(accountId) && afterAccounts.includes(accountId)) {
    console.log(`  新账户: ${accountId}`);
  }
}

function showRoutingOptions() {
  console.log(`
${colors.bold}📋 路由绑定方案${colors.reset}

${colors.bold}方案 1：账户级绑定${colors.reset}
  该飞书账户的所有消息 → 指定 Agent
  适用：一个机器人专门服务一个 Agent
  
${colors.bold}方案 2：群聊级绑定${colors.reset}
  特定群聊的消息 → 指定 Agent
  适用：把 Agent 绑定到特定群聊

${colors.yellow}提示：群聊级绑定优先级更高，会覆盖账户级绑定！${colors.reset}
`);
}

async function quickMode(options) {
  console.log(`\n${colors.cyan}🤖 飞书机器人配置助手${colors.reset}\n`);
  
  const { 
    appid, 
    appsecret, 
    accountid,
    botname,
    agentid, 
    chatid,
    routingmode,
    dryrun,
    force,
    norestart
  } = options;
  
  if (!appid || !appsecret) {
    log.error('需要提供 --app-id 和 --app-secret');
    process.exit(1);
  }

  if (!validateAppId(appid)) {
    log.error(`App ID 格式无效: ${appid}`);
    process.exit(1);
  }
  
  const config = loadConfig();
  const originalConfig = cloneConfig(config);
  const accountId = accountid || `bot-${Date.now()}`;

  if (!validateAccountId(accountId)) {
    log.error(`账户 ID 格式无效: ${accountId}`);
    process.exit(1);
  }

  if (config.channels?.feishu?.accounts?.[accountId]) {
    log.error(`账户 ID 已存在: ${accountId}`);
    process.exit(1);
  }

  const mode = routingmode || 'account';

  if (!['account', 'group'].includes(mode)) {
    log.error(`routing-mode 只支持 account 或 group，收到: ${mode}`);
    process.exit(1);
  }

  if (mode === 'group') {
    if (!chatid) {
      log.error('群聊级绑定需要提供 --chat-id');
      process.exit(1);
    }
    if (!validateChatId(chatid)) {
      log.error(`群聊 ID 格式无效: ${chatid}`);
      process.exit(1);
    }
  }

  const conflicts = findConflicts(config, { mode, accountId, chatid, agentid });
  if (conflicts.length > 0 && !force) {
    log.error('发现潜在冲突:');
    conflicts.forEach((item) => log.error(`  ${item}`));
    log.info('如确认覆盖风险，请追加 --force');
    process.exit(1);
  }

  if (conflicts.length > 0 && force) {
    log.warning('检测到冲突，但将按 --force 继续');
    conflicts.forEach((item) => log.warning(`  ${item}`));
  }
  
  const backupPath = createBackup();
  if (!backupPath) {
    log.error('无法创建配置备份，中止写入');
    process.exit(1);
  }
  log.success(`配置已备份: ${path.basename(backupPath)}`);
  
  if (!config.channels) config.channels = {};
  if (!config.channels.feishu) config.channels.feishu = { enabled: true };
  if (!config.channels.feishu.accounts) config.channels.feishu.accounts = {};
  
  config.channels.feishu.accounts[accountId] = {
    appId: appid,
    appSecret: appsecret,
    botName: botname || 'Feishu Bot',
    dmPolicy: options.dmpolicy || 'open',
    allowFrom: ['*'],
    enabled: true
  };
  
  if (!config.bindings) config.bindings = [];
  
  if (mode === 'account' && agentid) {
    config.bindings.push({
      agentId: agentid,
      match: {
        channel: 'feishu',
        accountId: accountId
      }
    });
    log.success(`已添加账户级绑定: ${agentid} ← ${accountId}`);
  } else if (mode === 'group' && agentid) {
    config.bindings.push({
      agentId: agentid,
      match: {
        channel: 'feishu',
        peer: { kind: 'group', id: chatid }
      }
    });
    log.success(`已添加群聊级绑定: ${agentid} ← ${chatid}`);
  }

  const errors = validateConfig(config);
  if (errors.length > 0) {
    log.error('配置校验失败:');
    errors.forEach((err) => log.error(`  ${err}`));
    log.info(`可从备份恢复: cp ${backupPath} ${CONFIG_PATH}`);
    process.exit(1);
  }

  previewConfigChange(originalConfig, config, accountId);

  if (dryrun === 'true') {
    log.success('dry-run 完成，未写入配置，未重启 Gateway');
    process.exit(0);
  }
  
  saveConfig(config);
  log.success('配置已更新');
  
  log.info('设置会话绑定颗粒度...');
  try {
    execSync('openclaw config set session.dmScope "per-account-channel-peer"', { stdio: 'pipe' });
    log.success('会话绑定颗粒度已设置');
  } catch (err) {
    log.warning('设置 dmScope 失败，请手动执行:');
    console.log('  openclaw config set session.dmScope "per-account-channel-peer"');
  }
  
  if (norestart === 'true') {
    log.warning('已跳过 Gateway 重启，请手动执行: openclaw gateway restart');
  } else {
    log.warning('正在重启 Gateway...');
    try {
      execSync('openclaw gateway restart', { stdio: 'inherit' });
      log.success('Gateway 重启完成');
    } catch (err) {
      log.error(`重启失败: ${err.message}`);
      log.info('请手动执行: openclaw gateway restart');
    }
  }
  
  console.log('\n' + '─'.repeat(50));
  log.success('配置完成！');
  console.log('\n配置摘要:');
  console.log(`  账户 ID: ${accountId}`);
  console.log(`  路由模式: ${mode}`);
  if (agentid) console.log(`  Agent: ${agentid}`);
  if (chatid) console.log(`  群聊: ${chatid}`);
  console.log('\n如配置有误，可从备份恢复:');
  console.log(`  cp ${backupPath} ${CONFIG_PATH}`);
  console.log('─'.repeat(50) + '\n');
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-/g, '');
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      options[key] = value;
      if (value !== 'true') i++;
    }
  }
  
  return options;
}

const options = parseArgs();

if (options.help || options.h) {
  showRoutingOptions();
  console.log(`
${colors.bold}用法:${colors.reset}
  node index.js [选项]

${colors.bold}选项:${colors.reset}
  --app-id <id>          飞书 App ID (必填)
  --app-secret <secret>  飞书 App Secret (必填)
  --account-id <id>      账户标识 (可选, 默认自动生成)
  --bot-name <name>      机器人名称 (可选)
  --dm-policy <policy>   DM 策略: open/pairing/allowlist (默认: open)
  --agent-id <id>        要绑定的 Agent ID (可选)
  --chat-id <id>         群聊 ID oc_xxx (群聊绑定时需要)
  --routing-mode <mode>  路由模式: account/group (默认: account)
  --dry-run              仅预览变更，不写入配置，不重启
  --force                忽略冲突警告，继续执行
  --no-restart           写入配置后不自动重启 Gateway
  --help, -h             显示帮助

${colors.bold}示例:${colors.reset}
  # 账户级绑定预演
  node index.js --app-id cli_xxx --app-secret yyy --agent-id recruiter --routing-mode account --dry-run

  # 群聊级绑定，不自动重启
  node index.js --app-id cli_xxx --app-secret yyy --agent-id recruiter --chat-id oc_xxx --routing-mode group --no-restart
`);
  process.exit(0);
}

if (options.appid) {
  quickMode(options);
} else {
  log.error('请提供 --app-id 和 --app-secret，或使用 --help 查看帮助');
  process.exit(1);
}
