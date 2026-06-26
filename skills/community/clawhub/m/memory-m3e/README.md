# memory-m3e

OpenClaw 语义记忆插件，使用外部 m3e-large embedding API 和 SQLite 本地存储。

## 特性

- ✅ 使用 m3e-large embedding API（1536维向量）
- ✅ SQLite 持久化存储
- ✅ 纯 JavaScript 余弦相似度搜索（无原生依赖）
- ✅ 定时索引刷新（默认10分钟）
- ✅ 三个工具：memory_store、memory_recall、memory_forget
- ✅ 自动捕获对话（autoCapture）
- ✅ 自动注入记忆（autoRecall）

## 性能

**实测数据（47条记忆）：**
- 写入：平均 200ms
- 召回：平均 91ms
- SQLite 操作：<2ms

详见：[安装使用指南](./SKILL.md)

## 快速开始

### 1. 安装

```bash
mkdir -p ~/.openclaw/extensions/memory-m3e
cd ~/.openclaw/extensions/memory-m3e
npm install
```

### 2. 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "plugins": {
    "slots": {
      "memory": "memory-m3e"
    },
    "entries": {
      "memory-m3e": {
        "enabled": true,
        "config": {
          "embedding": {
            "apiKey": "your-api-key",
            "baseUrl": "your-url",
            "model": "m3e-large"
          },
          "dbPath": "~/.openclaw/data/memory-m3e.db",
          "autoCapture": true,
          "autoRecall": true,
          "indexInterval": 600000
        }
      }
    }
  }
}
```

### 3. 重启

```bash
openclaw gateway restart
```

## 使用

### memory_store

```javascript
memory_store({
  text: "重要信息",
  category: "fact",  // preference | fact | decision | entity | other
  importance: 0.8    // 0-1
})
```

### memory_recall

```javascript
memory_recall({
  query: "查询关键词",
  limit: 5
})
```

### memory_forget

```javascript
memory_forget({ memoryId: "uuid" })
// 或
memory_forget({ query: "要删除的内容" })
```

## 依赖

- better-sqlite3: ^11.0.0
- @sinclair/typebox: ^0.32.0

## 许可

MIT
