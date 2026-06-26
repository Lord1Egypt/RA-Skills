#!/usr/bin/env node
/**
 * EO Agent Auto-Config Script
 * 
 * 自动为所有agent workspace配置EO-Enhanced能力
 * 
 * 用法:
 *   node eo-init.js                    # 配置所有workspace
 *   node eo-init.js --dry-run         # 预览模式
 *   node eo-init.js --agent jisu-admin # 只配置指定agent
 *   node eo-init.js --force           # 覆盖已存在的SOUL.md
 */

import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 配置
const CONFIG = {
  pluginName: 'eo-collaboration',
  addonFile: 'templates/SOUL-eo-addon.md',
  openclawConfig: '.openclaw/openclaw.json',
  workspaces: '.openclaw/workspace',
};

// ANSI颜色
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    target: 'all',
    agentIds: [],
    force: false,
    dryRun: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--dry-run':
        options.dryRun = true;
        break;
      case '--force':
        options.force = true;
        break;
      case '--agent':
        options.target = 'specific';
        options.agentIds.push(args[++i]);
        break;
    }
  }

  return options;
}

// 读取OpenClaw配置
function loadOpenClawConfig() {
  const configPath = join(process.env.HOME, CONFIG.openclawConfig);
  try {
    const content = readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    log(`无法读取OpenClaw配置: ${configPath}`, 'red');
    process.exit(1);
  }
}

// 获取所有agent列表
function getAgentList(config) {
  const agents = config.agents?.list || [];
  return agents.map(a => ({
    id: a.id,
    name: a.name,
    workspace: a.workspace || join(process.env.HOME, '.openclaw/workspace', `workspace-${a.id}`),
  }));
}

// 检查workspace是否存在
function workspaceExists(workspace) {
  return existsSync(workspace) && statSync(workspace).isDirectory();
}

// 读取现有SOUL.md
function readSoul(workspace) {
  const soulPath = join(workspace, 'SOUL.md');
  if (existsSync(soulPath)) {
    return readFileSync(soulPath, 'utf-8');
  }
  return null;
}

// 检查是否已是EO-Enhanced
function isEOEnhanced(soul) {
  return soul && soul.includes('EO-Enhanced');
}

// 生成新版SOUL.md
function generateEOSoul(existingSoul, agentId, agentName) {
  const addonPath = join(__dirname, '..', CONFIG.addonFile);
  let addon = '';
  
  if (existsSync(addonPath)) {
    addon = readFileSync(addonPath, 'utf-8');
  } else {
    // 内联fallback addon内容
    addon = getInlineAddon();
  }

  if (!existingSoul) {
    // 创建新的SOUL.md
    return `# SOUL.md - ${agentName}

_EO-Enhanced Agent - ${new Date().toISOString().split('T')[0]}_

${addon}
`;
  }

  // 更新已存在的SOUL.md
  if (isEOEnhanced(existingSoul)) {
    return null; // 已是EO版本
  }

  // 在文件末尾追加EO增强
  return `${existingSoul}\n\n---\n\n${addon}\n`;
}

// 内联fallback (当addon文件不存在时)
function getInlineAddon() {
  return `## 🚀 EO-Enhanced 能力

### 可用工具
- eo_collab: 多专家协作
- eo_plan: 项目规划  
- eo_architect: 架构设计
- eo_verify: 检查点验证
- eo_code_review: 代码审查

### 141专家军团
当遇到问题时，召唤对应领域专家协助。

### 主动感知规则
- 复杂任务自动触发多专家协作
- 上下文>70%自动压缩
- 会话结束自动记忆同步
- 30分钟空闲触发Dream Module

_🦞⚙️ EO-Enhanced Mode_
`;
}

// 写入SOUL.md
function writeSoul(workspace, content) {
  const soulPath = join(workspace, 'SOUL.md');
  writeFileSync(soulPath, content, 'utf-8');
}

// 主流程
async function main() {
  log('🦞 EO Agent Auto-Config', 'blue');
  log('=====================\n', 'blue');

  const options = parseArgs();
  const config = loadOpenClawConfig();
  let agents = getAgentList(config);

  // 过滤目标agents
  if (options.target === 'specific') {
    agents = agents.filter(a => options.agentIds.includes(a.id));
  }

  log(`检测到 ${agents.length} 个agent workspaces\n`, 'yellow');

  const results = {
    success: 0,
    skipped: 0,
    failed: 0,
    details: [],
  };

  for (const agent of agents) {
    const workspace = agent.workspace;
    const soulPath = join(workspace, 'SOUL.md');

    log(`处理 ${agent.id} (${agent.name})...`, 'blue');

    // 检查workspace是否存在
    if (!workspaceExists(workspace)) {
      log(`  ⏭️  Workspace不存在: ${workspace}`, 'yellow');
      results.skipped++;
      results.details.push({ id: agent.id, status: 'skipped', reason: 'workspace not found' });
      continue;
    }

    // 读取现有SOUL
    const existingSoul = readSoul(workspace);

    // 检查是否已是EO版本
    if (existingSoul && isEOEnhanced(existingSoul) && !options.force) {
      log(`  ✅ 已是EO-Enhanced版本，跳过`, 'green');
      results.skipped++;
      results.details.push({ id: agent.id, status: 'skipped', reason: 'already EO-Enhanced' });
      continue;
    }

    // 生成新版SOUL
    const newSoul = generateEOSoul(existingSoul, agent.id, agent.name);

    if (!newSoul) {
      log(`  ⏭️  已是EO-Enhanced版本`, 'green');
      results.skipped++;
      results.details.push({ id: agent.id, status: 'skipped', reason: 'already EO-Enhanced' });
      continue;
    }

    if (options.dryRun) {
      log(`  📋 [DRY-RUN] 将创建/更新: ${soulPath}`, 'yellow');
    } else {
      try {
        writeSoul(workspace, newSoul);
        log(`  ✅ 已配置EO-Enhanced能力`, 'green');
        results.success++;
        results.details.push({ id: agent.id, status: 'success' });
      } catch (e) {
        log(`  ❌ 写入失败: ${e.message}`, 'red');
        results.failed++;
        results.details.push({ id: agent.id, status: 'failed', error: e.message });
      }
    }
  }

  // 输出总结
  log('\n=====================', 'blue');
  log('📊 配置完成', 'blue');
  log(`  ✅ 成功: ${results.success}`);
  log(`  ⏭️  跳过: ${results.skipped}`);
  log(`  ❌ 失败: ${results.failed}`);

  if (options.dryRun) {
    log('\n💡 这只是预览模式，要实际执行请去掉 --dry-run 参数', 'yellow');
  }

  return results;
}

main().catch(e => {
  log(`Fatal error: ${e.message}`, 'red');
  process.exit(1);
});
