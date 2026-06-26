# Axes Design Worksheet

Fill this in to design your own multi-dim evaluation framework. Use [group-design-principles.md](../references/group-design-principles.md) for the rules and [canonical-vs-proxy-decision.md](../references/canonical-vs-proxy-decision.md) for measurement design.

---

## Step 1: Domain identification

**System class**: _______________________________________
(e.g., multi-agent deliberation / RAG / tool-using agent / single-LLM reasoning)

**Evaluation question**: _______________________________________
(What comparison should the framework answer? E.g., "does V2 ground better than V1?")

**Calibration cases (2-3 with expected ordinals)**:

1. _______________________________________ — expected: ______________
2. _______________________________________ — expected: ______________
3. _______________________________________ — expected: ______________

**Data availability map**:

- Case 1: _______________________________________ (e.g., "structured jsonl + round markdown")
- Case 2: _______________________________________ (e.g., "narrative logs only")
- Case 3: _______________________________________

---

## Step 2: Group structure

**Group count**: ______ (typically 2-4)

| Group | Layer name | What it asks |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

---

## Step 3: Dimensions per group

For each group, list 2-5 dimensions. Total cap: 8-12 dimensions across all groups. Each dimension gets one full row in Step 4.

**Group 1 dimensions**:

- 1.1 ________________________
- 1.2 ________________________
- 1.3 ________________________

**Group 2 dimensions**:

- 2.1 ________________________
- 2.2 ________________________
- 2.3 ________________________
- 2.4 ________________________

**Group 3 dimensions**:

- 3.1 ________________________
- 3.2 ________________________

(continue per group as needed)

---

## Step 4: Per-dimension rubric

For each dimension above, fill in:

### Dimension {N.M}: {name}

| Field | Content |
|---|---|
| Definition | (1-2 sentences) |
| Why it matters | (what failure mode does it catch?) |
| Canonical measure | (formula given full data) |
| Fallback proxy | (operationalization for partial data) |
| Score range | (e.g., [0, 1] / [-∞, +∞]) |
| Tie-break rule | (how to handle partial-credit) |
| Flag conditions | (when to attach `⚠`) |
| Failure modes | (when score is unreliable) |
| Expected ordinal | (which calibration case scores higher than which) |

A dimension without all 9 fields is not yet operational — it's a sketch.

---

## Step 5: Calibration check

For each calibration case from Step 1, predict the score in each group:

| Case | Group 1 mean | Group 2 mean | Group 3 mean |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

After running scoring, verify the ordinals hold. If not, log the discrepancy in your `iteration_log.md` and decide:

- Was the framework wrong? → adjust the rubric, re-run
- Was the prediction wrong? → keep the framework, document the surprise
- Was the scoring noisy? → tighten rules, re-score

---

## Step 6: Freeze

The framework freezes (becomes versioned) when:

- All calibration ordinals are explained (predicted-and-confirmed OR predicted-and-falsified-with-reason)
- At least 2-3 real iterations are logged
- The next instance can be scored without re-deriving the rubric

---

## Common mistakes during design

1. **Too many dimensions**: capping at 8-12 is generous; 6-8 is often clearer
2. **Composite temptation**: don't average groups into a single number, even "for convenience"
3. **Aspirational canonical**: if no calibration case has the canonical data, the canonical is theoretical — make sure proxy is the workhorse
4. **Skipping failure modes**: the failure mode list is the dimension's calibration; without it, the score is unverified
5. **Over-fitting to one calibration case**: 1 case can't validate a framework. Need 2-3, ideally with predicted ordinals between them
6. **Not iterating**: a framework that doesn't change after calibration is suspicious. Aim for 2-3 logged iterations before freezing
