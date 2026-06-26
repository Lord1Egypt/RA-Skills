// ws.mjs - WebSocket 实时推送 (v2.0)

import { WebSocketServer } from 'ws';
import { on, EVENTS } from '../events/event-bus.mjs';

let _wss = null;
const _clients = new Set();

export function startWebSocket(config) {
  const port = config?.api?.wsPort || 3457;

  _wss = new WebSocketServer({ port });

  _wss.on('connection', (ws) => {
    _clients.add(ws);
    console.log(`🔌 WebSocket 客户端连接 (当前: ${_clients.size})`);

    ws.on('close', () => {
      _clients.delete(ws);
      console.log(`🔌 WebSocket 客户端断开 (当前: ${_clients.size})`);
    });

    ws.on('message', (msg) => {
      try {
        const data = JSON.parse(msg.toString());
        if (data.type === 'ping') ws.send(JSON.stringify({ type: 'pong' }));
      } catch {}
    });

    // 发送欢迎消息
    ws.send(JSON.stringify({ type: 'connected', version: '2.0.0' }));
  });

  // 订阅所有事件并推送
  for (const event of Object.values(EVENTS)) {
    on(event, (data) => {
      broadcast({ type: event, data, timestamp: Date.now() });
    });
  }

  console.log(`✅ WebSocket 服务已启动: ws://localhost:${port}`);
  return _wss;
}

export function stopWebSocket() {
  if (_wss) {
    for (const client of _clients) client.close();
    _clients.clear();
    _wss.close();
    _wss = null;
    console.log('🛑 WebSocket 服务已停止');
  }
}

function broadcast(message) {
  const data = JSON.stringify(message);
  for (const client of _clients) {
    if (client.readyState === 1) { // OPEN
      try { client.send(data); } catch {}
    }
  }
}

export function getClientCount() {
  return _clients.size;
}