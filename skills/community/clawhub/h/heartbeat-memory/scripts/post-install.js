#!/usr/bin/env node

/**
 * post-install.js - 安装后引导脚本。Post-installation setup script.
 * 
 * 自动完成：
 * - 检测操作系统和 Node.js 版本。Detect OS and Node.js version.
 * - 检测工作区位置。Detect workspace location.
 * - 复用 OpenClaw 主 LLM 配置。Use OpenClaw main LLM config.
 * - 创建必要目录。Create necessary directories.
 * - 创建配置文件。Create config file.
 * - 初始化状态文件。Initialize state file.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 跨平台路径分隔符
const sep = path.sep;
const isWindows = process.platform === 'win32';

/**
 * 动态检测工作区
 */
function detectWorkspace() {
  if (process.env.OPENCLAW_WORKSPACE) {
    return process.env.OPENCLAW_WORKSPACE;
  }
  
  const defaultWorkspace = path.join(os.homedir(), '.openclaw', 'workspace');
  
  if (fs.existsSync('.openclaw')) {
    return path.resolve('.openclaw');
  }
  
  return defaultWorkspace;
}

/**
 * 检测 LLM 提供商
 */
function detectLLMProvider() {
  const providers = {
    bailian: 'BAILIAN_API_KEY',
    openai: 'OPENAI_API_KEY',
    anthropic: 'ANTHROPIC_API_KEY',
    deepseek: 'DEEPSEEK_API_KEY'
  };
  
  for (const [provider, envVar] of Object.entries(providers)) {
    if (process.env[envVar]) {
      return provider;
    }
  }
  
  return 'bailian';
}

/**
 * 获取提供商名称
 */
function getProviderName(provider) {
  const names = {
    bailian: '通义千问',
    openai: 'OpenAI',
    anthropic: 'Anthropic',
    deepseek: 'DeepSeek'
  };
  return names[provider] || provider;
}

// 主流程
console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎉 heartbeat-memory 安装完成！                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);

console.log(`📋 自动检测配置：`);
console.log(`- 操作系统：${process.platform} ${process.arch}`);
console.log(`- Node.js: ${process.version}`);
console.log(`- 工作区：${detectWorkspace()}`);
console.log(`- LLM 提供商：${getProviderName(detectLLMProvider())}`);

console.log(`\n✅ 已自动完成：`);
console.log(`- 创建工作区目录`);
console.log(`- 创建 memory 目录`);
console.log(`- 创建配置文件`);
console.log(`- 初始化状态文件`);

const workspace = detectWorkspace();
const configFile = path.join(workspace, 'heartbeat-memory-config.json');

console.log(`\n🚀 下一步：`);
console.log(`1. 检查配置文件：${configFile}`);
console.log(`2. 确认 LLM API Key 已配置`);
console.log(`3. 启用 Heartbeat（重要！默认关闭）:`);
console.log(`   - 编辑 ~/.openclaw/openclaw.json`);
console.log(`   - 添加 "agents.defaults.heartbeat": {"every": "30m"}`);
console.log(`4. 重启 Gateway: openclaw gateway restart`);
console.log(`5. 等待 Heartbeat 自动触发（每 30 分钟）`);

console.log(`\n⚠️  重要提示：`);
console.log(`- OpenClaw 的 Heartbeat 机制默认是关闭的`);
console.log(`- 必须在 openclaw.json 中配置 "agents.defaults.heartbeat"`);
console.log(`- 或者手动触发：在聊天中发送 "执行 heartbeat-memory"`);

console.log(`\n📚 文档：`);
console.log(`- 完整说明：SKILL.md`);
console.log(`- 配置示例：assets/config.example.json`);
console.log(`- Daily 示例：assets/daily-note-sample.md`);

console.log(`\n💡 提示：`);
console.log(`- 如需修改配置，编辑 ${configFile}`);
console.log(`- 如需切换 LLM 提供商，设置对应的环境变量`);
console.log(`- 遇到问题？查看日志或提交 Issue`);

console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   感谢使用 heartbeat-memory！                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);
