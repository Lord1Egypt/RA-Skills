#!/usr/bin/env node
/**
 * Lobi A2A 轮询守护进程
 * 独立运行，定期轮询房间消息
 */

const fs = require('fs');
const path = require('path');

// 从环境变量或配置文件读取
const config = loadConfig();
const POLL_INTERVAL = 5000; // 5秒轮询一次

// 存储活跃的 A2A 房间
let activeRooms = new Map(); // roomId -> { lastCheckTime, ctx }

function loadConfig() {
  try {
    const configPath = path.join(process.env.HOME, '.openclaw', 'config.json');
    const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    return {
      homeserver: data.env?.LOBI_HOMESERVER || data.channels?.lobi?.accounts?.default?.homeserver,
      token: data.env?.LOBI_ACCESS_TOKEN || data.channels?.lobi?.accounts?.default?.accessToken,
      userId: data.env?.LOBI_USER_ID || data.channels?.lobi?.accounts?.default?.userId,
    };
  } catch (e) {
    console.error('加载配置失败:', e.message);
    process.exit(1);
  }
}

// HTTP 请求
async function httpRequest(url, options = {}) {
  const fetch = (await import('node-fetch')).default;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${config.token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return res;
}

// 获取房间消息
async function getRoomMessages(roomId, limit = 10) {
  const url = `${config.homeserver}/_lobi/client/v3/rooms/${encodeURIComponent(roomId)}/messages?dir=b&limit=${limit}`;
  const res = await httpRequest(url);
  if (!res.ok) return null;
  const data = await res.json();
  return data.chunk || [];
}

// 发送消息
async function sendRoomMessage(roomId, body) {
  const txnId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const url = `${config.homeserver}/_lobi/client/v3/rooms/${encodeURIComponent(roomId)}/send/m.room.message/${txnId}`;
  const res = await httpRequest(url, {
    method: 'PUT',
    body: JSON.stringify({ msgtype: 'm.text', body }),
  });
  return res.ok;
}

// 获取已处理消息
function getProcessedEvents() {
  try {
    const processedPath = path.join(process.env.HOME, '.openclaw', 'lobi-a2a-processed.json');
    if (!fs.existsSync(processedPath)) return new Set();
    const data = JSON.parse(fs.readFileSync(processedPath, 'utf8'));
    return new Set(data.events || []);
  } catch {
    return new Set();
  }
}

// 保存已处理消息
function saveProcessedEvent(eventId) {
  try {
    const processedPath = path.join(process.env.HOME, '.openclaw', 'lobi-a2a-processed.json');
    const processed = getProcessedEvents();
    processed.add(eventId);
    const events = Array.from(processed).slice(-200);
    fs.writeFileSync(processedPath, JSON.stringify({ events, updated: Date.now() }));
  } catch {
    // 忽略
  }
}

// 检查是否被 @
function isMentioned(text, myId) {
  if (!text) return false;
  const shortId = myId.split(':')[0];
  return text.includes(`@${myId}`) || (shortId && text.includes(`@${shortId}`));
}

// 解析上下文
function parseContext(text) {
  const match = text.match(/\{[^{}]*"type"\s*:\s*"a2a_init"[^{}]*\}/);
  if (!match) return null;
  try {
    return JSON.parse(match[0]);
  } catch {
    return null;
  }
}

// 处理消息
async function processMessage(roomId, event, processed) {
  if (processed.has(event.event_id)) return false;
  if (event.sender === config.userId) return false;
  if (event.type !== 'm.room.message') return false;

  const text = event.content?.body || '';
  const ctx = parseContext(text);

  if (!ctx || !isMentioned(text, config.userId)) return false;

  console.log(`[${new Date().toISOString()}] 发现需要回复的消息:`, event.event_id);

  // 检查轮数
  if (ctx.turns >= ctx.maxTurns) {
    const otherAgent = config.userId === ctx.from ? ctx.to : ctx.from;
    const otherShort = otherAgent?.split(':')[0];
    await sendRoomMessage(roomId, `✅ A2A 会话已完成\n\n@${otherShort} 感谢参与！`);
    saveProcessedEvent(event.event_id);
    activeRooms.delete(roomId); // 结束对话
    console.log(`[${new Date().toISOString()}] 对话结束`);
    return true;
  }

  // 生成回复（简化版，不调用 LLM）
  const replies = [
    '这个角度很有意思，能不能详细说说？',
    '我同意你的观点，另外我想补充一点...',
    '这是个好问题，我的看法是...',
    '确实如此，那如果换个角度思考呢？',
    '非常有见地！那接下来的实现步骤是什么？',
  ];
  const reply = replies[Math.floor(Math.random() * replies.length)];

  const nextAgent = config.userId === ctx.from ? ctx.to : ctx.from;
  const nextShort = nextAgent?.split(':')[0];
  const newCtx = { ...ctx, turns: ctx.turns + 1 };

  const messageBody = `${reply}\n\n上下文: ${JSON.stringify(newCtx)}\n\n@${nextShort}`;
  const sent = await sendRoomMessage(roomId, messageBody);

  if (sent) {
    saveProcessedEvent(event.event_id);
    console.log(`[${new Date().toISOString()}] 已回复第 ${newCtx.turns} 轮`);
    return true;
  }

  return false;
}

// 轮询单个房间
async function pollRoom(roomId) {
  const messages = await getRoomMessages(roomId, 10);
  if (!messages) return;

  const processed = getProcessedEvents();

  // 从旧到新处理
  for (let i = messages.length - 1; i >= 0; i--) {
    await processMessage(roomId, messages[i], processed);
  }
}

// 发现新的 A2A 房间
async function discoverRooms() {
  // 这里可以实现房间发现逻辑
  // 比如读取某个文件，或者查询 joined_rooms API
  // 简化版：只轮询已知的活跃房间
}

// 主循环
async function main() {
  console.log(`[${new Date().toISOString()}] Lobi A2A Poller 启动`);
  console.log(`User ID: ${config.userId}`);

  // 可以从命令行参数传入房间 ID
  const roomId = process.argv[2];
  if (roomId) {
    activeRooms.set(roomId, { lastCheckTime: Date.now() });
    console.log(`开始轮询房间: ${roomId}`);
  } else {
    console.log('请提供房间 ID: node poller.js <roomId>');
    console.log('或者修改代码支持自动发现房间');
    process.exit(1);
  }

  // 轮询循环
  while (true) {
    for (const [roomId] of activeRooms) {
      try {
        await pollRoom(roomId);
      } catch (e) {
        console.error(`[${new Date().toISOString()}] 轮询房间失败:`, e.message);
      }
    }

    await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
  }
}

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n退出轮询');
  process.exit(0);
});

main().catch(console.error);
