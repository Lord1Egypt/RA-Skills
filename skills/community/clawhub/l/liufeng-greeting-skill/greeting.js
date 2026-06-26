------WebKitFormBoundaryxm3mm1rfrnl
Content-Disposition: form-data; name="file"; filename="greeting.js"
Content-Type: application/javascript

/**
 * 柳峰专属问候技能
 * 当用户发送问候消息时，回复个性化问候语并显示当前时间
 */

// 问候触发关键词（不区分大小写）
const GREETING_KEYWORDS = [
  '你好', 'hello', '嗨', '在吗', 'hi',
  '早上好', '下午好', '晚上好',
  'hey', 'hola', 'こんにちは', '안녕하세요'
];

// 个性化问候语模板
const GREETING_TEMPLATES = [
  "柳峰，你好！🌄 大白在这里随时为你服务。",
  "嗨，柳峰！很高兴见到你。",
  "柳峰，我在呢！有什么需要帮忙的吗？",
  "你好呀，柳峰！今天过得怎么样？",
  "柳峰，欢迎回来！大白已就位。"
];

/**
 * 检查消息是否包含问候关键词
 * @param {string} message - 用户输入的消息
 * @returns {boolean} - 是否触发问候
 */
function isGreetingMessage(message) {
  if (!message || typeof message !== 'string') {
    return false;
  }
  
  const lowerMessage = message.toLowerCase().trim();
  
  // 检查是否包含问候关键词
  for (const keyword of GREETING_KEYWORDS) {
    if (lowerMessage.includes(keyword.toLowerCase())) {
      return true;
    }
  }
  
  return false;
}

/**
 * 获取随机问候语
 * @returns {string} - 随机选择的问候语
 */
function getRandomGreeting() {
  const randomIndex = Math.floor(Math.random() * GREETING_TEMPLATES.length);
  return GREETING_TEMPLATES[randomIndex];
}

/**
 * 获取当前格式化时间
 * @returns {string} - 格式化的日期时间字符串
 */
function getCurrentTime() {
  const now = new Date();
  
  // 设置为中国时区
  const options = {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  };
  
  const formatter = new Intl.DateTimeFormat('zh-CN', options);
  const parts = formatter.formatToParts(now);
  
  const year = parts.find(p => p.type === 'year').value;
  const month = parts.find(p => p.type === 'month').value;
  const day = parts.find(p => p.type === 'day').value;
  const hour = parts.find(p => p.type === 'hour').value;
  const minute = parts.find(p => p.type === 'minute').value;
  const second = parts.find(p => p.type === 'second').value;
  
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 生成完整的问候回复
 * @returns {string} - 完整的问候回复
 */
function generateGreetingResponse() {
  const greeting = getRandomGreeting();
  const currentTime = getCurrentTime();
  
  return `${greeting}

当前时间：${currentTime}
时区：Asia/Shanghai (中国标准时间)`;
}

/**
 * 主处理函数 - 供OpenClaw调用
 * @param {Object} context - OpenClaw上下文对象
 * @param {string} context.message - 用户消息
 * @param {Object} context.user - 用户信息
 * @returns {Object|null} - 回复对象或null（不触发时）
 */
function handleGreeting(context) {
  const { message } = context;
  
  // 检查是否触发问候
  if (!isGreetingMessage(message)) {
    return null;
  }
  
  // 生成回复
  const reply = generateGreetingResponse();
  
  return {
    reply,
    metadata: {
      skill: 'liufeng-greeting-skill',
      version: '1.0.0',
      triggeredBy: message,
      timestamp: new Date().toISOString()
    }
  };
}

// 导出函数供OpenClaw使用
module.exports = {
  isGreetingMessage,
  getRandomGreeting,
  getCurrentTime,
  generateGreetingResponse,
  handleGreeting
};

// 测试代码（开发时使用）
if (require.main === module) {
  console.log('=== liufeng-greeting-skill 测试 ===');
  
  const testMessages = [
    '你好',
    'Hello!',
    '嗨，在吗？',
    '早上好',
    '今天天气怎么样？', // 不应触发
    '' // 空消息不应触发
  ];
  
  testMessages.forEach((msg, index) => {
    console.log(`\n测试 ${index + 1}: "${msg}"`);
    console.log('是否触发:', isGreetingMessage(msg));
    if (isGreetingMessage(msg)) {
      console.log('回复:', generateGreetingResponse());
    }
  });
}
------WebKitFormBoundaryxm3mm1rfrnl--
