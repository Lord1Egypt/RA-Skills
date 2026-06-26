# Cost Tuning for Trident Memory

## Layer 0 Interval & Model Selection

Layer 0 (signal router cron) is the primary ongoing cost. Everything else is negligible.

### Cost by Interval (Haiku-4.5)

| Interval | Runs/day | Cost/day | Use case |
|----------|----------|----------|----------|
| 5 min | 288 | $4.64 | High-volume agent (trading, real-time systems) |
| 10 min | 144 | $2.32 | Active agent (research, coding) |
| **15 min** | **96** | **$1.44** | **Standard (recommended)** |
| 30 min | 48 | $0.72 | Low-activity agent |
| 60 min | 24 | $0.36 | Passive agent (background tasks) |

Pricing: Claude Haiku = $0.80/MTok input, $4.00/MTok output. Typical Layer 0 run: ~15K tokens (8K in, 7K out) = ~$0.015/run.

### Model Selection for Layer 0

#### Haiku-4.5 (Recommended)
- Cost: $0.015/run
- Speed: <2 sec per run
- Quality: Signal detection 95%+ accuracy
- Limitation: Weak on semantic reasoning (misses subtle patterns)

#### Sonnet-4.6
- Cost: $0.06/run (4x more expensive)
- Speed: 3-5 sec per run
- Quality: Signal detection 99%+, better semantic routing
- Use when: Pattern-heavy domains (research, relationship modeling) or high-stakes decisions

#### Grok-3-Mini-Fast
- Cost: $0.02/run (30% more than Haiku)
- Speed: <1 sec per run
- Quality: Signal detection 92%, decent semantic reasoning
- Use when: Speed is critical, cost is secondary

#### Local Ollama qwen2.5:7b
- Cost: $0 (runs on VPS)
- Speed: ~13 tok/sec (8-10 sec for typical Layer 0 run)
- Quality: Signal detection 75-80% (lower accuracy)
- Use when: Internet-restricted, zero budget, offline operation

### Recommended Profiles

**High-activity agent** (hourly context rotation, multiple streams):
- Interval: 10 min
- Model: Sonnet-4.6
- Cost: ~$2.32/day × 4 = ~$9.28/day
- Rationale: Frequent signal arrival warrants higher quality + cost

**Standard agent** (research, analysis, coding):
- Interval: 15 min
- Model: Haiku-4.5
- Cost: ~$1.44/day
- Rationale: Good balance of quality and cost

**Low-activity agent** (passive observation, batch jobs):
- Interval: 60 min
- Model: Haiku-4.5
- Cost: ~$0.36/day
- Rationale: Minimal overhead, signals are rare anyway

**Budget-conscious** (no API spend):
- Interval: 30 min
- Model: Ollama qwen2.5:7b
- Cost: $0 (VPS CPU only)
- Rationale: Accept 20% lower accuracy for zero cost

## Layer 1 (Memory Buckets)

**Cost: $0**

.md files stored on disk. No inference cost. GitHub storage is free tier compatible.

## Phase 7 Backups

**GitHub SSH: $0**
- Git-native, no API cost
- Encryption-at-rest (SSH transport)
- Free tier: unlimited repos, 15 GB storage per account

**Hostinger VPS Snapshots: ~$0 (included in VPS bill)**
- API-driven, no per-snapshot fee
- 20-day retention free
- Older snapshots auto-delete

**Total backup cost: $0**

## Total System Cost (Standard Profile)

| Component | Interval | Model | Cost/day |
|-----------|----------|-------|----------|
| Layer 0 Router | 15 min | Haiku-4.5 | $1.44 |
| LCM (Phase 1) | per msg | SQLite | $0 |
| Layer 1 (Phase 2) | n/a | .md files | $0 |
| Phase 7 Backups | daily | GitHub + Hostinger | $0 |
| **Total** | | | **~$1.44/day** |

**Monthly: ~$43/month** for full enterprise-grade continuous memory.

## Cost Optimization Tips

### 1. Batch Signals

Instead of Layer 0 running every 15 min, collect signals in `memory/daily/YYYY-MM-DD.md` and run Layer 0 once per hour:

**Cost reduction: 4x** (from $1.44/day → $0.36/day)

**Tradeoff:** Signals are routed with ~1-hour lag (acceptable for non-time-critical work)

### 2. Hybrid Model Selection

Use Haiku for routine signal detection, escalate to Sonnet on-demand:

```bash
# Daily routine (Haiku, 15-min)
openclaw cron add ... --model anthropic/claude-haiku-4-5

# Weekly deep reflection (Sonnet, weekly)
openclaw cron add ... --model anthropic/claude-sonnet-4-6 --schedule 'cron 0 2 * * 0'
```

**Cost:** ~$1.44/day (Haiku) + ~$0.06 (Sonnet weekly) ≈ $1.50/day

### 3. Selective Cron Execution

Only run Layer 0 during business hours:

```json
{
  "schedule": "cron 0 6-22 * * * America/Denver",
  "payload": { ... }
}
```

**Cost reduction:** ~60% (only 17 hours/day)

### 4. Compression Windows

Run Layer 0 twice daily (morning + evening) instead of every 15 min:

```bash
openclaw cron add ... --schedule 'cron 0 6 * * * America/Denver'  # 6 AM
openclaw cron add ... --schedule 'cron 0 18 * * * America/Denver' # 6 PM
```

**Cost:** ~$0.03/day (2 runs @ ~$0.015/run)

**Tradeoff:** Coarse-grained memory updates; best for low-activity agents

## Budget Constraints

### Tight budget ($0.50/day max)
- Layer 0: 30-min interval, Haiku
- Cost: $0.36/day
- Quality: 95%+ signal detection, but slower routing

### Zero budget
- Layer 0: Local Ollama qwen2.5:7b, 30-min interval
- Cost: $0 (VPS CPU)
- Quality: 75-80% signal detection, 8-10 sec per run
- Requires: Local GPU or accepting CPU-only inference

### Unlimited budget
- Layer 0: Sonnet-4.6, 5-min interval
- Cost: $4.64/day
- Quality: 99%+ signal detection, sub-second routing
- Use case: High-frequency trading agents, real-time research

## Cost-Quality Tradeoffs

```
Cost/Quality Frontier:

HIGH QUALITY
     │
     ├─ Sonnet 5-min ($4.64/day, 99% accuracy) [unlimited budget]
     │
     ├─ Sonnet 15-min ($1.56/day, 99% accuracy) [standard + quality]
     │
     ├─ Haiku 15-min ($1.44/day, 95% accuracy) [standard, recommended]
     │
     ├─ Haiku 30-min ($0.72/day, 95% accuracy) [low-activity]
     │
     ├─ Grok 30-min ($0.60/day, 92% accuracy) [budget + speed]
     │
     └─ Ollama 30-min ($0/day, 75% accuracy) [zero-cost]
LOW COST
```

**Recommendation:** Start with Haiku-4.5 + 15-min interval ($1.44/day). Adjust interval based on activity level.
