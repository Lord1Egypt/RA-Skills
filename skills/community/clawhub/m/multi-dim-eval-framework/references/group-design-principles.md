# Group Design Principles

The five design principles + five meta-principles that govern any multi-dimensional evaluation framework following the MADEF pattern. These are domain-agnostic; the specific axes you design (see [axes-design-worksheet.md](../templates/axes-design-worksheet.md), or use [madef-axes.md](madef-axes.md) as a reference) are domain-specific.

---

## Five design principles

### 1. Cross-instance comparable

Every dimension has both a *canonical measure* (for instances with full grounding infrastructure) AND a *fallback proxy* (for instances without). Old experiments / legacy systems / partial-data cases must still be score-able with the same framework.

If you can only score new instances and not historical ones, you can't tell whether your "improvement" is real or just an artifact of the new instrumentation. Cross-instance comparability is the foundation of calibration.

### 2. No single composite score

Group sub-scores (typically 3 groups, but the count depends on your domain) report independently. **A single average would hide the most important signal — *which* dimension failed.**

A failing system with one group at 0.9 and another at 0.2 is not the same as a system with all groups at 0.55. Composite scores erase this distinction; group-wise reporting preserves it. Forcing the reader to look at the components is the point.

### 3. Operational

Every dimension specifies, in writing:

- **Data source** — which artifact / file / state object the measurement reads
- **Scoring rule** — formula or deterministic procedure, not narrative
- **Expected range** — [0,1] or [-∞, +∞], with interpretation thresholds
- **Failure modes** — when this score is unreliable
- **Expected ordinal** — for known calibration cases, which case should score higher than which

Without these, the dimension is rhetorical, not evaluable. A dimension you can't score *the same way twice* is decoration.

### 4. Failure-mode transparent

Each dimension lists conditions under which its score is unreliable. **A high score with a flagged failure mode is worth less than a lower score on clean data.** This forces the reader to look at the failure flags, not just the number.

Failures aren't bugs to fix later — they're the calibration signal for which dimensions are load-bearing in which scenarios.

### 5. Load-bearing over cosmetic

Dimensions are chosen because they distinguish between hypotheses or capability profiles, not because they are easy to compute. Counting widgets is easy; defining "claim groundedness" is hard, but it's the dimension that actually moves with the system's quality.

If two known-different instances score identically on a dimension, that dimension is cosmetic — drop it or refine it. The framework is only as good as its discriminative power.

---

## Five meta-principles (during scoring)

### M1. When a score is ambiguous, report the range

If a spot-check yields mixed results — say, 2 clear / 2 paraphrase / 1 unclear out of 5 sampled — report `score ∈ [0.3, 0.6]`, not `score = 0.5`. Premature precision misleads the reader into treating the midpoint as accurate.

### M2. Population-count normalization is required for cross-instance comparison

Some dimensions scale with population size (number of agents, number of rounds, dataset size). Either:

- Normalize the score (divide by `N-1` or `log2(N)`)
- Report the population count prominently next to the score

A density of 4 verifications/round means something different at N=3 vs N=5. Comparing raw counts across populations is a calibration error.

### M3. Stress conditions are evaluated separately from normal conditions

If you run stress tests (forced absences, edge inputs, adversarial cases), do not mix their scores into the regression of normal-condition scores. The stress signature is its own dimension; including stress data in normal-condition averages corrupts both.

### M4. The framework must be falsifiable

If your framework produces results that can't distinguish between two instances you intuit are different, the framework has a bug or your intuition was wrong. Either way, iterate. **A framework that "always confirms" is decorative.**

### M5. Calibration comes before claims

No new design decision should cite the framework until the framework has been run on prior known-quality instances and the scorecards have been reviewed. Otherwise you're using an uncalibrated tool to make decisions, which is exactly the failure mode the framework was supposed to prevent.

---

## What this approach is NOT

- **Not a ranking system.** "X scores higher than Y" is meaningless without identifying *which* group drove the gap.
- **Not a benchmark.** It does not produce a number comparable to external industry benchmarks. It is an internal tool for your specific evaluation question.
- **Not a proof of superiority.** High scores do not prove correct conclusions — only that the process had structural properties that correlate with quality.
- **Not fixed.** Each version of your framework freezes after calibration; future versions iterate when new instances reveal blind spots. Maintain a `change log` or `iteration log` documenting every adjustment.

---

## When this design pattern fits

This pattern (group-organized multi-dim evaluation with canonical/proxy duality) fits when:

- The system you're evaluating produces complex outputs that can't be reduced to a single quality score
- You need to compare instances across different infrastructure or different time periods (some have more grounding data than others)
- The dimensions you care about may *trade off* — improving one doesn't always improve another, and you need to see which dimension is sacrificing for which
- Your audience needs to debug *where* an instance fails, not just whether it passed

This pattern does NOT fit when:

- You need a single comparable number for ranking (use a benchmark, not this)
- All instances have identical instrumentation (canonical/proxy duality is wasted)
- The output space is simple and one metric captures it well

---

## Iteration discipline

A framework that's never been adjusted post-calibration is suspicious. Either it was designed perfectly on first try (rare) or calibration was too shallow.

Maintain an iteration log entry for every adjustment, including:

- **Trigger**: what calibration observation exposed the issue
- **Change**: what was modified in the framework definition
- **Rationale**: why the change, why now
- **Impact on prior scores**: which scorecards must be re-run

Even non-changes deserve entries: "we considered changing X, but the audit showed the existing rule was correct because Y." This builds the framework's epistemic record over time.

The framework freezes (becomes versioned) when at least 2-3 real adjustments have been logged and the ordinal calibration table holds. Without iteration, freezing is premature.
