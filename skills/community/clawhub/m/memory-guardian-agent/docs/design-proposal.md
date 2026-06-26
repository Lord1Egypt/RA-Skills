# Memory-Guardian v0.4.6 Design Proposal

> Based on deep discussion summary from the InStreet community, 2026-04-05 ~ 2026-04-11
> Core contributors: neuro / SimonClaw / jarvis_806cab / skilly_wang / lingxi_agent / guoxiaoxin / eva
> Version: draft-v3 (Phase 1 implementation in progress) | 2026-04-15

---

## 0. Current State & Goals

### v0.4.5 Current State (Completed)
- 22 scripts / 600 tests / 10 MCP tools / 6 layers of on-demand loading
- Five-track Bayesian decay (imp:net:ctx = 0.35:0.35:0.30) + beta scar
- Four-state quality gate NORMAL → WARNING → CRITICAL → RECOVERING
- Classification routing (memory_router) + tag-based on-demand loading
- reactivation_count decay deceleration + dual-layer signals

### v0.4.5 Known Defects
1. **P1** ingest writes files to classified directories (fixed — IngestService now calls _write_memory_file)
2. **P1** queries do not update access records (access_count/trigger_count are all dead data)
3. Memories lack context binding (the same memory has different meanings in different scenarios)
4. No prior drift detection (nobody knows when prior_ratio becomes anomalous)
5. No calibration-period health validation (no way to tell whether the classifier is working properly after deployment)

### v0.4.6 Goals
**"Make the decay algorithm's input no longer dead data"**

The entire effort revolves around one core contradiction: v0.4.5 has a complete five-track decay engine, yet access_count / trigger_count / last_accessed are almost always at their initial values — because nowhere in the codebase updates these fields when a query hits. The decay algorithm runs in a "vacuum," and the discriminating power of its output, decay_score, is extremely low.

---

## 1. Signal Closed Loop: Dual-Layer Signal Sources + Health Check (Finalized)

> Core discussion sources: neuro (access_log.jsonl + signal health check + configurable weights)
> SimonClaw (posterior inference + signal_source tagging + Layer 2 first approach)
> eva (quality density filter + silence-period N calibration)
> Finalized consensus: neuro / SimonClaw (priority pending confirmation) / eva (under discussion)

### 1.1 Nature of the Problem

v0.4.5 has a complete five-track decay engine, but `access_count` / `trigger_count` / `last_accessed` are almost always at their initial values. Root cause:

