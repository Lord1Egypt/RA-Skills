# 🚀 gstack-skills Quick Start

**5 minutes to get started with gstack-skills!**

---

## Installation (30 seconds)

### Option 1: Interactive (Easiest)

Just tell OpenClaw/WorkBuddy:

```
Please install gstack-skills for me
```

### Option 2: One-Click

**macOS/Linux:**
```bash
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
./install.sh
```

**Windows:**
```batch
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
install.bat
```

### Option 3: Manual

```bash
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
cp -r gstack-skills ~/.openclaw/skills/
```

---

## Start Using (1 minute)

Restart OpenClaw/WorkBuddy, then:

```
User: /gstack
```

You'll see all available commands!

---

## Try It Out (2 minutes)

### Example 1: Code Review

```
User: /review

AI: Reviewing your current branch...

Files changed: 3
Lines added: +127, Lines removed: -45

Critical Issues Found:
❌ 1. SQL Injection Risk in src/db/queries.py:42

Auto-fixes Applied:
✅ Fixed SQL injection
✅ Added rate limiting

Status: ⚠️ DONE_WITH_CONCERNS
NEXT: Run /qa for testing
```

### Example 2: Testing

```
User: /qa

AI: Running systematic QA tests...

Test Results:
• Unit Tests: 42/42 passed ✅
• Integration Tests: 15/15 passed ✅

Health Score: 95/100

Status: ✅ READY TO SHIP
```

### Example 3: Deployment

```
User: /ship

AI: Preparing automated release...

1. Merging base branch... ✅
2. Running tests... ✅ (57/57 passed)
3. Updating version... ✅ (v2.2.0)
4. Creating PR... ✅ (#247)

Status: ✅ DEPLOYED
```

---

## Common Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/gstack` | Show all commands | `/gstack` |
| `/review` | Code review | `/review` |
| `/qa` | Test and fix bugs | `/qa` |
| `/ship` | Deploy | `/ship` |
| `/office-hours` | Validate ideas | `/office-hours I have an idea...` |
| `/investigate` | Debugging | `/investigate the login bug` |

---

## Natural Language Works Too!

You don't need exact commands:

```
User: review my code

AI: Reviewing your current branch...
```

```
User: deploy to production

AI: Preparing automated release...
```

---

## Learn More

- **[INSTALL.md](INSTALL.md)**: Detailed installation guide
- **[CONVERSATION_GUIDE.md](CONVERSATION_GUIDE.md)**: How to use through conversation
- **[USAGE.md](USAGE.md)**: Complete usage guide
- **[EXAMPLES.md](EXAMPLES.md)**: Real-world examples

---

## What is gstack-skills?

Complete development workflow from Y Combinator CEO Garry Tan.

**Features:**
- 15 specialized tools
- Automated execution
- One-command usage
- Natural language support

**Benefit:**
Develop faster - code review in 2 minutes instead of 30, deployment in 3 minutes instead of 30.

---

## Questions?

Ask OpenClaw/WorkBuddy:

```
User: Help me with gstack-skills
```

Or say `/gstack` to see all commands.

---

**Ready to code faster! 🚀**

---

**Version**: 2.0.0 | **Platform**: OpenClaw | **WorkBuddy**
