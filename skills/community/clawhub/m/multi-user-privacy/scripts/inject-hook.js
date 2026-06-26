#!/usr/bin/env node

/**
 * 自动注入隐私检查 Hook
 * 
 * 用法：
 * node scripts/inject-hook.js
 * 
 * 功能：
 * 在 OpenClaw 主入口自动添加隐私检查调用
 */

const fs = require('fs');
const path = require('path');

const HOOK_CODE = `
// ========== 隐私检查自动注入（multi-user-privacy v0.3.1） ==========
const PrivacyGuard = (() => {
  try {
    return require('./skills/multi-user-privacy/privacy-guard');
  } catch (e) {
    console.warn('[PrivacyGuard] 技能未找到，跳过隐私检查');
    return null;
  }
})();

function checkAndInject(context) {
  if (!PrivacyGuard) return context;
  
  const startTime = Date.now();
  const result = PrivacyGuard.preCheck(context);
  
  if (result.status === 'PASS') {
    console.log(\`[PrivacyGuard] ✅ \${result.userId} (\${result.isAdmin ? '管理员' : '普通用户'})\`);
    return {
      ...context,
      _privacyCheck: {
        passed: true,
        userId: result.userId,
        isAdmin: result.isAdmin,
        memoryLoaded: result.memory.loaded.length,
        timestamp: result.timestamp
      }
    };
  } else {
    console.error(\`[PrivacyGuard] ❌ \${result.error}\`);
    return context;
  }
}

function checkReplyBeforeSend(message, userId) {
  if (!PrivacyGuard || !userId) return { allowed: true };
  
  const result = PrivacyGuard.beforeReply(message, userId);
  
  if (!result.allowed) {
    console.warn(\`[PrivacyGuard] ⚠️  拦截敏感消息：\${result.reason}\`);
    result.issues?.forEach(issue => {
      console.warn(\`  - \${issue.type}: \${issue.message}\`);
    });
  }
  
  return result;
}

// 导出到全局
global.privacyGuard = {
  checkAndInject,
  checkReplyBeforeSend
};
// ====================================================================
`;

function injectHook() {
  const mainFiles = [
    path.join(process.env.HOME, '.openclaw/runtime/main.js'),
    path.join(process.env.HOME, '.openclaw/src/index.js'),
    path.join(process.env.HOME, '.openclaw/app.js')
  ];
  
  let targetFile = null;
  for (const file of mainFiles) {
    if (fs.existsSync(file)) {
      targetFile = file;
      break;
    }
  }
  
  if (!targetFile) {
    console.log('⚠️  未找到 OpenClaw 主入口文件');
    console.log('请手动在 main.js 或 index.js 开头添加以下代码:');
    console.log(HOOK_CODE);
    return;
  }
  
  console.log(`📝 找到主入口：${targetFile}`);
  
  const content = fs.readFileSync(targetFile, 'utf-8');
  
  // 检查是否已经注入
  if (content.includes('PrivacyGuard')) {
    console.log('✅ 隐私检查已注入，跳过');
    return;
  }
  
  // 在文件开头注入
  const newContent = HOOK_CODE + '\n' + content;
  fs.writeFileSync(targetFile, newContent);
  
  console.log('✅ 隐私检查 Hook 注入成功！');
  console.log('\n📋 使用示例:');
  console.log(`
// 在发送消息前调用
const context = privacyGuard.checkAndInject(currentContext);

// 在回复前检查
const check = privacyGuard.checkReplyBeforeSend(response, userId);
if (!check.allowed) {
  response = rewriteResponse(response);
}
  `);
}

injectHook();
