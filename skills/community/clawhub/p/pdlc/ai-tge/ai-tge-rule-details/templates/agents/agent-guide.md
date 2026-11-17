<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-TGE
generatedVersion: "{version}"
source: ai-tge-rules/core-engine.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-TGE AGENT GUIDE SECTION -->

## AI-TGE — Test Governance Agents

AI-TGE ships two complementary governance agents that validate different phases of the test governance lifecycle.

### `test-governance-agent` (TGV__)

**Domain:** Strategy phase validation — test strategy completeness, register integrity, risk scoring
**AG-ID:** TGE-AG-01
**Tier:** 1 (always available)
**Trigger:** `TGV__`

**What it checks (20 checks, 5 categories):**

| Category | Focus | Checks |
|----------|-------|:------:|
| T — Strategy Completeness | Pyramid, goals, data, automation, entry/exit | 5 |
| R — Register Integrity | Source traceability, taxonomy, duplicates, status | 5 |
| S — Risk Scoring | 4-factor scoring, composite, buckets, ordering | 4 |
| C — Coverage Accuracy | Deprecated/overridden exclusion, view consistency | 3 |
| X — Cross-Reference | State file sync, AP version, reconciliation flag | 3 |

**When to call:**
- After AI-TGE Strategy phase completes (Stage 6)
- After architecture reconciliation (Stage 10)
- Before presenting test strategy to team
- Before starting AI-DLC v1 build (confirms governance is in place)

**Recovery if skipped:** Run `TGV__` at any time — it reads current `.governance/test/` state. Fix gaps by re-deriving from AP, re-scoring risks, or updating state file counts.

---

### `coverage-review-agent` (CVR__)

**Domain:** Observation phase validation — coverage trend analysis, gap progression, debt movement
**AG-ID:** TGE-AG-02
**Tier:** 1 (always available)
**Trigger:** `CVR__`

**What it checks (15 checks, 4 categories):**

| Category | Focus | Checks |
|----------|-------|:------:|
| G — Gap Analysis | New gaps since last check, gap aging, regression detection | 4 |
| P — Progress Tracking | Tests added vs. required, velocity trend, sprint targets | 4 |
| D — Debt Movement | Score changes, bucket migrations, Critical count trend | 4 |
| I — Integrity | Register ↔ coverage report sync, observation timestamp, story mapping | 3 |

**When to call:**
- After any coverage report generation (Stage 9)
- At sprint boundaries (confirms debt priorities for planning)
- Before release decisions (full coverage quality gate)
- When team asks "are we testing enough?"

**Recovery if skipped:** Run `CVR__` at any time. It compares current register state against coverage report. Gaps show immediately — no historical data required (though trends require >1 observation).

---

### Relationship Between TGV__ and CVR__

```
Strategy Phase ──► TGV__ validates strategy + register
                        │
                        ▼
Observation Phase ──► CVR__ validates coverage + trends
                        │
                        ▼
Release Decision ──► BOTH — full governance quality gate
```

**TGV__** ensures the *plan* is sound (what SHOULD be tested, is it traceable?).
**CVR__** ensures the *execution* is sound (what IS tested, are gaps shrinking?).

Neither replaces the other. Call both at release gates for complete validation.

<!-- END AI-TGE AGENT GUIDE SECTION -->
