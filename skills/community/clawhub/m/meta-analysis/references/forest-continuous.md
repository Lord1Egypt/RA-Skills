# Forest Plot — Continuous Outcomes

> 中文摘要：连续型结局（均数±标准差）森林图的论文级产出规范——metacont() 建模、SMD 与 MD 的选择、Hedges' g 与 Hartung-Knapp 校正、forest() 排版参数、以及效应量解读与常见误读。
>
> **Adapted from**: `meta-forest-binary-plot` (binary sibling template) and the `Continuity` branch of `meta-funnel-plot` / `meta-baujat-plot` / `meta-radial-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)
>
> Note: the upstream repository ships no standalone `meta-forest-continuous-plot` skill. This file reconstructs the continuous-outcome template from the upstream `metacont()` configuration used across the other AIPOCH meta plot scripts, plus `meta` package conventions.

See also: `forest-binary.md`, `revman_complete.md` §2.2, `esc_robust_meta.md` (effect-size conversion), `svg_editing.md`.

---

## 1. Purpose / When to Use

Use a continuous forest plot when each study reports **mean, SD and n per arm**.

| Situation | Effect measure |
|---|---|
| All studies use the *same* instrument and unit (e.g. mmHg, kg) | **MD** — clinically interpretable |
| Studies use *different* scales for the same construct (e.g. HAM-D vs BDI) | **SMD** (Hedges' g) |
| Skewed outcome, ratio-scale interpretation wanted | **ROM** (log ratio of means) |
| Only mean + CI or t/F/p available | Convert first → `esc_robust_meta.md`, then `metagen()` |

## 2. Input Data Requirements

| Column | Meaning | Constraint |
|---|---|---|
| `study` | Study label | Unique, non-empty |
| `group1_sample_size` | n, experimental | Integer > 0 |
| `group1_Mean` | Mean, experimental | Numeric |
| `group1_SD` | SD, experimental | Numeric > 0 |
| `group2_sample_size` | n, control | Integer > 0 |
| `group2_Mean` | Mean, control | Numeric |
| `group2_SD` | SD, control | Numeric > 0 |

Pre-flight validation:
- Reject SD = 0 or negative; reject SE mislabelled as SD (a common extraction error — SD ≈ SE × √n).
- Confirm **direction of scoring is aligned** across studies. If a higher score is good in some studies and bad in others, multiply the mean of the discordant studies by −1 before pooling and document it.
- If median/IQR was reported instead of mean/SD, convert with the Luo (mean) and Shi (SD) estimators, not the naive `IQR/1.35`, and flag the imputation.
- Change-from-baseline and final-value data may be combined for SMD but **not** for MD unless the same scale and anchoring apply.

## 3. R Implementation Essentials

```r
library(meta)

m <- metacont(
  n.e = df$group1_sample_size, mean.e = df$group1_Mean, sd.e = df$group1_SD,
  n.c = df$group2_sample_size, mean.c = df$group2_Mean, sd.c = df$group2_SD,
  studlab = df$study,
  sm               = "SMD",   # "SMD" | "MD" | "ROM"
  method.smd       = "Hedges",# small-sample corrected g (default, keep it)
  method.tau       = "REML",  # "DL" for RevMan parity; REML preferred otherwise
  method.random.ci = "HK",    # Hartung-Knapp — recommended when k is small
  random = TRUE, common = FALSE
)
```

`forest()` layout arguments specific to continuous data:

| Argument | Recommended value | Effect |
|---|---|---|
| `leftcols` | `c("studlab","n.e","mean.e","sd.e","n.c","mean.c","sd.c")` | Full raw-data audit trail |
| `rightcols` | `c("effect","ci","w.random")` | SMD/MD, CI, weight |
| `smlab` | `"Std. Mean Difference (95% CI)"` or `"Mean Difference (95% CI)"` | Header must name the measure |
| `xlab` | Unit for MD (e.g. `"mmHg"`); omit unit for SMD | SMD is unitless |
| `digits` | `2` for effect, `2` for CI | Avoid false precision |
| `layout` | `"RevMan5"` | Cochrane-familiar layout |
| `prediction` | `TRUE` when k ≥ 5 | 95% PI row under the diamond |
| `label.left` / `label.right` | Clinical direction text | e.g. "Favours intervention" |

The axis is **linear** (unlike OR/RR). The null reference line is at 0, not 1.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG master → EPS/TIFF/PDF per journal (`svg_editing.md`) |
| DPI | ≥ 300; 600 for line-art submissions |
| Width | 85 mm single column / 170 mm double column |
| Height | `2 + 0.4 * k` inches; widen further when 7 left columns are shown |
| Font | 8–10 pt final size; keep numeric columns monospaced-aligned |
| Colour | Blue squares + black diamond; must remain readable in greyscale |
| Decimals | Same number of decimals within a column across all rows |

With 7 left-hand columns a continuous forest plot easily exceeds 170 mm. If it does, drop `mean`/`sd` columns to a supplementary table rather than shrinking the font below 6 pt.

## 5. Interpretation Rules

1. Report `k`, total N, then `SMD = x.xx (95% CI y.yy–z.zz)` or `MD = x.xx unit (95% CI ...)`.
2. Report `I²`, `τ²`, `Q(df)`, `p` together.
3. For SMD apply Cohen's benchmarks **only as rough anchors**: 0.2 small · 0.5 moderate · 0.8 large. State that these are conventions, not clinical thresholds.
4. Where possible, back-translate SMD into the units of the most familiar instrument (`MD ≈ SMD × SD_reference`) so clinicians can judge relevance.
5. Compare the pooled estimate against the **MCID** (minimal clinically important difference) when one exists — statistical significance without MCID crossing is not a clinical claim.
6. When `method.random.ci = "HK"` is used, say so — the CI is wider than a standard DL CI by design.

## 6. Common Misreadings — Warn the User

- **SMD is unitless.** Never append a unit to it, and never describe it as "points on the scale".
- **Cohen's thresholds are not clinical thresholds.** An SMD of 0.2 can be clinically decisive in a lethal condition and trivial elsewhere.
- **Do not mix MD and SMD in one pooled estimate.** Pick one measure per outcome and state the rule.
- **Unaligned scale direction silently cancels real effects.** This is the most common fatal error in continuous meta-analysis — check it before pooling.
- **SD imputed from median/IQR/range inflates apparent precision.** Run a sensitivity analysis excluding imputed studies.
- **Hedges' g vs Cohen's d** — always use the small-sample-corrected g; d is upward-biased when n < 20 per arm.
- **Hartung-Knapp can produce a CI narrower than DL in rare configurations**; if that happens, report both and disclose.
- **A wide diamond crossing 0 means inconclusive, not equivalent.** Equivalence requires a pre-specified equivalence margin.
- Heterogeneity in continuous outcomes is often driven by instrument choice and follow-up length — check those covariates before concluding true clinical heterogeneity (see `baujat-plot.md`).
