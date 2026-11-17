/**
 * 图片处理脚本
 * 将学习图片按日期重命名并存档
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const ARCHIVE_DIR = path.join(WORKSPACE, 'kids-points', 'archive');

/**
 * 获取今日日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 处理图片
 * @param {string} imagePath - 图片路径
 * @param {string} description - 图片描述（可选）
 * @returns {string} - 存档后的路径
 */
function handleImage(imagePath, description = '学习') {
  // 确保存档目录存在
  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }
  
  // 获取文件扩展名
  const ext = path.extname(imagePath);
  const dateStr = getTodayStr();
  const timestamp = Date.now();
  
  // 生成新文件名
  const safeDesc = description.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_');
  const newFileName = `${dateStr}_${safeDesc}_${timestamp}${ext}`;
  const newPath = path.join(ARCHIVE_DIR, newFileName);
  
  // 复制文件到存档目录
  fs.copyFileSync(imagePath, newPath);
  
  console.log(`✅ 图片已存档：${newFileName}`);
  
  return newPath;
}

// 命令行调用
if (require.main === module) {
  const imagePath = process.argv[2];
  const description = process.argv[3] || '学习';
  
  if (!imagePath) {
    console.log('用法：node handle-image.js <图片路径> [描述]');
    console.log('例如：node handle-image.js ./photo.jpg 口算题卡');
    process.exit(1);
  }
  
  if (!fs.existsSync(imagePath)) {
    console.log(`❌ 文件不存在：${imagePath}`);
    process.exit(1);
  }
  
  handleImage(imagePath, description);
}

module.exports = { handleImage, getTodayStr, ARCHIVE_DIR };
