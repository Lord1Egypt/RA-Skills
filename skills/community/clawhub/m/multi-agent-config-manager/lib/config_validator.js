/**
 * 配置验证器 - 检查系统配置是否满足 multi-agent-engine 运行要求
 * 返回详细的配置检查报告，并在用户同意后自动完成配置
 */

import fs from 'fs';
import path from 'path';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');

// ===================== 配置检查项 =====================

/**
 * 检查 OpenClaw 版本
 */
export function checkOpenClawVersion() {
  const version = process.env.OPENCLAW_VERSION || 'unknown';
  const [major] = version.split('.').map(Number);

  if (major < 2026) {
    return {
      name: 'OpenClaw 版本',
      status: 'error',
      required: '2026.3.x+',
      current: version,
      message: `当前版本 ${version} 低于最低要求 2026.3.x+，多代理功能需要更新的 OpenClaw 版本支持 sessions_spawn API`
    };
  }

  return {
    name: 'OpenClaw 版本',
    status: 'pass',
    required: '2026.3.x+',
    current: version,
    message: `版本 ${version} 符合要求，支持多代理 API`
  };
}

/**
 * 检查 Node.js 版本
 */
export function checkNodeVersion() {
  const version = process.version;
  const [major, minor] = version.slice(1).split('.').map(Number);

  if (major < 20 || (major === 20 && minor < 5)) {
    return {
      name: 'Node.js 版本',
      status: 'error',
      required: '20.x+',
      current: version,
      message: `当前版本 ${version} 低于最低要求 20.x+，建议升级到 20.5+ 以获得更好的 ES Module 支持`
    };
  }

  return {
    name: 'Node.js 版本',
    status: 'pass',
    required: '20.x+',
    current: version,
    message: `版本 ${version} 符合要求，ES Module 支持良好`
  };
}

/**
 * 检查工作区目录结构
 */
export function checkWorkspaceStructure() {
  const checks = [
    {
      name: '工作区根目录',
      path: CONFIG_DIR,
      description: 'OpenClaw 工作区根目录，存放所有配置和输出文件',
      required: true,
      action: () => fs.mkdirSync(CONFIG_DIR, { recursive: true }),
      impact: '多代理系统运行的基础目录，必须存在'
    },
    {
      name: 'agents/ 代理工作区',
      path: path.join(CONFIG_DIR, 'agents'),
      description: '各代理的独立工作区，每个代理有自己的历史研究子目录',
      required: true,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, 'agents'), { recursive: true }),
      impact: '每个子代理的独立工作空间，用于存放该代理的历史研究过程文件和会话子目录'
    },
    {
      name: 'shared/ 共享输出目录',
      path: path.join(CONFIG_DIR, 'shared'),
      description: '共享输出根目录，存放所有研究的共享文件',
      required: true,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, 'shared'), { recursive: true }),
      impact: '多代理系统共享的输出空间，用于存放研究过程文件和最终报告'
    },
    {
      name: 'shared/researches/ 研究目录',
      path: path.join(CONFIG_DIR, 'shared', 'researches'),
      description: '研究任务目录，按任务名称和时间戳组织研究目录',
      required: true,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, 'shared', 'researches'), { recursive: true }),
      impact: '每个研究任务都有自己的子目录，用于隔离不同研究任务'
    },
    {
      name: 'shared/final/ 最终输出目录',
      path: path.join(CONFIG_DIR, 'shared', 'final'),
      description: '最终报告目录，存放所有研究的最终报告',
      required: true,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, 'shared', 'final'), { recursive: true }),
      impact: '存放所有研究任务的最终报告，用户查看和下载的最终成果'
    },
    {
      name: '.cache/ 缓存目录',
      path: path.join(CONFIG_DIR, '.cache'),
      description: '缓存目录，用于存储临时文件和缓存数据',
      required: false,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, '.cache'), { recursive: true }),
      impact: '可选目录，用于存储系统缓存和临时文件'
    },
    {
      name: 'logs/ 日志目录',
      path: path.join(CONFIG_DIR, 'logs'),
      description: '日志目录，用于存储系统运行日志',
      required: false,
      action: () => fs.mkdirSync(path.join(CONFIG_DIR, 'logs'), { recursive: true }),
      impact: '可选目录，用于存储系统运行日志和调试信息'
    }
  ];

  const results = [];

  for (const check of checks) {
    const exists = fs.existsSync(check.path);

    if (check.required && !exists) {
      results.push({
        ...check,
        status: 'error',
        message: `目录 ${check.path} 不存在且必需\n\n📋 目录作用: ${check.description}\n⚠️  影响说明: ${check.impact}\n\n🔧 需要自动创建此目录才能运行多代理系统`
      });
    } else if (exists) {
      results.push({
        ...check,
        status: 'pass',
        message: `目录 ${check.path} 已存在\n\n📋 目录作用: ${check.description}`
      });
    } else {
      results.push({
        ...check,
        status: 'warning',
        message: `目录 ${check.path} 可选，未创建\n\n📋 目录作用: ${check.description}`
      });
    }
  }

  return {
    name: '工作区目录结构',
    status: results.filter(r => r.status === 'error').length > 0 ? 'error' : 'pass',
    checks: results
  };
}

