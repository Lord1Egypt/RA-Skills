/**
 * 微信通知模块 — 将 OceanBus 消息实时推送到微信
 *
 * ⚠️ 必须用 https.request + 显式 Content-Length，
 *    微信 API 不接受 chunked transfer encoding。
 */
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ── 微信消息发送 ──────────────────────────────────────────────────────────

function sendWeixinMessage(opts) {
  return new Promise((resolve, reject) => {
    const { token, baseUrl, toUserId, text } = opts;
    const uin = crypto.randomBytes(4).toString('base64');
    const clientId = crypto.randomUUID();

    const body = JSON.stringify({
      msg: {
        from_user_id: '',
        to_user_id: toUserId,
        client_id: clientId,
        message_type: 2,
        message_state: 4,
        item_list: [{ type: 1, text_item: { text } }],
      },
      base_info: { channel_version: '2.1.1' },
    });

    const url = new URL(baseUrl.replace(/\/+$/, '') + '/ilink/bot/sendmessage');

    const req = https.request({
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        AuthorizationType: 'ilink_bot_token',
        Authorization: `Bearer ${token}`,
        'Content-Length': String(Buffer.byteLength(body)),
        'X-WECHAT-UIN': uin,
        'iLink-App-Id': 'bot',
        'iLink-App-ClientVersion': '0',
      },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) resolve();
        else reject(new Error(`微信 API ${res.statusCode}: ${data.slice(0, 200)}`));
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── 凭证自动发现（从 OpenClaw 微信插件读取） ────────────────────────────────

function discoverWeixinCredentials() {
  const accountsDir = path.join(
    os.homedir(), '.openclaw', 'openclaw-weixin', 'accounts'
  );

  if (!fs.existsSync(accountsDir)) return null;

  try {
    const files = fs.readdirSync(accountsDir).filter(f => f.endsWith('.json'));
    if (files.length === 0) return null;

    const first = path.join(accountsDir, files[0]);
    const data = JSON.parse(fs.readFileSync(first, 'utf-8'));

    if (!data.token || !data.userId) return null;

    return {
      token: data.token,
      baseUrl: data.baseUrl || 'https://ilinkai.weixin.qq.com',
      userId: data.userId,
      source: '微信插件',
    };
  } catch {
    return null;
  }
}

// ── 凭证解析（优先级：环境变量 > 自动发现 > 降级） ─────────────────────────

function resolveWeixinConfig() {
  // 1. 环境变量（显式配置，最高优先级）
  if (process.env.WECHAT_BOT_TOKEN && process.env.WECHAT_BOT_BASE_URL) {
    return {
      token: process.env.WECHAT_BOT_TOKEN,
      baseUrl: process.env.WECHAT_BOT_BASE_URL,
      userId: process.env.WECHAT_BOT_USER_ID || '',
      source: '环境变量',
    };
  }

  // 2. 自动发现（从 OpenClaw 微信插件读取）
  const discovered = discoverWeixinCredentials();
  if (discovered) return discovered;

  // 3. 降级：不推送微信
  return null;
}

// ── 新用户引导提示 ─────────────────────────────────────────────────────────

function printSetupGuide() {
  console.log('[monitor] 微信通知未配置。');
  console.log('');
  console.log('  方式一（推荐）：安装 OpenClaw 微信插件并扫码登录');
  console.log('    openclaw plugins install "@tencent-weixin/openclaw-weixin"');
  console.log('    openclaw channels login --channel openclaw-weixin');
  console.log('    openclaw gateway restart');
  console.log('');
  console.log('  方式二：手动设置环境变量');
  console.log('    export WECHAT_BOT_TOKEN="<token>"');
  console.log('    export WECHAT_BOT_BASE_URL="https://ilinkai.weixin.qq.com"');
  console.log('    export WECHAT_BOT_USER_ID="<你的微信 ID>"');
  console.log('');
  console.log('[monitor] 当前仅监听 OceanBus，不推送微信');
}

module.exports = { sendWeixinMessage, resolveWeixinConfig, printSetupGuide };
