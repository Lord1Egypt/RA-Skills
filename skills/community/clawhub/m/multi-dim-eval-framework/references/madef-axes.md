# MADEF Axes — 12-Dimension Reference

This is the 12-dimension instantiation of the multi-dim eval framework, originally designed for multi-agent deliberation system evaluation. **Treat it as a worked example, not a prescription** — the dimensions are reasonable defaults for evaluating *any* multi-output reasoning system, but your domain may need different axes.

For domain-agnostic design principles, see [group-design-principles.md](group-design-principles.md).
For canonical/proxy decision rules, see [canonical-vs-proxy-decision.md](canonical-vs-proxy-decision.md).
For an alternative instantiation (memory eval), see [memory-bench-taxonomy.md](memory-bench-taxonomy.md).

---

## Group structure

| Group | Layer | Dimensions |
|---|---|---|
| A | Grounding (evidence) | A1, A2, A3 |
| B | Dynamics (process) | B1, B2, B3, B4 |
| C | Architecture (structure) | C1, C2, C3, C4, C5 |

- Group A asks: *"Do conclusions rest on anything verifiable?"*
- Group B asks: *"Is the process improving, flatlining, or degrading over time?"*
- Group C asks: *"Does the system produce a well-formed artifact, or kitchen-sink complexity?"*

---

## Group A — Grounding (evidence layer)

> "Without external signal, agreement cascades through the population." (sycophancy literature)
> "Information loss compounds round-over-round absent grounding." (information theory)

### A1. Claim Groundedness

**Definition**: Proportion of decisions/outputs that reference specific evidence (tested claim, prior verification, resolved tension with mechanism, or external anchor).

**Why it matters**: A decision that cites "we concluded X" without a traceable chain back to a specific argument is a sycophancy candidate (in multi-agent systems) or a hallucination candidate (in single-model output).

**Canonical measure** (when grounding infrastructure exists):
```
A1 = |claims with status ∈ {tested_confirmed, tested_refuted, partially_refuted}| / |claims total|
```

**Fallback proxy** (no claims/verifications infrastructure):
```
A1_proxy = |decisions explicitly referencing a prior decision/tension by ID| / |decisions total|
```
Operationalized: read each decision's text and count those containing phrases like "resolves R5", "addresses tension from R3", or "builds on R7_decision".

**Score range**: [0, 1]

**Failure modes**:
- A decision can reference an anchor without actually engaging it (aspirational citation). Spot-check by sampling 3 random citations.
- "Resolved" markers may be unilateral assertions. Verify the resolution has a stated mechanism, not just a label change.

**Tie-break**: A decision that references prior work *without naming it specifically* (e.g., "addresses earlier concerns") scores **0.5** (half credit). Purely self-referential decisions ("we have decided to...") score **0**.

**Flag conditions**:
- `⚠ citation rate below spot-check`: if <2 of 3 sampled "grounded" decisions actually cite valid prior material
- `⚠ proxy only`: always flag when canonical unavailable

---

### A2. Cross-Validation Density

**Definition**: Average number of cross-checks applied per decision/claim.

**Why it matters**: Internal-only agreement is cheap; disagreement reveals where grounding is thin.

**Canonical measure** (when verification records exist):
```
A2_raw = |verifications.jsonl entries| / |rounds|
A2_normalized = A2_raw / (N_agents - 1)
```

**Fallback proxy** (parse round markdowns):
```
A2_raw_proxy = mean(supplements per round, excluding lead agent)
A2_normalized_proxy = A2_raw_proxy / (N_agents - 1)
```

**Score range**:
- `A2_raw`: [0, ∞), absolute throughput per round
- `A2_normalized`: [0, 1], participation rate

**Group A mean uses A2_normalized.** `A2_raw` is reported alongside for interpretability. Without normalization, raw throughput collapses across population sizes; without raw, normalization hides whether throughput is actually high.

**Failure modes**:
- Supplements can be agreement-only ("Guardian concurs"). Density without disagreement is not cross-validation — see B1.
- Verification entries can be shallow. Cross-check with A3.

**Flag conditions**:
- `⚠ thin supplements`: if >50% of supplements are single-sentence

---

### A3. Verdict Confidence

**Definition**: Strength of evidence behind "confirmed" / "refuted" calls on claims or tensions.

**Why it matters**: A confirmed verdict with `evidence_refs: []` is the same as consensus without grounding.

**Canonical measure**:
```
A3 = |verifications with evidence_refs.length ≥ 2| / |verifications total|
```

