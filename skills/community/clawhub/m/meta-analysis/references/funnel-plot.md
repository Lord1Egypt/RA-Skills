# Funnel Plot & Publication Bias

> 中文摘要：漏斗图与发表偏倚检验的论文级产出规范——contour-enhanced 漏斗图、Egger/Begg/Harbord/Peters 检验的选择、trim-and-fill 的定位、出图排版要求，以及"漏斗图不对称 ≠ 发表偏倚"等常见误读。
>
> **Adapted from**: `meta-funnel-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

See also: `revman_complete.md` §V and §IX (RevMan funnel / bias mapping), `tsa_diagnostics.md` (selection models), `radial-plot.md`, `svg_editing.md`.

---

## 1. Purpose / When to Use

A funnel plot visualises effect estimate (x) against study precision (y) to inspect **small-study effects**. Use it as a *diagnostic*, never as a standalone test.

| Situation | Action |
|---|---|
| k ≥ 10 studies, mixed sizes | Draw funnel + run asymmetry test |
| k = 3–9 | Draw funnel only; **do not** run or report a formal test (power too low) |
| k < 3 | Do not draw |
| All studies of near-identical size | Funnel is uninformative — say so, skip the test |

The Cochrane Handbook threshold is **k ≥ 10**. The upstream AIPOCH script permits testing from k = 3; that is too permissive and must be overridden.

## 2. Input Data Requirements

Same three input shapes as the forest templates:

| Type | Required columns |
|---|---|
| `Binary` | `study`, `group1_Events`, `group1_sample_size`, `group2_Events`, `group2_sample_size` |
| `Continuity` | `study`, `group1_sample_size`, `group1_Mean`, `group1_SD`, `group2_sample_size`, `group2_Mean`, `group2_SD` |
| `Survival` | `study`, `group1_HR`, `group1_95%Lower CI`, `group1_95%Upper CI` |

For survival input, convert to the log scale before pooling:
`logHR = log(HR)`, `SE = (log(upper) − log(lower)) / (2 × 1.96)`. Rows with non-positive HR or CI bounds must be dropped and reported as excluded.

## 3. R Implementation Essentials

```r
library(meta)

# Contour-enhanced funnel — the publication default
funnel(m,
  contour    = c(0.90, 0.95, 0.99),          # significance contours
  col.contour= c("gray85","gray70","gray55"),
  yaxis      = "se",        # "se" (default) | "invse" | "invvar" | "size"
  ref        = 1,           # 1 for OR/RR/HR, 0 for MD/SMD
  studlab    = TRUE, cex.studlab = 0.7,
  xlab = "Odds Ratio", ylab = "Standard Error"
)
legend("topright", c("p > 0.10","0.05 < p < 0.10","0.01 < p < 0.05","p < 0.01"),
       fill = c("white","gray85","gray70","gray55"), bty = "n")
```

Asymmetry tests — pick by outcome type, do not run all and report the friendliest:

| Test | `metabias()` call | Use when |
|---|---|---|
| Egger | `method.bias = "Egger"` | Continuous / generic (SMD, MD, logHR) |
| Harbord | `method.bias = "Harbord"` | **Binary, OR** — corrects Egger's known bias |
| Peters | `method.bias = "Peters"` | **Binary**, especially with rare events |
| Begg (rank) | `method.bias = "Begg"` | Low power; supplementary only |
| Thompson–Sharp | `method.bias = "Thompson"` | Heterogeneity present |

```r
metabias(m, method.bias = "Harbord", k.min = 10)
tf <- trimfill(m, common = FALSE, random = TRUE)   # sensitivity, not correction
funnel(tf)  # filled studies shown as open circles
```

Always set `y`-axis to SE with the axis **inverted** (precise studies at the top) — this is `meta`'s default; do not "fix" it.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG master → EPS/TIFF per journal |
| DPI | ≥ 300 (600 for line art). The upstream script's 150 dpi is **below journal minimum** |
| Size | Square, 85–100 mm per side; funnels distort if aspect ratio ≠ 1 |
| Font | 8–10 pt; study labels 6–7 pt and only if k ≤ 20 |
| Contours | Greyscale shading, lightest = least significant, with a legend |
| Reference line | Dashed vertical at the pooled estimate |
| Axis | Log x-axis for OR/RR/HR; linear for MD/SMD |

Report the numeric test output in the text or a table, not only in the figure caption.

## 5. Interpretation Rules

1. Describe the **visual** impression (symmetric / asymmetric / sparse) before quoting any p-value.
2. Report the test as: name, statistic, p-value, and k. E.g. `Egger's test: intercept = 1.24 (SE 0.51), t = 2.43, p = 0.031, k = 14`.
3. Use **p < 0.10** as the conventional asymmetry threshold (these tests are underpowered), and say which threshold you used.
4. Contour-enhanced reading: if missing studies fall in **non-significant** contour regions → consistent with publication bias. If they fall in **significant** regions → asymmetry more likely from heterogeneity or true small-study effects.
5. Trim-and-fill is a **sensitivity analysis**: report "adjusted estimate x.xx vs unadjusted y.yy, n filled = k". Never replace the primary estimate with the filled one.
6. Conclude in GRADE language: asymmetry supports downgrading for publication bias, it does not prove it.

## 6. Common Misreadings — Warn the User

- **Asymmetry ≠ publication bias.** Competing explanations: true small-study effects (smaller trials enrol sicker/better-selected patients), poorer methodological quality in small trials, heterogeneity, chance, and artefactual asymmetry from the effect measure itself.
- **Never test with k < 10.** A non-significant Egger test at k = 5 is uninformative, not reassuring — do not write "no publication bias was detected".
- **Egger's test is biased for binary outcomes** because logOR and its SE are mathematically correlated. Use Harbord or Peters instead.
- **Funnel plots with OR and few events are asymmetric by construction.** This is a known artefact, not evidence.
- **Trim-and-fill assumes suppression is symmetric and effect-driven.** It performs poorly under heterogeneity and can invent studies that never existed. Never present filled points as real data.
- **Begg's test is much less powerful than Egger's** — a null Begg result adds almost nothing.
- **Do not choose the y-axis that looks most symmetric.** Fix `yaxis = "se"` a priori.
- **A symmetric funnel does not rule out bias** — outcome-reporting bias and grey-literature exclusion leave no funnel signature.
- Pre-specify the test in the protocol. Post-hoc test selection is the main route to a misleading bias claim.
