---
name: likes-training-planner
description: Complete training plan solution for My Likes platform. Fetches historical data, analyzes training patterns, generates personalized plans, converts to Likes format, and pushes to calendar. All-in-one skill for running, cycling, swimming, and strength training.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏃",
        "requires": { "env": ["LIKES_API_KEY"] },
        "primaryEnv": "LIKES_API_KEY",
      },
  }
---

# Likes Training Planner

Complete training plan solution for My Likes platform. **One skill does it all**: fetch data → analyze → generate → push.

## 🤖 Bot 自动路由（多Bot支持）

本Skill支持多个Telegram Bot自动路由，不同Bot有不同的专注领域：

| Bot | 角色 | 专注功能 |
|-----|------|---------|
| **@likes_training_bot** | 训练分析师 | 数据分析、反馈点评 |
| **@likes_traning_2_bot** | 训练计划师 | 计划制定、推送日历 |

系统会自动识别当前使用的Bot，提供对应的功能和交互体验。

## Quick Start

### 1. Configure API Key

**OpenClaw Skill Center (Recommended):**
1. Open http://127.0.0.1:18789 → Skills
2. Find "likes-training-planner" 🏃
3. Click Configure, enter your Likes API Key
4. Save

Get API Key: https://my.likes.com.cn → 设置 → API 文档

### 2. Use the Skill

Just ask:
> "分析我过去30天的运动数据"
> 
> "根据我的记录，生成下周的训练计划"
> 
> "帮我制定一个8周马拉松备赛计划"

## Complete Workflow

### Step 1: Fetch Data

```bash
# Fetch activities (rate limit: 1 req/min, max 30 days)
node scripts/fetch_activities.cjs --days 7 --output data.json

# Fetch plans for next 42 days
node scripts/fetch_plans.cjs --start 2026-03-01 --output plans.json

# Fetch training feedback
node scripts/fetch_feedback.cjs --start 2026-03-01 --end 2026-03-07

# Fetch your training camps
node scripts/fetch_games.cjs --output camps.json

# Fetch camp details and members
node scripts/fetch_game.cjs --game-id 973 --output camp_details.json

# Fetch running ability (by run force or by race times)
node scripts/fetch_ability.cjs --runforce 51 --output ability.json
```

### Step 2: Analyze

```bash
node scripts/analyze_data.cjs data.json
```

Output includes:
- Total runs, distance, time
- Average pace, frequency
- Training characteristics
- Personalized recommendations

### Step 3: Generate Plan

Based on analysis, create a plan:
```json
{
  "plans": [
    {
      "name": "40min@(HRR+1.0~2.0)",
      "title": "轻松有氧跑",
      "start": "2026-03-10",
      "weight": "q3",
      "type": "qingsong",
      "sports": 1,
      "description": "根据近期数据，保持有氧基础"
    }
  ]
}
```

### Step 4: Push to Calendar

**Push to yourself:**
```bash
node scripts/push_plans.cjs plans.json
```

**Push to specific user(s):**
```bash
node scripts/push_plans.cjs plans.json --user-ids 123
```

**Bulk push to training camp members (coach only):**
```bash
node scripts/push_plans.cjs plans.json --game-id 973 --user-ids "4,5,6"
```

## API Scripts Reference

| Script | Purpose | Rate Limit |
|--------|---------|------------|
| `fetch_activities.cjs` | Download training history | 1 req/min, max 30 days |
| `fetch_plans.cjs` | Get calendar plans (42 days) | Standard |
| `fetch_feedback.cjs` | Get training feedback | Standard |
| `fetch_games.cjs` | List your training camps | Standard |
| `fetch_game.cjs` | Get camp details & members | Coach only |
| `fetch_ability.cjs` | Get run force, predicted times & pace zones (or estimate from race times) | Standard |
| `analyze_data.cjs` | Analyze patterns | N/A |
| `push_plans.cjs` | Push plans (supports bulk) | Standard |
| `configure.cjs` | Interactive setup | N/A |
| `set-config.cjs` | Quick config setter | N/A |

## fetch_activities.cjs Options

```bash
node scripts/fetch_activities.cjs [options]

Options:
  --days <n>        Number of days (default: 7, max: 30)
  --start <date>    Start date (YYYY-MM-DD)
  --end <date>      End date (YYYY-MM-DD, max 30 days from start)
  --user-id <id>    Query specific user (coach only)
  --page <n>        Page number (default: 1)
  --limit <n>       Items per page (default: 200, max: 2000)
  --order-by <field> Sort: sign_date, run_km, run_time, tss
  --order <asc|desc> Sort order (default: desc)
  --output <file>   Output file
```

## fetch_ability.cjs Options

```bash
node scripts/fetch_ability.cjs [options]
```

