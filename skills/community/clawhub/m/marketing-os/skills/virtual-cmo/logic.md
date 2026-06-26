# Virtual CMO — Core Logic

## Role

The Virtual CMO is the **strategic brain** of the Marketing OS. It does NOT execute campaigns. It analyzes, decides, and directs.

---

## Workflow (Step-by-Step)

### Step 1: Ingest Context

**Input Sources:**
- `market_data` — External signals (trends, competitors, audience signals)
- `business_context` — Internal constraints (products, budget, brand)
- `memory/market-insights.json` — Historical market knowledge
- `memory/learnings.json` — Past campaign learnings

**Action:** Merge all inputs into a unified context object. Flag any missing data with `"confidence": "low"`.

---

### Step 2: Market Analysis

**Prompt Used:** `prompts/cmo-analysis.txt`

**Processing Logic:**
1. Identify all observable market signals
2. Classify each signal by type: `demand`, `competition`, `trend`, `risk`
3. Assign a `signal_strength` score (1-10) based on:
   - Recency of data
   - Number of corroborating sources
   - Magnitude of change
4. Flag signals with `signal_strength < 4` as `"uncertain"`

**Output:** Structured list of signals with scores

---

### Step 3: Opportunity Identification

**Processing Logic:**
1. Cluster related signals into opportunity groups
2. For each opportunity, assess:
   - **Market size** (estimated TAM/SAM)
   - **Competition intensity** (low / medium / high)
   - **Alignment with business capabilities** (0-10)
   - **Urgency** (time-sensitive or evergreen)
3. Generate a `priority_score` (0-100) using weighted formula:
   ```
   priority_score = (signal_strength * 0.3) + (market_size * 0.25) + (capability_fit * 0.25) + (urgency * 0.2)
   ```

---

### Step 4: Strategy Formulation

**Prompt Used:** `prompts/cmo-strategy.txt`

**Processing Logic:**
1. For the top 3 opportunities (by `priority_score`):
   - Define target audience segments
   - Define positioning statement
   - Recommend channels (ranked by expected ROI)
   - Define success metrics (KPIs)
   - Identify risks and mitigations
2. Produce a ranked list of `recommended_actions`
3. Each action must have: `action`, `priority`, `expected_impact`, `risk_level`

---

### Step 5: Generate Output

**Output Schema:** `schemas/cmo_output.schema.json`

All outputs must include:
- `market_opportunities[]` — Scored and ranked
- `target_segments[]` — With persona details
- `priority_score` — Overall strategic priority
- `recommended_actions[]` — Concrete next steps
- `risks[]` — Each with severity and mitigation
- `next_steps[]` — Immediate actions for Operator
- `confidence_level` — Overall confidence in the analysis
- `data_gaps[]` — What information is missing

---

### Step 6: Dispatch to Operator

**Output Schema:** `schemas/cmo_to_operator.schema.json`

Generate a mission brief containing:
- `mission_id` — Unique identifier
- `objective` — Clear, measurable goal
- `target_audience` — From Step 4
- `strategy` — Positioning + channel strategy
- `priority` — critical / high / medium / low
- `recommended_channels[]` — Ranked list
- `actions[]` — Specific tasks for Operator
- `success_criteria` — How to measure success
- `constraints` — Budget, timeline, brand guidelines

---

### Step 7: Update Memory

Write to:
- `memory/market-insights.json` — New signals and opportunities
- `memory/learnings.json` — Any new patterns identified

---

## Decision Rules

| Condition | Action |
|---|---|
| `signal_strength >= 7` | Mark as high-confidence, recommend immediate action |
| `signal_strength 4-6` | Mark as moderate, recommend validation |
| `signal_strength < 4` | Mark as uncertain, recommend more data collection |
| No data available | Explicitly output `"status": "insufficient_data"`, do NOT guess |
| Conflicting signals | Present both sides, recommend A/B test |

---

## Interaction with Marketing Operator

- CMO **sends** mission briefs via `cmo_to_operator.schema.json`
- CMO **receives** feedback via `feedback.schema.json`
- CMO **never** directly executes tasks
- CMO **adjusts strategy** when feedback indicates underperformance (priority_score delta > 15%)

---

## Error Handling

- If `business_context` is missing → HALT, return error with `"missing_required_input": "business_context"`
- If all signals have `signal_strength < 3` → Output analysis with `"recommendation": "delay_action"` and `"reason": "insufficient_market_signal"`
- If memory files are corrupted/empty → Proceed with available data, flag `"memory_status": "degraded"`
