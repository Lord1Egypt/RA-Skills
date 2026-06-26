/**
 * 积分小贴士和语音播报模块
 * 
 * 功能：
 * - ✅ 随机激励语（记账后展示）
 * - ✅ 语音播报（调用 SenseAudio TTS）
 * - ✅ 趣味小贴士
 */

const path = require('path');
const fs = require('fs');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const AUDIO_DIR = path.join(WORKSPACE, 'audio');

/**
 * 激励语库（收入类）
 */
const INCOME_TIPS = [
  "🌟 太棒了！继续保持~",
  "💪 努力就会有收获，加油！",
  "🎉 又进步了一点，真棒！",
  "✨ 积少成多，你做得很好！",
  "🏆 优秀！坚持就是胜利！",
  "🌈 每一分都是成长的足迹！",
  "🚀 继续加油，未来可期！",
  "⭐ 今天的努力，明天的收获！",
  "🎯 目标明确，行动有力！",
  "💫 你比昨天更优秀了！"
];

/**
 * 激励语库（支出类 - 温和提醒）
 */
const EXPENSE_TIPS = [
  "💡 小失误没关系，下次注意就好~",
  "🌱 失败是成功之母，加油！",
  "🔄 及时调整，下次会更好！",
  "💪 挫折是成长的阶梯！",
  "🌟 知错能改，善莫大焉！",
  "🎯 记住这次教训，继续前进！",
  "✨ 每一次反思都是进步！",
  "🌈 阳光总在风雨后！",
  "🚀 调整状态，重新出发！",
  "⭐ 相信自己，你可以做得更好！"
];

/**
 * 趣味小贴士
 */
const FUN_TIPS = [
  "📚 你知道吗？坚持 21 天就能养成一个好习惯！",
  "🧠 学习时休息一下，效率会更高哦~",
  "💤 充足的睡眠能让记忆力提升 20%！",
  "🍎 多吃蔬菜水果，大脑更聪明！",
  "🏃 每天运动 30 分钟，学习更有精神！",
  "📖 阅读可以让人更专注，试试每天读书 15 分钟！",
  "🎵 听音乐可以放松心情，但学习时要专注哦~",
  "🌞 早上起床后晒晒太阳，一天都有好精神！",
  "💧 多喝水能让大脑保持清醒，记得每天喝 8 杯水！",
  "🎨 画画可以培养创造力，有空试试看！"
];

/**
 * 获取随机激励语
 */
function getRandomTip(type = 'income') {
  const tips = type === 'income' ? INCOME_TIPS : EXPENSE_TIPS;
  const randomIndex = Math.floor(Math.random() * tips.length);
  return tips[randomIndex];
}

/**
 * 获取随机趣味小贴士
 */
function getRandomFunTip() {
  const randomIndex = Math.floor(Math.random() * FUN_TIPS.length);
  return FUN_TIPS[randomIndex];
}

/**
 * 语音播报（调用 SenseAudio TTS）
 * @param {string} text - 要播报的文本
 * @returns {Promise<{success: boolean, filePath?: string, error?: string}>}
 */
async function speak(text, voice = 'child_0001_a') {
  const TTS_SCRIPT = path.join(WORKSPACE, 'skills', 'senseaudio-voice', 'scripts', 'tts.py');
  const dateStr = new Date().toISOString().split('T')[0];
  const outputDir = path.join(AUDIO_DIR, dateStr);
  
  // 确保输出目录存在
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // ✅ 使用 execSync 同步执行，等待播放完成再返回
  const { execSync } = require('child_process');
  const cmd = `python3 "${TTS_SCRIPT}" --voice "${voice}" --play "${text.replace(/"/g, '\\"')}"`;
  
  try {
    const stdout = execSync(cmd, { encoding: 'utf8', timeout: 60000 });
    console.log('🔊 语音播报成功');
    
    // 提取生成的文件路径（从 stdout 中解析）
    const fileMatch = stdout.match(/保存至 [:：]\s*(.+)/);
    const filePath = fileMatch ? fileMatch[1].trim() : null;
    
    return { success: true, filePath };
  } catch (error) {
    console.log('🔊 语音播报失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 生成纯文本版本（用于语音朗读）
 * 移除所有 emoji、markdown 符号、特殊格式
 */
function toPlainText(formattedMessage) {
  let plain = formattedMessage;
  
  // 移除 emoji（保留中文和标点）
  plain = plain.replace(/[\u{1F300}-\u{1F9FF}]/gu, '');
  plain = plain.replace(/[📊📈💸💰✅❌⚠️💡🌟💪🎉✨🏆🌈🚀⭐🎯💫🌱🔄📚🧠💤🍎🏃📖🎵🌞💧🎨]/g, '');
  
  // 移除 markdown 格式
  plain = plain.replace(/\*\*/g, ''); // 粗体
  plain = plain.replace(/\*/g, ''); // 斜体
  plain = plain.replace(/_/g, ''); // 下划线
  plain = plain.replace(/`/g, ''); // 代码
  plain = plain.replace(/^#+\s*/gm, ''); // 标题
  
  // 移除表格符号
  plain = plain.replace(/\|/g, ' ');
  plain = plain.replace(/---+/g, '');
  
  // 清理多余空白
  plain = plain.replace(/\n\s*\n/g, '\n');
  plain = plain.replace(/\s+/g, ' ').trim();
  
  // 移除特殊说明文字（不需要朗读的部分）
  plain = plain.replace(/_已自动记入账本，随时可以查看_/g, '');
  plain = plain.replace(/_已自动记入账本_/g, '');
  plain = plain.replace(/_数据来自 balance.md，随时可以查看_/g, '');
  plain = plain.replace(/_周报功能开发中..._/g, '');
  
  return plain;
}

/**
 * 生成带小贴士的响应消息
 */
function enhanceMessage(baseMessage, type = 'income', includeFunTip = false) {
  let message = baseMessage;
  
  // 添加激励语
  const tip = getRandomTip(type);
  message += `\n\n${tip}`;
  
  // 可选：添加趣味小贴士（随机概率 30%）
  if (includeFunTip && Math.random() < 0.3) {
    const funTip = getRandomFunTip();
    message += `\n\n💡 **小知识**: ${funTip}`;
  }
  
  return message;
}

module.exports = {
  getRandomTip,
  getRandomFunTip,
  speak,
  enhanceMessage,
  toPlainText,
  INCOME_TIPS,
  EXPENSE_TIPS,
  FUN_TIPS
};
