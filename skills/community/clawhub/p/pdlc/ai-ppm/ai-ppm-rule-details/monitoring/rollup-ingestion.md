<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 7: Roll-Up Ingestion

**Phase:** Monitoring & Dashboards
**Purpose:** Read FLO-carried roll-up snapshots from the Project layer and refresh the Portfolio Register with current project-level data. This is how the portfolio stays alive — without ingestion, the register becomes stale.

---

## Layered Communication Rule

> **AI-PPM NEVER reads Project-layer state files directly.** All Project-layer data arrives via AI-FLO (cross-layer upward). FLO assembles the snapshot from multiple Project-layer packages and delivers it keyed by Project ID.

**Fallback (no FLO):** Prompt user for manual status updates per project using a structured questionnaire.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Accept whatever data is available. No anomaly detection. Simple refresh. |
| **Standard** | Full refresh + anomaly detection (deterioration since last ingestion). Flag staleness. |
| **Comprehensive** | Full refresh + anomaly detection + trend analysis + extension E3 (dependency status) + E7 (benefits). |

---

## Step-by-Step Execution

### Step 7.1: Determine Data Source

Check FLO availability:

| FLO Status | Action |
|---|---|
| **Connected** | Scan for FLO roll-up payloads (by Project ID pattern) |
| **Not connected** | Switch to manual fallback (Step 7.1b) |

**Step 7.1b: Manual Fallback**

For each active project, present:

```
📋 Manual status update: {Project Name} (ID: {ID})

| Field | Last Known | Current? |
|-------|-----------|----------|
| Progress % | {last value} | _[  ]_ |
| RAG Status | {🟢🟡🔴} | _[🟢 / 🟡 / 🔴]_ |
| Budget Status | {on track / over / under} | _[  ]_ |
| Top Blocker | {last known or "none"} | _[  ]_ |
| Phase/Stage | {last known} | _[  ]_ |

Quick update or skip? [Update / No change / Skip this project]
```

### Step 7.2: Process Each Roll-Up Payload

For each payload received (via FLO or manual):

```
Extract per Project ID:
├── progress_pct          ← current completion percentage
├── rag_status            ← 🟢 On Track | 🟡 At Risk | 🔴 Off Track
├── current_phase         ← which Project-layer package is active
├── budget_actual         ← spend to date vs. planned
├── velocity_trend        ← accelerating / stable / decelerating
├── compliance_score      ← from GCE (if available)
├── test_coverage_pct     ← from TGE (if available)
├── open_issues           ← count from governance spine
├── top_risks[]           ← top 3 risks from project risk register
├── backlog_health        ← from POLC (size, stale %, refined %)
├── last_updated          ← timestamp of the snapshot
└── blockers[]            ← active blockers (if any)
```

### Step 7.3: Update Portfolio Register

For each project, update the register row with fresh data:

| Column | Source |
|---|---|
| Health (RAG) | `rag_status` from roll-up |
| Progress | `progress_pct` |
| Last Updated | `last_updated` timestamp |
| Phase | `current_phase` |
| Budget Status | Derived from `budget_actual` vs. planned |

### Step 7.4: Anomaly Detection (Standard+ Depth)

Compare current roll-up against previous:

| Anomaly | Trigger | Severity |
|---|---|---|
| **RAG deterioration** | Was 🟢, now 🟡 or 🔴 | Medium / High |
| **Progress stall** | <5% progress change in >2 weeks | Medium |
| **Budget overrun** | Actual exceeds planned by >15% | High |
| **Velocity drop** | Trend changed from stable/accelerating to decelerating | Medium |
| **Compliance drop** | Score dropped >10 points since last ingestion | Medium |
| **New blockers** | blockers[] is non-empty (was empty before) | High |
| **Stale data** | `last_updated` older than 2 weeks | Low (flag only) |

Report anomalies:

```
⚠️ Anomalies detected ({N} total):

| Project | Anomaly | Previous | Current | Severity |
|---------|---------|----------|---------|:--------:|
| {A} | RAG deterioration | 🟢 | 🟡 | ⚠️ Medium |
| {B} | Budget overrun | $80K/$100K | $120K/$100K | 🔴 High |
| {C} | Stale data | 3 weeks old | — | ℹ️ Info |

Recommended actions:
• {A}: Monitor closely — next sync should confirm or escalate
• {B}: Trigger rebalancing (Stage 9) — may need governance decision
• {C}: Request fresh data from project team
```

### Step 7.5: Calculate Portfolio Aggregates

Compute portfolio-level metrics from all project roll-ups:

```
Portfolio Aggregates:
├── Total active projects: {N}
├── Health distribution: {G}🟢 {Y}🟡 {R}🔴 {W}⚪
├── Average progress: {avg}%
├── Total budget (planned): ${sum}
├── Total budget (actual): ${sum}
├── Budget variance: {+/-}${amount} ({percent}%)
├── Projects on track: {N}/{total} ({percent}%)
├── Active blockers: {total count}
└── Data freshness: {oldest timestamp} to {newest}
```

### Step 7.6: Timestamp and Save

- Update `ppm-state.md` → Last Ingestion section
- Save aggregates for Stage 8 (dashboards)

### Step 7.7: Transition

```
✅ Roll-up ingestion complete
   • {N} projects refreshed
   • {M} anomalies flagged
   • Portfolio health: {G}🟢 {Y}🟡 {R}🔴

Proceed to Portfolio Dashboards (Stage 8)? [Yes / Investigate anomaly first / End session]
```

---

## Gate

No explicit gate — ingestion flows naturally into dashboards. However, high-severity anomalies may redirect to Stage 9 (rebalancing) before dashboards.

---

## Outputs

| Artifact | Status |
|---|---|
| `portfolio-register.md` | Updated (health, progress, budget, timestamp) |
| `ppm-state.md` | Updated (last ingestion timestamp, anomaly count) |

---

## Management Framework Contribution

Only if anomalies trigger governance action:
- `PPM-I-{NNN}: Anomaly — {Project Name} budget overrun detected ({amount} over ceiling). Escalation required.`
- `PPM-I-{NNN}: Anomaly — {Project Name} RAG deteriorated to 🔴. Rebalancing recommended.`

---

*This stage runs at every portfolio sync (biweekly) and every health review (monthly). It's the portfolio's heartbeat.*