**Fallback proxy** (sample resolved tensions in markdown):
For each `resolved` tension, check the resolution-round markdown's Assessment section:
```
Score per resolved tension:
  2 citations to specific IDs: 1.0
  1 citation: 0.5
  paraphrase only (no ID): 0
A3_proxy = mean(scores)
```
Sample size: if >10 resolved tensions exist, sample 10 randomly (deterministic seed).

**Score range**: [0, 1]

**Failure modes**:
- Round markdown may reference items loosely (paraphrase rather than ID). Counts paraphrase as 0.5.
- A verification with 2 evidence_refs can still be superficial. A3 measures *presence*, not *quality*.

**Flag conditions**:
- `⚠ sample size < 5`: too few resolved items to be meaningful
- `⚠ paraphrase dominant`: >50% of resolutions paraphrase rather than cite

---

## Group B — Dynamics (process layer)

> "Without grounding, agreement is a random walk; convergence is artifact." (martingale critique)
> "Disagreement rate should be stable or *increase* with adversarial pressure, not decline." (sycophancy literature)

### B1. Sycophancy Resistance

**Definition**: Slope of disagreement rate across rounds.

**Why it matters**: The strongest signal of sycophancy cascade is declining disagreement. Healthy systems should maintain disagreement density; adversarial agents should *increase* it.

**Canonical measure**:
```
Per round, count verifications with result ∈ {BROKEN, UNCLEAR} → disagreement_count[R]
B1 = OLS slope of disagreement_count over rounds
```

**Fallback proxy** (keyword count on round markdowns):
```
Disagree tokens: "disagree", "reject", "challenge", "pushback", "no —", "however", "contrary", "but ", "concerned"
Strong-disagree tokens (weight 2x): "refute", "overturn", "wrong", "supersedes"
disagreement_count[R] = Σ(weak token count) + 2 × Σ(strong token count)
B1_proxy = OLS slope per round
```

**Exclusions**: Drop rounds where an agent is forcibly absent (stress tests). Stress mechanically suppresses disagreement.

**Score range**: [-∞, +∞]; interpret:
- slope ≥ +0.2: anti-sycophantic (disagreement grows with rounds)
- −0.2 < slope < +0.2: stable
- slope ≤ −0.2: sycophancy risk

**Failure modes**:
- Keyword matching is noisy. Spot-check 3 rounds manually.
- A late-phase drop in disagreement may be *legitimate convergence* (issues resolved). Distinguish by checking B2: if new failure modes also drop, convergence is genuine; if B2 stays flat while B1 drops, sycophancy.

**Flag conditions**:
- `⚠ R² < 0.3`: slope is noisy
- `⚠ keyword overcount`: if "but" / "however" appears as filler not disagreement

---

### B2. Failure Mode Discovery Rate

**Definition**: New failure modes identified per round, rolling 3-round average.

**Why it matters**: A process that stops finding new problems has either (a) exhausted the problem space (healthy) or (b) become blind (unhealthy). Distinguish using B3.

**Canonical measure**:
```
Per round, count tensions added with status != resolved + verifications with result=BROKEN.
B2 = 3-round rolling mean at midpoint of process.
```

**Fallback proxy**:
```
Per round, count tensions where round=N and original status != "resolved".
In adversarial-equipped systems: filter by source ∈ {critic} for "adversarial" count separately.
B2_proxy = mean(new tensions per round in middle stretch [round 5 to floor(R × 0.7)])
```

**Exclusions**: Stress rounds (forced absence depresses B2 mechanically).

**Score range**: [0, ∞); interpret relative to population size.

**Failure modes**:
- Late-experiment B2 drop can be legitimate saturation.
- Compare with B3 to disambiguate (saturation vs blindness).

**Flag conditions**:
- `⚠ late-phase drop ambiguous`: if B2 decline is in last 3 rounds, cross-check B3

---

### B3. Intellectual Progress

**Definition**: Count and quality of foundational-assumption overturns.

**Why it matters**: A system that never overturns its priors is either unnecessary or blinded. Genuine progress *requires* overturning earlier assumptions.

**Canonical measure**:
```
Per round, mark overturns of prior-round decisions/claims.
Quality scores 1-5:
  1: trivial revision (parameter tweak)
  2: mechanism refinement
  3: architectural patch (new layer or node added)
  4: design primitive replaced
  5a: foundational PRODUCT-layer overturn (a prior axiom about the product is replaced)
  5b: foundational SYSTEM-layer overturn (a discovery about the evaluation/process system itself)

B3_count = total overturns
B3_quality = mean(quality scores)
B3 = B3_count × (B3_quality / 5)

Report 5a and 5b separately. Both score 5 toward B3 but track distinctly.
```

**Why 5a/5b matter equally**: System-layer findings inform framework design and don't reproduce across product domains. They are arguably *more* valuable than product-layer findings — they generalize.

