---
name: minimax-token
description: 检查 MiniMax API Token 剩余配额。支持定时检查并通过 Telegram 发送通知。适用于：查询 Token 余额、配置定时监控、设置余额不足提醒。
---

# MiniMax Token 检查工具

查询 MiniMax API 的 Token 剩余配额，支持定时检查和 Telegram 通知。

## 功能特性

- ✅ 查询 MiniMax API Token 剩余配额
- ✅ 支持定时自动检查（每小时）
- ✅ 通过 Telegram 发送通知
- ✅ 支持环境变量配置
- ✅ systemd 服务支持

## 依赖

```bash
# Python 依赖
pip3 install requests

# 系统依赖
# - curl (用于 API 请求)
# - python3
```

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `MINIMAX_API_KEY` | MiniMax API Key | 是 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 否 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 否 |
| `OPENCLAW_LOG_DIR` | 日志目录 (默认 ~/.openclaw/logs) | 否 |

## 使用方法

### 1. 配置环境变量

```bash
# 方式一: 环境变量
export MINIMAX_API_KEY="your_api_key"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 方式二: 运行参数
python3 minimax_token.py --check --api-key "your_api_key"
```

### 2. 单次检查

```bash
python3 minimax_token.py --check
```

### 3. 启动定时监控

```bash
python3 minimax_token.py --monitor
```

### 4. 安装为系统服务 (Linux)

```bash
# 复制 service 文件
cp minimax-token.service ~/.config/systemd/user/

# 启用服务
systemctl --user enable minimax-token
systemctl --user start minimax-token

# 查看日志
journalctl --user -u minimax-token -f
```

## 配置说明

所有敏感配置都通过环境变量读取，确保安全：
- API Key: `MINIMAX_API_KEY`
- Telegram Bot: `TELEGRAM_BOT_TOKEN`
- Chat ID: `TELEGRAM_CHAT_ID`

## 输出示例

```
📊 MiniMax-M2.5 配额状态

• 剩余时间: 50小时 30分钟
• 本周期: 已用 150/1000 次
• 剩余: 850 次
```

## 文件结构

```
minimax-token/
├── SKILL.md
└── scripts/
    ├── minimax_token.py        # 主脚本
    └── minimax-token.service   # systemd 服务配置
```
