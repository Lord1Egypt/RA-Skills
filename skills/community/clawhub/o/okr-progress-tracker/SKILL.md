---
name: cm-okr-progress-tracker
description: Track and evaluate OKR (Objectives and Key Results) progress by parsing OKR definitions from markdown, YAML, or JSON files. Scores key results, calculates objective health, predicts end-of-quarter outcomes, identifies at-risk goals, and produces actionable recommendations. Use when asked to track OKRs, evaluate key results, check OKR progress, predict quarter outcomes, audit objectives, score OKR health, or review goal tracking. Triggers on "OKR", "objectives and key results", "key results", "OKR progress", "OKR tracker", "quarter goals", "OKR health", "objective tracking", "goal tracking", "OKR score", "OKR review".
metadata:
  tags: ["okr", "objectives", "key-results", "goal-tracking", "strategy", "planning", "quarterly-review", "performance", "project-management"]
---

# OKR Progress Tracker

Track, evaluate, and forecast OKR (Objectives and Key Results) progress by analyzing your OKR definitions, current metrics, and time elapsed in the quarter. Identifies at-risk objectives, flags stalled key results, and provides data-driven recommendations for course correction.

## Usage

Invoke this skill when you need to assess OKR progress, prepare for a quarterly review, or identify which objectives need attention.

**Basic invocation:**
> Track OKR progress from okrs.yaml
> Evaluate our Q2 OKRs in /path/to/okrs.md

**With options:**
> Score OKRs and predict end-of-quarter outcomes
> Which OKRs are at risk? Check /team/okrs/
> Generate an OKR health report for the leadership review

The agent reads your OKR files, calculates progress, and produces a structured assessment.

## How It Works

### Step 1: Parse OKR Definitions

The agent reads OKR files in any of the supported formats and builds an internal model.

**Supported formats:**

**Markdown format:**
```markdown
## Objective: Improve platform reliability
- KR1: Reduce P1 incidents from 12/quarter to 3/quarter (current: 7)
- KR2: Achieve 99.95% uptime (current: 99.91%)
- KR3: Mean time to recovery under 15 minutes (current: 23 min)

## Objective: Accelerate developer velocity
- KR1: CI pipeline p95 under 8 minutes (current: 11 min)
- KR2: Deploy frequency from 2/week to 5/week (current: 3/week)
- KR3: Onboarding time for new devs under 3 days (current: 5 days)
```

**YAML format:**
```yaml
quarter: Q2 2026
start_date: 2026-04-01
end_date: 2026-06-30
objectives:
  - name: Improve platform reliability
    owner: platform-team
    key_results:
      - description: Reduce P1 incidents per quarter
        start_value: 12
        target_value: 3
        current_value: 7
        unit: incidents/quarter
        direction: decrease
      - description: Achieve monthly uptime target
        start_value: 99.85
        target_value: 99.95
        current_value: 99.91
        unit: percent
        direction: increase
```

**JSON format:**
```json
{
  "quarter": "Q2 2026",
  "objectives": [
    {
      "name": "Improve platform reliability",
      "key_results": [
        {
          "description": "Reduce P1 incidents",
          "start": 12, "target": 3, "current": 7
        }
      ]
    }
  ]
}
```

The agent auto-detects the format and normalizes internally. It handles partial data gracefully, asking the user for missing fields only when critical (like target values).

### Step 2: Determine Quarter Timeline

The agent calculates where you are in the quarter:

```
Quarter: Q2 2026 (April 1 - June 30)
Today: April 30, 2026
Elapsed: 30 of 91 days (33.0%)
Remaining: 61 days
Weeks remaining: 8.7
```

This timeline is critical for pace analysis: if 33% of time has passed, key results should ideally be at ~33% progress to be on track.

### Step 3: Score Each Key Result

For each key result, the agent calculates:

**Progress percentage:**
```
progress = (current - start) / (target - start) * 100

Example: P1 incidents
  start=12, target=3, current=7
  progress = (12 - 7) / (12 - 3) * 100 = 55.6%
```

