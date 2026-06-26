"""
个人代理浏览器核心脚本

调用系统安装的 agent-browser CLI，获取网页内容并返回结构化摘要。

依赖：
- agent-browser CLI (已通过 npm install -g agent-browser 安装)
- Node.js 环境
"""

const { exec } = require('child_process');
const fs = require('fs');

// 获取命令行参数
const url = process.argv[2];

if (!url) {
  console.error('❌ 用法: node run_browser.js <URL>');
  process.exit(1);
}

console.log(`🌐 正在访问: ${url}`);

// 调用 agent-browser CLI
// 使用 --output=markdown 参数获取干净的文本内容
const command = `agent-browser --url="${url}" --output=markdown --timeout=10000`;

exec(command, { timeout: 15000 }, (error, stdout, stderr) => {
  if (error) {
    console.error(`❌ 执行失败: ${error.message}`);
    process.exit(1);
  }
  
  if (stderr) {
    console.error(`⚠️ 警告: ${stderr}`);
  }
  
  // 从 stdout 中提取标题和内容
  // agent-browser 的 markdown 输出格式：# 标题\n\n内容...
  const lines = stdout.split('\n');
  let title = '';
  let content = '';
  let inContent = false;
  
  for (let line of lines) {
    if (line.startsWith('# ')) {
      title = line.substring(2).trim();
    } else if (line.trim() !== '' && !line.startsWith('#')) {
      content += line + '\n';
      inContent = true;
    }
  }
  
  // 如果没有提取到标题，使用 URL 作为标题
  if (!title) {
    title = url;
  }
  
  // 输出结构化 JSON，供 OpenClaw AI 代理解析
  const result = {
    success: true,
    url: url,
    title: title,
    content: content.trim(),
    summary: "此页面内容已提取，可用于后续分析。"
  };
  
  console.log(JSON.stringify(result, null, 2));
});