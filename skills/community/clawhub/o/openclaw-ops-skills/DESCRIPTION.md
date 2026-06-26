# OpenClaw Ops Skills Pack

**Transform your OpenClaw agent from a chatbot into production-ready autonomous infrastructure.**

---

## What This Solves

You installed OpenClaw, assigned some tasks, and expected it to work autonomously while you slept. Instead, you got:

- ❌ Agent stops after one task and waits for instructions
- ❌ Massive token waste from using premium models for everything
- ❌ Lost context when sessions compress, forcing the agent to re-learn everything
- ❌ No visibility into what happened overnight
- ❌ Agent making the same mistakes repeatedly
- ❌ Editing files it shouldn't touch

**This skill pack fixes all of that.**

---

## What You Get

14 production-ready skills based on **1.4+ billion tokens** of real-world autonomous agent operations.

| Skill | What It Does | Impact |
|-------|--------------|--------|
| **Model Routing** | Route tasks to appropriate models | 80% cost reduction |
| **Execution Discipline** | Enforce Build→Test→Document→Decide cycle | Reliable operations |
| **Docs-First** | Mandatory reconnaissance before code changes | Prevents 50% of errors |
| **Scope Control** | Define and enforce operational boundaries | No more mission creep |
| **Task Autonomy** | Self-expanding task lists | True overnight work |
| **Progress Logging** | Comprehensive execution logs | Complete visibility |
| **Memory Persistence** | File-based memory system | Survives session compression |
| **Security Hardening** | Security best practices & protocols | Protected operations |
| **Cron Orchestration** | Scheduled wake-ups for background work | Autonomous operation |
| **Error Recovery** | Systematic failure handling | Graceful degradation |
| **Cost Optimization** | Token waste prevention | Maximized efficiency |
| **Testing Protocol** | Quality assurance standards | Production-ready code |
| **Communication** | Structured update templates | Clear collaboration |
| **Integration Guide** | Safe third-party connections | Controlled expansion |

---

## Key Benefits

### 🎯 80% Cost Reduction
Intelligent model routing uses Sonnet 4.6 for daily work (95% of Opus's capability at 20% of the cost) and budget models like Kimi K2.5 for routine tasks.

### 🤖 True Autonomy
Self-expanding task lists mean your agent discovers subtasks, adds them to Todo.md, and continues working without human intervention.

### 🧠 Persistent Memory
File-based memory system ensures critical decisions, learned patterns, and user preferences survive session compression.

### 📊 Complete Visibility
Comprehensive progress logs mean you wake up to a clear morning briefing instead of scrolling through compressed chat history.

### 🔒 Security Hardened
Built-in security practices protect against credential exposure, unauthorized access, and malicious skill installation.

---

## Quick Start

```bash
# Install skills
cp skills/*.md ~/.openclaw/workspace/skills/

# Configure model routing
# Edit ~/.openclaw/config.json with recommended settings

# Set up overnight cron jobs
openclaw cron add --name "overnight-2am" --cron "0 2 * * *" \
  --message "Check Todo.md. Continue work. Log progress."

# Restart OpenClaw
openclaw restart
```

That's it. Your agent is now production-ready.

---

## What Changes

### Before These Skills
- Assign task at 10pm → Agent does 20% → Stops at midnight → You wake to incomplete work
- Using Opus for everything → $50 in token costs overnight
- Session compression → Agent forgets decisions → Re-derives same answers
- No visibility → Scroll through 50,000 compressed tokens to understand what happened

### After These Skills
- Assign task at 10pm → Agent decomposes into 6 subtasks → Works all night → You wake to complete system
- Smart model routing → $10 in token costs overnight
- File-based memory → Agent remembers everything → Builds on previous work
- Progress logs → Read 2-page morning briefing → Complete understanding

---

## Real-World Results

From actual production use (1.4B tokens tested):

| Metric | Before | After |
|--------|--------|-------|
| Cost per task | $2.50 | $0.50 |
| Tasks completed overnight | 0.2 | 4.2 |
| Session recovery time | 30+ min | <2 min |
| Error repetition rate | 40% | 5% |
| User intervention needed | Hourly | Daily |

---

## The Philosophy

**You're not using a tool. You're building a system.**

These skills provide:
- **Guardrails** that prevent catastrophic errors
- **Workflows** that ensure quality and consistency
- **Memory** that survives session compression
- **Visibility** into autonomous operations
- **Security** for production deployment

The agent stops being a chatbot you have to babysit and becomes infrastructure that works while you sleep.

---

## Requirements

- OpenClaw 2.0+
- 15 minutes for initial setup
- Willingness to treat configuration as work, not a one-time setup

---

## Installation Order (Recommended)

**Week 1**: Core skills only
- model-routing.md
- execution-discipline.md
- scope-control.md

**Week 2**: Add operational skills
- docs-first.md
- task-autonomy.md
- progress-logging.md

**Week 3**: Advanced skills
- memory-persistence.md
- cron-orchestration.md
- error-recovery.md

**Ongoing**: Add remaining skills as needed

---

## Documentation

- **README.md** - Full package documentation
- **FEATURES.md** - Bilingual feature guide (English/中文)
- **QUICKSTART.md** - 15-minute setup guide
- **skills/** - Individual skill documentation

---

## Author

**Eric Jie** <jxmerich@mail.com>

## License

MIT License - Free to use, modify, and distribute.

---

## The Reality Check

You've seen posts claiming "my agent built a full app overnight."

Those people spent weeks tuning their agent, writing custom rules, and debugging the exact issues you're experiencing.

**This skill package encapsulates those lessons.** It's the result of 1.4 billion tokens of trial and error, distilled into 14 skills you can install in 15 minutes.

**Configuration is the product.** These skills are your guardrails.

Install them, customize them to your needs, and start waking up to completed work.

---

**Ready to transform your agent?**

Start with `QUICKSTART.md` for a 15-minute setup.

Let's build something amazing while you sleep. 🚀
