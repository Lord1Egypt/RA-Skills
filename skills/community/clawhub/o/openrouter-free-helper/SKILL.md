---
name: openrouter-free-helper
description: 监控 OpenRouter 免费模型的到期通知和新模型发现，自动每日检查并推送飞书通知
requires:
  bins: [python3, bb-browser]
  python: [requests, beautifulsoup4]
allowed-tools: Bash, exec
---

# OpenRouter Free Helper

监控 OpenRouter 免费模型的两类关键信息：
1. **到期通知** - 识别 "Going away [日期]" 警告，提前提醒
2. **新模型发现** - 自动发现新加入的免费模型

## 🚀 快速开始

### 前置依赖

**1. 安装 bb-browser**（可选，用于增强发现链路）

```bash
# 使用 Homebrew 安装
brew install bb-browser

# 或使用 npm 全局安装
npm install -g bb-browser
```

**2. 配置 Chrome 调试模式**

bb-browser 需要 Chrome 在调试模式下运行（端口 9222）：

```bash
# 手动启动 Chrome 调试模式
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check
```

**或者**：脚本会自动检测并启动 Chrome 调试模式（首次启动可能需要 10-15 秒）

**3. Python 依赖**

```bash
pip3 install requests beautifulsoup4
```

### 安装技能

```bash
# 使用 ClawHub 安装
clawhub install openrouter-free-helper
```

### 配置

编辑配置文件 `~/.openclaw/workspace/skills/openrouter-free-helper/config/config.json`：

```json
{
  "check_time": "08:00",
  "notify_channel": "feishu",
  "notify_target": "user:ou_xxxxxxxxxxxxxxxxxxxxx",
  "status_file": "~/.openclaw/workspace/skills/openrouter-free-helper/data/status.json",
  "openclaw_config": "~/.openclaw/openclaw.json"
}
```

**参数说明**：
- `notify_target`: 飞书用户 ID（格式：`user:ou_xxx`）
- `check_time`: 每日检查时间（24 小时制）
- `status_file`: 状态文件路径（自动创建）

### 启用自动化

> ⚠️ **Cron 场景必须使用 `--no-notify`**，禁止脚本自行发送通知，统一交给 cron delivery 输出一次最终结果。

技能安装后**不会自动创建 Cron 任务**。如需每日自动检查，请手动添加一条 Cron，并让它读取固定任务说明文件。

示例：每日 08:00 执行
```bash
openclaw cron add --job '{
  "id": "openrouter-monitor-001",
  "name": "OpenRouter Free Model Monitor",
  "schedule": {"kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Read /Users/neoshi/.openclaw/workspace/skills/openrouter-free-helper/references/cron-task.md and follow it exactly. Keep the run self-contained in an isolated session rooted at /Users/neoshi/.openclaw/workspace. Return only a brief plain-text summary suitable for Feishu delivery.",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "user:ou_xxxxxxxxxxxxxxxxxxxxx"
  }
}'
```

检查 Cron 状态：
```bash
openclaw cron list
openclaw cron runs --jobId openrouter-monitor-001
```

---

## 📖 使用指南

### 手动检查

```bash
# 基础检查（静默模式，仅在变化时通知）
python3 ~/.openclaw/workspace/skills/openrouter-free-helper/scripts/check-models.py

# 详细输出（查看执行过程）
python3 ~/.openclaw/workspace/skills/openrouter-free-helper/scripts/check-models.py --verbose

# 模拟运行（不发送通知）
python3 ~/.openclaw/workspace/skills/openrouter-free-helper/scripts/check-models.py --verbose --dry-run

# Cron / agent-run 场景：禁止脚本自行发通知，交给上层 delivery
python3 ~/.openclaw/workspace/skills/openrouter-free-helper/scripts/check-models.py --no-notify
```

> ⚠️ **Cron 场景必须使用 `--no-notify`**，否则脚本内通知与 cron delivery 可能重复发送。

### 查询 bb-browser 适配器

```bash
# 获取所有免费模型列表
bb-browser site openrouter/free-models --json --openclaw

# 查询特定模型的到期信息
bb-browser site openrouter/model-expiry google/gemma-4-26b-a4b-it:free --json --openclaw
```

### 查看状态文件

```bash
cat ~/.openclaw/workspace/skills/openrouter-free-helper/data/status.json
```

**状态文件结构**：
```json
{
  "last_check": "2026-04-10T21:59:06.858640",
  "known_models": ["openrouter/google/gemma-4-26b-a4b-it:free", ...],
  "expiring_soon": [
    {
      "model": "arcee-ai/trinity-large-preview",
      "going_away_date": "2026-04-22",
      "days_left": 11,
      "url": "https://openrouter.ai/arcee-ai/trinity-large-preview"
    }
  ]
}
```

---

## 🔔 通知规则

### 到期提醒（分级推送）

| 级别 | 条件 | 行为 |
|------|------|------|
| 🚨 **紧急** | ≤1 天到期 | 立即推送 |
| ⚠️ **警告** | ≤3 天到期 | 推送提醒 |
| 📅 **预告** | >3 天到期 | 仅首次发现时推送 |

**去重机制**：
- 同一模型的到期通知，只在首次发现或日期变化时推送
- 避免每天重复发送相同提醒

### 新模型发现

- 仅在首次发现时推送
- 每次最多显示 10 个新模型
- 自动过滤已配置的模型

### 静默规则

以下情况**不发送通知**：
- 无新模型发现
- 到期通知无变化（且不在紧急/警告级别）
- 抓取失败（避免误报）

---

## 🛠️ 故障排查