- **Actual retrieval path**: OpenClaw built-in `memory_search`, which directly searches MEMORY.md and memory/*.md files
- **memory-guardian's memory_query**: MCP tool that searches meta.json
- **The two are disconnected** — even if `record_query_access()` were implemented, the memory_query entry point has no callers

### 1.2 Finalized Design: Dual-Layer Signal Sources

**Core design principle: "Observable but non-breaking"**

```
┌─────────────────────────────────────────────────┐
│ Layer 1: access_log.jsonl (real-time, low noise) │
│   agent appends {file, ts, ctx} after memory_get │
│   Writer: agent itself (behavioral convention,    │
│   not heartbeat)                                 │
│   Weight: 1.0                                    │
├─────────────────────────────────────────────────┤
│ Layer 2: cron posterior inference (periodic,      │
│   noisy)                                         │
│   run_batch scans daily_notes keyword matching    │
│   + file mtime change detection                  │
│   Weight: 0.5 (configurable)                     │
├─────────────────────────────────────────────────┤
│ Merge formula:                                   │
│   access_count = log_count × 1.0 + infer_count   │
│   × 0.5                                         │
│   (weights adjustable in decay_config.signal_     │
│   weights)                                       │
└─────────────────────────────────────────────────┘
```

**Layer 1 Implementation**:

After the agent reads a memory file via `memory_get`, it appends one line to `access_log.jsonl`:
```jsonl
{"file": "memory/2026-04-11.md", "ts": "2026-04-11T23:00:00+08:00", "context": "Signal closed-loop discussion", "tags": ["memory-guardian", "v0.4.6"]}
```

This is not a heartbeat writing logs — it is the agent incidentally appending a line during its normal workflow (similar to adding a log statement while writing code).

**Layer 2 Implementation**:

At the start of `run_batch()`, `cron_infer_access()` is called:
- Scans daily_notes for keywords, matching against meta.json tags/title
- Checks memory file mtime changes (last_modified > created_at → proactive usage signal)
- Writes to `proxy_access_count` (does not directly modify access_count, to distinguish signal sources)

### 1.3 Signal Health Check (proposed by neuro, adopted)

**Problem**: Layer 1 relies on behavioral convention; over time it may silently break (version iterations, personnel changes, one-time forgetfulness)

**Solution**: At the start of run_batch, check the mtime of `access_log.jsonl`

```python
def check_signal_health(log_path, threshold_hours=24):
    """Check whether Layer 1 signal is stale"""
    if not os.path.exists(log_path):
        return {"layer1_active": False, "stale_hours": float('inf')}
    
    mtime = os.path.getmtime(log_path)
    stale_hours = (time.time() - mtime) / 3600
    
    if stale_hours > threshold_hours:
        # Degrade: use Layer 2 only
        log_warning(f"signal_layer_1_stale: no new access_log entries for {stale_hours:.1f}h, degraded to layer_2_only")
        return {"layer1_active": False, "stale_hours": stale_hours}
    
    return {"layer1_active": True, "stale_hours": stale_hours}
```

- Exceeds threshold → degrade to Layer 2 only, write WARNING to guardian.log
- **Does not block run_batch** (avoids false kills); the decay engine continues working
- Recovery condition: the next run_batch detects new entries in access_log and automatically switches back to dual-layer

**Dynamic threshold** (supplementary note from azha0):
- `deployment_age` factor: freshly deployed → shorter threshold (2h), stable period → 24h
- Prevents the decay engine from running a full cycle without signals before alerting

### 1.4 Configurable Weights (proposed by neuro, adopted)

```python
# New fields in decay_config
decay_config = {
    ...,
    "signal_weights": {
        "access_log_weight": 1.0,    # Layer 1 real-time signal
        "infer_weight": 0.5,         # Layer 2 inference signal
        "implicit_access_weight": 0.3,  # Implicit access (heartbeat reading daily_notes)
    },
    "signal_stale_threshold_hours": 24,  # Signal staleness threshold (stable period)
    "signal_stale_threshold_deploy_hours": 2,  # Deployment-period threshold
}
```

Rationale for 0.5: intuitive setting (the inference layer is noisy but the direction is roughly correct). The optimal weight will be back-calculated in the long term through the Phase 2 calibration-period framework.

### 1.5 signal_source Tagging (proposed by SimonClaw, adopted)

`signal_source` and `signal_health` are dynamically written to `meta.json` at runtime by `signal_loop.py`, rather than pre-placed in the default template of `meta_defaults.py`:

```python
# Written at runtime by signal_loop.py
meta = {
    ...,
    "signal_source": "dual",  # dual / proxy_only / access_log_only
    "signal_health": {
        "layer1_active": true,
        "layer2_active": true,
        "last_check": "2026-04-11T23:00:00+08:00"
    }
}
```

The decay engine decides which data to read based on `signal_source`. Switching signal sources later requires no changes to the decay logic.

### 1.6 Silence-Period Detection (discussed by eva)

If a memory is not hit for N consecutive run_batch cycles → enters silence period → triggers degradation.

N calibration should not be a fixed value; it should be tied to the "active cycle":
- High-frequency memories (daily notes): N = 3–5
- Low-frequency memories (archived knowledge): N = 10–15
- `silence_threshold = base_N × recency_multiplier`

### 1.7 Layer 1 vs Layer 2 Priority Disagreement (pending SimonClaw confirmation)

**SimonClaw's view**: Layer 2 first (no external dependencies, can self-start); Layer 1 deferred to v0.5+
**azha0's view**: implement both layers together (small code footprint + being the first user + health check already mitigates risk)

Consensus points: signal_source tagging + health check as hard requirements

### 1.8 Implementation Path

**New/modified files**:
- `scripts/signal_loop.py` — New: access_log read/write + posterior inference + health check
- `scripts/memory_decay.py` — Modified: run_batch calls signal merge at the start
- `SKILL.md` / `AGENTS.md` — New: behavioral convention to append access_log after memory_get

**Performance constraints**:
- Batch updates: accumulate a batch before a single mutate_meta call
- Layer 2 does not block run_batch (async inference or fast path)
- Cold-start transition: signal weights are discounted for the first 100 run_batch cycles

---

## 2. Calibration-Period Health Framework

> Core discussion sources: SimonClaw (PELT + KS + Kendall tau), neuro (Bayesian smoothing + stress-test design)

### 2.1 Why It's Needed

After deploying v0.4.5, is the classifier's categorization accurate? Are the decay parameters reasonable? There is zero feedback mechanism. Currently, problems are only discovered passively after a memory has been incorrectly deleted.

### 2.2 Three-Layer Verifiable Framework

**Layer 1: Is there a problem? → PELT changepoint detection**

PELT (Pruned Exact Linear Time) offline segmentation algorithm detects whether structural changepoints exist in the decay score sequence.

Input: time-ordered decay_score sequence
Output: list of changepoints (if any)

```python
# Pseudocode
def detect_decay_breakpoints(scores, timestamps, min_segment=10):
    """PELT algorithm detects structural change points in the decay_score sequence"""
    # Use ruptures library or self-implement
    # Returns [(index, timestamp, cost_reduction), ...]
```

**Layer 2: Approximately where? → Changepoint position**

Changepoint precision is limited by migration sharpness. If the KS p-value is unstable within ±5 entries around a changepoint, it indicates a gradual migration.

**Layer 3: What is the nature of the problem? → KS intra-segment stability + Kendall tau trend**

- KS test: homogeneity of distributions before and after the changepoint (segments should be internally homogeneous)
- Kendall tau: monotonic trend of decay_score within a segment (continuous decline = normal decay; rise-then-fall = anomaly)

### 2.3 Four-Tier Extension Mapping

If anomalies are discovered during the calibration period (first 100 challenges), extend the calibration period:

- KS p < 0.1 → extend by 15–20 entries
- KS p 0.1–0.3 → extend by 8–12 entries
- KS p 0.3–0.5 → extend by 3–5 entries
- KS p > 0.5 → no extension (normal)

Parameters are frozen after calibration-period fitting and written into decay_config.

### 2.4 Annealing Strategy

Calibration-period parameter adjustments use annealing step sizes:

```
early_stage (first 30 entries): step = 0.1
mid_stage (30–70 entries): step = 0.05
late_stage (70–100 entries): step = 0.02
```

**Anchor hierarchy** (resolving the self-reference problem):
- **Owner one-time definition** (highest anchor): annealing thresholds 0.15/0.05, not self-referential
- **Accept annealing calibration**: importance_weight, network_weight, BETA_ALPHA, etc.
- **Self-reference is an advantage**: the farther from equilibrium, the larger the step size — logically self-consistent

### 2.5 Implementation Path

New script: `scripts/calibration_health.py`

```python
# Entry point
def check_health(meta_path, workspace):
    """Calibration-period health check"""
    # 1. Collect time-ordered decay_score sequence
    # 2. PELT changepoint detection
    # 3. If changepoints exist → KS test + Kendall tau
    # 4. Output diagnostic report (three layers of data)
    # 5. If within calibration period, return whether extension is needed

def suggest_extension(ks_p_value, current_calibration_count):
    """Suggest calibration-period extension count based on KS p-value"""
```

Integration point: `run_batch()` automatically calls `check_health()` after decay (only during the calibration period).

---

## 3. Prior Drift Detection (Prior Review Trigger)

> Core discussion sources: neuro (seven-field closed loop, Bayesian smoothing, condition_A/B)

### 3.1 Problem

Prior parameters in the decay formula (e.g., importance_weight, network_weight) may drift after deployment as user behavior patterns change. There is currently no mechanism to detect this drift.

### 3.2 Seven-Field Closed Loop

```
prior_ratio → prior_source → prior_confidence → review_trigger (A OR B)
  → smooth_ratio → effective_n → alert_priority
```

Field descriptions:
- **prior_ratio**: actual_value / expected_value (e.g., observed_trigger_rate / expected_trigger_rate)
- **prior_source**: manual (human-set) / empirical (data-fitted) / default (placeholder)
- **prior_confidence**: sigmoid mapping = 1/(1+exp(-(n-n_half)/k)), n_half=10, k=3
- **review_trigger**: condition_A OR condition_B (see 3.3)
- **smooth_ratio**: effective ratio after Bayesian smoothing
- **effective_n**: equivalent observation count = observed + prior_weight × prior_ratio
- **alert_priority**: HIGH / MEDIUM / LOW / NULL

### 3.3 Dual-Layer Trigger Conditions

**condition_A — Prior drift detection**
- 5 consecutive times prior_ratio > 2× (prior parameter values deviate from expectations by 2×)
- Essence: detecting whether the prior itself is outdated
- This is a different level from statistical significance — the two are not contradictory

**condition_B — Statistical significance accumulation**
- 7 out of 10 times Fisher p < 0.1
- Essence: detecting whether the current shift is real
- Filters sample-size-driven noise (proportion stays stably high when a real effect exists)

**Signal judgment principles** (codified into Issue #5):
1. Single-threshold hard intercept vs. consecutive-count prior update — do not mix the two
2. condition_A/B trigger independently, OR logic
3. Trigger conditions are only updated during the calibration period, then frozen (preventing recursive dilemma)

### 3.4 Bayesian Smoothing

```python
def bayesian_smooth(observed, prior_ratio, prior_weight):
    """Bayesian smoothing: fuse observed values and prior"""
    effective_n = observed + prior_weight * prior_ratio
    if effective_n < 1:
        return prior_ratio  # Insufficient data, trust the prior
    smooth_ratio = (observed * observed_value + prior_weight * prior_value) / effective_n
    return smooth_ratio
```

prior_weight three-tier thresholds:
- prior_confidence >= 0.8 → prior_weight = 3 (strong trust in prior)
- 0.5 <= prior_confidence < 0.8 → prior_weight = 1
- prior_confidence < 0.5 → prior_weight = 0.3 (weak trust in prior)

### 3.5 Gradient Effect of prior_confidence

- manual + high confidence → aggressive alert threshold (small deviation triggers alert)
- empirical + low confidence → conservative alert threshold (large deviation required to trigger alert)
- prior_ratio > 1.5 → requires higher effective_n threshold (naturally high drift rate)

### 3.6 Implementation Path

New script: `scripts/prior_review.py`

Integration points:
- After decay in `run_batch()`, calculate the prior_ratio for each prior parameter
- During the calibration period, record prior_ratio into `decay_config.prior_history`
- When review_trigger fires, write to the L2 queue + push notification

---

## 4. Granularity Drift Matrix

> Core discussion sources: neuro (drift matrix, structural proximity, two-layer analysis)

### 4.1 Problem

Are the granularity boundaries of memory classification reasonable? For example, if "L3-lesson" is frequently reclassified as "L2-behavior," it indicates a problem with the boundary definitions. Currently there is no awareness of this.

### 4.2 Matrix Structure

```
         lesson  behavior  preference  fact  procedure  ...
lesson      -       12        3         1       2
behavior    8       -        5         2       7
preference  2       4        -         0       1
...
```

Matrix values = actual reclassification counts (recorded in case_lifecycle).

### 4.3 Two-Layer Analysis

**Heatmap layer**: directly displays actual reclassification counts — immediately obvious which edges are most active.

**Statistical test layer**:
- Fisher's exact test (small samples < 5): exact but conservative
- Chi-squared test (large samples >= 5): approximate but efficient
- Auto-switching logic: any cell < 5 → Fisher

### 4.4 Structural Proximity Adjustment

Different classifications have different expected reclassification frequencies (fact→procedure is naturally higher than fact→lesson).

```python
def expected_drift_rate(src_tag, dst_tag, taxonomy_tree):
    """Calculate expected drift rate based on tree-level distance"""
    distance = tree_distance(src_tag, dst_tag, taxonomy_tree)
    # Closer distance → higher expected drift rate
    base_rate = 0.02 * math.exp(-0.5 * distance)
    return base_rate
```

Anomaly judgment: actual/expected ratio significantly > 1 → this edge is a structural problem.

### 4.5 Diagnostic Output

```
Drift Matrix Diagnostic Report (2026-04-11):
Anomalous edges (actual/expected > 2.0):
  🔴 lesson → behavior: actual=12, expected=2.1, ratio=5.7
  🟡 behavior → procedure: actual=7, expected=3.8, ratio=1.8
Normal edges: remaining 119 edges
Sparsity: matrix fill rate 23%, statistical test auto-switches to Fisher
```

### 4.6 Implementation Path

New script: `scripts/drift_matrix.py`

Data source: reclassification event records in case_lifecycle (requires v0.4.5 case_grow to have already recorded these)


---

## 5. Memory Context Binding

> Core discussion source: jarvis_806cab

### 5.1 Problem

"The user prefers a concise style" has completely different meanings in a work-report scenario versus a technical-discussion scenario. Currently, memories have no scenario annotation, so retrieval cannot distinguish between them.

### 5.2 Three Candidate Approaches

**Approach A: Scenario Context Annotation (Split)**
- Split each memory into multiple entries, stored separately by scenario
- Precise but severe bloat
- Simple retrieval

**Approach B: Context-Aware Retrieval (Weighted)**
- Memories are not split; at retrieval time, weighting is applied based on current context
- New optional `context_scope` field
- Calculate context_overlap_score at retrieval time

**Approach C: Accept Ambiguity (Preserve Original)**
- No special handling
- Simple but sacrifices precision

### 5.3 Recommended Approach: B + C Hybrid

**Core idea**: accept ambiguity by default (C), but provide context-weighting capability at retrieval time (B).

**New field** (optional, not mandatory):
```json
{
  "context_scope": {
    "domains": ["work-report", "technical-discussion"],
    "scope_note": "Concise means refined paragraphs, not omitting key information"
  }
}
```

**Retrieval enhancement**:
```python
def context_overlap_score(memory, query_context):
    """Calculate overlap between a memory's context and the query context"""
    mem_scopes = memory.get("context_scope", {}).get("domains", [])
    query_domains = query_context.get("domains", [])
    if not mem_scopes or not query_domains:
        return 1.0  # No context annotation → no impact
    overlap = len(set(mem_scopes) & set(query_domains))
    return 0.7 + 0.3 * (overlap / max(len(query_domains), 1))
```

**Low-threshold fallback**: when context_overlap_score < 0.7, load other memories with the same tag as alternatives.

### 5.4 Write Strategy

- Not all memories are required to have context_scope annotation (gradual adoption)
- context_scope is only added for L1 (high-cost/irreversible) memories or when manually confirmed
- No automatic scenario inference (accuracy of auto-inference is insufficient as a classification basis)

---

## 6. L2 Blocking Granularity Tiers

> Core discussion source: neuro

### 6.1 Core Insight

High-frequency L2 triggering = classification criteria are too lenient, not a user-confirmation-fatigue problem. Truly high-risk operations are naturally low-frequency.

**Direction**: tighten the trigger conditions themselves, rather than limiting trigger frequency.

### 6.2 Two-Tier Design

**L1 (Silent / Low Risk)**
- Condition: reversibility <= 1 and no boundary_words match
- Behavior: execute directly, log the action
- Example: updating a low-importance memory

**L2 (Explicit Confirmation / High Risk)**
- Condition: reversibility >= 2 or boundary_words match
- Behavior: pause → summary diff comparison → await confirmation
- Example: deleting a memory / overwriting a user preference

### 6.3 Self-Calibration Mechanism

Three signals are used to evaluate L2 judgment quality:
- **confirm**: user confirmed the L2 block → judgment correct
- **cancel**: user cancelled the L2 block → possible false positive
- **downgrade**: user said "don't ask next time" → trigger conditions should be relaxed

Data structure:
```json
{
  "l2_audit": {
    "total_triggered": 42,
    "confirmed": 38,
    "cancelled": 3,
    "downgraded": 1,
    "false_positive_rate": 0.071
  }
}
```

When false_positive_rate > 0.3, automatically tighten trigger conditions (raise the reversibility threshold or narrow the boundary_words scope).

---

## 7. confirmed.negative Priority

> Core discussion source: jarvis_806cab

### 7.1 Insight

Negative feedback (user proactively correcting) carries more information than positive confirmation.

### 7.2 Implementation

v0.4.5 already had a `feedback_polarity` field design, but it was never implemented. v0.4.6 delivers it:

```
confirmed.negative trigger:
  1. confidence immediately drops by 0.5
  2. last_challenged timestamp is triggered
  3. push to owner for adjudication (L3 notification)
  4. push content: original memory + correction content + diff summary
```

### 7.3 Integration with case_lifecycle

confirmed.negative events are recorded in case_lifecycle:
```json
{
  "event_type": "challenge",
  "feedback_polarity": "negative",
  "user_action": "correct",
  "original_content": "...",
  "corrected_content": "...",
  "confidence_before": 0.8,
  "confidence_after": 0.3,
  "owner_decision": null  // awaiting L3
}
```

---

## 8. Collaboration Convention: change-control matrix

> Core discussion source: skilly_wang


### 8.1 Three-Layer Spec Change Process

The three layers are confirmed (Must/Must-not + Evidence schema + Default knobs), with a new cross-cutting change-control:

**Constraints changes (Layer 1)**
- Impact: behavioral red lines
- Process: owner confirmation → full test suite → progressive canary → rollback plan
- Log tag: D1 (danger level 1)
- Cannot be executed automatically in cron

**Schema changes (Layer 2)**
- Impact: telemetry interface stability
- Process: design review → compatibility testing → version number increment
- Log tag: D2
- Must verify cross-time comparability

**Defaults changes (Layer 3)**
- Impact: tunable parameters
- Process: diff-aware config snapshot → unit tests → parameter boundary validation
- Log tag: D3
- Can be executed automatically in cron

### 8.2 Schema Drift vs. Threshold Drift

Key distinction:
- **Schema drift** (field structure changes): affects cross-time comparability, must follow D2 process
- **Threshold drift** (parameter value changes): does not affect the interface, D3 process suffices

Schema stability is the true guarantee of cross-time comparability.

### 8.3 Lint Rules

New code lint rules:
- Numeric constants must be annotated as either `interface_cap` or `implementation_param`
- `interface_cap` changes require D2 review
- `implementation_param` changes require D3 review

---

## 9. Implementation Priority & Milestones

### Phase 1: Signal Closed Loop (P0, estimated 1–2 days) ✅ Design finalized 🚧 Implementation in progress

**Goal**: Make the decay algorithm's input no longer dead data

**Completed:**
- [x] Added `scripts/signal_loop.py`: access_log.jsonl read/write + cron_infer_access + signal health check
- [x] Added `access_log.jsonl` format definition and read/write utilities
- [x] Implemented `cron_infer_access()`: scans daily_notes keywords + file mtime changes
- [x] Implemented `check_signal_health()`: checks access_log mtime, degrades when threshold exceeded
- [x] Modified `run_batch()`: calls signal merge at the start (Layer 1 + Layer 2)
- [x] decay_config new `signal_weights` and `signal_stale_threshold` fields
- [x] meta.json new `signal_source` and `signal_health` fields
- [x] AGENTS.md new behavioral convention: append access_log after memory_get
- [x] Test: verify dual-layer signal merge formula
- [x] Test: verify signal health check (simulate Layer 1 break → degradation → recovery)
- [x] Test: verify network_factor discriminating power improvement
- [x] references/signal-loop.md updated (with cron task template)
- [x] SKILL.md rewritten (~300 → ~100 lines; implementation details moved to references/, conforming to skill-creator spec)

### Phase 2: Calibration-Period Health (P1, estimated 2–3 days)

**Goal**: Know whether the classifier is working properly after deployment

- [ ] Add `scripts/calibration_health.py`
- [ ] PELT changepoint detection (using ruptures or self-implemented)
- [ ] KS test + Kendall tau
- [ ] Four-tier extension mapping
- [ ] Annealing strategy (step-size switching)
- [ ] Anchor hierarchy design
- [ ] Integrate into `run_batch()`
- [ ] Test: simulate calibration-period anomaly scenarios

### Phase 3: Prior Drift Detection (P1, estimated 2–3 days)

**Goal**: Automatically alert when prior parameters drift

- [ ] Add `scripts/prior_review.py`
- [ ] Seven-field closed-loop data structure
- [ ] condition_A / condition_B dual-layer trigger
- [ ] Bayesian smoothing + prior_confidence sigmoid
- [ ] alert_priority gradient
- [ ] Integrate into `run_batch()`
- [ ] Test: simulate prior drift scenarios

### Phase 4: Granularity Drift Matrix (P2, estimated 1–2 days)

**Goal**: Perceive classification boundary problems

- [ ] Add `scripts/drift_matrix.py`
- [ ] Heatmap + statistical test two-layer analysis
- [ ] Structural proximity expected values
- [ ] Fisher/chi-squared auto-switching
- [ ] Diagnostic report output
- [ ] Test: simulate reclassification data

### Phase 5: Memory Context Binding (P2, estimated 1 day)

**Goal**: Correctly retrieve the same memory in different scenarios

- [ ] Add `context_scope` optional field
- [ ] `context_overlap_score()` computation
- [ ] memory_query integration with context weighting
- [ ] Low-threshold alternative memory loading
- [ ] Test: ambiguous memory scenarios

### Phase 6: L2 Blocking Optimization + confirmed.negative (P2, estimated 1–2 days)

**Goal**: More precise blocking, more effective feedback

- [ ] L1/L2 two-tier judgment logic refinement
- [ ] L2 self-calibration (confirm/cancel/downgrade)
- [ ] false_positive_rate monitoring
- [ ] confirmed.negative event handling
- [ ] case_lifecycle integration
- [ ] Test: false-positive scenarios + correction scenarios

---

## 10. Compatibility with v0.4.5

### No Breaking Changes to Existing Interfaces
- All new features are implemented via new scripts / new fields
- Existing MCP tool signatures remain unchanged
- meta.json is backward compatible (new fields are optional)

### New Script List
- `scripts/calibration_health.py` — calibration-period health
- `scripts/prior_review.py` — prior drift detection
- `scripts/drift_matrix.py` — granularity drift matrix

### New meta.json Fields
```json
{
  "decay_config": {
    "calibration": {
      "enabled": true,
      "start_at": "...",
      "count": 0,
      "extended": 0,
      "breakpoints": [],
      "annealing_stage": "early"
    },
    "prior_history": [],
    "drift_matrix": {}
  }
}
```

### New Memory Fields
```json
{
  "context_scope": {
    "domains": [],
    "scope_note": ""
  },
  "l2_audit": {
    "total_triggered": 0,
    "confirmed": 0,
    "cancelled": 0,
    "downgraded": 0
  }
}
```

---

## 10.5 Bootstrap MEMORY.md Cleanup Mechanism (Implemented)

### Background

The bootstrap flow extracts memory entries from MEMORY.md and writes them into classified directories (under memory/, organized by tag into files). However, after writing, MEMORY.md still retains the original content, causing information redundancy — the same memory exists simultaneously in MEMORY.md and in the classified files.

### Approach: Step 3.5 — Cleanup After Writing

Between Step 3 (write classified files) and Step 4 (generate index) of the bootstrap flow, add Step 3.5:

1. **Backup**: `MEMORY.md` → `MEMORY.md.pre-bootstrap.bak` (rollable back)
2. **Cleanup**: remove paragraphs/sections from MEMORY.md that have been successfully extracted and written to the classified directory
3. **Preserve**:
   - Top index area (if present)
   - quick-reference / frequently used information and other non-memory content
4. **Validate**: ensure the preserved portion has intact formatting with no dangling references

```python
# Pseudocode
def clean_memory_after_bootstrap(memory_path, ingested_sections, backup=True):
    """Bootstrap Step 3.5: clean archived content from MEMORY.md"""
    if backup:
        shutil.copy2(memory_path, memory_path + ".pre-bootstrap.bak")
    
    content = Path(memory_path).read_text(encoding="utf-8")
    # Remove archived sections
    for section in ingested_sections:
        content = remove_section(content, section)
    
    Path(memory_path).write_text(content, encoding="utf-8")
```

### Design Principles

- **MEMORY.md is a quick index, not a memory store**: the classified directory is the persistence layer
- **Irreversible but rollback-safe**: .pre-bootstrap.bak provides a safety net
- **Idempotent**: repeated execution does not lose data (on the second run, there are no matching paragraphs left to remove)

---

## 10.6 Quality Improvements & Bug Fixes

### Fixed Defects

**1. signal_loop.py Variable Shadowing (Fixed)**
- **Problem**: `cron_infer_access()` used `for i in range(...)` to iterate over date offsets, but inside the loop body `i` was overwritten as a memory index, causing incorrect date calculations
- **Fix**: renamed the loop variable to `for day_offset in range(...)`
- **Impact**: after the fix, Layer 2 posterior inference time-window calculations are correct

**2. memory_sync.py Circular Import (Fixed)**
- **Problem**: `memory_sync.py` imported functions from `mg_utils`, but `mg_utils` indirectly imported `memory_sync`, forming a circular dependency
- **Fix**: promoted shared functions to `mg_utils`; `memory_sync` only imports from `mg_utils` in one direction
- **Impact**: eliminated ImportError at startup

**3. mg_schema/__init__.py Import Placement (Fixed)**
- **Problem**: `import json` was located inside a function body rather than at the top of the file, not conforming to Python conventions
- **Fix**: moved `import json` to the top of `mg_schema/__init__.py`
- **Impact**: eliminated linter warnings, conforms to PEP 8

**4. SKILL.md Spec Compliance (Completed)**
- **Problem**: SKILL.md was approximately 300 lines, containing extensive implementation details and version history, not conforming to the skill-creator spec
- **Fix**: completely rewritten to ~100 lines; implementation details moved to the `references/` directory; version history removed
- **Changes**:
  - `SKILL.md`: 300 → 100 lines, pure usage guide
  - `references/`: added multiple reference documents (implementation details, API docs, etc.)
  - Conforms to skill-creator spec requirements

### Current Project Statistics (as of 2026-04-15)

- **22 core scripts** (excluding 4 legacy migration scripts: migrate.py, migrate_retag.py, migrate_to_v042.py, migrate_v03_to_v04.py; total 26 .py files including the mg_schema subpackage)
- **600 tests** (covering signal closed loop, health check, decay merge, etc.)
- **10 MCP tools**
- **SKILL.md**: ~100 lines (spec compliant)

---

## Appendix A: Discussion Contributor Index

- **neuro** — access_log.jsonl direction, signal health check, configurable weights, Bayesian smoothing, prior_review seven-field design, condition_A/B, drift matrix, L2 self-calibration, reactivation_count
- **SimonClaw** — posterior inference direction four, signal_source tagging, Layer 2 first approach, PELT + KS + Kendall tau, annealing strategy, anchor hierarchy, audit chain
- **jarvis_806cab** — confirmed.negative priority, memory context binding problem
- **skilly_wang** — three-layer spec architecture, change-control matrix, evidence schema
- **lingxi_agent** — four-dimensional evaluation framework (accuracy / stability / coverage / efficiency)
- **guoxiaoxin** — sliding-window classification, stability filter
- **eva** — quality density filter, silence-period N calibration
- **number_seven** — experience library design feedback

## Appendix B: Relationship to Issue #5

This proposal is the engineering implementation of Issue #5 (write-side calibration design). All core viewpoints from the community discussion have been incorporated:

1. ✅ Calibration-layer three-layer verifiable framework (§2)
2. ✅ prior_review_trigger seven-field closed loop (§3)
3. ✅ Granularity drift matrix (§4)
4. ✅ Memory context binding (§5)
5. ✅ L2 blocking granularity tiers (§6)
6. ✅ confirmed.negative priority (§7)
7. ✅ change-control matrix (§8)
8. ✅ Signal closed loop (§1, P0 engineering defect fix)
