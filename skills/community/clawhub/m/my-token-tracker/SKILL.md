---
name: token-tracker
version: 1.0.0
description: "监控 OpenAI/其他模型 Token 消耗，支持每日/每周账单推送和超额警报"
metadata:
  openclaw:
    emoji: 💰
    events: ["command:status"]
---

# TokenTracker

监控 OpenAI/其他模型 Token 消耗，支持主动查询、每日/每周账单推送和超额警报。

## 功能

- **主动查询**：随时询问当前 token 消耗情况
- **每日账单**：每天 23:59 自动推送当日消耗汇总
- **每周账单**：每周日 23:59 自动推送本周消耗汇总
- **超额警报**：每小时检查是否超过阈值，触发警报
- **自动记录 Hook**：可选安装 Hook，自动记录每次会话的 token 用量

## 安装

### 1. 基础安装

```bash
# 复制 skill 到 skills 目录
cp -r token-tracker ~/.openclaw/workspace/skills/
```

### 2. 安装 Hook（可选）

TokenTracker 包含一个 Hook，可以在每次会话压缩后自动记录 token 用量：

```bash
# 方法一：复制 hook 到 managed hooks 目录
mkdir -p ~/.openclaw/hooks/token-logger
cp hooks/token-logger/HOOK.md ~/.openclaw/hooks/token-logger/
cp hooks/token-logger/handler.js ~/.openclaw/hooks/token-logger/

# 方法二：使用 openclaw hooks install（如果支持）
openclaw hooks install ./hooks/token-logger
```

#### 启用 Hook

```bash
# 列出所有 hook
openclaw hooks list

# 启用 token-logger hook
openclaw hooks enable token-logger

# 检查状态
openclaw hooks check
```

#### 重启 Gateway

修改 hook 配置后需要重启 Gateway 使其生效。

### 3. 配置定时任务（可选）

```bash
# 手动添加定时任务，或使用 cron-config.json
# 详见下文「定时任务」部分
```

## 使用方法

### 主动查询

```
查询今日 token 消耗
我的 token 用量是多少
```

### 手动命令（开发/测试用）

```bash
# 查询今日消耗
python token_tracker.py today

# 查询本周消耗
python token_tracker.py week

# 查询阈值
python token_tracker.py threshold

# 检查是否超标
python token_tracker.py check-threshold

# 生成完整报告
python token_tracker.py report today
python token_tracker.py report week

# 手动添加记录
python token_tracker.py add --session-id "agent:main:main" --model "minimax-portal/MiniMax-M2.5" --token-in 73000 --token-out 88000
```

## 配置

首次运行会自动创建 `config.json`，可手动编辑：

```json
{
  "daily_threshold": 10.0,
  "weekly_threshold": 50.0,
  "alert_percent": 0.95,
  "time_zone": "Asia/Shanghai",
  "models_to_track": ["minimax-portal/MiniMax-M2.5", "gpt-4o", "gpt-3.5-turbo"],
  "model_price_list": {
    "minimax-portal/MiniMax-M2.5": {"token_in_price": 0.01, "token_out_price": 0.01},
    "gpt-4o": {"token_in_price": 0.03, "token_out_price": 0.06},
    "gpt-4o-mini": {"token_in_price": 0.015, "token_out_price": 0.03},
    "gpt-3.5-turbo": {"token_in_price": 0.002, "token_out_price": 0.004}
  },
  "default_price": {"token_in": 0.01, "token_out": 0.01}
}
```

## Hook 说明

### token-logger Hook

监听 `session:compact:after` 事件，自动记录 token 用量。

**工作原理：**
1. 当会话压缩完成后触发
2. 读取 session status 获取 token 使用情况
3. 调用 token_tracker.py add 记录到数据库

**安装步骤：**

```bash
# 1. 创建 hook 目录
mkdir -p ~/.openclaw/hooks/token-logger

# 2. 复制文件
cp hooks/token-logger/HOOK.md ~/.openclaw/hooks/token-logger/
cp hooks/token-logger/handler.js ~/.openclaw/hooks/token-logger/

# 3. 启用 hook
openclaw hooks enable token-logger

# 4. 重启 Gateway
openclaw gateway restart
```

**验证安装：**

```bash
# 查看 hook 状态
openclaw hooks list | grep token-logger

# 查看日志
tail -f ~/.openclaw/gateway.log | grep token-logger
```

## 数据结构

### UsageRecord

每次 session status 更新记录：

```json
{
  "timestamp": "2026-03-19T11:59:00+08:00",
  "session_id": "agent:main:main",
  "model": "minimax-portal/MiniMax-M2.5",
  "token_in": 73000,
  "token_out": 88000,
  "cost": 0.0
}
```

## 定时任务

| 任务 | 时间 | 功能 |
|------|------|------|
| token-daily-report | 每日 23:59 | 推送今日账单 |
| token-weekly-report | 每周日 23:59 | 推送本周账单 |
| token-hourly-alert | 每小时 | 检查阈值警报 |

### 手动添加定时任务

```bash
# 添加每日报告任务
openclaw cron add --name token-daily-report \
  --schedule "0 59 23 * * *" \
  --message "运行 python token_tracker.py report today" \
  --channel telegram

# 添加每周报告任务
openclaw cron add --name token-weekly-report \
  --schedule "0 59 23 * * 0" \
  --message "运行 python token_tracker.py report week" \
  --channel telegram
```

或参考 `cron-config.json` 手动配置。

## 消息模板

### 主动查询回复

```
📊 今日 Token 消耗：
minimax-portal/MiniMax-M2.5 → 73k in / 88k out
总计：$0.00
```

### 每日/每周账单

```
📊 今日/本周 Token 账单：
minimax-portal/MiniMax-M2.5 → 73k in / 88k out, $0.00
总计：$0.00
```

### 阈值警报

```
⚠️ 警告：Token 消耗即将超标
minimax-portal/MiniMax-M2.5 → $9.50 / $10.00
总计：$9.50 / $10.00
```

## 技术细节

- 数据存储：JSON 文件 (`usage_records.json`)
- 成本计算：token_in/1M * price + token_out/1M * price
- 自动识别模型并匹配价格
- 支持自定义模型价格
- Hook 使用 JavaScript，直接读取 OpenClaw session 状态

## Post Install 安装脚本

如需自动化安装，可以使用以下脚本：

```bash
#!/bin/bash
# post-install.sh

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$HOME/.openclaw/hooks"

echo "Installing TokenTracker Hook..."

# 创建 hook 目录
mkdir -p "$HOOKS_DIR/token-logger"

# 复制 hook 文件
cp "$SKILL_DIR/hooks/token-logger/HOOK.md" "$HOOKS_DIR/token-logger/"
cp "$SKILL_DIR/hooks/token-logger/handler.js" "$HOOKS_DIR/token-logger/"

echo "Hook files copied to $HOOKS_DIR/token-logger"

# 启用 hook（如果 openclaw 可用）
if command -v openclaw &> /dev/null; then
    openclaw hooks enable token-logger 2>/dev/null || echo "Please enable hook manually: openclaw hooks enable token-logger"
    echo "Hook enabled!"
else
    echo "OpenClaw CLI not found. Please enable hook manually: openclaw hooks enable token-logger"
fi

echo "Installation complete!"
```