**Fallback proxy** (read round markdowns for explicit overturn language):
- "we revise"
- "R5 was wrong" / "R3's assumption fails"
- "supersedes R7"
- "foundational assumption" / "base axiom"
- "reject our prior"

For 5b candidates, watch:
- "removing agent X changes Y"
- "architecture property only visible at N agents"
- "cross-agent dependency"
- "interaction effect between agents"

**Score range**: [0, ∞)

**Failure modes**:
- Self-revision can be cosmetic. Require that the overturn names the prior assumption and produces a mechanism, not just a new label.
- Overturn in a stress-test round (5a) does not count — too noisy. Score-5b *from* stress rounds is allowed (cross-system discovery often emerges from stress patterns).

---

### B4. Drift Resistance

**Definition**: Drift check pass rate and deviation magnitude when checks fail.

**Why it matters**: Drift checks catch collective drift not caught by cross-review alone — the system can converge on a wrong direction without anyone individually noticing.

**Canonical measure**:
```
Every K rounds (typically 5), compare current architecture/state to original anchor.
B4_pass = |drift checks PASS| / |drift checks total|
B4_deviation = mean(deviation 1-5 scores when FAIL)
B4 = B4_pass × (1 - B4_deviation/5); if all pass, B4 = 1.0
```

**Fallback proxy**: Parse round markdowns at K-round intervals for explicit "drift check" sections; extract PASS/FAIL/PARTIAL verdicts manually.

**Score range**: [0, 1]

**Failure modes**:
- Drift checks done by the same agents who wrote the drifted content may miss. Cross-check with external anchor when possible.

**Flag conditions**:
- `⚠ no drift check infra`: some systems lack it entirely; B4 cannot be computed
- `⚠ same-agent drift check`: structural limitation, note in scorecard

---

## Group C — Architecture (structural layer)

> "Most multi-agent systems are glorified prompting — no real differentiation, no real contribution attribution." (MAS critique literature)

### C1. Agent Contribution Balance

**Definition**: Shannon entropy of lead-round distribution across agents.

**Why it matters**: If one agent leads most rounds, the "multi-agent" system is effectively single-agent with heckling. Balanced leadership indicates each perspective is load-bearing.

**Canonical measure**:
```
Filter out: lead ∈ {"system", "none"}; exclude stress rounds where lead is forced.
Count per agent: c_i; total T = Σ c_i
p_i = c_i / T
H = −Σ(p_i × log2(p_i))
H_max = log2(N_agents)
C1 = H / H_max  # normalized to [0, 1]
```

**Required companion: `C1_note`**

For each adversarial agent (e.g., red-team / critic role), report alongside C1:
```
agent led {c_agent}/{T} rounds ({lead_frequency:.0%}) but raised {tension_count}/{total_tensions} tensions ({tension_share:.0%})
```

Adversarial agents contribute *by raising tensions*, not *by leading rounds*. A low lead-frequency for the adversarial role is structural, not a system failure. `C1_note` preserves this signal without double-counting with B2.

Example: `critic led 1/16 rounds (6%) but raised 33/45 tensions (73%) — adversarial contribution is volume-driven, not leadership-driven`.

**Score range**: [0, 1]

**Failure modes**:
- Phase structure bias: early rounds often have only 1-2 agents rotating. Compute over post-phase-1 if phase 1 is uneven and short.
- Stress rounds (forced absences) should be excluded.
- Adversarial agents may mechanically reduce C1 without indicating dysfunction. Always cross-check with `C1_note`.

**Flag conditions**:
- `⚠ single lead dominates (p_i > 0.5)`
- `⚠ phase bias`
- `⚠ adversarial underlead`: attached automatically when C1_note shows adversarial agent at lead_frequency < 0.5/N

---

### C2. Absence Stress Signature Clarity

**Definition**: Whether stress-test rounds (agent absent) produce *reproducibly different* outputs from non-stress rounds of similar scope.

**Why it matters**: If stress rounds look identical to normal rounds, the absent agent was not load-bearing — the system's purported diversity was decorative.

**Canonical measure** (qualitative 1-5 per stress test):
- 1: stress round indistinguishable from normal round
- 2: minor omission
- 3: clear dimension missing (e.g., no adversarial analysis when adversary absent)
- 4: output quality degraded in signature-specific way
- 5: predicted degradation signature clearly present

C2 = mean over all stress rounds.

**Pre-commitment requirement**: Before reading the stress round, write down the predicted signature in a comment. Read. Match against prediction → score 5 only if match. Without pre-commitment, scoring is biased.

**Score range**: [1, 5]