### Chrome 调试模式问题

**症状**：`bb-browser` 报错 "Chrome not connected"

**解决**：
```bash
# 1. 检查 Chrome 是否运行
ps aux | grep "remote-debugging-port=9222"

# 2. 手动启动 Chrome 调试模式
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222

# 3. 验证端口是否可访问
curl http://127.0.0.1:9222/json/version
```

### bb-browser 适配器问题

**症状**：`bb-browser site openrouter/free-models` 返回空列表

**检查**：
```bash
# 查看适配器是否存在
ls -la ~/.bb-browser/sites/openrouter/

# 测试适配器
bb-browser site openrouter/free-models --json --openclaw
```

**修复**：重新安装技能或手动创建适配器（见 `references/openrouter-structure.md`）

### Python 依赖缺失

**症状**：`ModuleNotFoundError: No module named 'requests'`

**解决**：
```bash
pip3 install requests beautifulsoup4
```

---

## 📁 文件结构

```
~/.openclaw/workspace/skills/openrouter-free-helper/
├── SKILL.md                      # 技能文档
├── config/
│   └── config.json               # 配置文件
├── data/
│   └── status.json               # 状态文件（自动生成）
├── scripts/
│   ├── check-models.py           # 主检查脚本
│   └── fetch_page.py             # 网页抓取模块
├── references/
│   ├── cron-task.md              # Cron 任务说明
│   └── openrouter-structure.md   # OpenRouter 结构分析
└── adapters/
    └── openrouter/               # bb-browser 适配器（在 ~/.bb-browser/sites/）
```

---

## 🔧 高级配置

### 修改检查频率

编辑 Cron 配置：
```bash
openclaw cron edit
```

将 `0 8 * * *` 改为其他时间（如每小时检查：`0 * * * *`）

### 添加更多监控模型

编辑 `~/.openclaw/openclaw.json`，在 `agents.defaults.models` 或 `agents[].model` 中添加 `:free` 后缀的模型 ID：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "openrouter/google/gemma-4-26b-a4b-it:free": {},
        "openrouter/google/gemma-4-31b-it:free": {}
      }
    }
  }
}
```

脚本会自动识别并监控这些模型的到期状态。

---

## 📊 技术实现

### 页面抓取策略

1. **Layer 1**: `requests`（优先，稳定且快速）
2. **Layer 2**: `urllib`（标准库兜底）

说明：本地 Python 脚本不再伪装调用 OpenClaw 工具。工具型抓取属于 agent 运行期能力，不应在脚本里用 subprocess 硬模拟。

### 新模型发现链路

1. 优先尝试 `bb-browser site openrouter/free-models --json --openclaw`
2. 若失败，则回退到 OpenRouter 内部 API：
   - 端点：`https://openrouter.ai/api/frontend/models`
   - 无需认证，可直接提取免费模型列表

### Chrome 调试模式管理

- 自动检测 Chrome 调试端口是否可用（`http://127.0.0.1:9222/json/version`）
- 若不可用，可启动独立 profile：`/tmp/openclaw-chrome-debug`
- 设计目标是不干扰用户现有 Chrome 会话

---

## 🌟 特性亮点

- ✅ **零打扰**：无变化时静默执行
- ✅ **分级提醒**：紧急/警告/预告三级通知
- ✅ **去重机制**：避免重复推送相同信息
- ✅ **自动修复**：Chrome 未运行时自动启动
- ✅ **多层兜底**：三层抓取 + API fallback
- ✅ **时区感知**：所有时间计算基于 Asia/Shanghai

---

## 📝 更新日志

### v1.0.10 (2026-05-09)
- 修正新模型发现链路：使用 `endpoint.model_variant_slug` 替代顶层 `slug`，确保返回带 `:free` 后缀的完整端点 ID

### v1.0.9 (2026-04-16)
- 调整发现顺序：API 优先，bb-browser 作为 fallback（更稳定，主路径不依赖 Chrome）

### v1.0.8 (2026-04-16)
- 摘要输出现在包含具体的模型名称和到期详情（不再只说数量）
- 收紧 cron prompt，禁止 async exec completion 后输出任何消息（不只是禁止重复摘要）
- 给 cron 命令加 `--verbose` 让模型能看到详细信息并整合到最终摘要

### v1.0.7 (2026-04-15)
- 为已配置但未带 `:free` 后缀的 `openrouter/*` 模型增加轻量页面探测，补抓“实际免费但未显式标 free”的模型
- 收紧 cron prompt，强制 `--no-notify` 并避免 async exec completion 后重复转述
- 保持检测策略轻量，不引入完整 pricing 系统复杂度

### v1.0.5 (2026-04-14)
- 新增 `--no-notify` 模式，供 cron 场景避免脚本内直接发通知
- 收紧 cron-task 规则，禁止中间态与“已推送”类措辞
- 脱敏发布内容，移除用户特定默认通知目标

### v1.0.1 (2026-04-11)
- 修正配置模型读取路径
- 修正状态文件与 JSON 读取容错
- 收紧到期提醒去重策略，避免重复提醒
- 精简抓取链路，改为 requests + urllib 的诚实 fallback
- 新增 cron-task.md 作为 cron 固定任务说明

### v1.0.0 (2026-04-10)
- 初始版本发布
- 支持到期通知检测
- 支持新模型发现
- 分级提醒机制
- 智能 Chrome 管理
- 多层 fallback 机制

---

## 🤝 贡献

问题反馈或功能建议，欢迎通过 GitHub Issues 提交。

---

**最后更新**: 2026-04-10  
**维护者**: Silvermoon
