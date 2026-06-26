# Cost Watchdog 💰

> An AI agent skill that monitors API spend per task, flags runaway loops, and estimates cost before executing expensive operations.

---

## 🚀 What's New in v2.1

### ✨ New Features

**1. Expanded Provider Coverage**
- ✅ **Groq** - Llama 3.1/3.2, Mixtral, Gemma, DeepSeek (ultra-fast, cheap)
- ✅ **DeepSeek** - R1, V3, Coder V2 (strong reasoning, competitive pricing)
- ✅ **Perplexity** - Sonar Pro/Small (search-enhanced models)
- ✅ **OpenRouter** - Aggregated models with auto-routing
- **Total:** 9 providers, 50+ models covered

**2. Cost Visualization** 📊
- Daily/weekly spending reports
- ASCII bar charts for task costs
- Provider breakdown comparisons
- Trend analysis

**3. Smart Budgeting** 🧠
- Auto-adjust budgets based on task priority
- Learn from past spending patterns
- Get smarter cost estimates
- Suggest cheaper model alternatives (50%+ savings)

---

## 📊 The Problem

Pricing models are now debated almost as intensely as capabilities, especially as more tools move toward usage-based billing. Early versions of AutoGen caused one team to rack up **$2,400 in API costs overnight** due to an infinite loop. This is a real and recurring pain point.

---

## 💡 What It Does

Cost Watchdog is a capability layer for AI agents that makes API cost a first-class concern:

### Core Features
- ✅ **Pre-execution estimates** — Know what an operation will cost before running it
- ✅ **Runaway loop detection** — Flags dangerous patterns: unbounded loops, recursive agents, missing retry limits
- ✅ **Budget enforcement** — Set spending ceilings with warnings at 50%, 80%, and 95%
- ✅ **Cost optimization** — Suggests model tiering, caching, batching, and early termination
- ✅ **Codebase auditing** — Scans agent code for cost-unsafe patterns with specific fixes
- ✅ **Multi-provider pricing** — Current rates for 9 providers, 50+ models

### New in v2.1
- ✅ **Visual reports** — Daily/weekly spending breakdowns with ASCII charts
- ✅ **Smart budgeting** — Auto-adjust based on priority, learn from history
- ✅ **Cheaper alternatives** — Suggest models with 50%+ savings
- ✅ **Pattern learning** — Improve estimates based on past task costs

---

## 🛠️ Installation

### As a Personal Skill (all projects)

```bash
# Symlink to OpenClaw skills directory
ln -s ~/Documents/cost-watchdog ~/.npm-global/lib/node_modules/openclaw/skills/cost-watchdog
```

### As a Project Skill (single project)

```bash
# Copy to project skills directory
cp -r ~/Documents/cost-watchdog .claude/skills/cost-watchdog
```

---

## 📖 Usage

### Manual Invocation

```bash
# Basic commands
/cost-watchdog estimate          # Estimate cost of current task
/cost-watchdog report            # Session spend report
/cost-watchdog set-budget 10.00  # Set $10 budget
/cost-watchdog check             # Check spend vs budget
/cost-watchdog reset             # Reset session counters
/cost-watchdog audit src/        # Audit code for cost risks
/cost-watchdog price gpt-4o     # Look up model pricing

# NEW v2.1: Visualization
/cost-watchdog visualize daily        # Show today's spending
/cost-watchdog visualize weekly       # Show last 7 days
/cost-watchdog visualize chart        # ASCII bar chart
/cost-watchdog visualize providers    # Breakdown by provider

# NEW v2.1: Smart budgeting
/cost-watchdog set-budget 5.00 --priority=high   # Auto-adjust for priority
/cost-watchdog alternatives claude-sonnet-4-6    # Find cheaper models
/cost-watchdog learn task-type 0.85 120000       # Learn from completed task
/cost-watchdog estimate task-type 150000         # Smart estimate with learning
```

### Automatic Invocation

The skill auto-activates when Claude detects:
- API calls to LLM providers in code
- Agent loops or recursive patterns
- Cost/budget/billing discussions
- Batch processing workflows

---

## 📁 File Structure

