#!/usr/bin/env node
/**
 * kids-points 技能包装器
 * 
 * 功能：
 * 1. 首次使用时自动检查依赖
 * 2. 提供友好的安装引导
 * 3. 加载实际的 handler.js
 */

const fs = require('fs');
const path = require('path');
const { checkSkillDependencies, checkApiKey } = require('./install-dependencies.js');

const HANDLER_PATH = path.join(__dirname, 'handler.js');
const FIRST_RUN_FLAG = path.join(__dirname, '.first-run-check');

/**
 * 检查是否是首次运行
 */
function isFirstRun() {
  return !fs.existsSync(FIRST_RUN_FLAG);
}

/**
 * 标记已完成首次检查
 */
function markFirstRunComplete() {
  fs.writeFileSync(FIRST_RUN_FLAG, new Date().toISOString());
}

/**
 * 显示欢迎信息
 */
function showWelcome() {
  console.log('');
  console.log('🎉 ' + '='.repeat(58));
  console.log('   欢迎使用 kids-points 儿童积分语音助手！');
  console.log('🎉 ' + '='.repeat(58));
  console.log('');
}

/**
 * 加载实际的处理器
 */
function loadHandler() {
  try {
    const handler = require(HANDLER_PATH);
    return handler;
  } catch (e) {
    console.error('❌ 无法加载技能处理器:', e.message);
    return null;
  }
}

/**
 * 初始化技能
 */
function initSkill() {
  showWelcome();
  
  // 检查依赖
  const { missing } = checkSkillDependencies();
  const apiKeyStatus = checkApiKey();
  
  console.log('');
  
  // 首次运行提示
  if (isFirstRun()) {
    if (missing.length === 0 && apiKeyStatus.configured) {
      console.log('✅ 所有依赖已就绪，语音功能可用！');
    } else if (missing.length > 0) {
      console.log('💡 提示：安装依赖技能后可解锁语音功能');
      console.log('   文字记账功能可以直接使用哦~');
    } else if (!apiKeyStatus.configured) {
      console.log('💡 提示：配置 API Key 后可解锁语音功能');
      console.log('   目前基本免费，访问 https://senseaudio.cn');
    }
    
    console.log('');
    console.log('📚 发送 "帮助" 查看使用说明');
    console.log('📋 查看 DEPENDENCIES.md 了解详细配置');
    console.log('');
    
    markFirstRunComplete();
  }
  
  return loadHandler();
}

// 导出包装后的处理器
const handler = initSkill();

if (handler) {
  module.exports = handler;
} else {
  console.error('❌ 技能初始化失败');
  module.exports = {};
}
