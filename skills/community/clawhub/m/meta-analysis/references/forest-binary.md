# Forest Plot — Binary Outcomes

> 中文摘要：二分类结局（事件数/样本量）森林图的论文级产出规范——metabin() 建模、forest() 排版参数（leftcols/rightcols/layout）、字号尺寸 DPI 配色、以及效应量与异质性的解读与常见误读。
>
> **Adapted from**: `meta-forest-binary-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

See also: `revman_complete.md` §IV (RevMan→R forest mapping), `forest-continuous.md`, `svg_editing.md` (journal format export).

---

## 1. Purpose / When to Use

Use a binary forest plot when every included study reports **event counts and group totals** for two arms (experimental vs control), and the synthesis target is OR, RR, or RD.

| Situation | Use this template |
|---|---|
| RCTs / cohorts with dichotomous outcome (death, response, AE) | Yes |
| Only effect estimates + CI available (no counts) | No → `metagen()`, see `revman_complete.md` §2.4 |
| Continuous outcome (mean ± SD) | No → `forest-continuous.md` |
| Single-arm proportions | No → `single_group_meta.md` |

Minimum k = 2 to draw, but k ≥ 5 before drawing inferential conclusions from the pooled diamond.

## 2. Input Data Requirements

Long-format CSV, one row per study:

| Column | Meaning | Constraint |
|---|---|---|
| `study` | Study label (Author + Year) | Unique, non-empty |
| `outcome_new` | Outcome name (optional) | Used for titles/filenames |
| `group1_Events` | Events, experimental arm | Integer ≥ 0 |
| `group1_sample_size` | Total N, experimental arm | Integer > 0 |
| `group2_Events` | Events, control arm | Integer ≥ 0 |
| `group2_sample_size` | Total N, control arm | Integer > 0 |

Pre-flight validation (block execution on failure):
- Events ≤ total in **both** arms.
- No negative or non-integer counts.
- Flag double-zero rows (`0/n` in both arms) — MH drops them by default; Peto or a continuity correction is needed if they matter.
- If any arm has zero events, prefer `method = "Peto"` (rare events) or `MH.exact = TRUE` over the default 0.5 correction.

## 3. R Implementation Essentials

```r
library(meta)

m <- metabin(
  event.e = df$group1_Events, n.e = df$group1_sample_size,
  event.c = df$group2_Events, n.c = df$group2_sample_size,
  studlab = df$study,
  sm      = "OR",     # "OR" | "RR" | "RD"
  method  = "MH",     # "MH" | "Peto" | "Inverse" | "GLMM"
  random  = TRUE, common = FALSE
)
```

Key `forest()` arguments that control publication layout:

| Argument | Recommended value | Effect |
|---|---|---|
| `layout` | `"RevMan5"` | Reviewer-familiar Cochrane look |
| `leftcols` | `c("studlab","event.e","n.e","event.c","n.c")` | Raw counts on the left |
| `rightcols` | `c("effect","ci","w.random")` | Effect, CI, weight on the right |
| `common` / `random` | `FALSE` / `TRUE` | Show only the model you pre-specified |
| `text.random` | `"Total (95% CI)"` | Label for the summary diamond |
| `lty.random` | `0` | Suppress the prediction-line artifact |
| `col.square` / `col.diamond` | `"blue"` / `"black"` | Study markers vs pooled diamond |
| `colgap` | `grid::unit(6,"mm")` | Prevents column collision |
| `prediction` | `TRUE` when k ≥ 5 | Adds 95% prediction interval |
| `label.e` / `label.c` | Real arm names | Never leave as "Experimental/Control" in a paper |
| `smlab` | `"Odds Ratio (95% CI)"` | Column header above the plot area |

Log-scaled effects (OR/RR) must be plotted on a log axis — `metabin()` handles this automatically; do **not** hand-build a linear-axis OR plot.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG (editable master) + TIFF/EPS for submission; PNG only for drafts |
| DPI | ≥ 300 for colour/greyscale, 600–1200 for line art (`ggsave(dpi = 600)`) |
| Width | Single column 85 mm, double column 170 mm |
| Height | Scale with k: `2 + 0.4 * k` inches, then verify no row overlap |
| Base font | 8–10 pt at final print size; never below 6 pt |
| Colour | Greyscale-safe; blue squares + black diamond survives B&W printing |
| Reference line | Solid vertical line at 1.0 (OR/RR) or 0 (RD) |
| Arrow labels | `"Favours [treatment]" / "Favours [control]"` below the axis |

Export path: render SVG first, then convert per journal spec — see `svg_editing.md`.

## 5. Interpretation Rules

Report in this order:
1. **k and N** — number of studies and total participants.
2. **Pooled effect** — `OR = x.xx (95% CI y.yy–z.zz), p = ...`, random-effects unless fixed was pre-specified.
3. **Heterogeneity** — `I² = xx%, τ² = x.xxx, Q(df) = xx.x, p = ...`. Always report all four, not I² alone.
4. **Prediction interval** when k ≥ 5 — this, not the CI, describes where a future study is expected to land.
5. **Direction** — state explicitly which arm is favoured, in clinical terms.

Heterogeneity bands (Cochrane Handbook): 0–40% may be unimportant · 30–60% moderate · 50–90% substantial · 75–100% considerable. Bands overlap by design — interpret alongside τ² and the p-value for Q, not mechanically.

## 6. Common Misreadings — Warn the User

- **Weight ≠ importance.** Square size reflects precision (inverse variance), not study quality or clinical relevance.
- **Overlapping CIs do not imply homogeneity**, and non-overlapping CIs do not prove heterogeneity. Use Q/I²/τ².
- **I² is not an absolute measure of variance.** With small k or very precise studies, I² can be high while τ² is trivially small.
- **A narrow diamond crossing 1.0 is evidence of no meaningful effect; a wide diamond crossing 1.0 is inconclusive.** These are different conclusions and must not be reported identically.
- **Random-effects widens the CI but does not fix heterogeneity** — it prices it in. Still investigate the source (see `baujat-plot.md`, `radial-plot.md`).
- **OR overstates RR when the outcome is common** (baseline risk > ~10%). Prefer RR for common outcomes in RCTs.
- **Do not pool k = 2.** Draw the plot if asked, but state that τ² is unestimable in practice and no pooled inference should be drawn.
- **Zero-cell handling changes the answer.** Always disclose which correction or method was used.
- Never report a pooled result without the corresponding heterogeneity statistics in the same sentence or table row.
