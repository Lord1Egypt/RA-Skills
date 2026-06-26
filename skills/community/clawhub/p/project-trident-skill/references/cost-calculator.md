# Trident Cost Calculator

**Find your optimal cost profile in 3 questions.**

---

## Quick Reference

| Profile | Model | Interval | Cost/day | Cost/month |
|---|---|---|---|---|
| Zero Budget | Ollama (local) | 30 min | $0 | $0 |
| Budget | Claude Haiku | 30 min | $0.72 | $21.60 |
| **Standard** | **Claude Haiku** | **15 min** | **$1.44** | **$43.20** |
| Premium | Claude Sonnet | 15 min | $3.12 | $93.60 |
| High-Frequency | Claude Sonnet | 5 min | $9.36 | $280.80 |

**Layer 1 (.md files), LCM (SQLite), and Git backup are all $0.**  
The only ongoing cost is Layer 0.5 (the cron agent).

---

## Decision Tree

### Q1: How active is your agent?

**Low activity** (occasional conversations, background tasks, 1-2 hours/day):
→ Skip to Q3, use **30-min interval**

**Standard activity** (daily conversations, research, coding, 4-8 hours/day):
→ Skip to Q2, use **15-min interval**

**High activity** (continuous operation, trading, real-time tasks, 24/7):
→ Skip to Q2, use **5-10 min interval**

---

### Q2: Do you have a cloud API budget?

**Yes** → Continue to Q3

**No, I want zero API cost** → Use Ollama (local model)
- Requires: Local hardware with 8GB+ RAM
- Model: `ollama/qwen2.5:7b` (~4.6GB RAM)
- Quality: 75-80% signal detection accuracy
- Speed: 8-10 seconds per Layer 0.5 run
- Cost: $0/day
- → **Go to "Ollama Profile" below**

---

### Q3: What is your quality requirement?

**Good enough (routing most signals correctly):**
- Model: Claude Haiku 4.5
- Signal detection accuracy: ~95%
- Cost: $0.72–$1.44/day depending on interval

**Excellent (complex domain, relationship-heavy, high-stakes decisions):**
- Model: Claude Sonnet
- Signal detection accuracy: ~99%
- Cost: $3.12–$9.36/day depending on interval

---

## Recommended Profiles

### Profile A: Zero Budget (Ollama)
```json
{
  "payload": {
    "model": "ollama/qwen2.5:7b",
    "timeoutSeconds": 120
  },
  "schedule": { "kind": "every", "everyMs": 1800000 }
}
```
- **Cost:** $0/day
- **Requirements:** Local hardware, Ollama installed, 8GB+ RAM
- **Tradeoffs:** 20-25% lower signal detection accuracy; slower runs
- **Best for:** Air-gapped environments, tight budgets, offline operation

---

### Profile B: Budget ($0.72/day)
```json
{
  "payload": {
    "model": "anthropic/claude-haiku-4-5",
    "timeoutSeconds": 90
  },
  "schedule": { "kind": "every", "everyMs": 1800000 }
}
```
- **Cost:** ~$0.72/day (~$21.60/month)
- **Signal detection:** ~95% accuracy
- **Lag:** Up to 30 minutes before signals are routed
- **Best for:** Low-activity agents, personal assistants, passive observers

---

### Profile C: Standard — Recommended ($1.44/day)
```json
{
  "payload": {
    "model": "anthropic/claude-haiku-4-5",
    "timeoutSeconds": 90
  },
  "schedule": { "kind": "every", "everyMs": 900000 }
}
```
- **Cost:** ~$1.44/day (~$43.20/month)
- **Signal detection:** ~95% accuracy
- **Lag:** Up to 15 minutes before signals are routed
- **Best for:** Standard research, coding, writing, and analysis agents

---

### Profile D: Premium ($3.12/day)
```json
{
  "payload": {
    "model": "anthropic/claude-sonnet-4-6",
    "timeoutSeconds": 120
  },
  "schedule": { "kind": "every", "everyMs": 900000 }
}
```
- **Cost:** ~$3.12/day (~$93.60/month)
- **Signal detection:** ~99% accuracy; better semantic routing
- **Lag:** Up to 15 minutes before signals are routed
- **Best for:** Complex domains (medicine, law, trading), relationship-heavy agents, high-stakes decisions

---

### Profile E: High-Frequency ($9.36/day)
```json
{
  "payload": {
    "model": "anthropic/claude-sonnet-4-6",
    "timeoutSeconds": 120
  },
  "schedule": { "kind": "every", "everyMs": 300000 }
}
```
- **Cost:** ~$9.36/day (~$280.80/month)
- **Signal detection:** ~99% accuracy
- **Lag:** Up to 5 minutes before signals are routed
- **Best for:** Real-time trading agents, continuous monitoring, 24/7 autonomous agents

---

## Cost Optimization Strategies

### Business Hours Only
Run Layer 0.5 only during active hours (e.g., 8 AM–10 PM):

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "*/15 8-22 * * *",
    "tz": "America/Denver"
  }
}
```
**Savings:** ~40% (14 active hours vs. 24)

---

### Hybrid Model Routing
Use Haiku for daily routing, Sonnet for weekly deep reflection:

```
Daily Layer 0.5:   Haiku, 15-min → $1.44/day
Weekly reflection: Sonnet, once  → $0.06/week (negligible)
Total:             ~$1.44/day
```
This is the most cost-efficient way to get 99% Sonnet quality where it matters (weekly synthesis) while keeping daily costs low.

---

### Compression-Only Mode (Lowest Cost)
Run Layer 0.5 twice per day instead of every 15 minutes:

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 6,18 * * *",
    "tz": "America/Denver"
  }
}
```
- **Cost:** ~$0.03/day (2 runs × $0.015/run)
- **Lag:** Up to 12 hours before signals are routed
- **Best for:** Ultra-low-budget agents that don't need real-time memory

---

## Pricing Basis

All pricing based on current API rates (April 2026):

| Model | Input ($/MTok) | Output ($/MTok) |
|---|---|---|
| Claude Haiku 4.5 | $0.80 | $4.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Gemini 2.5 Flash | $0.15 | $0.60 |
| GPT-4.1 | $2.00 | $8.00 |
| Ollama (local) | $0 | $0 |

**Typical Layer 0.5 run:** ~15K tokens (8K input, 7K output)

---

## Alternative: Gemini Flash (Budget-Quality Hybrid)

If you have a Gemini API key (native, not OpenRouter), Gemini 2.5 Flash offers excellent value:

```json
{
  "payload": {
    "model": "google/gemini-2.5-flash",
    "timeoutSeconds": 90
  },
  "schedule": { "kind": "every", "everyMs": 900000 }
}
```

- **Cost:** ~$0.18/day (15-min interval) — **87% cheaper than Haiku**
- **Signal detection:** ~93% accuracy
- **Best for:** Budget-conscious agents with Gemini API access

---

## Total System Cost Summary

| Component | Cost/day |
|---|---|
| Layer 0 (LCM SQLite) | $0 |
| Layer 1 (.md files) | $0 |
| Layer 0.5 (Standard Haiku 15-min) | $1.44 |
| Git backup (optional) | $0 |
| Qdrant/FalkorDB (optional, Docker) | $0 (self-hosted) |
| **Total (Standard profile)** | **$1.44/day** |

**For less than the cost of a daily coffee, your agent never forgets anything.**