Mode 1 — by run force (get predicted times and pace zones):
  --runforce <0-99>   Ability value, e.g. 50 or 50.5 (required for mode 1)
  --celsius <0-40>   Optional. Temperature in Celsius, default 6

Mode 2 — by race times (get estimated run force, at least one required):
  --time-5km <sec|M:SS|H:MM:SS>
  --time-10km, --time-hm, --time-fm, --time-3km, --time-mile   Same format

Optional:
  --output <file>   Output file (default: stdout)
  --key <api_key>   Override API key

Examples:
  node scripts/fetch_ability.cjs --runforce 51
  node scripts/fetch_ability.cjs --time-5km 32:28 --time-10km 1:07:20 --output ability.json
```

## push_plans.cjs Options

```bash
node scripts/push_plans.cjs <plans.json> [options]

Options:
  --key <api_key>    Use specific API key
  --game-id <id>     Training camp ID (for bulk push)
  --user-ids <ids>   Comma-separated user IDs (e.g., "4,5,6")
  --dry-run          Preview without pushing
```

**Bulk Push Requirements:**
- Must provide `game_id` when using `user_ids`
- You must be creator or coach of the camp
- All user_ids must be camp members
- Max 200 plans per request

## Training Code Format (name field)

Format: `task1;task2;...`

**Basic task**: `duration@(type+range)`
- `30min@(HRR+1.0~2.0)` - 30 min easy run
- `5km@(PACE+5'00~4'30)` - 5km with pace target

**Interval group**: `{task1;task2}xN`
- Example: `{5min@(HRR+3.0~4.0);1min@(rest)}x3`

**Rest**: `duration@(rest)` (parentheses required)
- Example: `2min@(rest)`

### Intensity Types

| Type | Description | Example |
|------|-------------|---------|
| HRR | Heart rate reserve % | `HRR+1.0~2.0` |
| VDOT | VDOT pace zone | `VDOT+4.0~5.0` |
| PACE | Absolute pace (min'sec) | `PACE+5'30~4'50` |
| t/ | Threshold pace % | `t/0.88~0.99` |
| MHR | Max heart rate % | `MHR+0.85~0.95` |
| LTHR | Lactate threshold HR % | `LTHR+1.0~1.05` |
| EFFORT | Perceived effort | `EFFORT+0.8~1.0` |
| FTP | Power % (cycling) | `FTP+0.75~0.85` |
| CP | Absolute power W | `CP+200~240` |
| CSS | Critical swim speed % | `CSS+0.95~1.05` |
| TSP | Threshold swim pace % | `TSP+0.95~1.05` |
| OPEN | Open-ended | `OPEN+1` |

### Duration Units

- `min` = minutes
- `s` = seconds
- `m` = meters
- `km` = kilometers
- `c` = count/reps

## Training Type Mapping

| Type Code | Description |
|-----------|-------------|
| qingsong | Easy run |
| xiuxi | Rest day |
| e | Aerobic training |
| lsd | Long slow distance |
| m | Marathon pace |
| t | Threshold/lactate training |
| i | Interval training |
| r | Speed/repetition |
| ft | Fartlek |
| com | Combined workout |
| ch | Variable pace |
| jili | Strength training |
| max | Max HR test |
| drift | Aerobic stability test |
| other | Other |
| 1/7/2/3/4/5/6 | 1.6km/2km/3km/5km/10km/HM/FM test |

## Intensity Weights

| Weight | Color | Description |
|--------|-------|-------------|
| q1 | Red | High intensity |
| q2 | Orange | Medium intensity |
| q3 | Green | Low intensity |
| xuanxiu | Blue | Optional/recovery |

## Example Usage

### Coach: Bulk Push to Camp Members

```bash
# 1. Get your camps
node scripts/fetch_games.cjs

# 2. Get camp members
node scripts/fetch_game.cjs --game-id 973

# 3. Create plan for members
# ... edit plan.json ...

# 4. Bulk push to specific members
node scripts/push_plans.cjs plan.json --game-id 973 --user-ids "4,5,6"
```

### Analyze and Generate in One Go

```bash
# Fetch and analyze
cd /opt/homebrew/lib/node_modules/openclaw/skills/likes-training-planner
node scripts/fetch_activities.cjs --days 14 | node scripts/analyze_data.cjs
```

## Configuration

### Priority (highest to lowest):
1. Command line `--key`
2. Environment variable `LIKES_API_KEY`
3. OpenClaw config: `skills.likes-training-planner.apiKey`
4. User config: `~/.openclaw/likes-training-planner.json`

## References

- **API documentation**: See [references/api-docs.md](references/api-docs.md)
- **Code format details**: See [references/code-format.md](references/code-format.md)
- **Sport-specific examples**: See [references/sport-examples.md](references/sport-examples.md)

## Installation

```bash
curl -fsSL https://gitee.com/chenyinshu/likes-training-planner/raw/main/install.sh | bash
```
