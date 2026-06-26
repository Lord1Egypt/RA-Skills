#!/usr/bin/env node
/**
 * Kim 消息号发送脚本
 * 用法：message.js -u <用户名> -m <消息内容>
 * 环境变量：KIM_APP_KEY, KIM_SECRET_KEY
 * 
 * 密钥加载策略：
 * 1. 优先使用环境变量
 * 2. 环境变量缺失或发送失败时，自动 fallback 到密钥文件
 * 
 * 支持的密钥文件路径（按优先级）：
 * - ~/.openclaw/.secrets
 * - ~/.kim_credentials
 * - ./kim_credentials
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

const BASE_URL = 'https://is-gateway.corp.kuaishou.com';

// 常见的密钥文件路径（按优先级排序）
const CREDENTIAL_FILES = [
  path.join(os.homedir(), '.openclaw', '.secrets'),
  path.join(os.homedir(), '.kim_credentials'),
  path.join(process.cwd(), 'kim_credentials'),
];

// 解析参数
const args = process.argv.slice(2);
let username = '';
let message = '';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '-u' || args[i] === '--user') {
    username = args[i + 1] ?? '';
    i++;
  } else if (args[i] === '-m' || args[i] === '--message') {
    message = args[i + 1] ?? '';
    i++;
  }
}

if (!username || !message) {
  console.error('用法：message.js -u <用户名> -m <消息内容>');
  console.error('  -u, --user     目标用户名 (必填)');
  console.error('  -m, --message  消息内容 (必填)');
  process.exit(1);
}

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
  });
}

function httpsPost(url, body, headers) {
  const u = new URL(url);
  const options = {
    hostname: u.hostname,
    port: u.port || 443,
    path: u.pathname + u.search,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body, 'utf8'),
      ...headers,
    },
  };
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.write(body, 'utf8');
    req.end();
  });
}

async function getAccessToken(appKey, secretKey) {
  const params = new URLSearchParams({ appKey, secretKey });
  const url = `${BASE_URL}/token/get?${params}`;
  const raw = await httpsGet(url);
  const data = JSON.parse(raw);
  if (data.code !== 0) {
    throw new Error(`获取 accessToken 失败：${JSON.stringify(data)}`);
  }
  return data.result.accessToken;
}

/**
 * 单用户发送 - /openapi/v2/message/send
 */
async function sendSingleUser(token, targetUser, msg) {
  const url = `${BASE_URL}/openapi/v2/message/send`;
  const payload = JSON.stringify({
    msgType: 'markdown',
    markdown: { content: msg },
    username: targetUser,
  });
  const raw = await httpsPost(url, payload, {
    Authorization: `Bearer ${token}`,
  });
  return JSON.parse(raw);
}

/**
 * 批量用户发送 - /openapi/v2/message/batch/send
 */
async function sendBatchUsers(token, targetUser, msg) {
  const url = `${BASE_URL}/openapi/v2/message/batch/send`;
  const payload = JSON.stringify({
    msgType: 'markdown',
    markdown: { content: msg },
    usernames: [targetUser],
  });
  const raw = await httpsPost(url, payload, {
    Authorization: `Bearer ${token}`,
  });
  return JSON.parse(raw);
}

/**
 * 检查错误是否是"用户不在可见范围"
 * 错误码：10122003, 10122004
 */
function isUserNotVisibleError(result) {
  const msg = (result.message || '').toLowerCase();
  return result.code === 10122003 || result.code === 10122004 || 
         msg.includes('不在应用可见范围') || msg.includes('username 错误');
}

/**
 * 从密钥文件读取密钥
 */
function loadCredentialsFromFile() {
  for (const credFile of CREDENTIAL_FILES) {
    try {
      if (fs.existsSync(credFile)) {
        const content = fs.readFileSync(credFile, 'utf8');
        const appKeyMatch = content.match(/^KIM_APPKEY=(.*)$/m);
        const secretKeyMatch = content.match(/^KIM_SECRET=(.*)$/m);
        
        if (appKeyMatch && secretKeyMatch) {
          return {
            appKey: appKeyMatch[1].trim(),
            secretKey: secretKeyMatch[1].trim(),
          };
        }
      }
    } catch (err) {
      // 继续尝试下一个文件
    }
  }
  return null;
}

/**
 * 尝试发送消息（两种接口）
 */
