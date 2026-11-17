# Risk Matrix (Risk Matrix · Calibrated 5×5)

A unified risk probability×impact scale and color bands, ensuring risk ratings across different Agents / different projects are comparable and accountable.

## 1. Probability / Likelihood Scale 1–5

| Level | Label | Description (qualitative anchor) | Suggested quantitative range |
|------|------|----------------|--------------|
| 1 | Very Low | essentially will not happen; rare in industry/history | <10% |
| 2 | Low | happens rarely; needs specific conditions to trigger | 10%–30% |
| 3 | Medium | may happen; common in similar projects | 30%–55% |
| 4 | High | very likely to happen; occurs in most similar projects | 55%–80% |
| 5 | Very High | almost certain; will occur without mitigation | >80% |

## 2. Impact Scale 1–5

| Level | Label | Description (anchored by dimension) |
|------|------|-------------------|
| 1 | Very Small | minor delay/cost overrun (<5%); locally reversible |
| 2 | Small | minor delay/cost overrun (5%–15%); easily remediable |
| 3 | Medium | noticeable delay/cost overrun (15%–30%); requires replanning |
| 4 | Large | severe delay/cost overrun (30%–50%); scope or quality impaired |
| 5 | Very Large | catastrophic: project goal fails / compliance or reputation incident |

> Impact can be taken as the highest of whichever leading dimension dominates: schedule / cost / scope / quality / compliance.

## 3. Score = Likelihood × Impact (∈ [1, 25])

## 4. Color Bands (Thresholds)—the risk register's severity field must correspond to them

| Score range | band severity | color | expected handling |
|----------|---------------|------|----------|
| 1 – 4 | low | Green (low) | accept / monitor |
| 5 – 9 | medium | Yellow (medium) | plan mitigation, review periodically |
| 10 – 15 | high | Orange (high) | actively mitigate + report, strong tracking |
| 16 – 25 | critical | Red (critical) | immediately escalate to CCB / sponsor, must have a contingency plan |

## 5. 5×5 Matrix Overview (rows = Impact, columns = Likelihood)

```
Impact\Likelihood |  1  |  2  |  3  |  4  |  5
   5      |  5  | 10  | 15  | 20  | 25   (red)
   4      |  4  |  8  | 12  | 16  | 20   (orange/red)
   3      |  3  |  6  |  9  | 12  | 15   (yellow/orange)
   2      |  2  |  4  |  6  |  8  | 10   (green/yellow)
   1      |  1  |  2  |  3  |  4  |  5   (green)
```

- Green zone: 1–4 | Yellow zone: 5–9 | Orange zone: 10–15 | Red zone: 16–25

## 6. Consistency Check (enforced by consistency_check.py)

- `likelihood` / `impact` must be **integers 1–5**;
- `score` must equal `likelihood × impact` (otherwise treated as a data error);
- `severity` must exist and fall into the color band corresponding to `score` (green/yellow/orange/red), otherwise **delivery is blocked**.

> The risk register template `templates/common/risk_register.md` renders this matrix's quick-reference table at the top, so you can compare directly while filling in the form.
