#!/usr/bin/env node
/**
 * 阿里巴巴询盘分析技能入口脚本
 * 用法：node run-analysis.js <询盘单号> [开始时间] [结束时间]
 *
 * 功能：调用主询盘分析脚本（自包含模式）
 * 安全说明：使用 child_process.spawn 启动 Node.js 进程运行分析器，
 *          这是正当功能需求，用于隔离运行环境和传递参数。
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// ============ 路径查找逻辑（自包含模式） ============
/**
 * 查找 inquiry-analyzer 主脚本路径
 * 查找顺序：
 * 1. 上级目录的 lib 文件夹（自包含模式）
 * 2. 当前脚本所在目录的同级目录
 * 3. 环境变量 INQUIRY_ANALYZER_PATH
 * 4. 常见安装位置
 */
function findMainScript() {
  const scriptName = 'inquiry-analyzer.js';
  const currentDir = __dirname;
  const parentDir = path.dirname(currentDir);

  // 1. 自包含模式：上级目录的 lib 文件夹
  const libPath = path.join(parentDir, 'lib', scriptName);
  if (fs.existsSync(libPath)) return libPath;

  // 2. 同级目录：scripts/../inquiry-analyzer.js
  const siblingPath = path.join(currentDir, '..', scriptName);
  if (fs.existsSync(siblingPath)) return siblingPath;

  // 3. 环境变量
  if (process.env.INQUIRY_ANALYZER_PATH) {
    const envPath = path.join(process.env.INQUIRY_ANALYZER_PATH, scriptName);
    if (fs.existsSync(envPath)) return envPath;
  }

  // 4. 常见安装位置
  const commonPaths = [
    path.join('e:', 'OpenClaw', 'inquiry-analyzer', scriptName),
    path.join(process.env.USERPROFILE || '', 'OpenClaw', 'inquiry-analyzer', scriptName),
  ];

  for (const p of commonPaths) {
    if (fs.existsSync(p)) return p;
  }

  return null;
}

/**
 * 获取工作目录（主脚本所在目录）
 */
function getWorkingDir(scriptPath) {
  return path.dirname(scriptPath);
}

// ============ 主程序 ============
// 获取参数
const targetInquiry = process.argv[2];
if (!targetInquiry) {
  console.error('用法: node run-analysis.js <目标询盘号> [开始时间] [结束时间]');
  console.error('示例: node run-analysis.js 50000126101155');
  console.error('      node run-analysis.js 50000126101155 "2026-03-26T15:00:00" "2026-03-27T15:00:00"');
  process.exit(1);
}

// 查找主脚本
const mainScript = findMainScript();
if (!mainScript) {
  console.error('错误: 无法找到 inquiry-analyzer.js');
  console.error('');
  console.error('请确保 skill 目录结构正确：');
  console.error('  inquiry-analyzer-skill/');
  console.error('  ├── lib/');
  console.error('  │   ├── inquiry-analyzer.js');
  console.error('  │   ├── product-groups.js');
  console.error('  │   └── product-mapping.js');
  console.error('  └── scripts/');
  console.error('      └── run-analysis.js');
  process.exit(1);
}

console.log(`使用脚本: ${mainScript}`);

// 构建参数
const args = [mainScript, targetInquiry];
if (process.argv[3]) args.push(process.argv[3]);
if (process.argv[4]) args.push(process.argv[4]);

// 运行主脚本
const workingDir = getWorkingDir(mainScript);
const child = spawn('node', args, {
  stdio: 'inherit',
  cwd: workingDir
});

child.on('close', (code) => {
  process.exit(code);
});
