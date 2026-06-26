/**
 * 图片处理（可选功能）
 * 
 * 功能：保存学习相关图片到 archive 目录
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = process.env.POINTS_DIR || path.join(WORKSPACE, 'kids-points');
const ARCHIVE_DIR = path.join(POINTS_DIR, 'archive');

/**
 * 处理图片附件
 */
function handleImage(attachment, message) {
  // 确保存档目录存在
  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }
  
  const dateStr = new Date().toISOString().split('T')[0];
  const timestamp = Date.now();
  
  // 从消息中提取描述
  let description = '学习';
  if (message) {
    if (message.includes('口算')) description = '口算';
    else if (message.includes('抄写')) description = '抄写';
    else if (message.includes('默写')) description = '默写';
    else if (message.includes('英语')) description = '英语';
    else if (message.includes('跳绳')) description = '跳绳';
    else if (message.includes('作业')) description = '作业';
  }
  
  // 生成文件名
  const ext = attachment.path ? path.extname(attachment.path) : '.jpg';
  const fileName = `${dateStr}_${description}_${timestamp}${ext}`;
  const destPath = path.join(ARCHIVE_DIR, fileName);
  
  // 如果附件有本地路径，复制文件
  if (attachment.path && fs.existsSync(attachment.path)) {
    fs.copyFileSync(attachment.path, destPath);
    return `✅ **图片已存档**\n\n📁 文件名：\`${fileName}\`\n📂 位置：\`kids-points/archive/\``;
  }
  
  // 如果是远程图片，记录信息
  if (attachment.url) {
    const infoFile = path.join(ARCHIVE_DIR, `${fileName}.info.json`);
    fs.writeFileSync(infoFile, JSON.stringify({
      originalUrl: attachment.url,
      description,
      date: dateStr,
      message: message?.substring(0, 200)
    }, null, 2));
    return `✅ **图片信息已记录**\n\n📝 描述：${description}\n📅 日期：${dateStr}`;
  }
  
  return null;
}

module.exports = {
  handleImage
};
