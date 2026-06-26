// index.mjs - 主入口 (v2.0)

import { loadConfig } from './db/config-loader.mjs';
import { initDatabase, migrateFromJSON } from './db/database.mjs';
import { initTokenizer } from './search/tokenizer.mjs';
import { initEmbedder } from './search/embedder.mjs';
import { startScheduler, stopScheduler } from './dream/scheduler.mjs';
import { startServer, stopServer } from './api/server.mjs';
import { startWebSocket, stopWebSocket } from './api/ws.mjs';

const config = loadConfig();

export async function init(customConfig) {
  Object.assign(config, customConfig || {});

  console.log('🚀 layered-memory-sys v2.0 初始化...');

  // 1. 数据库
  await initDatabase(config);
  migrateFromJSON(config);

  // 2. 分词器
  await initTokenizer(config);

  // 3. Embedding
  await initEmbedder(config);

  // 4. 调度器
  if (config.scheduler?.enabled !== false) {
    startScheduler(config);
  }

  // 5. API 服务（可选）
  if (config.api?.enabled) {
    startServer(config);
  }

  if (config.api?.wsEnabled) {
    try {
      startWebSocket(config);
    } catch (e) {
      console.warn('WebSocket 启动失败（ws 模块未安装）:', e.message);
    }
  }

  console.log('✅ layered-memory-sys v2.0 就绪');
  return { config };
}

export async function shutdown() {
  stopScheduler();
  stopServer();
  stopWebSocket();
  console.log('🛑 layered-memory-sys v2.0 已关闭');
}

// CLI 模式
if (process.argv[1] && process.argv[1].endsWith('index.mjs')) {
  const cmd = process.argv[2];

  switch (cmd) {
    case 'init':
      init().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
      break;

    case 'test':
      import('../scripts/test-v2.mjs').then(() => process.exit(0));
      break;

    case 'migrate':
      initDatabase(config).then(() => {
        migrateFromJSON(config);
        process.exit(0);
      }).catch(e => { console.error(e); process.exit(1); });
      break;

    default:
      console.log('layered-memory-sys v2.0');
      console.log('用法: node index.mjs <init|test|migrate>');
      console.log('  init    - 初始化并启动所有服务');
      console.log('  test    - 运行测试');
      console.log('  migrate - 从 JSON 迁移到 SQLite');
  }
}