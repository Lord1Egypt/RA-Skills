#!/usr/bin/env node

/**
 * OPC智脑一键安装脚本（Node.js版本）
 * 作者：李屹镒（公众号：科技新潮。视频号：小李君与AI）
 * 用法：npx install-opc [目标项目路径]
 */

const fs = require('fs');
const path = require('path');

// 颜色定义
const colors = {
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  reset: '\x1b[0m'
};

function log(color, message) {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 获取源目录（OPC智脑所在目录）
const SOURCE_DIR = path.resolve(__dirname);

// 获取目标目录
const TARGET_DIR = path.resolve(process.argv[2] || '.');

log('blue', '========================================');
log('blue', '  OPC智脑一键安装脚本');
log('blue', '========================================');
console.log('');

log('green', `✓ 源目录：${SOURCE_DIR}`);
log('green', `✓ 目标目录：${TARGET_DIR}`);
console.log('');

// 创建目录
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 复制文件
function copyFile(src, dest) {
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    return true;
  }
  return false;
}

// 复制目录
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return 0;
  
  ensureDir(dest);
  let count = 0;
  
  const items = fs.readdirSync(src);
  for (const item of items) {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    
    if (fs.statSync(srcPath).isDirectory()) {
      count += copyDir(srcPath, destPath);
    } else {
      copyFile(srcPath, destPath);
      count++;
    }
  }
  
  return count;
}

// 步骤1：复制AGENTS.md
log('blue', '[1/5] 复制AGENTS.md...');
if (copyFile(path.join(SOURCE_DIR, 'AGENTS.md'), path.join(TARGET_DIR, 'AGENTS.md'))) {
  log('green', '  ✓ AGENTS.md 已复制');
} else {
  log('yellow', '  ⚠ AGENTS.md 不存在，跳过');
}

// 步骤2：创建.codeartsdoer目录结构
log('blue', '[2/5] 创建.codeartsdoer目录结构...');
ensureDir(path.join(TARGET_DIR, '.codeartsdoer', 'agents'));
ensureDir(path.join(TARGET_DIR, '.codeartsdoer', 'skills'));
log('green', '  ✓ 目录结构已创建');

// 步骤3：复制opc-zhinao.json
log('blue', '[3/5] 复制opc-zhinao.json...');
const agentSource = path.join(SOURCE_DIR, '.codeartsdoer', 'agents', 'opc-zhinao.json');
const agentTarget = path.join(TARGET_DIR, '.codeartsdoer', 'agents', 'opc-zhinao.json');
if (copyFile(agentSource, agentTarget)) {
  log('green', '  ✓ opc-zhinao.json 已复制');
} else {
  log('yellow', '  ⚠ opc-zhinao.json 不存在，跳过');
}

// 步骤4：复制所有skills
log('blue', '[4/5] 复制所有skills...');
const skillsSource = path.join(SOURCE_DIR, '.codeartsdoer', 'skills');
const skillsTarget = path.join(TARGET_DIR, '.codeartsdoer', 'skills');

if (fs.existsSync(skillsSource)) {
  const skills = fs.readdirSync(skillsSource).filter(item => {
    return fs.statSync(path.join(skillsSource, item)).isDirectory();
  });
  
  let totalFiles = 0;
  for (const skill of skills) {
    const src = path.join(skillsSource, skill);
    const dest = path.join(skillsTarget, skill);
    const count = copyDir(src, dest);
    totalFiles += count;
    log('green', `  ✓ ${skill} 已复制`);
  }
  
  log('green', `  ✓ 共复制 ${skills.length} 个skills，${totalFiles} 个文件`);
} else {
  log('yellow', '  ⚠ skills目录不存在，跳过');
}

// 步骤5：复制skills-registry.json
log('blue', '[5/5] 复制skills-registry.json...');
const registrySource = path.join(SOURCE_DIR, 'opc-skills', 'skills-registry.json');
const registryTarget = path.join(TARGET_DIR, 'skills-registry.json');
if (copyFile(registrySource, registryTarget)) {
  log('green', '  ✓ skills-registry.json 已复制');
} else {
  log('yellow', '  ⚠ skills-registry.json 不存在，跳过');
}

// 完成
console.log('');
log('green', '========================================');
log('green', '  ✓ OPC智脑安装完成！');
log('green', '========================================');
console.log('');
log('blue', '已安装文件：');
console.log('  ├── AGENTS.md');
console.log('  └── .codeartsdoer/');
console.log('      ├── agents/');
console.log('      │   └── opc-zhinao.json');
console.log('      └── skills/');
console.log('          ├── skill1-idea-feasibility/');
console.log('          ├── skill2-mvp-design/');
console.log('          ├── skill3-opc-compliance/');
console.log('          ├── skill4-seed-coldstart/');
console.log('          ├── skill5-scale-growth/');
console.log('          ├── feasibility-scoring/');
console.log('          ├── report-export/');
console.log('          └── user-feedback/');
console.log('');
log('blue', '下一步：');
console.log(`  1. 在码道IDE中打开项目：${TARGET_DIR}`);
console.log('  2. IDE会自动识别opc-zhinao.json和AGENTS.md');
console.log('  3. 输入创业Idea开始诊断');
console.log('');
log('blue', '验证安装：');
console.log('  运行以下命令检查文件是否完整：');
console.log(`  ls -la ${path.join(TARGET_DIR, '.codeartsdoer', 'skills')}`);