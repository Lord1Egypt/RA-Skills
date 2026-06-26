---
name: jclaw-smart-web-monitor
description: "Smart web monitor with AI-powered matching. Unlike keyword/regex monitors, this skill uses the agent's own LLM reasoning to evaluate whether a web page matches your condition — enabling natural language monitoring like '是否有新的风控岗位？排除实习'. Supports keyword/regex/CSS/JSONPath for simple cases, and LLM for intelligent matching. Triggers on: monitor website, watch page, check for changes, web monitor, smart monitor, 监控网页, 网页变化检测, 职位监控. Requires: Python 3, openclaw cron."
---

# Smart Web Monitor (智能网页监控)

Watch any web page for changes — with **AI-powered understanding**. Instead of rigid keyword matching, describe what you're looking for in natural language and let the agent decide.

### Why "Smart"?

| 普通监控 | Smart Web Monitor |
|----------|-------------------|
| 关键词匹配：`risk manager` | 自然语言：`"是否有风控岗位？排除实习"` |
| 静态正则：`risk.{0,20}manager` | Agent 理解上下文语义 |
| 匹配即通知 | 匹配后 Agent 可以总结、分析、过滤 |
| 一次判断 | Agent 持续推理，理解页面结构变化 |

## Quick Start

### Create a Monitor

```bash
# Simple: keyword match
python3 scripts/monitor.py create \
  --name "hk-risk-jobs" \
  --url "https://careers.example.com/risk" \
  --match-type keyword \
  --match-value "risk manager,hong kong,compliance"

# Smart: LLM match (agent evaluates with natural language understanding)
python3 scripts/monitor.py create \
  --name "hk-fintech-news" \
  --url "https://36kr.com" \
  --match-type llm \
  --match-value "是否有香港金融科技、虚拟银行相关新闻？排除广告。"
```

### Run (keyword/regex/css/jsonpath)

```bash
python3 scripts/monitor.py run --event hk-risk-jobs
# → auto-matches, auto-pauses on match
```

### Fetch for LLM (extract text only)

```bash
python3 scripts/monitor.py fetch --event hk-fintech-news
# → outputs JSON with page text for LLM agent to evaluate
```

### After Match — Pause & Resume

```bash
python3 scripts/monitor.py resume --event xxx   # 继续
python3 scripts/monitor.py pause --event xxx    # 暂停
python3 scripts/monitor.py disable --event xxx  # 停用
python3 scripts/monitor.py enable --event xxx   # 启用
```

## Match Types

| Type | How It Works | Smart? | Example |
|---|---|---|---|
| `keyword` | Comma-separated keywords (case-insensitive) | ❌ | `risk manager,hong kong` |
| `regex` | Regular expression pattern | ❌ | `risk.{0,20}manager` |
| `css` | CSS selector — matches if elements exist | ❌ | `.job-listing .title` |
| `jsonpath` | JSONPath for API responses | ❌ | `$.data.jobs[*].title` |
| `llm` | 🤖 **Agent evaluates with LLM reasoning** | ✅ | `是否有风控岗位？排除实习` |

### 🤖 LLM Match (Smart Matching — 核心功能)

This is what makes the monitor "smart". Instead of rigid pattern matching, the agent **reads the page and thinks**.

How it works:
1. **`monitor.py fetch`** — fetches page, extracts clean text → outputs JSON
2. **Cron agent** — reads the text, evaluates using its own LLM reasoning
3. Agent decides: does this match the condition?
4. If matched → notifies you with a summary → auto-pauses (won't spam)
5. If not matched → silently skips

This enables **natural language conditions** that would be impossible with regex:
- "是否有新的职位空缺？排除已见过的"
- "页面上有没有提到 Series B 或以上的融资？"
- "是否出现了与 AI 安全相关的文章？排除广告和推广内容"

## State Machine

```
active ──(match found)──→ paused ──(resume)──→ active
   │                                            ↑
   └──(disable)──→ disabled ──(enable)──────────┘
```

## Monitor Config Format

```json
{
  "name": "hk-risk-jobs",
  "description": "Hong Kong risk management jobs",
  "urls": [{"url": "https://careers.example.com/risk", "label": "Example"}],
  "match": {
    "type": "llm",
    "value": "是否有香港风控或合规岗位？排除实习。"
  },
  "interval": 7200,
  "state": "active",
  "enabled": true
}
```

## Cron Integration

### For keyword/regex/css/jsonpath monitors:

```bash
openclaw cron add \
  --name "Monitor: hk-risk-jobs" \
  --cron "0 */2 * * *" \
  --tz "Asia/Hong_Kong" \
  --session isolated \
  --message "Run monitor: cd /home/node/.openclaw/workspace/skills/web-monitor && python3 scripts/monitor.py run --event hk-risk-jobs" \
  --announce --channel discord --to "user:YOUR_ID" --light-context
```

### For LLM monitors:

```bash
openclaw cron add \
  --name "Monitor: hk-fintech-news" \
  --cron "0 */3 * * *" \
  --tz "Asia/Hong_Kong" \
  --session isolated \
  --message 'You are a web monitor agent. Run: cd /home/node/.openclaw/workspace/skills/web-monitor && python3 scripts/monitor.py fetch --event hk-fintech-news. Read the output JSON. For each URL, evaluate if the page content matches the condition: "是否有香港金融科技相关新闻？排除广告。" If matched: output a brief summary of what matched. If not matched: say "no match". If matched, also run: python3 scripts/monitor.py pause --event hk-fintech-news' \
  --announce --channel discord --to "user:YOUR_ID" --light-context
```

## All Commands

| Command | Usage |
|---|---|
| `create` | Create new monitor |
| `run --event X` | Run with built-in matching |
| `fetch --event X` | Fetch page text (for LLM) |
| `list` | Show all monitors |
| `show --event X` | Show config |
| `resume/pause/disable/enable` | State management |
| `delete --event X` | Delete monitor |
| `add-url` | Add URL to monitor |