/**
 * 检查代理配置
 */
export function checkAgentConfig() {
  const profilesFile = path.join(CONFIG_DIR, '.multi-agent-profiles.json');

  if (!fs.existsSync(profilesFile)) {
    return {
      name: '代理配置',
      status: 'error',
      required: true,
      message: `配置文件 ${profilesFile} 不存在\n\n📋 目录作用: 代理配置文件，定义每个代理的角色、职责和能力\n⚠️  影响说明: 没有配置文件，多代理系统无法识别和启动任何子代理\n\n🔧 需要自动创建此配置文件才能运行多代理系统`
    };
  }

  try {
    const config = JSON.parse(fs.readFileSync(profilesFile, 'utf-8'));
    const agents = config.agents || [];

    if (agents.length === 0) {
      return {
        name: '代理配置',
        status: 'error',
        required: true,
        message: `配置文件存在但没有任何代理配置，需要创建至少 1 个代理\n\n📋 目录作用: 代理配置文件，定义每个代理的角色、职责和能力\n⚠️  影响说明: 没有代理配置，多代理系统无法识别和启动任何子代理\n\n🔧 需要创建至少 1 个代理配置才能运行多代理系统`
      };
    }

    // 检查每个代理的工作区
    const agentResults = [];
    for (const agent of agents) {
      const agentWorkspace = path.join(CONFIG_DIR, 'agents', agent.name);
      const exists = fs.existsSync(agentWorkspace);

      if (!exists) {
        agentResults.push({
          name: `代理工作区: ${agent.name}`,
          status: 'error',
          message: `代理 ${agent.name} 的工作区 ${agentWorkspace} 不存在\n\n📋 目录作用: 代理 ${agent.name} 的独立工作空间，存放该代理的历史研究过程文件\n⚠️  影响说明: 没有独立工作区，代理无法存放过程文件，会导致任务失败\n\n🔧 需要自动创建代理工作区才能运行多代理系统`
        });
      } else {
        agentResults.push({
          name: `代理工作区: ${agent.name}`,
          status: 'pass',
          message: `代理 ${agent.name} 的工作区已存在\n\n📋 目录作用: 代理 ${agent.name} 的独立工作空间，存放该代理的历史研究过程文件`
        });
      }
    }

    return {
      name: '代理配置',
      status: agentResults.some(r => r.status === 'error') ? 'error' : 'pass',
      agentCount: agents.length,
      agentResults
    };
  } catch (error) {
    return {
      name: '代理配置',
      status: 'error',
      required: true,
      message: `配置文件解析失败: ${error.message}`
    };
  }
}