**Pace ratio** (progress vs. time elapsed):
```
pace = progress_pct / time_elapsed_pct

Example: 55.6% progress / 33.0% time elapsed = 1.68x pace
  > 1.0 = ahead of schedule
  = 1.0 = on track
  < 1.0 = behind schedule
  < 0.5 = significantly at risk
```

**Projected end-of-quarter value** (linear extrapolation):
```
projected = start + (current - start) * (total_days / elapsed_days)

Example: P1 incidents
  projected = 12 + (7 - 12) * (91 / 30) = 12 + (-5 * 3.03) = -3.2
  Clamped to achievable range: projected = 0 incidents (exceeds target)
```

**Confidence level** based on:
- Pace ratio
- Variance in progress (if historical data points available)
- Time remaining (more time = more uncertainty)
- Whether progress follows a linear, exponential, or step-function pattern

### Step 4: Classify Key Result Health

Each key result receives a health classification:

| Status | Criteria | Symbol |
|--------|----------|--------|
| **On Track** | Pace ratio >= 0.9 | [=] |
| **Needs Attention** | Pace ratio 0.6 - 0.9 | [~] |
| **At Risk** | Pace ratio 0.3 - 0.6 | [!] |
| **Off Track** | Pace ratio < 0.3 | [X] |
| **Achieved** | Current meets or exceeds target | [+] |
| **Not Started** | No progress from start value | [-] |

The agent adjusts thresholds based on quarter progress. Early in the quarter, it applies wider tolerances (some KRs ramp up late). Late in the quarter, thresholds tighten.

### Step 5: Roll Up to Objective Health

Each objective score is the weighted average of its key results:

```
Objective Score = average(KR1_progress, KR2_progress, KR3_progress)
```

The agent applies a "weakest link" modifier: if any single KR is Off Track, the objective health is capped at "Needs Attention" regardless of other KRs, since objectives require all key results to be meaningful.

**Objective health classifications:**
- **Strong (0.7-1.0)**: Most KRs on track or achieved
- **Moderate (0.4-0.7)**: Mixed progress, some KRs lagging
- **Weak (0.0-0.4)**: Majority of KRs behind schedule
- **Critical**: Any KR at 0% progress past 50% of quarter

### Step 6: Trend Analysis (If Historical Data Available)

If the user provides multiple snapshots or the OKR file includes a history of values, the agent performs trend analysis:

- **Velocity calculation**: rate of progress per week
- **Acceleration/deceleration**: is progress speeding up or slowing down?
- **Plateau detection**: has a KR stalled (no movement in 2+ weeks)?
- **Trajectory plotting**: when will the KR hit its target at current velocity?

```
KR: Reduce P1 incidents (target: 3)
  Week 1: 12 -> 11 (-1)
  Week 2: 11 -> 9  (-2)
  Week 3: 9  -> 7  (-2)
  Week 4: 7  -> 7  (0)   <-- STALL DETECTED

  Current velocity: -1.25/week (slowing)
  At current velocity: target reached in week 7 (on schedule, but decelerating)
  Risk: Plateau pattern suggests operational changes needed
```

### Step 7: Generate Recommendations

For each at-risk or off-track key result, the agent produces actionable recommendations:

**For stalled KRs:**
- Identify what changed around the stall point
- Suggest owner check-in or scope reassessment
- Recommend breaking the KR into intermediate milestones

**For behind-pace KRs:**
- Calculate the required weekly progress to still hit the target
- Flag if the required pace is unrealistic (e.g., need 3x current velocity)
- Suggest scope reduction, additional resources, or target adjustment

**For on-track KRs:**
- Identify if the KR was sandbagged (too easy) based on early completion
- Suggest stretch goals if applicable

**For objectives with mixed KRs:**
- Identify which KR is the bottleneck
- Suggest rebalancing effort across KRs
- Flag dependency chains between KRs

### Step 8: Produce the Report

