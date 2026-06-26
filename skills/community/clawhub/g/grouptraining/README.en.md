# Likes Training Planner Skill 🏃

English | [中文](README.zh.md)

**All-in-one training plan solution for My Likes platform**

Fetch data → Analyze → Generate → Preview → Confirm → Push. One skill does it all!

---

## ⚠️ Important: Installation Location

**You MUST install to the correct directory for the skill to work properly:**

✅ **Correct location:**
```
~/.openclaw/workspace/skills/likes-training-planner/
```

❌ **Wrong locations (will NOT show API key input box):**
```
~/.openclaw/workspace/likes-training-planner/          # Wrong: workspace root
~/.openclaw/skills/likes-training-planner/            # Wrong: missing workspace
/opt/homebrew/.../openclaw/skills/likes-training-planner/  # Wrong: built-in dir
```

---

## 🚀 Quick Start

### Installation

**Method 1: One-line install (Recommended)**
```bash
curl -fsSL https://gitee.com/chenyinshu/likes-training-planner/raw/main/install.sh | bash
```

**Method 2: Manual install**
```bash
# 1. Download
cd ~/.openclaw/workspace/skills
curl -L -o likes-training-planner.skill \
  https://gitee.com/chenyinshu/likes-training-planner/releases/latest/download/likes-training-planner.skill

# 2. Extract (must be in workspace/skills/ directory)
unzip -q likes-training-planner.skill
rm likes-training-planner.skill

# 3. Restart OpenClaw
openclaw gateway restart
```

### Configuration

**OpenClaw Skill Center (Recommended):**
1. Open http://127.0.0.1:18789 → **Skills**
2. Find **likes-training-planner** 🏃
3. Click **Configure**, enter your Likes API Key
4. Save

**Note:** The API Key input box will always be visible (showing `********` when saved), allowing you to view or modify it anytime.

Get your API Key: https://my.likes.com.cn → Settings → API Documentation

### Usage

Just ask OpenClaw:
> "Analyze my past 30 days of training data"
> 
> "Generate next week's training plan based on my records"
> 
> "Help me create an 8-week marathon preparation plan"

---

## 📋 Complete Workflow

### 1. Fetch Data
```bash
cd ~/.openclaw/workspace/skills/likes-training-planner
node scripts/fetch_activities.cjs --days 30 --output data.json
```

### 2. Analyze
```bash
node scripts/analyze_data.cjs data.json
```

Output example:
```json
{
  "period": { "days": 30, "start": "2026-02-01", "end": "2026-03-01" },
  "summary": {
    "totalRuns": 45,
    "totalKm": 156.5,
    "avgDailyKm": 5.2,
    "frequency": 1.5
  },
  "characteristics": "High frequency, medium distance, aerobic base",
  "recommendations": ["Can add more interval training", "Try longer runs on weekends"]
}
```

### 3. Generate Plan
Create a JSON file with your plan:
```json
{
  "plans": [
    {
      "name": "40min@(HRR+1.0~2.0)",
      "title": "Easy Aerobic",
      "start": "2026-03-10",
      "weight": "q3",
      "type": "qingsong",
      "sports": 1
    }
  ]
}
```

### 4. Preview and Confirm ⭐ (v1.4)

**Always review before pushing!**

```bash
node scripts/preview_plan.cjs plans.json
```

Shows:
- 📅 Day-by-day breakdown
- 📊 Weekly summary
- 🏃 Training type distribution
- ⚡ Intensity breakdown

Interactive options:
- `[Y]` Confirm and push
- `[N]` Cancel
- `[E]` Edit the plan file first

### 5. Push to Calendar

After confirmation:

```bash
node scripts/push_plans.cjs plans.json
```

**One-command workflow with preview:**
```bash
# Preview first
node scripts/preview_plan.cjs plans.json && node scripts/push_plans.cjs plans.json
```

---

## 📚 Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `fetch_activities.cjs` | Download training history | `--days 30 --output data.json` |
| `get_activity_detail.cjs` | Get single activity detail (with GPS) | `--id 12345 --mode detailed` |
| `analyze_data.cjs` | Analyze patterns | `analyze_data.cjs data.json` |
| `fetch_plans.cjs` | Get calendar plans (42 days) | `--start 2026-03-01` |
| `fetch_feedback.cjs` | Get training feedback (with coach comment status) | `--start 2026-03-01 --end 2026-03-07` |
| `add_feedback_comment.cjs` | Add coach comment | `--feedback-id 123 --content "Comment"` |
| `fetch_games.cjs` | List your training camps | `--output camps.json` |
| `fetch_game.cjs` | Get training camp details and members | `--game-id 973` |
| `fetch_ability.cjs` | Running ability (run force / predicted times / pace zones) | `--runforce 51` or `--time-5km 32:28` |
| `preview_plan.cjs` | ⭐ Preview plan (v1.4) | `preview_plan.cjs plans.json` |
| `push_plans.cjs` | Push plans (supports bulk, overwrite) | `push_plans.cjs plans.json` |
| `configure.cjs` | Interactive setup | `configure.cjs` |
| `set-config.cjs` | Quick config | `set-config.cjs API_KEY` |

