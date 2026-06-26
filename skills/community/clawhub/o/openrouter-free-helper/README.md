# OpenRouter Free Model Monitor

<div align="center">

**监控 OpenRouter 免费模型的到期通知和新模型发现**

*Monitor OpenRouter free models for expiration notices and new model discoveries*

[![ClawHub](https://img.shields.io/badge/ClawHub-openrouter--free--helper-blue)](https://clawhub.ai/skills/openrouter-free-helper)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

</div>

---

## 📖 简介 | Introduction

**中文**：  
OpenRouter Free Model Monitor 是一个自动化工具，用于监控 OpenRouter 平台上的免费模型。它会自动检测两类关键信息：

1. **到期通知** - 识别模型的 "Going away [日期]" 警告，提前提醒用户
2. **新模型发现** - 自动发现新加入的免费模型并推送通知

该工具设计为 OpenClaw 技能，支持每日自动检查并通过飞书推送通知。

**English**:  
OpenRouter Free Model Monitor is an automated tool for monitoring free models on the OpenRouter platform. It automatically detects two types of critical information:

1. **Expiration Notices** - Identifies "Going away [date]" warnings and alerts users in advance
2. **New Model Discovery** - Automatically discovers newly added free models and sends notifications

This tool is designed as an OpenClaw skill, supporting daily automated checks with Feishu notifications.

---

## ✨ 特性 | Features

| 中文 | English |
|------|---------|
| 🚨 **分级提醒** - 紧急 (≤1 天) / 警告 (≤3 天) / 预告 (>3 天) | 🚨 **Tiered Alerts** - Urgent (≤1 day) / Warning (≤3 days) / Notice (>3 days) |
| 🔕 **智能去重** - 仅首次发现、日期变化或严重级别升级时提醒 | 🔕 **Smart Deduplication** - Alerts only on first discovery, date changes, or severity upgrades |
| 🌐 **诚实抓取链路** - requests → urllib | 🌐 **Honest Fetch Chain** - requests → urllib |
| 🔎 **双路发现** - bb-browser 优先，失败回退 OpenRouter API | 🔎 **Dual Discovery Path** - bb-browser first, OpenRouter API fallback |
| 🤖 **自动 Chrome** - 仅用于增强发现链路，不再依赖它完成全部抓取 | 🤖 **Auto Chrome** - Used only for enhanced discovery, no longer required for all fetching |
| 📅 **定时检查** - 支持 Cron 每日自动执行 | 📅 **Scheduled Checks** - Supports daily Cron automation |
| 📱 **飞书通知** - 无缝集成飞书消息推送 | 📱 **Feishu Integration** - Seamless Feishu message notifications |

---

## 🚀 快速开始 | Quick Start

### 前置要求 | Prerequisites

```bash
# 1. 安装 bb-browser (可选 | Optional, for enhanced discovery)
brew install bb-browser
# 或 | Or: npm install -g bb-browser

# 2. Python 依赖 | Python Dependencies
pip3 install requests

# 3. Chrome 调试模式 | Chrome Debug Mode
# 仅当你想启用 bb-browser 增强发现时需要。
# Only needed when you want bb-browser based enhanced discovery.
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222
```

### 安装方式 | Installation

**方式 1: 使用 ClawHub (推荐) | Method 1: Via ClawHub (Recommended)**
```bash
clawhub install openrouter-free-helper
```

**方式 2: Git 克隆 | Method 2: Git Clone**
```bash
git clone https://github.com/Suidge/openrouter-free-helper.git \
  ~/.openclaw/workspace/skills/openrouter-free-helper
```

### 添加 Cron 自动检查 | Add a Scheduled Cron Check

> ⚠️ **Cron 场景必须使用 `--no-notify`**，避免脚本内通知与 cron delivery 重复。

> 安装 skill **不会自动创建 Cron**。如果你需要每日自动运行，请手动添加。  
> Installing the skill does **not** auto-create a Cron job. Add it manually if you want scheduled checks.

示例：每日 08:00 检查并投递到飞书  
Example: run daily at 08:00 and deliver to Feishu

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

检查状态  
Check status

```bash
openclaw cron list
openclaw cron runs --jobId openrouter-monitor-001
```

### 配置 | Configuration

编辑配置文件 | Edit config file `config/config.json`:

```json
{
  "check_time": "08:00",
  "notify_channel": "feishu",
  "notify_target": "user:ou_xxxxxxxxxxxxxxxxxxxxx",
  "status_file": "~/.openclaw/workspace/skills/openrouter-free-helper/data/status.json",
  "openclaw_config": "~/.openclaw/openclaw.json"
}
```

| 参数 | Parameter | 说明 | Description |
|------|-----------|------|-------------|
| `check_time` | 检查时间 | 每日检查时间 (24 小时制) | Daily check time (24h format) |
| `notify_target` | 通知目标 | 飞书用户 ID (格式：`user:ou_xxx`) | Feishu user ID (format: `user:ou_xxx`) |

---

## 📖 使用指南 | Usage Guide

### 手动检查 | Manual Check

```bash
# 基础检查 (静默模式) | Basic check (silent mode)
python3 scripts/check-models.py

# 详细输出 | Verbose output
python3 scripts/check-models.py --verbose

# 模拟运行 (不发送通知) | Dry run (no notifications)
python3 scripts/check-models.py --verbose --dry-run

# Cron / agent-run 场景：禁止脚本自行发通知，交给上层 delivery
# Cron / agent-run mode: suppress script-side notifications and let outer delivery send once
python3 scripts/check-models.py --no-notify
```

> ⚠️ **Cron 场景必须使用 `--no-notify`**，否则脚本内通知与 cron delivery 可能重复发送。

### 使用 bb-browser 适配器 | Using bb-browser Adapters

```bash
# 获取所有免费模型 | Get all free models
bb-browser site openrouter/free-models --json --openclaw

# 查询特定模型到期信息 | Check specific model expiry
bb-browser site openrouter/model-expiry google/gemma-4-26b-a4b-it:free --json --openclaw
```

### 查看状态文件 | View Status File

```bash
cat data/status.json
```

**示例输出 | Example Output**:
```json
{
  "last_check": "2026-04-11T08:26:03.179157+08:00",
  "known_models": ["openrouter/google/gemma-4-26b-a4b-it:free"],
  "expiring_soon": [],
  "fetch_errors": []
}
```

---

## 🔔 通知规则 | Notification Rules

### 到期提醒分级 | Expiration Alert Tiers

| 级别 | Level | 条件 | Condition | 行为 | Action |
|------|-------|------|-----------|------|--------|
| 🚨 | 紧急 | ≤1 天 | ≤1 day | 立即推送 | Send immediately |
| ⚠️ | 警告 | ≤3 天 | ≤3 days | 推送提醒 | Send reminder |
| 📅 | 预告 | >3 天 | >3 days | 仅首次 | First discovery only |

### 静默规则 | Silent Mode Rules

以下情况**不发送通知** | **No notification** in these cases:
- 无新模型发现 | No new models discovered
- 到期通知无变化 (且不在紧急/警告级别) | No expiration changes (and not urgent/warning level)
- 抓取失败 (避免误报) | Fetch failed (avoid false positives)

---

## 🛠️ 故障排查 | Troubleshooting

### Chrome 调试模式问题 | Chrome Debug Mode Issues

**症状 | Symptom**: `bb-browser` 报错 "Chrome not connected"

**解决方案 | Solution**:
```bash
# 1. 检查 Chrome 是否运行 | Check if Chrome is running
ps aux | grep "remote-debugging-port=9222"

# 2. 手动启动 Chrome 调试模式 | Manually start Chrome debug mode
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222

# 3. 验证端口 | Verify port
curl http://127.0.0.1:9222/json/version
```

### Python 依赖缺失 | Missing Python Dependencies

**症状 | Symptom**: `ModuleNotFoundError: No module named 'requests'`

**解决方案 | Solution**:
```bash
pip3 install requests beautifulsoup4
```

### bb-browser 适配器问题 | bb-browser Adapter Issues

**症状 | Symptom**: 返回空列表 | Returns empty list

**检查 | Check**:
```bash
ls -la ~/.bb-browser/sites/openrouter/
bb-browser site openrouter/free-models --json --openclaw
```

---

## 📁 项目结构 | Project Structure

```
openrouter-free-helper/
├── README.md                    # 项目说明 | Project documentation
├── SKILL.md                     # OpenClaw 技能文档 | OpenClaw skill doc
├── package.json                 # 项目元数据 | Project metadata
├── config/
│   └── config.json              # 配置文件 | Configuration file
├── data/
│   └── status.json              # 状态文件 (自动生成) | Status file (auto-generated)
├── scripts/
│   ├── check-models.py          # 主检查脚本 | Main check script
│   └── fetch_page.py            # 网页抓取模块 | Web scraping helper
└── references/
    ├── cron-task.md             # Cron 任务说明 | Cron task instructions
    └── openrouter-structure.md  # OpenRouter 结构分析 | OpenRouter structure analysis
```

---

## 🔧 高级配置 | Advanced Configuration

### 修改检查频率 | Modify Check Frequency

编辑 Cron 配置 | Edit Cron config:
```bash
openclaw cron edit
```

将 `0 8 * * *` 改为其他时间 (如每小时检查：`0 * * * *`)  
Change `0 8 * * *` to other time (e.g., hourly: `0 * * * *`)

### 添加更多监控模型 | Add More Monitored Models

编辑 `~/.openclaw/openclaw.json`，在 `agents.defaults.models` 或 `agents[].model` 中添加 `:free` 后缀的模型 ID：

Edit `~/.openclaw/openclaw.json`, add `:free` suffixed model IDs in `agents.defaults.models` or `agents[].model`:

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
The script will automatically identify and monitor these models' expiration status.

---

## 📊 技术实现 | Technical Implementation

### 页面抓取链路 | Page Fetch Chain

1. **Layer 1**: `requests` (首选 | preferred)
2. **Layer 2**: `urllib` (标准库兜底 | stdlib fallback)

本地 Python 脚本不再伪装调用 OpenClaw 工具。  
The local Python script no longer pretends to call OpenClaw tools via subprocess shims.

### 新模型发现链路 | New Model Discovery Path

1. 优先使用 `bb-browser site openrouter/free-models --json --openclaw`  
   First try `bb-browser site openrouter/free-models --json --openclaw`
2. 若失败，回退 OpenRouter 内部 API  
   If that fails, fall back to OpenRouter internal API

- **端点 | Endpoint**: `https://openrouter.ai/api/frontend/models`
- **无需认证 | No auth required**

### 智能 Chrome 管理 | Smart Chrome Management

- ✅ 自动检测 Chrome 调试模式状态 | Auto-detect Chrome debug mode status
- ✅ 端口探活验证 | Port probing verification
- ✅ 独立 profile 避免冲突 | Isolated profile to avoid conflicts
- ✅ 仅服务于增强发现链路 | Used only for enhanced discovery

---

## 📝 更新日志 | Changelog

### v1.0.9 (2026-04-16)
- 🔄 Switch discovery order: API-first, bb-browser fallback (more stable, no Chrome dependency for primary path)

### v1.0.8 (2026-04-16)
- 🔔 Improve summary output to include specific model names and expiration details
- 🔕 Harder cron prompt to forbid any output after async exec completion (not just duplicate summary)
- 📋 Add `--verbose` to cron command so agent can see detailed discovery info

### v1.0.7 (2026-04-15)
- 🧭 Add lightweight free-page probing for configured `openrouter/*` models that do not use the `:free` suffix
- 🔕 Harden cron prompt to force `--no-notify` and discourage duplicate relay after async exec completion
- 🩹 Keep the detection strategy intentionally lightweight, avoiding full pricing-system complexity

### v1.0.5 (2026-04-14)
- 🔕 Add `--no-notify` mode so cron runs do not send direct Feishu notifications from the script
- 🧹 Update cron instructions to require a single final summary only, with no intermediate delivery wording
- 🔐 Remove user-specific default notification target from published skill content

### v1.0.4 (2026-04-11)
- 📝 Clarify that installing the skill does not auto-create a Cron job
- ➕ Add explicit `openclaw cron add` setup guidance to README and SKILL.md
- 🔗 Point scheduled runs to `references/cron-task.md`

### v1.0.3 (2026-04-11)
- 🔧 Fix configured free-model lookup to read `agents.defaults.models`
- 🛡 Add safer JSON/status loading and preserve known model state on partial failures
- 🔕 Tighten expiration dedup logic to avoid repeated daily warning spam
- 🌐 Replace misleading multi-tool fetch shim with an honest `requests -> urllib` fallback chain
- 📝 Sync README and SKILL docs with actual runtime behavior
- ➕ Add `references/cron-task.md` for cron-safe task guidance

### v1.0.2 (2026-04-10)
- 🌐 Add GitHub repository
- 📝 Update repository URL in package.json

### v1.0.1 (2026-04-10)
- 📝 Fix installation instructions in SKILL.md
- ➕ Add homepage link to ClawHub

### v1.0.0 (2026-04-10)
- 🎉 Initial release
- ✅ Expiration notice detection
- ✅ New model discovery
- ✅ Tiered alert system
- ✅ Smart Chrome management
- ✅ Multi-layer fallback mechanism

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！  
Issues and Pull Requests are welcome!

**问题反馈 | Bug Reports**: https://github.com/Suidge/openrouter-free-helper/issues

---

## 📄 许可证 | License

MIT License

---

<div align="center">

**Made with ❤️ by Silvermoon**

[⬆️ 返回顶部 | Back to Top](#openrouter-free-model-monitor)

</div>