```
cost-watchdog/
├── SKILL.md                        # Main skill definition
├── README.md                       # This file
├── references/
│   ├── pricing.md                  # Current API pricing (9 providers, 50+ models)
│   ├── optimization.md             # Cost optimization strategies
│   ├── patterns.md                 # Dangerous patterns & safe alternatives
│   └── calculators.md              # Token counting & cost calculation code
└── scripts/
    ├── cost-visualizer.py          # Generate charts and reports
    └── smart-budget.py             # Smart budgeting with learning
```

---

## 🌐 Covered Providers (v2.1)

### Major Providers

| Provider | Models | Key Features |
|----------|--------|--------------|
| **Anthropic** | Claude Opus 4.6, Sonnet 4.6, Haiku 4.5 | Prompt caching, batch API |
| **OpenAI** | GPT-4o, GPT-4.1 family, o3/o4 series | Cached input, batch API |
| **Google** | Gemini 2.5 Pro/Flash, Gemini 2.0 Flash | Free tier, large context |
| **Mistral** | Large, Small, Codestral, Embed | Competitive pricing |
| **Cohere** | Command R+, Command R, Embed v3 | Enterprise focus |

### New in v2.1

| Provider | Models | Key Features |
|----------|--------|--------------|
| **Groq** | Llama 3.1/3.2, Mixtral, Gemma, DeepSeek | Ultra-fast (100+ tokens/sec), very cheap |
| **DeepSeek** | R1, V3, Coder V2 | Strong reasoning, competitive pricing |
| **Perplexity** | Sonar Pro, Sonar, Small | Search-enhanced, real-time web |
| **OpenRouter** | 20+ aggregated models | Auto-routing to cheapest provider |

**Total:** 9 providers, 50+ models

---

## 📊 Visualization Examples

### Daily Report
```
📊 Daily Cost Report - 2026-04-16
══════════════════════════════════════════════════════
💰 Total Cost: $2.45
📝 Total Sessions: 12
🔢 Total Tokens: 145,000
📈 Daily Average: $0.20 per session

──────────────────────────────────────────────────────
🏆 Top 5 Most Expensive Tasks:
──────────────────────────────────────────────────────
1. Document summarization       $0.85
2. Code review batch            $0.62
3. Translation job              $0.45
4. Chat session                 $0.33
5. Image analysis               $0.20

──────────────────────────────────────────────────────
📊 Provider Breakdown:
──────────────────────────────────────────────────────
  claude          $1.85 (8 sessions)
  openai          $0.45 (3 sessions)
  groq            $0.15 (1 session)
══════════════════════════════════════════════════════
```

### ASCII Chart
```
📊 Top Tasks by Cost
══════════════════════════════════════════════════════
Document summarization  ████████████████████ $0.85
Code review batch       ██████████████ $0.62
Translation job         ██████████ $0.45
Chat session            ███████ $0.33
Image analysis          ████ $0.20
══════════════════════════════════════════════════════
```

---

## 🧠 Smart Budgeting Examples

### Set Budget with Priority
```bash
/cost-watchdog set-budget 5.00 --priority=high

✅ Response:
✅ Budget adjusted: $5.00 × 1.5 (high priority) = $7.50
🛡️ I'll alert you at $6.00 and block at $7.50
```

### Learn from Completed Task
```bash
/cost-watchdog learn document-summarization 0.85 120000 15

# Response:
✅ Learned: document-summarization
   Avg cost: $0.85, Avg tokens: 120K, Avg duration: 15min
   Confidence: 75% (based on 8 samples)
```

### Get Smart Estimate
```bash
/cost-watchdog estimate document-summarization 150000

# Response:
💰 Estimate for document-summarization:
   Cost: $0.92 (learned from 8 previous tasks)
   Confidence: 75%
   Range: $0.65 - $1.25 (based on std dev)
   Source: learned pattern
```

### Find Cheaper Alternatives
```bash
/cost-watchdog alternatives claude-sonnet-4-6 --savings=50

# Response:
💡 Cheaper alternatives to claude-sonnet-4-6 (>50% savings):
   • claude-haiku-4-5: Save 67%
     Trade-off: Much faster, lower quality for complex tasks
   • gpt-4o-mini: Save 87%
     Trade-off: Good for simple tasks, less capable on complex reasoning
   • groq-llama-3.2-8b: Save 94%
     Trade-off: Very fast, good for simple tasks
```