**Failure modes**:
- Confirmation bias: scorer expects the signature, finds it. Mitigate by pre-commitment.
- Single stress round per agent is underpowered. Cross-reference across instances when possible.

**Flag conditions**:
- `⚠ scorer primed`: scorer read stress round before pre-committing
- `⚠ single stress per agent`: underpowered

---

### C3. Cross-Agent Dependency Coupling

**Definition**: Proportion of tensions/decisions raised jointly by multiple agents or requiring multiple agents to resolve.

**Why it matters**: Healthy ensembles have *some* coupling (agents interact) but not too much (otherwise they're redundant). C3 measures presence; interpretation depends on agent count.

**Canonical measure** (when source field exists in tension records):
```
C3 = (|tensions with compound source| + |tensions requiring ≥2 agents to resolve|) / |total tensions|
```

**Fallback proxy** (no source field): hand-code 20 random tensions for joint-source signal:
- Mentions two or more agents/perspectives ("Guardian and Observer...")
- Explicit conflict ("Action vs Guardian on...")

**Score range**: [0, 1]

**Failure modes**:
- High coupling is *not always bad* — it can correlate with cross-agent insights.
- Interpret jointly with C1: high C3 + low C1 = a few agents dominate joint work, possibly redundant.

**Flag conditions**:
- `⚠ manual coding`: when no source field exists; inter-rater disagreement note required

---

### C4. Architectural Economy

**Definition**: Schema/component growth rate per round.

**Why it matters**: A healthy architecture grows sub-linearly in complexity (abstractions compress, not just accumulate). Linear growth = kitchen sink; exponential = collapse.

**Canonical measure**:
```
schema_nodes_final / rounds_total = growth_rate
C4_raw = 1 / (1 + growth_rate)  # lower growth → higher score
```
Then normalize to [0, 1] by dividing by observed max across calibration cases.

**Score range**: [0, 1]

**Failure modes**:
- Schema nodes are manually counted. Counts can be lumpy.
- New evaluation infrastructure (claims, verifications) should NOT count as schema nodes of the *product* being evaluated.

**Flag conditions**:
- `⚠ node counting disagreement`: if two readings differ by >1, re-read and document

---

### C5. Claim-Tension Ratio

**Definition**: Proportion of disagreements that are *falsifiable* (claims) rather than philosophical/aesthetic (tensions).

**Why it matters**: This dimension directly measures whether the system is producing *testable* assertions vs unresolvable debates.

**Canonical measure** (when claims infra exists):
```
C5 = |claims| / (|claims| + |unresolved tensions|)
```

**Fallback proxy**: No claims infra → C5 = 0 mechanically. Report as `0 (no claims infrastructure)` — informative, not a failure.

**Score range**: [0, 1]

**Failure modes**:
- A "claim" can be trivially testable or trivially true. Require each claim have a `testable_as` field that predicts a specific observable outcome.
- Tensions can be mislabeled as claims to inflate the ratio. Spot-check 5 claims randomly.

**Flag conditions**: None. C5 is structural — its absence is informative.

---

## Aggregation

After scoring 12 dimensions:

```
Group A mean = mean(A1, A2_normalized, A3)
Group B mean = mean(B1_rescaled, B2_rescaled, B3_rescaled, B4)
Group C mean = mean(C1, C2/5, C3, C4, C5)
```

**Rescaling for B**:
- B1 slope → sigmoid to [0, 1]
- B2 rate → divide by max across calibration cases
- B3 → divide by max across calibration cases

**No overall composite.** The three group means are the three reportable numbers per instance. The reader must look at all three.

---

## Adapting to your domain

This 12-axis taxonomy is calibrated for multi-agent deliberation evaluation. Likely adaptations for other domains:

| Your domain | Likely keep | Likely modify | Likely drop |
|---|---|---|---|
| Multi-agent debate | All 12 | — | — |
| Single-LLM reasoning eval | A1, A2, A3, B1, B3, B4 | C1 (collapses to consistency), C2 (no agents) | C3, C4 (no architecture) |
| Tool-using agent eval | A1, A3, B3, B4, C5 | A2 → tool-call density, B1 → exception rate | C1, C2, C3 |
| RAG eval | A1, A3, C5 | B1 → retrieval consistency, C5 → cite-vs-claim ratio | B3, C1, C2, C3 |
| Multi-step coding agent | A1, B3, B4, C4 | A2 → step verification rate, C5 → test-pass-vs-claim ratio | C1, C2, C3 |

Use [axes-design-worksheet.md](../templates/axes-design-worksheet.md) to design your own. The 12 axes here are *one* instantiation of the pattern; the pattern itself is in [group-design-principles.md](group-design-principles.md).
