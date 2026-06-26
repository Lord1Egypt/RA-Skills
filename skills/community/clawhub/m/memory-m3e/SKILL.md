# memory-m3e

语义记忆插件，使用 m3e-large embedding API + SQLite 存储。

## 特性

- ✅ 使用外部 m3e-large embedding API（1536维）
- ✅ SQLite 持久化存储
- ✅ 纯 JS 余弦相似度搜索（无原生依赖问题）
- ✅ 定时索引刷新（默认10分钟）
- ✅ 三个工具：memory_store, memory_recall, memory_forget

## 配置

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
            "baseUrl": "http://your-embedding-server",
            "model": "m3e-large"
          },
          "dbPath": "~/.openclaw/data/memory-m3e.db",
          "indexInterval": 600000
        }
      }
    }
  }
}
```

## 使用

```javascript
// 存储
memory_store({
  text: "Frappe API 开发经验",
  category: "fact",
  importance: 0.8
})

// 搜索
memory_recall({
  query: "Frappe 项目",
  limit: 5
})

// 删除
memory_forget({ memoryId: "uuid" })
memory_forget({ query: "要删除的内容" })
```

## 性能（实测，47条记忆）

- memory_store: avg **200ms**（embedding ~198ms + sqlite ~2ms）
- memory_recall: avg **91ms**（embedding ~83ms + 全表搜索 ~8ms）
- 索引刷新：每10分钟自动执行

---
作者：小女子 🥰