---

## 🎯 Priority-Based Budget Multipliers

| Priority | Multiplier | Use Case |
|----------|-----------|----------|
| **low** | 0.5× | Experiments, testing, learning |
| **medium** | 1.0× | Normal work, standard tasks |
| **high** | 1.5× | Important deliverables, client work |
| **critical** | 2.0× | Production, deadlines, critical path |

---

## 💰 Quick Cost Comparison (1M input + 100K output)

| Model | Cost | Best For |
|-------|------|----------|
| **GPT-4.1-nano** | $0.14 | Simple classification, extraction |
| **DeepSeek-Coder V2** | $0.17 | Code generation |
| **Groq Llama 3.2 8B** | $0.06 | Fast responses, simple tasks |
| **Gemini 2.0 Flash** | $0.14 | Good value, general tasks |
| **Claude Haiku 4.5** | $1.20 | Best value premium |
| **Claude Sonnet 4.6** | $4.50 | Top tier quality |
| **Claude Opus 4.6** | $22.50 | Maximum reasoning power |

---

## 🔧 Scripts

### Cost Visualizer
```bash
# Navigate to scripts directory
cd ~/Documents/cost-watchdog/scripts/

# Generate daily report
python cost-visualizer.py daily

# Generate weekly report
python cost-visualizer.py weekly

# Show top expensive tasks
python cost-visualizer.py tasks

# Show provider breakdown
python cost-visualizer.py providers

# Show ASCII chart
python cost-visualizer.py chart
```

### Smart Budget Manager
```bash
# Set budget with priority
python smart-budget.py set 5.00 --priority=high

# Get status
python smart-budget.py status

# Estimate task cost
python smart-budget.py estimate document-summarization 150000 claude-sonnet-4-6

# Find alternatives
python smart-budget.py alternatives claude-sonnet-4-6 --savings=50

# Learn from task
python smart-budget.py learn document-summarization 0.85 120000 15
```

---

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Core skill definition, triggers, and instructions
- **[references/pricing.md](references/pricing.md)** - Complete pricing tables for all providers
- **[references/optimization.md](references/optimization.md)** - Cost optimization strategies
- **[references/patterns.md](references/patterns.md)** - Dangerous patterns and safe alternatives
- **[references/calculators.md](references/calculators.md)** - Token counting and cost calculation

---

## 🎓 Best Practices

1. **Set budget BEFORE starting expensive work**
2. **Use `estimate` before batch operations**
3. **Check `check` periodically during long tasks**
4. **Audit code before deploying agent workflows**
5. **Review `report` at end of day to learn spending patterns**
6. **Use `alternatives` to find cheaper models for simple tasks**
7. **Use `learn` after completing tasks to improve future estimates**

---

## 🚦 Budget Status Levels

| Status | Threshold | Action |
|--------|-----------|--------|
| ✅ **ok** | 0-50% | Normal operation |
| ⚠️ **caution** | 50-80% | Monitor spending |
| ⚠️ **warning** | 80-95% | Consider wrapping up |
| 🚨 **critical** | 95-100% | Finish current task only |
| ❌ **over_budget** | >100% | Stop or increase budget |

---

## 📝 Changelog

### v2.1 (April 2026)
- ✅ Added Groq, DeepSeek, Perplexity, OpenRouter providers
- ✅ Added cost visualization (daily/weekly reports, ASCII charts)
- ✅ Added smart budgeting (auto-adjust, learn from patterns)
- ✅ Added cheaper alternative suggestions
- ✅ Added pattern learning for better estimates
- ✅ Updated pricing tables (50+ models)

### v2.0 (March 2026)
- ✅ Initial release with core features
- ✅ Anthropic, OpenAI, Google, Mistral, Cohere pricing
- ✅ Runaway loop detection
- ✅ Budget enforcement

---

## 📄 License

MIT

## 👤 Author

Nima Ansari
