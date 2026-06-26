const fs = require('fs');
const path = require('path');

// 读取文本文件
function readTextFile(filePath) {
  return fs.readFileSync(filePath, 'utf-8');
}

// 读取 Word 文档（需要 mammoth 库）
async function readDocx(filePath) {
  const mammoth = require('mammoth');
  const result = await mammoth.extractRawText({ path: filePath });
  return result.value;
}

// 读取 PDF（需要 pdf-parse 库）
async function readPdf(filePath) {
  const pdf = require('pdf-parse');
  const dataBuffer = fs.readFileSync(filePath);
  const data = await pdf(dataBuffer);
  return data.text;
}

// 主入口
module.exports = async function(context) {
  const filePath = context.args.path;
  const ext = path.extname(filePath).toLowerCase();
  
  // 安全检查：限制可访问路径
  const allowedRoots = [
    process.env.OPENCLAW_WORKSPACE,
    'D:\\个人'  // 用户授权的路径
  ];
  
  if (!allowedRoots.some(root => filePath.startsWith(root))) {
    return { error: '路径不在允许范围内' };
  }
  
  // 根据扩展名选择读取方式
  switch (ext) {
    case '.txt':
    case '.md':
    case '.json':
      return readTextFile(filePath);
    case '.docx':
      return await readDocx(filePath);
    case '.pdf':
      return await readPdf(filePath);
    default:
      return { error: '不支持的文件格式' };
  }
};