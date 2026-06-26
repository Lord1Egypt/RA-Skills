---
name: token-logger
description: "自动记录每次会话的 Token 消耗到 TokenTracker"
metadata:
  openclaw:
    emoji: 💰
    events: ["session:compact:after"]
    requires:
      bins: ["node"]
---

# Token Logger Hook

自动在会话压缩后记录 Token 消耗到 TokenTracker 数据库。

## 功能

- 监听 `session:compact:after` 事件
- 获取当前 session 的 token 使用情况
- 调用 token_tracker.py 记录用量

## 工作原理

1. 当会话压缩完成后触发
2. 通过 OpenClaw API 获取 session status
3. 解析 token_in、token_out 和模型信息
4. 调用 token_tracker.py add 命令记录

## 安装

```bash
# 复制 hook 到 managed hooks 目录
cp -r hooks/token-logger ~/.openclaw/hooks/

# 启用 hook
openclaw hooks enable token-logger

# 重启 Gateway
```

## 配置

无需额外配置。hook 会自动读取 TokenTracker 的配置。

## 依赖

- Node.js
- Python 3.x
- TokenTracker skill 已安装
