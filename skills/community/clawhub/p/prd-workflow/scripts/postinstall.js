#!/usr/bin/env node
/**
 * prd-workflow 安装后脚本 v2.8.7
 *
 * 自动检测并安装依赖：
 * - Node.js: mermaid-cli（必需，流程图渲染）
 * - Python: html2image（推荐，轻量截图方案）
 * - Node.js: playwright（备选，完整截图方案）
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// 配置
const PYTHON_DEPS = {
  'html2image': {
    name: 'html2image',
    description: '轻量 HTML 截图工具（推荐，~31KB）',
    checkCommand: 'python3 -c "import html2image; print(html2image.__version__)"',
    installCommand: 'pip3 install --break-system-packages html2image',
    fallbackCommand: 'pip3 install html2image',  // 旧版 pip
    required: false
  }
};

const NODE_DEPS = {
  'mermaid-cli': {
    name: 'mermaid-cli',
    description: 'Mermaid 流程图渲染工具（必需，~2MB）',
    checkCommand: 'mmdc --version',
    installCommand: 'npm install -g @mermaid-js/mermaid-cli',
    required: true,
    hint: '用于生成流程图、时序图、ER 图等'
  },
  'adm-zip': {
    name: 'adm-zip',
    description: 'Word 文档图片检查（推荐，~50KB）',
    checkCommand: 'node -e "require(\'adm-zip\')"',
    installCommand: 'npm install adm-zip',
    required: false,
    hint: '用于验证 Word 文档是否正确嵌入图片'
  },
  'playwright': {
    name: 'Playwright',
    description: '完整截图方案（备选，~50MB）',
    checkCommand: 'playwright --version',
    installCommand: 'npm install -g playwright',
    postInstallCommand: 'npx playwright install chromium',
    required: false,
    hint: 'html2image 不可用时的备选截图方案'
  }
};

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 检测命令是否存在
function commandExists(command) {
  try {
    execSync(command, { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

// 询问用户
function askQuestion(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.toLowerCase().trim());
    });
  });
}

// 安装 Python 依赖
async function installPythonDependency(name, config) {
  log(`\n📦 安装 ${config.name}...`, 'blue');

  // 检查 Python
  if (!commandExists('python3 --version')) {
    log(`❌ 未找到 Python3，跳过安装`, 'red');
    return false;
  }

  try {
    // 尝试主安装命令
    log(`   执行：${config.installCommand}`, 'yellow');
    execSync(config.installCommand, { stdio: 'inherit' });
    log(`✅ ${config.name} 安装成功！`, 'green');
    return true;
  } catch (error) {
    // 尝试备选命令
    if (config.fallbackCommand) {
      try {
        log(`   重试：${config.fallbackCommand}`, 'yellow');
        execSync(config.fallbackCommand, { stdio: 'inherit' });
        log(`✅ ${config.name} 安装成功！`, 'green');
        return true;
      } catch (error2) {
        // 忽略，继续
      }
    }

    log(`❌ ${config.name} 安装失败：${error.message}`, 'red');
    return false;
  }
}

// 安装 Node.js 依赖
async function installNodeDependency(name, config) {
  log(`\n📦 安装 ${config.name}...`, 'blue');

  try {
    log(`   执行：${config.installCommand}`, 'yellow');
    execSync(config.installCommand, { stdio: 'inherit' });

    if (config.postInstallCommand) {
      log(`   执行：${config.postInstallCommand}`, 'yellow');
      execSync(config.postInstallCommand, { stdio: 'inherit' });
    }

    log(`✅ ${config.name} 安装成功！`, 'green');
    return true;
  } catch (error) {
    log(`❌ ${config.name} 安装失败：${error.message}`, 'red');
    return false;
  }
}

// 主函数
async function main() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🚀 prd-workflow 安装后配置', 'cyan');
  log('='.repeat(60), 'cyan');

  const results = {
    installed: [],
    skipped: [],
    failed: []
  };

  // ============ Python 依赖 ============
  log('\n📋 Python 依赖检测', 'blue');

  for (const [name, config] of Object.entries(PYTHON_DEPS)) {
    log(`\n🔍 检测：${config.name}`, 'blue');
    log(`   说明：${config.description}`, 'blue');

    // 检查是否已安装
    if (commandExists(config.checkCommand)) {
      log(`✅ ${config.name} 已安装`, 'green');
      results.installed.push(name);
      continue;
    }

    // 询问用户
    log(`⚠️  ${config.name} 未安装（可选依赖）`, 'yellow');
    log(`💡 建议安装以获得最佳截图体验`, 'yellow');

    const answer = await askQuestion(`   是否安装 ${config.name}? [Y/n] `);

    if (answer === '' || answer === 'y' || answer === 'yes') {
      const success = await installPythonDependency(name, config);
      if (success) {
        results.installed.push(name);
      } else {
        results.failed.push(name);
      }
    } else {
      log(`⏭️  跳过 ${config.name} 安装`, 'yellow');
      results.skipped.push(name);
    }
  }

  // ============ Node.js 依赖 ============
  log('\n📋 Node.js 依赖检测', 'blue');

  for (const [name, config] of Object.entries(NODE_DEPS)) {
    log(`\n🔍 检测：${config.name}`, 'blue');
    log(`   说明：${config.description}`, 'blue');
    if (config.hint) {
      log(`   用途：${config.hint}`, 'blue');
    }

    // 检查是否已安装
    if (commandExists(config.checkCommand)) {
      log(`✅ ${config.name} 已安装`, 'green');
      results.installed.push(name);
      continue;
    }

    // 必需依赖：直接安装，不询问
    if (config.required) {
      log(`⚠️  ${config.name} 未安装（必需依赖）`, 'yellow');
      log(`📦 正在安装必需依赖...`, 'yellow');

      const success = await installNodeDependency(name, config);
      if (success) {
        results.installed.push(name);
      } else {
        results.failed.push(name);
        log(`❌ 必需依赖安装失败，部分功能可能不可用`, 'red');
      }
      continue;
    }

    // 可选依赖：跳过 Playwright 的逻辑
    if (name === 'playwright') {
      // 只有在 Python 依赖未安装时才提示安装 Playwright
      if (results.installed.includes('html2image')) {
        log(`⏭️  已有 html2image，跳过 Playwright`, 'yellow');
        results.skipped.push(name);
        continue;
      }
    }

    log(`⚠️  ${config.name} 未安装（可选依赖）`, 'yellow');
    if (config.hint) {
      log(`💡 ${config.hint}`, 'yellow');
    }

    const answer = await askQuestion(`   是否安装 ${config.name}? [y/N] `);

    if (answer === 'y' || answer === 'yes') {
      const success = await installNodeDependency(name, config);
      if (success) {
        results.installed.push(name);
      } else {
        results.failed.push(name);
      }
    } else {
      log(`⏭️  跳过 ${config.name} 安装`, 'yellow');
      results.skipped.push(name);
    }
  }

  // ============ 安装总结 ============
  log('\n' + '='.repeat(60), 'cyan');
  log('📊 安装总结', 'cyan');
  log('='.repeat(60), 'cyan');

  if (results.installed.length > 0) {
    log(`✅ 已安装：${results.installed.join(', ')}`, 'green');
  }

  if (results.skipped.length > 0) {
    log(`⏭️  已跳过：${results.skipped.join(', ')}`, 'yellow');
  }

  if (results.failed.length > 0) {
    log(`❌ 安装失败：${results.failed.join(', ')}`, 'red');
  }

  // ============ 使用说明 ============
  log('\n📖 使用说明:', 'cyan');
  log('  prd-workflow generate "养老规划 PRD"', 'blue');

  log('\n💡 依赖说明:', 'cyan');
  log('  流程图：npm install -g @mermaid-js/mermaid-cli（必需）', 'blue');
  log('  截图推荐：pip3 install --break-system-packages html2image', 'blue');
  log('  截图备选：npm install -g playwright && npx playwright install chromium', 'blue');
  log('  macOS 零依赖：自动使用 Safari 截图', 'blue');

  log('\n' + '='.repeat(60), 'cyan');
  log('✅ prd-workflow 安装完成！', 'green');
  log('='.repeat(60), 'cyan');

  if (results.failed.length > 0) {
    process.exit(1);
  }
}

// 执行
main().catch(error => {
  log(`\n❌ 安装后脚本执行失败：${error.message}`, 'red');
  process.exit(1);
});