/**
 * 检查工作流配置
 */
export function checkWorkflowConfig() {
  const workflowsFile = path.join(CONFIG_DIR, '.multi-agent-workflows.json');

  if (!fs.existsSync(workflowsFile)) {
    return {
      name: '工作流配置',
      status: 'warning',
      required: false,
      message: `配置文件 ${workflowsFile} 不存在，将使用默认工作流配置`
    };
  }

  try {
    const config = JSON.parse(fs.readFileSync(workflowsFile, 'utf-8'));
    const workflows = config.workflows || [];

    if (workflows.length === 0) {
      return {
        name: '工作流配置',
        status: 'warning',
        required: false,
        message: `配置文件存在但没有任何工作流定义，将使用默认工作流配置`
      };
    }

    return {
      name: '工作流配置',
      status: 'pass',
      workflowCount: workflows.length,
      message: `已加载 ${workflows.length} 个工作流配置`
    };
  } catch (error) {
    return {
      name: '工作流配置',
      status: 'warning',
      required: false,
      message: `配置文件解析失败: ${error.message}`
    };
  }
}

/**
 * 检查模型配置
 */
export function checkModelConfig() {
  const openclawConfigPath = path.join(CONFIG_DIR, 'openclaw.json');

  if (!fs.existsSync(openclawConfigPath)) {
    return {
      name: '模型配置',
      status: 'warning',
      required: false,
      message: `OpenClaw 配置文件 ${openclawConfigPath} 不存在，将使用默认模型池`
    };
  }

  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf-8'));
    const providers = config.providers || {};
    const models = [];

    // 收集所有模型
    for (const [providerName, providerConfig] of Object.entries(providers)) {
      if (Array.isArray(providerConfig.models)) {
        models.push(...providerConfig.models.map(m => `${providerName}/${m}`));
      }
    }

    if (models.length === 0) {
      return {
        name: '模型配置',
        status: 'warning',
        required: false,
        message: `未检测到任何模型配置，将使用默认模型池`
      };
    }

    return {
      name: '模型配置',
      status: 'pass',
      modelCount: models.length,
      models: models.slice(0, 10), // 只显示前 10 个
      message: `已加载 ${models.length} 个模型配置`
    };
  } catch (error) {
    return {
      name: '模型配置',
      status: 'warning',
      required: false,
      message: `配置文件解析失败: ${error.message}`
    };
  }
}

/**
 * 生成完整的配置检查报告
 */
export function generateConfigReport() {
  const checks = [
    checkOpenClawVersion(),
    checkNodeVersion(),
    checkWorkspaceStructure(),
    checkAgentConfig(),
    checkWorkflowConfig(),
    checkModelConfig()
  ];

  // 展开所有检查项（特别是工作区目录结构，它包含多个子检查项）
  const allErrorItems = [];
  const allWarningItems = [];
  
  for (const check of checks) {
    if (check.status === 'error') {
      if (check.checks && Array.isArray(check.checks)) {
        // 如果检查项有子检查项，展开它们
        const subErrors = check.checks.filter(c => c.status === 'error');
        allErrorItems.push(...subErrors);
        const subWarnings = check.checks.filter(c => c.status === 'warning');
        allWarningItems.push(...subWarnings);
      } else {
        allErrorItems.push(check);
      }
    } else if (check.status === 'warning') {
      if (check.checks && Array.isArray(check.checks)) {
        const subWarnings = check.checks.filter(c => c.status === 'warning');
        allWarningItems.push(...subWarnings);
      } else {
        allWarningItems.push(check);
      }
    }
  }

  return {
    summary: {
      total: checks.length,
      pass: checks.filter(c => c.status === 'pass').length,
      warning: allWarningItems.length,
      error: allErrorItems.length
    },
    checks,
    errors: allErrorItems,
    warnings: allWarningItems
  };
}

