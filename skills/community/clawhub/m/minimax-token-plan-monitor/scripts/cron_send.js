// 专门给 cron 调用的脚本
// 通过 /v1/chat/completions 带上 bb session key，让消息在 bb session 里处理

const http = require('http');

const bbSessionKey = 'agent:bb:qqbot:direct:9bb108cd680d558f5bb78a066df4fb37';
const gatewayPort = 37701;
const authToken = '8d9c37620f26ffb66ec81daba1547ac537b6dee5aa0cc8fd';

function sendToBbSession(message) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      model: 'openclaw/bb',
      messages: [{ role: 'user', content: message }],
      max_tokens: 100
    });
    
    const options = {
      hostname: 'localhost',
      port: gatewayPort,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Authorization': `Bearer ${authToken}`,
        'x-openclaw-session-key': bbSessionKey
      }
    };
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.error('[Cron] Response status:', res.statusCode);
        console.error('[Cron] Response:', data.substring(0, 500));
        resolve(data);
      });
    });
    
    req.on('error', (e) => {
      console.error('[Cron] Error:', e.message);
      reject(e);
    });
    
    req.write(postData);
    req.end();
  });
}

async function main() {
  console.error('[Cron] Triggering bb session for MiniMax check...');
  
  const result = await sendToBbSession(
    '执行MiniMax用量查询脚本并通过QQ发送通知给我。脚本路径: /root/.openclaw/workspace/bb/skills/minimax-token-plan/scripts/check_and_notify.js'
  );
  
  console.error('[Cron] Done!');
}

main().catch(console.error);
