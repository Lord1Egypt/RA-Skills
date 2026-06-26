#!/usr/bin/env node
/**
 * 依赖检测与自动安装模块
 * 支持 macOS、Ubuntu/Debian、Linux、Windows
 * 自动检测并安装缺失的依赖，带详细进度日志
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Homebrew 安装脚本（macOS 专用，使用官方安装脚本，后续会配置中科大镜像）
const HOMEBREW_INSTALL_SCRIPT = `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`;

// Homebrew 镜像配置脚本（使用中科大镜像）
const HOMEBREW_MIRROR_CONFIG = `
set -e
# 设置 Homebrew 镜像（中科大镜像）
export HOMEBREW_API_DOMAIN=https://mirrors.ustc.edu.cn/brew-api/
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export HOMEBREW_BREW_GIT_REMOTE=https://mirrors.ustc.edu.cn/brew.git
export HOMEBREW_CORE_GIT_REMOTE=https://mirrors.ustc.edu.cn/homebrew-core.git
export HOMEBREW_NODES=4
`;

// Chocolatey 安装脚本（Windows 专用）
const CHOCO_INSTALL_SCRIPT = 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))';

// 依赖项定义
const DEPENDENCIES = {
  nodejs: {
    name: 'nodejs',
    description: 'Node.js 运行时环境',
    checkCmd: 'node --version',
    install: {
      macos: 'brew install node',
      ubuntu: 'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs',
      linux: 'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs',
      windows: 'choco install nodejs-lts -y --no-progress'
    }
  },
  python: {
    name: 'python',
    description: 'Python 3.x 运行时',
    checkCmd: 'python3 --version',
    install: {
      macos: 'brew install python',
      ubuntu: 'sudo apt-get install -y python3 python3-pip',
      linux: 'sudo apt-get install -y python3 python3-pip',
      windows: 'choco install python -y --no-progress'
    }
  },
  poppler: {
    name: 'poppler',
    description: 'PDF 转图片工具',
    checkCmd: 'pdftoppm -v',
    install: {
      macos: 'brew install poppler',
      ubuntu: 'sudo apt-get install -y poppler-utils',
      linux: 'sudo apt-get install -y poppler-utils',
      windows: 'choco install poppler -y --no-progress'
    }
  },
  tesseract: {
    name: 'tesseract',
    description: 'OCR 引擎（支持中英文）',
    checkCmd: 'tesseract --version',
    install: {
      macos: 'brew install tesseract tesseract-lang',
      ubuntu: 'sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng',
      linux: 'sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng',
      windows: 'choco install tesseract-ocr -y --no-progress'
    }
  },
  pdfplumber: {
    name: 'pdfplumber',
    description: 'Python PDF 文本提取库',
    checkCmd: 'python3 -c "import pdfplumber"',
    install: {
      macos: 'pip3 install pdfplumber',
      ubuntu: 'pip3 install pdfplumber',
      linux: 'pip3 install pdfplumber',
      windows: 'pip install pdfplumber'
    }
  }
};

/**
 * 检测操作系统
 */
function getOS() {
  const platform = process.platform;
  if (platform === 'darwin') return 'macos';
  if (platform === 'linux') {
    // 进一步检测 Linux 发行版
    try {
      const release = execSync('cat /etc/os-release', { encoding: 'utf8' });
      if (release.includes('Ubuntu') || release.includes('Debian')) return 'ubuntu';
      return 'linux'; // 其他 Linux
    } catch {
      return 'linux';
    }
  }
  if (platform === 'win32') return 'windows';
  return 'unknown';
}

/**
 * 检测单个依赖是否已安装
 */
