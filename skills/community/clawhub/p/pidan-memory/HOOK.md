---
name: pidan-memory
description: "自动向量记忆系统 - 每次对话后自动评估并存储重要信息"
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "events": ["message:received", "message:sent"],
      "requires": { "bins": ["python3"] },
    },
  }
---

# Pidan Memory Hook

基于 LanceDB + Ollama 的自动向量记忆系统。

## 功能

- 监听每条消息（用户发送和助手回复）
- 自动评估是否需要记住重要信息
- 存储到向量数据库，支持语义搜索

## 事件

- `message:received` - 用户发送消息时
- `message:sent` - 助手回复消息后

## 要求

- Python 3.9+
- Ollama 运行中（localhost:11434）
- LanceDB 已安装

## 工作原理

1. 接收消息事件
2. 提取用户 ID 和消息内容
3. 调用 Python 脚本进行自动评估
4. 如果匹配记忆规则，存入向量数据库
