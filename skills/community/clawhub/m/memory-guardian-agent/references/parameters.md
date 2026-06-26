# parameters.md — Decay Parameters + Dual Mode + Type Alpha

> Complete parameter reference for the five-track Bayesian decay engine. Source: `scripts/memory_decay.py` + `scripts/mg_utils.py`

---

## Core Weights

```
final = (0.35 × importance_factor + 0.35 × network_factor + 0.30 × context_factor) × β_effective
```

| Parameter | Value | Code Constant |
|-----------|-------|---------------|
| IMPORTANCE_WEIGHT | 0.35 | `IMPORTANCE_WEIGHT` |
| NETWORK_WEIGHT | 0.35 | `NETWORK_WEIGHT` |
| CONTEXT_WEIGHT | 0.30 | `CONTEXT_WEIGHT` |

---

## Track 1: importance_factor

- `base = get_effective_importance(mem)` — range [0.0, 1.0]
- Cost signal modifier accumulates then caps at 1.0

| Cost Type | Weight Factor | Code |
|-----------|--------------|------|
| write_cost | × 0.0 | `COST_IMPORTANCE_MODIFIER["write"]` |
| verify_cost | × 0.05 | `COST_IMPORTANCE_MODIFIER["verify"]` |
| human_cost | × 0.10 | `COST_IMPORTANCE_MODIFIER["human"]` |
| transfer_cost | × 0.05 | `COST_IMPORTANCE_MODIFIER["transfer"]` |

---

## Track 2: network_factor

- Base formula: `0.3 + 0.7 × min(raw_access + raw_trigger × 0.5, 1.0)`
- action_conclusion exists → × 1.1 (cap 1.0)
- confidence > 0.7 → × (1 + 0.05 × (confidence - 0.7))

### Cooldown Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| COOLING_THRESHOLD | 5 | Trigger count within 24h to activate cooldown |
| COOLING_NETWORK_CAP | 0.3 | network_factor upper limit during cooldown |
| COOLING_WINDOW_HOURS | 24 | Frequency detection window |

---

## Track 3: context_factor

- `recency = exp(-λ × days_since_creation)` — standard exponential decay
- Accessed within 24h → +0.1 boost (linear decay to 0)
- Accessed within 24-72h → +0.03 boost

---

## Track 5: β (Scar + Idle Decay)

### Log-Smooth β (v0.4.1)

```
β_log_smooth = max(1, 1 + α × ln(idle_days / base_days))
base_days = 7 + importance × 23
```

| Parameter | Default | Configurable | Description |
|-----------|---------|--------------|-------------|
| BETA_ALPHA_DEFAULT | 2.0 | `decay_config.alpha` | Decay sensitivity |
| BETA_BASE_DAYS_CONSTANT | 7 | Fixed | Base days constant |
| BETA_BASE_DAYS_SCALE | 23 | Fixed | Importance scaling |
| BETA_IMPORTANCE_CAP | 1.0 | Fixed | Importance cap (prevents infinite base_days) |
| BETA_CAP | 3.0 | Fixed | β hard cap |
| BETA_ARCHIVE_MARK | 3.0 | Fixed | Above this value, mark as archive candidate |

### Special Cases
- importance < 0.1 → α reduced to 1.0 (gentle decay for very low importance)
- idle_days < base_days → β = 1.0 (no decay)

### Failure Rebound (Scar)

```
failure_boost = min(failure_count × 0.05, 2.0)
time_decay = max(0, 0.02 × days_since_creation / 30)
β_effective = β_log_smooth × (1 + failure_boost) - time_decay
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| FAILURE_REBOUND | 0.05 | β increase per failure |
| FAILURE_BOOST_CAP | 2.0 | failure_boost upper limit |
| BETA_DECAY | 0.02 | Scar fade-over-time rate |
| β lower bound | 0.1 | effective_beta absolute lower bound |

---

## Zombie Detection

| Parameter | Value | Description |
|-----------|-------|-------------|
| ZOMBIE_THRESHOLD_DAYS | 30 | Only active wakeup streak for 30 consecutive days |
| ZOMBIE_ACCELERATION | 1.5 | β multiplied by this value to accelerate decay |

- `passive_wakeup_streak == 0 AND idle_days > 30` → zombie = true
- zombie's β_log_smooth × 1.5

---

## Per-Type Decay (v0.4.2)

| memory_type | α | β_cap | Description |
|-------------|-----|-------|-------------|
| static | 1.0 | 1.0 | bootstrap/core, extremely low decay |
| derive | 2.0 | 3.0 | induced memories, moderate decay |
| absorb | 3.0 | 3.5 | externally absorbed, aggressive decay |
| (no type) | 2.0 | 3.0 | default: derive |

Source: `mg_utils.MEMORY_TYPE_ALPHA_DEFAULTS` + `MEMORY_TYPE_BETA_CAP_DEFAULTS`

---

## TTL (Quadrant Survival Period)

| case_origin | TTL (days) | Description |
|-------------|-----------|-------------|
| absorb | 30 | Fast decay |
| derive | 90 | Moderate |
| new_type | 180 | Slow |
| suspend | 365 | Long-term suspension |

- TTL expired → `final × 0.5` (soft archive)
- 7-day grace period: TTL remaining < 7 days AND recently triggered → extend to 7 days

---

## Archive/Delete Thresholds

| Condition | Action |
|-----------|--------|
| score < 0.2 AND status == active | → archived |
| score < 0.05 | → deleted |
| β ≥ 3.0 | → mark as archive_candidate (no auto-archive) |
