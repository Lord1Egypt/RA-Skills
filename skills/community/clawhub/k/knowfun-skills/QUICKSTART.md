# 🚀 Quickstart Guide

English | [简体中文](QUICKSTART_CN.md)

Get started with Knowfun.io in 5 minutes — works with Claude Code, Cursor, Cline, and OpenClaw.

---

## Choose Your Platform

| Platform | Install Method | Time |
|----------|----------------|------|
| **Claude Code** | `curl` + copy SKILL.md | ~1 min |
| **Cursor / Cline** | `npm install -g knowfun-skills` | ~30 sec |
| **OpenClaw** | `npx clawhub install knowfun-skills` | ~30 sec |

---

## Step 1: Install

### Claude Code

```bash
# Install the skill globally
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

### Cursor / Cline

```bash
npm install -g knowfun-skills
```

### OpenClaw

```bash
npx clawhub install knowfun-skills
```

---

## Step 2: Get Your API Key (2 minutes)

1. Visit https://www.knowfun.io/api-platform
2. Click "Create API Key"
3. Give it a name like "My Development Key"
4. Copy the API key (starts with `kf_`)

---

## Step 3: Configure (30 seconds)

```bash
# Set for current session
export KNOWFUN_API_KEY="kf_your_api_key_here"

# Or persist permanently (recommended)
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Step 4: Verify Installation

```bash
knowfun credits
```

Expected output:
```
✅ Available: 1,000 credits
📊 Total Earned: 1,000 credits
📉 Total Used: 0 credits
```

> **Claude Code users**: run `/knowfun credits` inside a Claude Code session.

---

## Step 5: Create Your First Content (2 minutes)

### Claude Code

Ask Claude naturally:
```
Create a Knowfun course about "Introduction to Python"
```

Or use the slash command directly:
```
/knowfun create course "Introduction to Python: variables, loops, and functions"
```

### Cursor / Cline / OpenClaw

```bash
knowfun create course "Introduction to Python"
```

Or tell your AI assistant:
```
Use knowfun to create a course about Python basics
```

---

## What Happens Next

Your task will be processed in the background. Within 2–5 minutes you'll have a shareable URL.

Check status:
```bash
knowfun status <taskId>
```

Get the result URL:
```bash
knowfun detail <taskId>
```

---

## All Content Types

```bash
knowfun create course "Introduction to Python"
knowfun create poster "Climate Change: Key Facts"
knowfun create game   "Learn JavaScript Variables"
knowfun create film   "History of the Internet"
```

Processing times: posters 1–3 min · courses 2–5 min · games 3–7 min · films 5–10 min

---

## Check Credits & Schema

```bash
knowfun credits   # Check your balance
knowfun schema    # View all configuration options
knowfun list 10   # Recent tasks
```

---

## Troubleshooting

### "Command not found: knowfun"
```bash
npm install -g knowfun-skills
```

### "API Key not found"
```bash
echo $KNOWFUN_API_KEY          # Check if set
export KNOWFUN_API_KEY="kf_…"  # Set it
```

### "Insufficient credits"
Visit https://www.knowfun.io/api-platform to top up.

### Task stuck in "processing"
Wait a few more minutes. If stuck > 15 min, contact support.

---

## Documentation

- **[README.md](README.md)** — Complete overview
- **[INSTALLATION.md](INSTALLATION.md)** — Detailed per-platform installation
- **[api-reference.md](api-reference.md)** — Full API reference
- **[examples.md](examples.md)** — 20+ usage examples

---

**Need more help?** Check [examples.md](examples.md) or open a [GitHub Issue](https://github.com/MindStarAI/KnowFun-Skills/issues).
