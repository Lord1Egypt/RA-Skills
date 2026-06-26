---
name: minimax-token-remains
description: 查询 MiniMax API Token 使用情况，支持小时级/周级用量监控，秒级完成。触发词：查 token、查看额度、剩余次数、token 余额。
emoji: 💰
openclaw:
  version: ">=2026.1"
---

# minimax-token-remains

查询 MiniMax 账号当前 API Token 使用情况，包括小时级请求次数剩余和周配额。

## 功能

- ✅ 查询当前小时请求次数（已用/剩余）
- ✅ 查询本周总配额（已用/剩余）
- ✅ 纯 exec 执行，不耗 LLM token
- ✅ 秒级返回，结构化输出

## 触发方式

直接说：
- "查一下 token 余额"
- "剩余多少次"
- "token 额度还剩多少"
- "查看 MiniMax 用量"

## 输出格式

```
【MiniMax Token 查询结果】

⏰ 本小时：98 / 600 次（剩余 502 次）
📅 本周：656 / 6000 次（剩余 5344 次）

💡 模型：MiniMax-M2.7（主用）
⏱️ 重置时间：本小时 / 本周日
```

如果失败：
```
❌ 查询失败：网络或 API 问题
```

## 工作原理

1. 从 auth-profiles.json 读取当前 minimax key
2. 调用 `https://www.minimaxi.com/v1/token_plan/remains`
3. 解析 JSON 输出，提取小时级/周级数据
4. 格式化后直接展示给用户

## 超时保护

单次 API 调用最多等待 10 秒，超时返回失败。