#!/usr/bin/env node
// start-api.mjs - 启动 API 服务（用于面板）

import { initDatabase, migrateFromJSON } from '../src/db/database.mjs';
import { initTokenizer } from '../src/search/tokenizer.mjs';
import { initEmbedder } from '../src/search/embedder.mjs';
import { startServer } from '../src/api/server.mjs';
import { startWebSocket } from '../src/api/ws.mjs';
import { loadConfig } from '../src/db/config-loader.mjs';

const config = loadConfig();
config.api = { enabled: true, port: 3456, wsEnabled: true, wsPort: 3457 };

await initDatabase(config);
migrateFromJSON(config);
await initTokenizer(config);
await initEmbedder(config);

startServer(config);
try { startWebSocket(config); } catch (e) { console.warn('WebSocket:', e.message); }

console.log('\n📊 统计面板: http://localhost:3456');
console.log('🔌 WebSocket: ws://localhost:3457');
console.log('按 Ctrl+C 停止');