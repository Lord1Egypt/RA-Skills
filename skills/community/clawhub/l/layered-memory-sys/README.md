# layered-memory-sys 技能使用指南

## 安装

```bash
cd ~/.openclaw/workspace/skills
git clone <repo-url> layered-memory-sys
cd layered-memory-sys
npm install
```

## 快速开始

### 初始化
```bash
node src/index.mjs init
```

### 测试
```bash
node scripts/test-v2.mjs
```

### 启动 API 服务
```bash
node scripts/start-api.mjs
# 面板地址: http://localhost:3456
# WebSocket: ws://localhost:3457
```

## 配置

创建 `~/.openclaw/workspace/memory/config.json`：

```json
{
  "embedding": {
    "mode": "auto",
    "localModel": "Xenova/paraphrase-multilingual-MiniLM-L12-v2",
    "apiProvider": "doubao",
    "apiKey": ""
  },
  "tokenizer": {
    "mode": "auto"
  },
  "scheduler": {
    "enabled": true,
    "jobs": [
      { "id": "dream-cycle", "cron": "0 3 * * *" },
      { "id": "remind-check", "cron": "* * * * *" }
    ]
  },
  "api": {
    "enabled": false,
    "port": 3456,
    "wsEnabled": false,
    "wsPort": 3457
  }
}
```

## API 使用

### 搜索记忆
```bash
curl -X POST http://localhost:3456/api/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"记忆系统","limit":10}'
```

### 创建记忆
```bash
curl -X POST http://localhost:3456/api/memories \
  -H 'Content-Type: application/json' \
  -d '{"title":"测试","summary":"这是一条测试记忆","layer":"active","tags":["测试"]}'
```

### 触发梦境
```bash
curl -X POST http://localhost:3456/api/dream/run
```

## 心跳集成

在 HEARTBEAT.md 中添加：
```
调用路径: skills/layered-memory-sys/scripts/heartbeat-handler.mjs
```

## 环境变量

| 变量 | 说明 |
|------|------|
| MEMORY_DIR | 记忆数据目录 |
| SESSION_DIR | Session 日志目录 |
| DOUBAO_API_KEY | 豆包 API Key |
| DASHSCOPE_API_KEY | 通义 API Key |

## 依赖说明

### 必需
- sql.js — SQLite WASM
- ws — WebSocket

### 可选（推荐）
- nodejieba — 中文分词
- @xenova/transformers — 本地 Embedding 模型

## 事件订阅

其他技能可订阅以下事件：
```javascript
import { on, EVENTS } from 'layered-memory-sys/src/events/event-bus.mjs';

on(EVENTS.MEMORY_CREATED, (mem) => { ... });
on(EVENTS.DREAM_COMPLETED, (stats) => { ... });
on(EVENTS.REMINDER_TRIGGERED, (reminder) => { ... });
```

## v2.0 特性

- ✅ SQLite 存储（并发安全）
- ✅ jieba 中文分词
- ✅ TF-IDF 搜索（Embedding fallback）
- ✅ 时间衰减召回
- ✅ Cron 调度器
- ✅ REST API
- ✅ WebSocket 实时推送
- ✅ 事件总线
- ✅ 来源追溯
- ✅ 自动 JSON 迁移

---

发布版本: 2.0.0
发布日期: 2026-05-06
