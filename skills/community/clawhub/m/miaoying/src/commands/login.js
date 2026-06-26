import fs from 'fs';
import path from 'path';
import os from 'os';
import https from 'https';
import QRCode from 'qrcode';
import { execFile } from 'child_process';

const API_HOST = 'www.aiphoto8.cn';
const CONFIG_DIR = path.join(os.homedir(), '.miaoying');
const CONFIG_PATH = path.join(CONFIG_DIR, 'config.json');

function httpsRequest(options, data) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let body = '';
      res.on('data', chunk => (body += chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error(`Failed to parse response: ${body}`));
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) return null;
  try {
    const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const config = JSON.parse(content);
    return config.apiKey || null;
  } catch {
    return null;
  }
}

function saveConfig(apiKey) {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
  fs.writeFileSync(CONFIG_PATH, JSON.stringify({ apiKey }, null, 2));
}

function decodeApiKey(obfuscatedKey, userId) {
  const keyStr = userId.toString().slice(0, 4);
  const buf = Buffer.from(obfuscatedKey, 'base64');
  for (let i = 0; i < buf.length; i++) {
    buf[i] ^= keyStr.charCodeAt(i % keyStr.length);
  }
  return buf.toString();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function login(options = {}) {
  const output = options.output || path.join(os.homedir(), 'Desktop', 'miaoying_login_qr.png');
  const quiet = options.quiet || false;

  // Check if already logged in
  const existingKey = loadConfig();
  if (existingKey) {
    console.log('🔑 检测到已保存的 API Key，是否重新获取？');
    console.log('   配置路径:', CONFIG_PATH);
    console.log('');
    console.log('如需重新登录，请删除 ~/.miaoying/config.json 文件后再次运行此命令');
    console.log('或者设置环境变量 MIAOYING_API_KEY 使用其他 Key');
    return;
  }

  console.log('🔑 正在获取登录二维码...');

  // Step 1: Get QR code scene
  const loginResponse = await httpsRequest(
    {
      hostname: API_HOST,
      port: 443,
      path: '/weapi/weixin/qrcodeApiKeyLogin',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': 0
      }
    }
  );

  if (!loginResponse.data || !loginResponse.data.sceneId || !loginResponse.data.url) {
    console.error('❌ 获取登录二维码失败:', JSON.stringify(loginResponse));
    process.exit(1);
  }

  const { sceneId, url } = loginResponse.data;
  console.log('✅ 二维码已生成');

  // Step 2: Generate QR code image
  const qrDir = path.dirname(output);
  if (!fs.existsSync(qrDir)) {
    fs.mkdirSync(qrDir, { recursive: true });
  }

  await QRCode.toFile(output, url, {
    width: 300,
    margin: 2,
    color: { dark: '#000000', light: '#ffffff' }
  });

  if (!quiet) {
    console.log('');
    console.log('📱 二维码已保存到:', output);
    console.log('');
    console.log('📲 请用微信扫描上方二维码获取 API Key');
    console.log('');
    console.log('   1. 打开微信');
    console.log('   2. 扫描上方二维码');
    console.log('   3. 按提示完成授权');
    console.log('');
    console.log('⏱️  二维码 10 分钟内有效');
    console.log('💡 扫码后会自动检测，无需手动操作');
    console.log('');

    // Try to open the QR image with default viewer
    try {
      if (process.platform === 'darwin') {
        execFile('open', [output], () => {});
      } else if (process.platform === 'win32') {
        execFile('cmd', ['/c', 'start', '', output], () => {});
      } else {
        execFile('xdg-open', [output], () => {});
      }
    } catch {
      // Silently fail - user can open manually
    }
  }

  // Step 4: Poll for result
  console.log('⏳ 等待扫码中...');

  // First wait 15 seconds to give user time to scan
  await sleep(15000);

  const startTime = Date.now();
  const maxWaitTime = 10 * 60 * 1000; // 10 minutes
  let pollInterval = 5000; // 5 seconds

  while (Date.now() - startTime < maxWaitTime) {
    try {
      const pollResponse = await httpsRequest({
        hostname: API_HOST,
        port: 443,
        path: `/weapi/weixin/getUserWithSceneId/${sceneId}`,
        method: 'GET'
      });

      // Check if we got a successful response with apiKey
      if (pollResponse.data && pollResponse.data.apiKey && pollResponse.data._id) {
        const { apiKey: obfuscatedKey, _id, nickname } = pollResponse.data;
        const realApiKey = decodeApiKey(obfuscatedKey, _id);

        // Save to config
        saveConfig(realApiKey);

        console.log('');
        console.log('✅ API Key 获取成功！');
        console.log('   用户:', nickname || _id);
        console.log('   已自动保存到:', CONFIG_PATH);
        console.log('');
        console.log('🎉 登录完成！后续使用无需再次扫码。');
        return;
      }

      // If response has data but no apiKey, it might be processing
      if (pollResponse.data && !pollResponse.error) {
        // Still waiting for apiKey to be generated
        process.stdout.write('.');
      }
    } catch (err) {
      // Likely still waiting for scan (400 error)
      process.stdout.write('.');
    }

    await sleep(pollInterval);
  }

  console.log('');
  console.log('❌ 登录超时（10 分钟）');
  console.log('   请重新运行此命令获取新的二维码');
  process.exit(1);
}

export async function logout() {
  const existingKey = loadConfig();
  if (!existingKey) {
    console.log('🔑 未检测到已保存的 API Key');
    return;
  }

  console.log('🔑 正在禁用当前 API Key...');

  try {
    await httpsRequest(
      {
        hostname: API_HOST,
        port: 443,
        path: '/api/openapi/apikeys/self/deactivate',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${existingKey}`,
          'Content-Length': Buffer.byteLength(JSON.stringify({ reason: 'user_logout' }))
        }
      },
      JSON.stringify({ reason: 'user_logout' })
    );

    console.log('✅ 当前 API Key 已禁用');
  } catch (err) {
    console.log('⚠️  禁用 API Key 时出错:', err.message);
  }

  // Remove local config
  if (fs.existsSync(CONFIG_PATH)) {
    fs.unlinkSync(CONFIG_PATH);
    console.log('✅ 本地配置已删除');
  }
}
