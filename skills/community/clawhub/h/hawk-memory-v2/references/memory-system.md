# Four-Tier Memory Architecture

---

## Design Principles

- **Recency first**: most recent memories have highest retrieval weight
- **Load on demand**: not all layers enter context at startup
- **Traceable**: historical content is archived, not deleted

---

## Four Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 0: Working Memory                                    │
│  Location: Memory + LanceDB (working table)                  │
│  Content: Recent 5-10 turns, current task                   │
│  Context: Always injected                                     │
│  Decay: 1 day → Layer 1                                    │
│  Promotion: access_count ≥ 5 → Layer 2                      │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Short-term Memory                                 │
│  Location: LanceDB (shortterm table)                        │
│  Content: 24h dialog, structured summaries                    │
│  Decay: Weibull, half-life 30 days, beta=1.0             │
│  Promotion: access_count ≥ 10 + importance ≥ 0.7 → Layer 2  │
│  Demotion: decay_score < 0.15 → Layer 3                  │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Long-term Memory                                 │
│  Location: LanceDB (longterm table)                         │
│  Content: importance ≥ 0.7 knowledge/decisions/rules        │
│  Decay: Weibull, half-life 90 days, beta=0.6 (slowest)  │
│  Demotion: >90 days unaccessed → Layer 3                   │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Archive Memory                                   │
│  Location: LanceDB (archive table)                           │
│  Content: decay_score < 0.15 or >90 days                   │
│  Context: NOT auto-loaded                                   │
│  Recall: via memory_search on-demand                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Weibull Decay Formula

```
decay_score = exp(-(age_days / half_life) ^ beta)

Composite score = (recency × 0.4) + (frequency × 0.3) + (importance × 0.3)
```

| Layer | Half-life | Beta | Description |
|-------|-----------|------|-------------|
| Working | 1 day | 0.8 | Fast decay |
| Short-term | 30 days | 1.0 | Standard decay |
| Long-term | 90 days | 0.6 | Slowest decay |

---

## Promotion Rules

```
Working → Short-term: 24h unaccessed
Short-term → Long-term: access_count ≥ 10 AND importance ≥ 0.7
Any → Archive: decay_score < 0.15 OR > 90 days unaccessed
```

---

## Startup Loading

On each session start:

1. Load `memory/today.md`
2. Load `memory/week.md`
3. Load `memory/month.md` (if exists)
4. Load Top10 from Working Memory (LanceDB)
5. Load importance Top5 from Short-term Memory
6. **Do NOT auto-load** Long-term and Archive (load on-demand)

---

## LanceDB Table Mapping

| context-hawk layer | memory-lancedb-pro tier |
|-------------------|------------------------|
| Working | Working | Active memories |
| Short-term | Peripheral | Secondary active |
| Long-term | Core | High-value memories |
| Archive | Archived | Decayed memories |

---

## Configuration

```json
{
  "decay.recencyHalfLifeDays": 30,
  "decay.frequencyWeight": 0.3,
  "decay.intrinsicWeight": 0.3,
  "tier.coreAccessThreshold": 10,
  "tier.peripheralAgeDays": 90,
  "auto_check_rounds": 10
}
```
