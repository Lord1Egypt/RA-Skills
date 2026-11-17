<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 16: Value & Metrics Engine

**Phase:** Operations (repeating)
**Classification:** Extension — opt-in when analytics/data infrastructure exists
**Purpose:** Track product KPIs, measure benefits realization, run experiment/hypothesis loops, and feed value data back into prioritization.

---

## Activation

This stage is an **extension**. It activates when:
- User says "track value" / "measure outcomes" / "benefits realization"
- Data infrastructure is confirmed available (analytics, metrics pipeline)
- Context factor `Data-Driven Capability = Full analytics`

If not activated, skip this stage. Prioritization in Stage 6 operates on qualitative judgment instead of quantitative data.

---

## Steps

### Step 16.1: Define Product KPIs

For each product goal (from Stage 2), define a measurable KPI:

| Goal | KPI | Baseline | Target | Measurement Source |
|------|-----|----------|--------|-------------------|
| Payment <2s | P95 transaction latency | 8s | <2s | APM dashboard |
| 10K MAU | Monthly active users | 0 | 10,000 | Analytics platform |
| Reduce drop-off | Onboarding completion rate | 60% | >80% | Funnel analytics |

**Rules:**
- Every KPI must have: baseline, target, measurement source, and review cadence
- Prefer leading indicators (predict success) over lagging (confirm failure after the fact)
- Max 5-7 KPIs at any time (focus beats coverage)

### Step 16.2: Benefits Realization Tracking

After each release ships, track whether goals were achieved:

| Release | Goal | KPI | Before Release | After Release | Delta | Verdict |
|---------|------|-----|:---:|:---:|:---:|:---:|
| R1 (MVP) | Payment <2s | P95 latency | 8s | 1.8s | -6.2s | ✅ Met |
| R1 (MVP) | Reduce drop-off | Completion rate | 60% | 72% | +12% | ⚠️ Improved but below 80% target |

**Verdicts:** ✅ Met | ⚠️ Partial | ❌ Missed | 📊 Too early to measure

### Step 16.3: Cost of Delay Analysis

For HIGH-priority items, quantify the cost of NOT building them:

```
EPIC-003: Provider Abstraction
• Revenue at risk: $X/month (can't add new providers without it)
• User impact: 0 new payment options until this ships
• Cost of 1-sprint delay: ~$X in lost potential revenue
• WSJF impact: Time Criticality score = 9/10
```

This feeds back into Stage 6 (prioritization) — items with high CoD move up.

### Step 16.4: Experiment/Hypothesis Loops

For features where value is uncertain, design experiments:

| # | Hypothesis | Experiment | Success Metric | Duration | Result |
|---|-----------|-----------|---------------|----------|:---:|
| H1 | One-click payment increases conversion | A/B test: old vs. new flow | Conversion rate +15% | 2 weeks | Pending |
| H2 | Users want crypto payment | Landing page smoke test | >500 sign-ups in 1 week | 1 week | ❌ Failed (87 sign-ups) |

**Rules:**
- Define success/failure criteria BEFORE running the experiment
- Failed hypotheses → remove/deprioritize the related epic
- Validated hypotheses → increase confidence; proceed with full build

### Step 16.5: Feed Metrics Into Prioritization

Value data changes priorities:
- KPI missed after release → create corrective epic (iterate)
- Experiment validated → confidence up → epic priority unchanged or increased
- Experiment failed → epic deprioritized or removed
- CoD analysis reveals high urgency → reprioritize

Log: `POLC-D-NNN: Priority adjusted based on metrics — {description}.`

### Step 16.6: Persist Metrics

Update or create metrics tracking (appended to existing artifacts):
- KPI table in `product-vision.md` (or separate `metrics-dashboard.md` if comprehensive)
- Benefits realization in `release-plan.md` (per-release outcomes)
- Experiment results logged in governance spine: `POLC-L-NNN`

---

## Gate

**Gate 16 — Metrics Reviewed:**

Present to user:
```
Value & Metrics update:
• KPIs tracked: {N}
• Goals on track: {N} ✅ | Partial: {N} ⚠️ | Missed: {N} ❌
• Experiments: {N} running | {N} validated | {N} failed
• Priority adjustments needed: {yes/no}

Continue to next cycle, or end session?
```

---

## Transition

→ **Stage 14: Backlog Operations** (next cycle in standalone mode)
→ **Session end** (chain mode — user returns when needed)

---

*Detail file for AI-POLC Stage 16 | Phase: Operations (Extension)*
