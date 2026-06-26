---
name: Memory Engine
slug: memory-engine
version: 2.0.0
description: OpenClaw 3.8+ 智能上下文管理与记忆系统插件
author: lizhelong0907
tags: [memory, context, openclaw]
---

# Memory Engine

OpenClaw 3.8+ 智能上下文管理与记忆系统插件。

## 功能

- 本地向量存储：基于 SQLite + ONNX 本地推理，无需联网
- 语义搜索：支持语义相似度匹配
- 自动知识提取：从对话中自动提取关键信息
- 记忆分类：支持多种记忆类型（fact/experience/lesson/preference/skill）
- 重要性评分：根据重要性自动过滤低价值记忆
- 去重：基于语义相似度自动去重

## 安装

```bash
npm install memory-engine
# 或从 GitHub 安装
npm install github:lizhelong0907/memory-engine
```

## 使用

### 通过 OpenClaw

插件提供以下工具：

- **memory_save** - 保存重要信息到记忆系统
- **memory_search** - 搜索记忆  
- **memory_list** - 列出所有记忆
- **memory_stats** - 获取记忆统计信息

### 编程使用

```javascript
const { createMemoryEngine } = require('memory-engine');

async function main() {
  const engine = await createMemoryEngine({
    dbPath: './data/memories.db'
  });

  // 保存记忆
  await engine.addMemory({
    content: '用户爱吃水煎饺',
    type: 'preference',
    importance: 0.8
  });

  // 搜索记忆
  const results = await engine.searchMemories('吃');
  console.log(results);

  await engine.shutdown();
}

main();
```

## 配置

详见 [CONFIG.md](./CONFIG.md)

## 数据库

- 默认路径：`~/.openclaw/memory/memories.db`
- 使用 SQLite 存储

## 模型

内置模型：`models/all-MiniLM-L6-v2.onnx`

- 维度：384
- 大小：~90MB
- 无需额外下载

## 许可证

MIT
