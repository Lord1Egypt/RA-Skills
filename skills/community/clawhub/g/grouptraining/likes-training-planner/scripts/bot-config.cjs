#!/usr/bin/env node
/**
 * Bot 检测与路由
 * 根据当前 Telegram Bot 自动切换工作模式
 */

const fs = require('fs');
const path = require('path');

// Bot 配置
const BOT_CONFIG = {
  "likes_training_bot": {
    id: "likes_training_bot",
    name: "训练分析师",
    role: "analysis",
    description: "专注训练数据分析、运动反馈点评",
    features: ["数据分析", "反馈点评", "训练报告"],
    welcomeMessage: `你好！我是你的🏃 训练数据分析师。

我可以帮你：
📊 分析历史运动数据
💬 点评学员训练反馈  
📈 生成数据洞察报告
🔍 查询训练营详情

请告诉我你想分析什么？

示例：
- "分析最近7天的数据"
- "点评 game 484 的学员反馈"
- "查询训练营成员列表"`,
    promptSuffix: "\n\n[当前模式：数据分析]"
  },
  "likes_traning_2_bot": {
    id: "likes_traning_2_bot", 
    name: "训练计划师",
    role: "planning",
    description: "专注训练计划制定、推送到日历",
    features: ["计划生成", "计划预览", "推送到日历"],
    welcomeMessage: `你好！我是你的📝 训练计划制定师。

我可以帮你：
📝 制定个性化训练计划
👀 预览并确认计划内容
📅 推送到 Likes 日历
📋 管理现有训练计划

请告诉我你想制定什么计划？

示例：
- "生成下周的训练计划"
- "制定8周马拉松备赛计划"
- "推送计划到学员日历"`,
    promptSuffix: "\n\n[当前模式：计划制定]"
  },
  "default": {
    id: "default",
    name: "训练助手",
    role: "general",
    description: "综合训练助手",
    features: ["数据", "计划", "反馈"],
    welcomeMessage: "你好！我是你的训练助手。请告诉我你需要什么帮助？",
    promptSuffix: ""
  }
};

/**
 * 检测当前Bot
 * 从环境变量或上下文中检测
 */
function detectBot() {
  // 尝试多种方式检测当前bot
  const botName = process.env.TELEGRAM_BOT_NAME || 
                  process.env.BOT_NAME ||
                  process.env.OPENCLAW_CHANNEL_ACCOUNT ||
                  detectBotFromArgs() ||
                  'default';
  
  return BOT_CONFIG[botName] || BOT_CONFIG.default;
}

/**
 * 从命令行参数检测
 */
function detectBotFromArgs() {
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--bot' && args[i + 1]) {
      return args[i + 1];
    }
  }
  return null;
}

/**
 * 从 OpenClaw 上下文文件检测（如果有）
 */
function detectBotFromContext() {
  try {
    const contextFile = path.join(process.env.HOME, '.openclaw', 'current_context.json');
    if (fs.existsSync(contextFile)) {
      const context = JSON.parse(fs.readFileSync(contextFile, 'utf8'));
      return context.botName || context.account || null;
    }
  } catch (e) {
    // 忽略错误
  }
  return null;
}

/**
 * 保存当前Bot上下文
 */
function saveBotContext(botConfig) {
  try {
    const contextFile = path.join(process.env.HOME, '.openclaw', 'workspace', '.bot_context');
    fs.writeFileSync(contextFile, JSON.stringify({
      botId: botConfig.id,
      botName: botConfig.name,
      role: botConfig.role,
      timestamp: new Date().toISOString()
    }, null, 2));
  } catch (e) {
    // 忽略错误
  }
}

/**
 * 加载保存的Bot上下文
 */
function loadBotContext() {
  try {
    const contextFile = path.join(process.env.HOME, '.openclaw', 'workspace', '.bot_context');
    if (fs.existsSync(contextFile)) {
      return JSON.parse(fs.readFileSync(contextFile, 'utf8'));
    }
  } catch (e) {
    // 忽略错误
  }
  return null;
}

/**
 * 获取当前Bot配置
 */
function getCurrentBot() {
  // 首先尝试加载保存的上下文
  const savedContext = loadBotContext();
  if (savedContext && BOT_CONFIG[savedContext.botId]) {
    return BOT_CONFIG[savedContext.botId];
  }
  
  // 否则动态检测
  const bot = detectBot();
  saveBotContext(bot);
  return bot;
}

/**
 * 显示欢迎信息
 */
function showWelcome() {
  const bot = getCurrentBot();
  console.log(bot.welcomeMessage);
}

/**
 * 检查当前Bot是否有某个功能
 */
function hasFeature(feature) {
  const bot = getCurrentBot();
  return bot.features.includes(feature) || bot.role === 'general';
}

/**
 * 获取Bot特定的提示后缀
 */
function getPromptSuffix() {
  const bot = getCurrentBot();
  return bot.promptSuffix;
}

// 如果是直接运行此脚本
if (require.main === module) {
  const bot = getCurrentBot();
  
  if (process.argv.includes('--welcome')) {
    showWelcome();
  } else if (process.argv.includes('--info')) {
    console.log(JSON.stringify(bot, null, 2));
  } else if (process.argv.includes('--role')) {
    console.log(bot.role);
  } else {
    console.log(`当前Bot: ${bot.name} (${bot.id})`);
    console.log(`角色: ${bot.description}`);
    console.log(`功能: ${bot.features.join(', ')}`);
  }
}

module.exports = {
  BOT_CONFIG,
  detectBot,
  getCurrentBot,
  showWelcome,
  hasFeature,
  getPromptSuffix,
  saveBotContext,
  loadBotContext
};