The agent generates a structured report:

```
# OKR Progress Report — Q2 2026
# Snapshot: April 30, 2026 (33% through quarter)

## Overall Health: Moderate (0.58)
  2 objectives on track, 1 needs attention

## Objective 1: Improve Platform Reliability
   Health: Strong (0.72) | Owner: platform-team

   [=] KR1: Reduce P1 incidents to 3/quarter
       Progress: 55.6% | Pace: 1.68x | Projected: 0 (exceeds target)
       Status: Ahead of schedule

   [~] KR2: Achieve 99.95% uptime
       Progress: 60.0% | Pace: 1.18x | Projected: 99.97%
       Status: On track, slight deceleration in week 4

   [!] KR3: MTTR under 15 minutes
       Progress: 27.6% | Pace: 0.84x | Projected: 18.2 min
       Status: NEEDS ATTENTION — will miss target at current pace
       Recommendation: Need to improve by 1.3 min/week (currently 0.8 min/week).
         Consider automated runbook rollout to reduce manual investigation time.

## Objective 2: Accelerate Developer Velocity
   Health: Moderate (0.51) | Owner: dx-team
   ...

## At-Risk Summary
  1. KR3 (MTTR) — pace 0.84x, needs 63% increase in improvement rate
  2. KR5 (Onboarding) — pace 0.55x, recommend reducing target to 4 days

## Recommendations
  1. Schedule deep-dive on MTTR with on-call team this week
  2. Reassess onboarding KR target — 3 days may be unrealistic given hiring freeze
  3. KR1 (P1 incidents) likely to be achieved early — consider stretch target
```

## Output

The agent produces:

- **Executive summary**: overall OKR health score, count of on-track vs. at-risk objectives
- **Per-objective breakdown**: health score, owner, and per-KR detail
- **Per-KR metrics**: progress %, pace ratio, projected end value, health status
- **At-risk register**: ranked list of KRs most likely to miss targets
- **Recommendations**: 3-7 specific, actionable recommendations with rationale
- **Timeline context**: days remaining, percentage through quarter, required pace adjustments

Output formats:
- **Narrative** (default): human-readable report for standup or review meetings
- **Table**: compact tabular view for dashboards
- **Detailed**: includes trend analysis, historical data points, and confidence intervals

## Advanced Features

### Cascade Analysis

When OKRs reference each other (company -> team -> individual), the agent traces the cascade:

```
Company OKR: Grow revenue 30% YoY
  └─ Team OKR: Launch 3 enterprise features
      └─ Individual OKR: Ship SSO integration by May 15
         Status: At Risk (blocked on IdP vendor)
         Impact: Delays team OKR, which delays company revenue feature pipeline
```

### Cross-Team Dependency Detection

The agent identifies when one team's KR depends on another team's work:

```
WARNING: Team Alpha's KR2 (API v3 migration) depends on
Team Beta's KR1 (schema redesign), which is Off Track.
Team Alpha's KR2 is at risk regardless of their own progress.
```

### Scoring Calibration

The agent supports different scoring methodologies:
- **Google-style (0.0-1.0)**: 0.7 = fully met expectations, 1.0 = exceptional
- **Binary**: met/not met per KR
- **Percentage**: raw progress percentage
- **Traffic light**: green/yellow/red

### Quarter-over-Quarter Comparison

If previous quarter OKR files are available, the agent compares:
- Score improvement or regression per objective area
- KR target ambition levels (are targets getting harder or easier?)
- Recurring at-risk themes (same area struggling quarter after quarter)

## Tips for Best Results

- Include `start_value`, `target_value`, and `current_value` for each KR to get accurate scoring
- Specify `direction` (increase/decrease) when it is not obvious from context
- Update `current_value` weekly for trend analysis to work
- Include owner information to enable team-level rollups
- Store OKR files in version control to enable quarter-over-quarter comparison
- Use consistent KR formats: quantitative targets are scored much more accurately than qualitative ones
