#!/usr/bin/env node
/**
 * kids-points 依赖自动安装脚本
 * 
 * 功能：
 * 1. 检查依赖技能是否安装
 * 2. 提示用户安装（可选）
 * 3. 检查 API Key 配置
 * 4. 提供友好的配置引导
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const SKILL_CONFIG = path.join(__dirname, '..', 'skill.json');

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

/**
 * 加载技能配置
 */
function loadSkillConfig() {
  try {
    const data = fs.readFileSync(SKILL_CONFIG, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    log('❌ 无法读取技能配置', 'red');
    return null;
  }
}

/**
 * 检查依赖技能是否安装
 */
function checkSkillDependencies() {
  const config = loadSkillConfig();
  if (!config || !config.dependencies) {
    return { installed: true, missing: [] };
  }
  
  const missing = [];
  const installed = [];
  
  if (config.dependencies.skills) {
    for (const skill of config.dependencies.skills) {
      const skillPath = path.join(WORKSPACE, 'skills', skill.id);
      if (fs.existsSync(skillPath)) {
        installed.push(skill);
        log(`✅ ${skill.name} 已安装`, 'green');
      } else {
        missing.push(skill);
        log(`⚠️  ${skill.name} 未安装`, 'yellow');
      }
    }
  }
  
  return { installed, missing, optional: config.dependencies.skills.every(s => !s.required) };
}

/**
 * 检查 API Key 配置
 */
function checkApiKey() {
  try {
    const configPath = path.join(process.env.HOME || '~', '.openclaw/openclaw.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const apiKey = config.env?.SENSE_API_KEY;
    
    if (apiKey && apiKey.length > 10) {
      log('✅ SenseAudio API Key 已配置', 'green');
      return { configured: true };
    }
  } catch (e) {
    // 忽略错误
  }
  
  log('⚠️  SenseAudio API Key 未配置', 'yellow');
  return { configured: false };
}

/**
 * 显示安装提示
 */
function showInstallPrompt(missing) {
  if (missing.length === 0) {
    log('\n✅ 所有依赖已就绪！', 'green');
    return;
  }
  
  log('\n' + '='.repeat(60), 'cyan');
  log('📦 发现未安装的依赖技能', 'cyan');
  log('='.repeat(60), 'cyan');
  
  console.log('');
  for (const skill of missing) {
    console.log(`  • ${skill.name} (${skill.id})`);
    console.log(`    用途：${skill.features.join(', ')}`);
    console.log(`    说明：${skill.reason}`);
    console.log('');
  }
  
  log('💡 提示：这些是可选依赖，不影响文字功能使用', 'blue');
  log('   但安装后可以解锁语音功能，体验更好哦！', 'blue');
  console.log('');
  
  // 提供安装命令
  log('🔧 快速安装命令：', 'cyan');
  for (const skill of missing) {
    console.log(`   clawhub install ${skill.id}`);
  }
  console.log('');
  
  log('📋 或者手动安装：', 'cyan');
  console.log('   1. 访问 https://clawhub.com');
  console.log('   2. 搜索技能名称');
  console.log('   3. 点击安装');
  console.log('');
  
  // API Key 提示
  const apiKeyStatus = checkApiKey();
  if (!apiKeyStatus.configured) {
    log('🔑 SenseAudio API Key 配置：', 'cyan');
    console.log('   1. 访问 https://senseaudio.cn');
    console.log('   2. 免费注册账号（目前基本免费）');
    console.log('   3. 创建应用获取 API Key');
    console.log('   4. 添加到 ~/.openclaw/openclaw.json 的 env 配置');
    console.log('');
  }
  
  log('='.repeat(60), 'cyan');
}

/**
 * 自动安装（如果用户同意）
 */
function autoInstall(missing, callback) {
  if (missing.length === 0) {
    callback(true);
    return;
  }
  
  // 由于是命令行工具，这里只提供指导
  // 实际的自动安装需要 ClawHub API 支持
  log('\n💡 提示：请手动运行上述安装命令', 'blue');
  log('   安装完成后重启技能即可使用语音功能', 'blue');
  
  callback(true);
}

/**
 * 主函数
 */
function main() {
  log('🔍 检查 kids-points 依赖...', 'cyan');
  console.log('');
  
  const { installed, missing, optional } = checkSkillDependencies();
  const apiKeyStatus = checkApiKey();
  
  console.log('');
  showInstallPrompt(missing);
  
  // 总结
  log('📊 功能可用性：', 'cyan');
  console.log('');
  console.log('  ✅ 文字记账 - 可用');
  console.log('  ✅ 积分查询 - 可用');
  console.log('  ✅ 规则修改 - 可用');
  console.log(`  ${missing.length === 0 && apiKeyStatus.configured ? '✅' : '⚠️'}  语音记账 - ${missing.length === 0 && apiKeyStatus.configured ? '可用' : '需配置'}`);
  console.log(`  ${missing.length === 0 && apiKeyStatus.configured ? '✅' : '⚠️'}  语音播报 - ${missing.length === 0 && apiKeyStatus.configured ? '可用' : '需配置'}`);
  console.log('');
  
  if (missing.length === 0 && apiKeyStatus.configured) {
    log('🎉 所有功能已就绪，开始使用吧！', 'green');
  } else if (missing.length === 0 && !apiKeyStatus.configured) {
    log('💡 配置 API Key 后可解锁完整语音功能', 'blue');
  } else {
    log('💡 安装依赖技能后可解锁语音功能', 'blue');
  }
  
  console.log('');
}

// 运行
main();

module.exports = {
  checkSkillDependencies,
  checkApiKey,
  showInstallPrompt,
  autoInstall
};
