# Canonical vs Proxy — Decision Tree

When designing or applying a multi-dim evaluation framework, you decide for each dimension: which measurement is *canonical* (the ideal one, available when full instrumentation exists) and which is *fallback proxy* (the workaround when data is incomplete). This document gives the decision rules.

---

## Why two-track measurement at all

Most evaluation work assumes "we have the data we need". In practice:

- Legacy systems lack instrumentation that newer systems have
- Old experiments captured different state than current ones
- Cross-team comparisons hit asymmetric data availability
- Partial system failures leave some dimensions unmeasured

If your framework only works when full data exists, you can't compare across instances with different data — which is most real comparisons. Canonical/proxy duality lets you score everything on the same axes, with explicit confidence levels.

---

## Decision rule 1: When is canonical available?

**Canonical** = the dimension's data source is structured and queryable as machine state (jsonl, database, structured logs).

For the system you're evaluating, ask:

1. Is the relevant signal captured as structured records (e.g., `claims.jsonl`, `verifications.jsonl`, `decisions.jsonl`)?
2. Are the records continuously written, not just at endpoints?
3. Is the schema stable (or versioned) across the time range you're scoring?

If yes to all three: canonical applies. Use the formal formula.
If no to any: proxy applies.

---

## Decision rule 2: How to design a fallback proxy

A fallback proxy is a measurement that:

- Reads from less structured artifacts (markdown logs, narrative reports, sampled outputs)
- Captures *the same underlying property* the canonical measure captures
- Has known noise characteristics (you understand when it under-reports / over-reports)

### Steps to design a proxy

1. **State what the canonical measures.** E.g., "fraction of decisions referencing testable evidence". The underlying property is *grounded reasoning*.
2. **Find a less-structured signal of the same property.** E.g., search round markdown for explicit citations like "resolves R5" or "addresses R3 tension".
3. **Define the operationalization.** E.g., count substrings, sample 5 randomly, hand-rate.
4. **Acknowledge the noise.** E.g., "may miss paraphrases that don't use ID syntax" / "may include aspirational citations that don't actually resolve".
5. **Set rules for when to fall back further.** E.g., "if proxy yields < 5 hits, sample manually instead".

---

## Decision rule 3: Tie-breaking on partial citation / partial evidence

Common case: a measurement is *partially* the canonical signal — not zero, not one. Examples:

- A decision references prior work but doesn't name a specific ID
- A verification has only 1 evidence ref where canonical wants ≥2
- A claim is "tested confirmed" but the test was a single observation

Default tie-break: **half-credit (0.5)**.

When to deviate:

- If the partial reference is *aspirational* (cites without engaging) → score 0
- If the partial reference is *unambiguous* (paraphrases a specific anchor cleanly) → score 1
- If you can't tell, score 0.5 and flag for spot-check

---

## Decision rule 4: When to flag `⚠ proxy used`

Whenever the canonical measure is unavailable and you fall back to proxy, attach a flag to the score. Reasons:

- Reader needs to know confidence is reduced
- Cross-instance comparison should weight canonical-data instances more
- Future iterations may upgrade proxy to canonical; the flag tracks where to go back

Flag format suggestion: `score = 0.42 ⚠ proxy used` or `score = 0.42 ⚠ markdown sample, n=5`.

---

## Decision rule 5: When to escalate from proxy to refusal

If the proxy itself can't be computed reliably:

- Sample size too low (< 3 hits)
- Source artifacts ambiguous
- Spot-check disagreement between two readers > 30%

Then: **don't score**. Report as "score unavailable, integrity caveat in scorecard". Forcing a number where none is reliable is worse than leaving the dimension blank.

---

## Decision rule 6: When the canonical changes mid-instance

If a system's instrumentation upgrades partway through the time period being scored (e.g., claims infra was added at round 8 of a 13-round experiment):

- Compute canonical over the post-upgrade window
- Compute proxy over the pre-upgrade window
- Report both with window labels: `A1 = 0.85 (post-upgrade canonical) / 0.42 (pre-upgrade proxy)`
- Don't average across windows; the noise characteristics differ

---

## Decision rule 7: State integrity check (gate before scoring)

Before scoring any instance, verify the data source is intact:

```
integrity_ok = (
  line_count(decisions.jsonl) ≥ R × 0.8
  AND line_count(lead_history.jsonl) ≥ R × 0.8
  AND tensions.jsonl covers rounds beyond R1
)
```

If `integrity_ok == False`:

- Proceed with scoring, BUT all scores relying on state files carry `⚠ state incomplete`
- Open the scorecard with a "Data integrity caveat" section
- Document what's missing and which dimensions are degraded

State files can drop mid-experiment without obvious failure. Surface this before it silently corrupts your scores.

---

## Worked example: A1 Claim Groundedness (from MADEF)

**Canonical** (when `claims.jsonl` exists):
```
A1 = |claims with status ∈ {tested_confirmed, tested_refuted, partially_refuted}| / |claims total|
```

**Fallback proxy** (no claims infrastructure):
```
A1_proxy = |decisions explicitly referencing prior decision/tension by ID| / |decisions total|
```

**Tie-break** for proxy: name-mention of a primitive (e.g., "Ledger", "Veto") without R# tag scores 0.5; pure self-reference scores 0.

**Flag conditions**:

- `⚠ citation rate below spot-check`: random-sample 3 "grounded" decisions; if <2 actually cite valid material
- `⚠ proxy only`: always flag when canonical unavailable

**Why this proxy works**: the underlying property (do decisions ground in prior work?) is captured *partially* by ID-citation patterns even without claims infrastructure. The noise is documented (paraphrase under-counts; aspirational citation over-counts).

---

## When designing your own dimensions

For each dimension you author, fill in:

| Field | Content |
|---|---|
| Canonical | (formula given full data) |
| Fallback proxy | (operationalization for partial data) |
| Tie-break rule | (how to handle partial-credit cases) |
| Flag conditions | (when to attach `⚠`) |
| Refusal threshold | (when proxy is too noisy to score at all) |

A dimension without all five fields is not yet operational — it's a sketch of a dimension.

See [axes-design-worksheet.md](../templates/axes-design-worksheet.md) for a fill-in template.

---

## Common mistakes

### Mistake 1: Treating proxy as second-class

The proxy isn't a worse version of the canonical — it's a *different* measurement with its own noise profile. When you score 0.42 with proxy and 0.85 with canonical for the same instance, the gap may be real (the canonical captures something the proxy can't) — *not* "proxy is wrong". Treat both as legitimate measurements; cross-comparing them surfaces what each captures.

### Mistake 2: Forcing canonical when only proxy fits

If structured records aren't continuous, don't pretend they are. A canonical formula run on partial data produces garbage with false precision. Falling back to proxy with a documented noise profile is more honest.

### Mistake 3: Skipping the spot-check

Proxy formulas typically require sampling (e.g., 5 random items, hand-rate). Skipping the spot-check turns proxy into a black box. The spot-check is the proxy's calibration; without it, the proxy score is unverified.
