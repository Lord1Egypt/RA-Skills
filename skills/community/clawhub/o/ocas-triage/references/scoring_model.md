# Triage Scoring Model

---

## Priority Score Formula

```
priority_score = urgency_score
              + deadline_proximity
              + consequence_weight
              + interruption_intent
              + quick_completion_bonus
              + queue_aging

Clamp result: min 0, max 100
```

All components are additive. Multiple components may fire on the same task.

---

## Component Definitions

### Urgency score (+40)

Fired when the input contains explicit urgency language.

Signal phrases: now, urgent, right away, ASAP, immediately, before [meal/time],
this is time-sensitive, can't wait

Example: "Change the reservation right away" → +40

---

### Interruption intent (+35)

Fired when the input signals the user wants to override or redirect current
work.

Signal phrases: actually, wait, hold on, change that, stop, before you do that,
scratch that, forget the last thing

Example: "Actually, before you research hotels — cancel the dinner reservation"
→ +35 interruption intent, likely also triggers urgency

---

### Deadline proximity

Fired when a deadline is present (explicit or inferred).

| Condition | Points |
|---|---|
| Deadline within 1 hour | +35 |
| Deadline same day | +20 |
| Deadline within week | +10 |

Only the highest-matching tier fires. Tiers do not stack.

Inferred deadline example: "Change the 7pm reservation" — if the reservation
time is known, infer deadline as the reservation time minus a reasonable
buffer (default 30 minutes).

---

### Consequence weight (+30)

Fired when delay could cause material loss or friction.

Signal categories:
- Reservations (restaurant, hotel, travel, tickets)
- Financial transactions (payments, transfers, purchases with deadlines)
- Coordination with other people (scheduling, commitments made to others)

Example: "Confirm the hotel booking before the hold expires" → +30

---

### Quick completion bonus

Fired based on estimated completion time. Incentivizes clearing quick wins
before large tasks consume the slot.

| Estimated time | Points |
|---|---|
| < 10 seconds | +40 |
| < 1 minute | +25 |
| < 5 minutes | +15 |
| < 30 minutes | +5 |

Only the highest-matching tier fires.

---

### Queue aging (+2/hr, max +20)

Applied on every priority recalculation cycle (every 60 seconds).

Ensures tasks do not stagnate indefinitely.

`aging_bonus = min(floor(hours_waiting * 2), 20)`

Tasks in `waiting_external` do not accrue aging — they are blocked on external
resolution, not on queue position.

---

## Task Selection Formula

After scoring, selection uses value-per-time:

```
task_score = priority_score / max(estimated_completion_seconds / 60, 1)
```

The denominator converts seconds to minutes, floored at 1 to avoid division
by zero. A 10-second task with priority 80 scores 80/(10/60) = 480, surfacing
ahead of a 30-minute task with priority 90 (score 3.0).

### Tie-breaking (identical task_score)

Apply in order:
1. Earlier deadline wins
2. Shorter `estimated_completion_seconds` wins
3. Older `created_at` wins (FIFO as final tiebreaker)

---

## Preemption Threshold

A new task triggers preemption of the active task when:

```
new_task.priority_score - active_task.priority_score > 25
```

The threshold is evaluated on raw `priority_score`, not `task_score`.

On preemption:
- active task is checkpointed and returned to `queued`
- resume bonus: +10 added to its `priority_score` on return
- queue aging continues from original `created_at`

---

## Estimation Heuristics

Initial estimates are heuristic. Refine using `history.jsonl` over time.

| Bucket | Seconds | Signals |
|---|---|---|
| < 10 seconds | 5 | Single lookup, factual answer, simple status |
| < 1 minute | 30 | Short draft, quick search, simple calculation |
| 1–10 minutes | 300 | Research task, multi-step retrieval, short writing |
| 10–30 minutes | 1200 | Complex research, multi-skill coordination, long draft |
| > 30 minutes | 3600 | Long-running project, multi-stage analysis |

Null estimates default to 1800 seconds (30 minutes).

Estimation accuracy is tracked as an OKR. Target: ≥ 0.75 of tasks complete
within their estimated bucket.

---

## Scoring Examples

**"Change the dinner reservation to 7:30, it's in 45 minutes"**
- Urgency: none explicitly, but deadline proximity fires
- Deadline proximity: within 1 hour → +35
- Consequence: reservation → +30
- Quick completion: <1 minute → +25
- Total before aging: 90 → clamped to 100

**"Research hotels in Kyoto for the trip next month"**
- No urgency, no interruption, deadline within week → +10
- Consequence: none
- Estimated completion: 10–30 minutes → +5
- Total: 15 (+ aging over time)

**"Actually, before the hotel research — send Shannon a message about dinner"**
- Interruption intent → +35
- Quick completion (short message): <1 minute → +25
- Total: 60 — will preempt the Kyoto research task (60 - 15 = 45 > 25 threshold)
