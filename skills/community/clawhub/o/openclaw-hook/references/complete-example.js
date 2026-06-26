/**
 * OpenClaw Internal Hook 完整示例
 * 
 * 功能：在 agent:bootstrap 时检查工作区状态并发送 Telegram 通知
 * 位置：~/.openclaw/hooks/my-hook/handler.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// ============================================
// 1. 发送 Telegram 通知
// ============================================
async function sendTelegramNotification(botToken, chatId, message) {
  const data = JSON.stringify({
    chat_id: chatId,
    text: message,
    // 不使用 parse_mode 避免解析问题
  });
  
  return new Promise((resolve) => {
    const options = {
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${botToken}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // ⚠️ 关键：使用 Buffer.byteLength 而不是 data.length
        'Content-Length': Buffer.byteLength(data),
      },
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve(true);
        } else {
          console.error('[my-hook] Telegram API error:', res.statusCode, body);
          resolve(false);
        }
      });
    });
    
    req.on('error', (e) => {
      console.error('[my-hook] Telegram request error:', e.message);
      resolve(false);
    });
    
    req.write(data);
    req.end();
  });
}

// ============================================
// 2. 从配置文件获取 bot token
// ============================================
function getBotToken(accountName = 'default') {
  try {
    const configPath = path.join(os.homedir(), '.openclaw/openclaw.json');
    const content = fs.readFileSync(configPath, 'utf-8');
    
    // 尝试匹配指定账号
    const accountMatch = content.match(
      new RegExp(`"${accountName}"[\\s\\S]*?"botToken"\\s*:\\s*"([^"]+)"`)
    );
    if (accountMatch?.[1]) return accountMatch[1];
    
    // 回退到第一个 token
    const tokenMatch = content.match(/"botToken":\s*"([^"]+)"/);
    return tokenMatch?.[1] || null;
  } catch (e) {
    console.error('[my-hook] Config read error:', e.message);
    return null;
  }
}

// ============================================
// 3. 主 Handler
// ============================================
const handler = async (event) => {
  // --- 安全检查 ---
  if (!event || typeof event !== 'object') {
    console.error('[my-hook] No event object');
    return;
  }

  // 只处理 agent:bootstrap
  if (event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  // 检查上下文
  if (!event.context || typeof event.context !== 'object') {
    console.error('[my-hook] No context');
    return;
  }

  // 跳过 sub-agent
  const sessionKey = event.sessionKey || '';
  if (sessionKey.includes(':subagent:')) {
    console.error('[my-hook] Skipping sub-agent');
    return;
  }

  // 获取工作区
  const workspaceDir = event.context?.workspaceDir;
  if (!workspaceDir) {
    console.error('[my-hook] No workspaceDir');
    return;
  }

  console.error('[my-hook] Using workspace:', workspaceDir);

  // --- 读取工作区状态 ---
  let statusInfo = '';
  
  try {
    const memoryDir = path.join(workspaceDir, 'memory');
    if (fs.existsSync(memoryDir)) {
      const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
      if (files.length > 0) {
        statusInfo = `\n📝 Memory: ${files.length} files`;
      }
    }
  } catch (e) {
    // 忽略错误
  }

  // --- 注入虚拟文件 ---
  const reminderContent = `
# Hook Reminder

This is injected by my-hook at ${new Date().toISOString()}.

Session: ${sessionKey}
Agent: ${event.context?.agentId || 'unknown'}
`.trim();

  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'HOOK_REMINDER.md',
      content: reminderContent,
      virtual: true,
    });
  }

  // --- 发送通知 ---
  try {
    const botToken = getBotToken('default');
    const chatId = 'YOUR_CHAT_ID'; // 替换
    
    if (botToken) {
      const timeStr = new Date().toLocaleString('zh-CN', {
        timeZone: 'Asia/Shanghai'
      });
      
      const message = 
        `✅ Hook 已执行\n\n` +
        `━━━━━━━━━━━━━━━━━━━━━━\n` +
        `📚 Agent: ${event.context?.agentId || 'unknown'}\n` +
        `⏰ ${timeStr}` +
        statusInfo;
      
      const result = await sendTelegramNotification(botToken, chatId, message);
      console.error('[my-hook] Telegram:', result ? 'success' : 'failed');
    }
  } catch (e) {
    console.error('[my-hook] Notification error:', e.message);
  }
};

// ============================================
// 4. 导出（必须！）
// ============================================
module.exports = handler;
module.exports.default = handler;
ts.default = handler;
ult = handler;
ts.default = handler;