async function trySendMessage(appKey, secretKey) {
  const token = await getAccessToken(appKey, secretKey);
  let lastResult = null;
  
  // 尝试单用户接口
  try {
    let result = await sendSingleUser(token, username, message);
    
    if (result.code === 0) {
      return { success: true, result };
    }
    
    lastResult = result;
  } catch (err) {
    lastResult = { code: -1, message: err.message };
  }
  
  // 单用户失败，尝试批量用户接口
  try {
    let result = await sendBatchUsers(token, username, message);
    
    if (result.code === 0) {
      return { success: true, result };
    }
    
    lastResult = result;
  } catch (err) {
    lastResult = { code: -1, message: err.message };
  }
  
  return { success: false, result: lastResult };
}

async function main() {
  console.log(`📤 正在发送消息给用户：${username}`);
  
  let usedFallback = false;
  let appKey = process.env.KIM_APP_KEY;
  let secretKey = process.env.KIM_SECRET_KEY;
  
  // 检查是否使用环境变量
  const hasEnvCredentials = !!(appKey && secretKey);
  
  if (hasEnvCredentials) {
    // 环境变量已设置，先尝试直接发送
    console.log(`🔑 使用环境变量中的密钥...`);
    const sendResult = await trySendMessage(appKey, secretKey);
    
    if (sendResult.success) {
      console.log('✅ 消息发送成功！');
      console.log(JSON.stringify(sendResult.result, null, 2));
      return;
    }
    
    // 发送失败，记录原因并准备 fallback
    console.log(`⚠️ 环境变量密钥发送失败：${sendResult.result?.message || '未知错误'}`);
    console.log(`🔄 尝试从密钥文件加载...`);
    usedFallback = true;
  }
  
  // 环境变量未设置或发送失败，尝试从文件加载
  const fileCredentials = loadCredentialsFromFile();
  
  if (!fileCredentials) {
    console.error('');
    console.error('❌ 无法获取 Kim 密钥');
    console.error('');
    console.error('💡 请配置密钥：');
    console.error('   方式 1: 设置环境变量');
    console.error('     export KIM_APP_KEY=your_app_key');
    console.error('     export KIM_SECRET_KEY=your_secret_key');
    console.error('');
    console.error('   方式 2: 创建密钥文件（推荐）');
    console.error('     KIM_APPKEY=your_app_key');
    console.error('     KIM_SECRET=your_secret_key');
    process.exit(1);
  }
  
  appKey = fileCredentials.appKey;
  secretKey = fileCredentials.secretKey;
  
  // 使用文件中的密钥重试发送
  console.log(`🔑 从密钥文件加载成功`);
  const sendResult = await trySendMessage(appKey, secretKey);
  
  if (sendResult.success) {
    console.log('✅ 消息发送成功！');
    console.log(JSON.stringify(sendResult.result, null, 2));
    
    // 如果触发了 fallback，输出警告
    if (usedFallback) {
      console.log('');
      console.log('⚠️  警告：本次发送触发了密钥 fallback 机制');
      console.log('   建议检查环境变量 KIM_APP_KEY 和 KIM_SECRET_KEY 是否正确配置');
    }
    return;
  }
  
  // 两个方式都失败，输出详细错误
  console.error('');
  console.error('❌ 消息发送失败');
  console.error('');
  console.error('错误详情:', {
    code: sendResult.result?.code,
    message: sendResult.result?.message
  });
  console.error('');
  
  // 根据错误类型给出建议
  if (isUserNotVisibleError(sendResult.result)) {
    console.error('💡 可能原因：');
    console.error('   1. 用户名不正确（请确认是快手邮箱前缀，如 wangyang）');
    console.error('   2. 该用户未授权此 Kim 应用');
    console.error('   3. 应用配置中未添加该用户到可见范围');
    console.error('');
    console.error('✅ 解决方案：');
    console.error('   - 请对方在 Kim 中授权此应用');
    console.error('   - 或联系应用管理员添加用户到可见范围');
    console.error('   - 或改用其他方式联系（如微信、电话等）');
  } else {
    console.error('💡 建议：');
    console.error('   - 检查用户名是否正确');
    console.error('   - 检查消息内容是否合规');
    console.error('   - 联系应用管理员或查看 Kim 开放平台文档');
  }
  
  // 如果触发了 fallback，输出警告
  if (usedFallback) {
    console.error('');
    console.error('⚠️  警告：本次发送触发了密钥 fallback 机制');
    console.error('   建议检查环境变量 KIM_APP_KEY 和 KIM_SECRET_KEY 是否正确配置');
  }
  
  process.exit(1);
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