---

## 🔧 Training Code Format

Likes `name` field format:

```
# Simple task
duration@(type+range)
30min@(HRR+1.0~2.0)

# Interval group  
{task1;task2}xN
{5min@(HRR+3.0~4.0);1min@(rest)}x3

# Complete workout
10min@(HRR+1.0~2.0);{1000m@(VDOT+4.0~5.0);2min@(rest)}x4;10min@(HRR+1.0~2.0)
```

See [references/code-format.md](likes-training-planner/references/code-format.md) for complete guide.

---

## 📁 File Structure

```
~/.openclaw/workspace/skills/likes-training-planner/  ← MUST be here!
├── SKILL.md                    # Main documentation
├── references/
│   ├── api-docs.md            # API documentation
│   ├── code-format.md         # Code format reference
│   └── sport-examples.md      # Training examples
└── scripts/
    ├── fetch_activities.cjs   # ⭐ Download data
    ├── get_activity_detail.cjs # ⭐ Activity detail (with GPS)
    ├── analyze_data.cjs       # ⭐ Analyze patterns
    ├── fetch_plans.cjs        # Get plans
    ├── fetch_feedback.cjs     # Get feedback
    ├── add_feedback_comment.cjs # Add comment
    ├── fetch_games.cjs        # List camps
    ├── fetch_game.cjs         # Camp details
    ├── fetch_ability.cjs      # Running ability (run force / predicted times / pace zones)
    ├── preview_plan.cjs       # ⭐ Preview & confirm (v1.4)
    ├── push_plans.cjs         # Push plans
    ├── configure.cjs          # Setup wizard
    └── set-config.cjs         # Quick config
```

---

## 🆕 Changelog

### v1.7.0 - Running Ability Query
- ✅ Added `fetch_ability.cjs` - Calls GET /api/open/ability
- ✅ Query by run force (runforce) for predicted times and pace zones (E/M/T/A/I/R)
- ✅ Reverse lookup run force from race times (time_5km, time_10km, time_hm, time_fm, etc.)

### v1.6.0 - Activity Detail & Plan Overwrite
- ✅ Added `get_activity_detail.cjs` - Get single activity detail (supports GPS track)
- ✅ `push_plans` added `overwrite` parameter - Overwrite existing plans to avoid duplicates

### v1.5.0 - Full API Support
- ✅ Added `fetch_plans.cjs` - Get calendar plans
- ✅ Added `fetch_feedback.cjs` - Get training feedback (with coach comment status)
- ✅ Added `add_feedback_comment.cjs` - Add coach comments
- ✅ Added `fetch_games.cjs` - List training camps
- ✅ Added `fetch_game.cjs` - Get training camp details and members

### v1.4 - Preview & Confirmation Workflow ⭐
- ✅ Added `preview_plan.cjs` - Preview before pushing
- ✅ Mandatory review workflow: preview → confirm → push
- ✅ Clear weekly schedule visualization
- ✅ User confirmation required before push

### v1.3 - Complete Solution
- ✅ Added `fetch_activities.cjs` - Automatic data download
- ✅ Added `analyze_data.cjs` - Smart training analysis
- ✅ One skill does everything: fetch → analyze → generate → push
- ✅ No separate MCP server needed

### v1.2 - Skill Center Integration
- ✅ OpenClaw Skill Center support
- ✅ Graphical configuration UI
- ✅ .cjs scripts for ES module compatibility

### v1.1 - Configuration Support
- ✅ Configuration wizard
- ✅ Multiple auth methods

### v1.0 - Initial Release
- ✅ Basic plan generation and push

---

## 📝 License

MIT

---

## 🔗 Links

- **Repository**: https://gitee.com/chenyinshu/likes-training-planner
- **Releases**: https://gitee.com/chenyinshu/likes-training-planner/releases
- **My Likes**: https://my.likes.com.cn

---

## ❓ Troubleshooting

### API Key input box not showing?

**Check installation location:**
```bash
# Should show: ~/.openclaw/workspace/skills/likes-training-planner/
ls ~/.openclaw/workspace/skills/likes-training-planner/

# If installed elsewhere, move it:
mv ~/.openclaw/workspace/likes-training-planner ~/.openclaw/workspace/skills/
openclaw gateway restart
```

### Skill not appearing in Skill Center?

1. Check directory structure:
   ```bash
   ls ~/.openclaw/workspace/skills/
   # Should show: likes-training-planner/
   ```

2. Verify SKILL.md exists:
   ```bash
   cat ~/.openclaw/workspace/skills/likes-training-planner/SKILL.md | head -10
   ```

3. Restart OpenClaw:
   ```bash
   openclaw gateway restart
   ```

4. Hard refresh browser (Cmd+Shift+R)