function checkDependency(depName) {
  const dep = DEPENDENCIES[depName];
  if (!dep) return false;

  try {
    execSync(dep.checkCmd, { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 检测所有依赖
 */
function checkAllDependencies() {
  const os = getOS();
  const missing = [];
  const installed = [];

  console.error('\n🚀 License Pre-Audit - 依赖检测');
  console.error('═══════════════════════════════════════════');
  console.error(`🖥️  检测到操作系统：${os.toUpperCase()}`);
  console.error('─'.repeat(60));

  for (const [key, dep] of Object.entries(DEPENDENCIES)) {
    const isInstalled = checkDependency(key);
    if (isInstalled) {
      installed.push(dep.name);
      console.error(`✅ ${dep.name.padEnd(15)} - ${dep.description} - 已安装`);
    } else {
      missing.push({ key, dep, os });
      console.error(`❌ ${dep.name.padEnd(15)} - ${dep.description} - 未安装`);
    }
  }

  console.error('─'.repeat(60));
  console.error(`📊 结果：${installed.length} 个已安装，${missing.length} 个缺失\n`);

  return { installed, missing, os };
}

/**
 * 检测 Homebrew 是否已安装（macOS 专用）
 */
function checkHomebrew() {
  try {
    execSync('brew --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 安装 Homebrew（macOS 专用，使用默认中科大镜像，无需用户交互）
 */
function installHomebrew() {
  return new Promise((resolve) => {
    console.error('\n🔍 未检测到 Homebrew，开始自动安装...');
    console.error('─'.repeat(60));
    console.error('📦 正在安装 Homebrew...');
    console.error('   使用镜像：中科大镜像 (USTC)');
    console.error('   执行命令：自动下载并安装（默认选项，无需交互）');
    console.error('   安装进度：');
    console.error('─'.repeat(60));

    const child = spawn('bash', ['-c', HOMEBREW_INSTALL_SCRIPT], {
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      console.error('─'.repeat(60));
      if (code === 0) {
        console.error('✅ Homebrew 安装成功！');
        console.error('💡 提示：可能需要重启终端才能使用 brew 命令\n');
        resolve(true);
      } else {
        console.error(`❌ Homebrew 安装失败 (退出码：${code})`);
        console.error('\n⚠️  请手动安装 Homebrew：');
        console.error('   1. 打开终端');
        console.error('   2. 执行：/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"');
        console.error('   3. 按提示输入密码（如果需要）');
        console.error('   4. 安装后重启终端\n');
        resolve(false);
      }
    });

    child.on('error', (err) => {
      console.error(`❌ Homebrew 安装失败：${err.message}`);
      resolve(false);
    });
  });
}

/**
 * 检测 Chocolatey 是否已安装
 */
function checkChocolatey() {
  try {
    execSync('choco --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 安装 Chocolatey（Windows 专用）
 */
function installChocolatey() {
  return new Promise((resolve) => {
    console.error('\n🔍 未检测到 Chocolatey，开始自动安装...');
    console.error('─'.repeat(60));
    console.error('📦 正在安装 Chocolatey...');
    console.error('   执行命令：powershell.exe (自动下载并安装)');
    console.error('   安装进度：');
    console.error('─'.repeat(60));

    const child = spawn('powershell.exe', [
      '-NoProfile',
      '-ExecutionPolicy', 'Bypass',
      '-Command',
      CHOCO_INSTALL_SCRIPT
    ], {
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      console.error('─'.repeat(60));
      if (code === 0) {
        console.error('✅ Chocolatey 安装成功！');
        console.error('💡 提示：可能需要重启终端才能使用 choco 命令\n');
        resolve(true);
      } else {
        console.error(`❌ Chocolatey 安装失败 (退出码：${code})`);
        console.error('\n⚠️  请手动安装 Chocolatey：');
        console.error('   1. 以管理员身份打开 PowerShell');
        console.error('   2. 执行：Set-ExecutionPolicy Bypass -Scope Process -Force');
        console.error('   3. 执行：iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))');
        console.error('   4. 安装后重启终端\n');
        resolve(false);
      }
    });

    child.on('error', (err) => {
      console.error(`❌ Chocolatey 安装失败：${err.message}`);
      resolve(false);
    });
  });
}

/**
 * 显示 Windows 手动安装指引（已废弃，改为自动安装）
 */
function showWindowsManualInstall(dep) {
  // 不再使用，所有 Windows 安装都自动化
  console.error(`⚠️  ${dep.name}: 自动安装失败，请手动执行：choco install ${dep.name} -y`);
}

/**
 * 执行安装命令（支持进度输出）
 */
function executeInstallCommand(cmd, depName, os) {
  return new Promise((resolve) => {
    console.error(`\n📦 正在安装 ${depName}...`);
    console.error(`   操作系统：${os.toUpperCase()}`);
    console.error(`   执行命令：${cmd}`);
    console.error('   安装进度：');
    console.error('─'.repeat(60));

    const isWindows = os === 'windows';
    let child;

    if (isWindows) {
      // Windows: 使用 PowerShell 执行 choco 命令
      const childProc = spawn('powershell.exe', [
        '-NoProfile',
        '-ExecutionPolicy', 'Bypass',
        '-Command',
        cmd
      ], {
        stdio: 'inherit',
        shell: true
      });
      child = childProc;
    } else {
      // macOS/Linux: 直接执行命令
      const cmdParts = cmd.split(' ');
      const exe = cmdParts[0];
      const args = cmdParts.slice(1);
      child = spawn(exe, args, {
        stdio: 'inherit',
        shell: false
      });
    }

    child.on('close', (code) => {
      console.error('─'.repeat(60));
      if (code === 0) {
        console.error(`✅ ${depName} 安装成功！`);
        resolve(true);
      } else {
        console.error(`❌ ${depName} 安装失败 (退出码：${code})`);
        resolve(false);
      }
    });

    child.on('error', (err) => {
      console.error(`❌ ${depName} 安装失败：${err.message}`);
      resolve(false);
    });
  });
}

/**
 * 自动安装缺失的依赖
 */
async function installMissingDependencies(missing, os) {
  if (missing.length === 0) {
    console.error('✅ 所有依赖已安装，无需操作\n');
    return true;
  }

  console.error('\n🔍 发现缺失的依赖，开始自动安装...');
  console.error('─'.repeat(60));
  console.error('缺失项列表：');
  missing.forEach(({ dep }) => {
    console.error(`   ❌ ${dep.name} - ${dep.description}`);
  });
  console.error('─'.repeat(60));
  console.error('\n🚀 开始自动安装所有缺失的依赖...\n');

  let hasError = false;

  // macOS 特殊处理：先检测并安装 Homebrew
  if (os === 'macos') {
    console.error('🔍 检测到 macOS 系统，检查 Homebrew 环境...');
    if (!checkHomebrew()) {
      console.error('❌ 未检测到 Homebrew，开始自动安装...');
      const brewSuccess = await installHomebrew();
      if (!brewSuccess) {
        console.error('\n❌ Homebrew 安装失败，无法继续自动安装依赖');
        console.error('请手动安装 Homebrew 后重试');
        return false;
      }
      // 等待一下确保 Homebrew 可用
      console.error('⏳ 等待 Homebrew 初始化...');
      await new Promise(resolve => setTimeout(resolve, 3000));
    } else {
      console.error('✅ Homebrew 已安装，准备安装依赖\n');
    }
  }

  // Windows 特殊处理：先检测并安装 Chocolatey
  if (os === 'windows') {
    console.error('🔍 检测到 Windows 系统，检查 Chocolatey 环境...');
    if (!checkChocolatey()) {
      console.error('❌ 未检测到 Chocolatey，开始自动安装...');
      const chocoSuccess = await installChocolatey();
      if (!chocoSuccess) {
        console.error('\n❌ Chocolatey 安装失败，无法继续自动安装依赖');
        console.error('请手动安装 Chocolatey 后重试');
        return false;
      }
      // 等待一下确保 Chocolatey 可用
      console.error('⏳ 等待 Chocolatey 初始化...');
      await new Promise(resolve => setTimeout(resolve, 3000));
    } else {
      console.error('✅ Chocolatey 已安装，准备安装依赖\n');
    }
  }

  for (const { key, dep, os: targetOs } of missing) {
    const installConfig = dep.install[targetOs];
    
    if (!installConfig) {
      console.error(`\n⚠️  ${dep.name}: 不支持当前操作系统`);
      console.error(`   请手动安装：${dep.description}`);
      hasError = true;
      continue;
    }

    const installCmd = installConfig;

    try {
      // Windows 特殊处理：使用 executeInstallCommand
      if (targetOs === 'windows') {
        const success = await executeInstallCommand(installCmd, dep.name, targetOs);
        if (success) {
          // 验证安装
          console.error('🔍 验证安装...');
          if (checkDependency(key)) {
            console.error(`✅ ${dep.name} 安装成功！\n`);
          } else {
            console.error(`⚠️  ${dep.name} 安装可能失败，请手动验证\n`);
            hasError = true;
          }
        } else {
          console.error(`\n❌ ${dep.name} 安装失败`);
          hasError = true;
        }
        continue;
      }

      // 检测是否需要 sudo（Linux/Mac）
      const needsSudo = installCmd.startsWith('sudo');
      
      if (needsSudo) {
        console.error(`\n⚠️  ${dep.name} 需要 sudo 权限，请输入密码：`);
      }

      console.error(`\n📦 正在安装 ${dep.name}...`);
      console.error(`   命令：${installCmd}`);
      console.error('   进度：');
      console.error('─'.repeat(60));

      // 执行安装（继承 stdio 以显示进度）
      execSync(installCmd, { 
        stdio: 'inherit',
        timeout: 300000 // 5 分钟超时
      });

      console.error('─'.repeat(60));

      // 验证安装
      console.error('🔍 验证安装...');
      if (checkDependency(key)) {
        console.error(`✅ ${dep.name} 安装成功！\n`);
      } else {
        console.error(`⚠️  ${dep.name} 安装可能失败，请手动验证`);
        hasError = true;
      }
    } catch (error) {
      console.error(`\n❌ ${dep.name} 安装失败：${error.message}`);
      console.error('   请检查错误信息后重试');
      hasError = true;
    }
  }

  console.error('\n' + '═'.repeat(60));
  
  if (hasError) {
    console.error('⚠️  部分依赖安装失败，请手动安装缺失的依赖');
    console.error('\n💡 提示：以下命令可手动安装：\n');
    missing.forEach(({ dep, os: targetOs }) => {
      if (typeof dep.install[targetOs] === 'string') {
        console.error(`   ${dep.install[targetOs]}`);
      } else if (dep.install[targetOs]?.cmd) {
        console.error(`   ${dep.install[targetOs].cmd}`);
      }
    });
    return false;
  } else {
    console.error('✅ 所有依赖安装成功！\n');
    console.error('═'.repeat(60));
    return true;
  }
}

/**
 * 主函数：检测并自动安装依赖（完全自动化，无需用户确认）
 * @returns {Promise<boolean>} 是否所有依赖就绪
 */
async function ensureDependencies() {
  const { installed, missing, os } = checkAllDependencies();

  if (missing.length === 0) {
    return true;
  }

  // 完全自动安装模式：不询问，直接开始安装
  console.error('\n🚀 发现缺失依赖，开始自动安装...\n');
  return await installMissingDependencies(missing, os);
}

/**
 * 快速检查：只检测，不安装
 * @returns {Object} 检测结果
 */
function quickCheck() {
  const { installed, missing, os } = checkAllDependencies();
  return { installed, missing, os, allInstalled: missing.length === 0 };
}

module.exports = {
  ensureDependencies,
  checkAllDependencies,
  quickCheck,
  getOS,
  checkHomebrew,
  installHomebrew,
  checkChocolatey,
  installChocolatey,
  DEPENDENCIES,
  executeInstallCommand,
  showWindowsManualInstall
};
