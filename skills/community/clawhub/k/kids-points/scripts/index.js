#!/usr/bin/env node
/**
 * kids-points 技能入口
 * 处理飞书消息，调用相应的处理函数
 */

const handler = require('./handler');

/**
 * 主处理函数
 * @param {string} message - 用户消息
 * @returns {string} - 响应消息
 */
function processMessage(message) {
  const text = message.trim();
  
  // 判断消息类型
  if (text.startsWith('学习积分')) {
    const result = handler.handlePointsInput(text);
    return result.message;
  }
  
  if (text.startsWith('积分消费')) {
    const result = handler.handleExpenseInput(text);
    return result.message;
  }
  
  if (text.includes('今日积分') || text.includes('今天积分')) {
    const result = handler.generateDailyReport();
    return result.message;
  }
  
  if (text.includes('本周积分')) {
    return '📈 周报功能开发中... 敬请期待!';
  }
  
  if (text.includes('本月积分')) {
    return '📅 月报功能开发中... 敬请期待!';
  }
  
  if (text.startsWith('修改规则')) {
    return '⚙️ 规则修改功能开发中... 敬请期待!';
  }
  
  // 默认响应
  return `📚 **学习积分小助手**\n\n我可以帮你:\n• 记录积分 (说"学习积分...")\n• 记录消费 (说"积分消费...")\n• 查看今日积分\n\n试试对我说:\n> "学习积分 今天完成了汉字抄写 2 课，口算题卡 2 篇全对"`;
}

// 如果是命令行调用
if (require.main === module) {
  const message = process.argv.slice(2).join(' ');
  if (message) {
    console.log(processMessage(message));
  } else {
    console.log('用法：node index.js <消息内容>');
    console.log('例如：node index.js "学习积分 今天完成了口算题卡 2 篇"');
  }
}

module.exports = { processMessage };
