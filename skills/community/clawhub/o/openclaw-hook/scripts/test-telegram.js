#!/usr/bin/env node
/**
 * Telegram 发送测试脚本
 * 
 * 用法: node test-telegram.js <message>
 *       node test-telegram.js --test
 * 
 * 用于快速测试 Telegram Bot API 发送功能，排查问题。
 */

const fs = require('fs');
const https = require('https');
const path = require('path');
const os = require('os');

// 从配置文件获取 bot token
function getBotToken() {
  const configPath = process.env.OPENCLAW_CONFIG || 
    path.join(os.homedir(), '.openclaw/openclaw.json');
  try {
    const configContent = fs.readFileSync(configPath, 'utf-8');
    const tokenMatch = configContent.match(/"botToken":\s*"([^"]+)"/);
    return tokenMatch?.[1] || null;
  } catch (e) {
    console.error('Failed to read config:', e.message);
    return null;
  }
}

// 发送消息
async function sendMessage(botToken, chatId, message) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      chat_id: chatId,
      text: message,
    });
    
    console.log('\n--- Request Details ---');
    console.log('Message length (chars):', message.length);
    console.log('JSON length (chars):', data.length);
    console.log('JSON byte length:', Buffer.byteLength(data));
    
    const options = {
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${botToken}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data), // 关键！
      },
    };
    
    console.log('Content-Length header:', Buffer.byteLength(data));
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        console.log('\n--- Response ---');
        console.log('Status:', res.statusCode);
        
        try {
          const result = JSON.parse(body);
          if (result.ok) {
            console.log('✅ Success! Message ID:', result.result.message_id);
          } else {
            console.log('❌ Failed:', result.description);
          }
        } catch (e) {
          console.log('Response body:', body);
        }
        
        resolve(res.statusCode === 200);
      });
    });
    
    req.on('error', (e) => {
      console.error('Request error:', e.message);
      reject(e);
    });
    
    req.write(data);
    req.end();
  });
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: node test-telegram.js <message>');
    console.log('       node test-telegram.js --test');
    process.exit(1);
  }
  
  const botToken = getBotToken();
  if (!botToken) {
    console.error('❌ No bot token found in config');
    process.exit(1);
  }
  
  console.log('Bot token found (length:', botToken.length + ')');
  
  // 默认 chat ID，可以从环境变量传入
  const chatId = process.env.TELEGRAM_CHAT_ID || 'YOUR_CHAT_ID';
  
  let message;
  if (args[0] === '--test') {
    // 测试模式：发送包含中文的消息
    message = 
      `✅ Telegram 测试消息\n\n` +
      `━━━━━━━━━━━━━━━━━━━━━━\n` +
      `📚 这是一条测试消息\n` +
      `⏰ ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`;
  } else {
    message = args.join(' ');
  }
  
  console.log('\n--- Message ---');
  console.log(message);
  
  try {
    await sendMessage(botToken, chatId, message);
  } catch (e) {
    console.error('Failed to send message:', e.message);
    process.exit(1);
  }
}

main();