/**
 * 自动完成配置（用户同意后调用）
 */
export async function autoConfigure(configReport) {
  const errors = configReport.errors;
  const warnings = configReport.warnings;

  console.log('\n🔧 开始自动配置...\n');

  // 执行必需的配置操作
  for (const error of errors) {
    console.log(`  → ${error.name}: ${error.message}`);
    if (error.action) {
      try {
        error.action();
        console.log(`     ✅ 已完成`);
      } catch (err) {
        console.log(`     ❌ 失败: ${err.message}`);
        return { success: false, error: err.message };
      }
    }
  }

  // 执行可选的配置操作
  for (const warning of warnings) {
    if (warning.action && warning.required !== true) {
      console.log(`  → ${warning.name}: ${warning.message}`);
      try {
        warning.action();
        console.log(`     ✅ 已完成`);
      } catch (err) {
        console.log(`     ⚠️  跳过: ${err.message}`);
      }
    }
  }

  console.log('\n✅ 配置完成！\n');

  return { success: true };
}

/**
 * 生成配置说明文档（给用户看的）
 */
export function generateConfigGuide() {
  const report = generateConfigReport();

  let guide = `📋 多代理编排引擎 - 配置检查报告\n${'═'.repeat(60)}\n\n`;
  guide += `## 📊 配置概览\n`;
  guide += `- 总检查项: ${report.summary.total}\n`;
  guide += `- ✅ 通过: ${report.summary.pass}\n`;
  guide += `- ⚠️  警告: ${report.summary.warning}\n`;
  guide += `- ❌ 错误: ${report.summary.error}\n\n`;

  if (report.errors.length > 0) {
    guide += `## ❌ 需要修复的配置 (${report.errors.length} 项)\n\n`;
    for (const error of report.errors) {
      guide += `### ${error.name}\n`;
      guide += `- 当前状态: ${error.current || '未配置'}\n`;
      guide += `- 要求: ${error.required}\n`;
      guide += `- 说明: ${error.message}\n\n`;
    }
  }

  if (report.warnings.length > 0) {
    guide += `## ⚠️  可选配置 (${report.warnings.length} 项)\n\n`;
    for (const warning of report.warnings) {
      guide += `### ${warning.name}\n`;
      guide += `- 当前状态: ${warning.current || '未配置'}\n`;
      guide += `- 说明: ${warning.message}\n\n`;
    }
  }

  guide += `## ✅ 已满足的配置\n\n`;
  for (const check of report.checks) {
    if (check.status === 'pass') {
      guide += `- ${check.name}: ${check.current || '已配置'}\n`;
    }
  }

  guide += `\n## 🔧 自动配置选项\n\n`;
  guide += `如果同意自动配置，系统将执行以下操作：\n\n`;

  for (const error of report.errors) {
    guide += `1. 创建 ${error.name}\n`;
    guide += `   路径: ${error.path}\n`;
    guide += `   操作: ${error.message}\n\n`;
  }

  for (const warning of report.warnings) {
    if (warning.action && warning.required !== true) {
      guide += `2. 创建 ${warning.name}\n`;
      guide += `   路径: ${warning.path}\n`;
      guide += `   操作: ${warning.message}\n\n`;
    }
  }

  guide += `## 📝 手动配置选项\n\n`;
  guide += `如果不希望自动配置，可以手动完成以下步骤：\n\n`;
  guide += `1. 确认 OpenClaw 版本 >= 2026.3.x\n`;
  guide += `2. 确认 Node.js 版本 >= 20.5\n`;
  guide += `3. 确认工作区目录存在: ${CONFIG_DIR}\n`;
  guide += `4. 创建代理配置: ${path.join(CONFIG_DIR, 'multi-agent-profiles.json')}\n`;
  guide += `5. 创建工作流配置: ${path.join(CONFIG_DIR, 'multi-agent-workflows.json')}\n\n`;

  return guide;
}
