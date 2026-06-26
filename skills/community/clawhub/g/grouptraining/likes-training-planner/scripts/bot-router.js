// Bot 路由配置
// 根据 Telegram Bot ID 自动切换工作模式

const BOT_ROUTES = {
  "likes_training_bot": {
    name: "训练分析师",
    description: "专注训练数据分析、运动反馈点评",
    defaultCommand: "analyze",
    features: ["fetch_activities", "analyze_data", "fetch_feedback", "add_feedback_comment"],
    welcomeMessage: "你好！我是你的训练数据分析师。\n\n我可以帮你：\n📊 分析历史运动数据\n💬 点评训练反馈\n📈 生成数据报告\n\n请告诉我你想分析什么？"
  },
  "likes_traning_2_bot": {
    name: "训练计划师",
    description: "专注训练计划制定、推送到日历",
    defaultCommand: "generate_plan",
    features: ["generate_plan", "preview_plan", "push_plans", "fetch_plans"],
    welcomeMessage: "你好！我是你的训练计划制定师。\n\n我可以帮你：\n📝 制定个性化训练计划\n👀 预览并确认计划\n📅 推送到Likes日历\n\n请告诉我你想制定什么计划？"
  },
  "default": {
    name: "训练助手",
    description: "综合训练助手",
    defaultCommand: "help",
    features: ["all"],
    welcomeMessage: "你好！我是你的训练助手。\n\n我可以帮你管理训练数据和计划。\n请告诉我你需要什么帮助？"
  }
};

function detectBot() {
  // 从环境变量或消息上下文中检测当前bot
  const botName = process.env.TELEGRAM_BOT_NAME || 
                  process.env.BOT_NAME || 
                  getContext('channel.account') ||
                  'default';
  
  return BOT_ROUTES[botName] || BOT_ROUTES.default;
}

function getContext(key) {
  // 从OpenClaw上下文中获取信息
  // 实际实现需要根据OpenClaw的API
  try {
    // 尝试从全局上下文读取
    if (typeof global !== 'undefined' && global.OPENCLAW_CONTEXT) {
      return key.split('.').reduce((obj, k) => obj && obj[k], global.OPENCLAW_CONTEXT);
    }
  } catch (e) {
    // 忽略错误，返回默认值
  }
  return null;
}

module.exports = { BOT_ROUTES, detectBot };
