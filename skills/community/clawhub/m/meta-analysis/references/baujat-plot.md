# Baujat Plot — Heterogeneity Source Diagnostics

> 中文摘要：Baujat 图用于定位异质性来源与影响点——横轴为对总 Q 的贡献、纵轴为对合并效应的影响，右上角研究需重点核查。含 R 实现、论文级排版、解读规则，并纠正上游脚本坐标轴标签互换的错误。
>
> **Adapted from**: `meta-baujat-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

See also: `tsa_diagnostics.md` §baujat() (existing short entry — this file is the extended plotting/reporting companion), `radial-plot.md`, `forest-binary.md`.

---

## 1. Purpose / When to Use

A Baujat plot (Baujat 2002) separates two distinct questions that I² cannot answer:

- **Which studies create the heterogeneity?** (contribution to Cochran's Q)
- **Which studies move the pooled answer?** (influence on the overall estimate)

Use it whenever `I² > 50%`, or before any leave-one-out sensitivity analysis, to decide *which* studies deserve scrutiny. It is a diagnostic for the analyst — include it in the supplement, not usually the main paper.

| Situation | Use |
|---|---|
| I² > 50% and you must explain why | Yes |
| Choosing candidates for sensitivity analysis | Yes |
| k < 3 | No — undefined/uninformative |
| k > 30 | Yes, but suppress most labels or the plot is unreadable |

## 2. Input Data Requirements

Any `meta` object (`metabin`, `metacont`, `metagen`). Upstream accepts the same three CSV shapes as the funnel template (`Binary` / `Continuity` / `Survival`); see `funnel-plot.md` §2 for the column contracts.

Hard requirement: **k ≥ 3**. With k = 3 each point is dominated by the other two, so treat results as indicative only.

## 3. R Implementation Essentials

```r
library(meta)

bj <- baujat(m, yscale = 1, pos = 4, xmin = 1, ymin = 1)   # base-graphics version
# Programmatic access (no plot):
bj <- baujat(m, plot = FALSE)
# bj$x = contribution to overall heterogeneity (Q)
# bj$y = influence on the overall result
```

ggplot2 version for a publication-grade figure:

```r
d <- data.frame(study = m$studlab, x = bj$x, y = bj$y)
d$flag <- d$x > 2 * mean(d$x) | d$y > 2 * mean(d$y)

ggplot(d, aes(x, y)) +
  geom_vline(xintercept = mean(d$x), linetype = "dashed", colour = "grey50") +
  geom_hline(yintercept = mean(d$y), linetype = "dashed", colour = "grey50") +
  geom_point(aes(colour = flag), size = 3) +
  ggrepel::geom_text_repel(aes(label = study), size = 2.8, max.overlaps = 15) +
  scale_colour_manual(values = c(`FALSE` = "#2166ac", `TRUE` = "#b2182b"),
                      labels = c("Typical", "Potential outlier"), name = NULL) +
  labs(x = "Contribution to overall heterogeneity (Q)",
       y = "Influence on overall result") +
  theme_bw(base_size = 11) + theme(legend.position = "bottom")
```

> ⚠️ **Axis-label correction.** The upstream `baujat_plot.R` labels `bj$x` as "Contribution to overall result" and `bj$y` as "Contribution to heterogeneity (Q)" — these are **swapped**. Additionally, its manual fallback branch computes `x = (ΔTE)²` (influence) and `y = ΔQ` (heterogeneity), i.e. the opposite assignment to the primary `baujat()` branch. Use the orientation above (x = Q contribution, y = influence), which matches `meta`/`metafor` and `tsa_diagnostics.md`.

Use `ggrepel` for labels; fall back to `geom_text` only when unavailable, and reduce to top-10 labels if crowded.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG master → PDF/EPS/TIFF |
| DPI | ≥ 300 (upstream default of 150 is **below journal minimum**) |
| Size | 10 × 8 in draft; 120–170 mm wide at final size |
| Font | 9–11 pt axes, 7–8 pt point labels |
| Colour | Two-colour categorical (`#2166ac` typical / `#b2182b` flagged); greyscale-safe via shape as backup |
| Guides | Dashed mean lines on both axes to define quadrants |
| Labels | Study labels required — an unlabelled Baujat plot is useless |

Also export the underlying table (`study, x, y, rank`) as CSV so reviewers can verify the flagged studies.

## 5. Interpretation Rules — Read by Quadrant

| Quadrant | Meaning | Action |
|---|---|---|
| **Upper-right** (high Q contribution + high influence) | Drives heterogeneity **and** the pooled answer | Highest priority: verify data extraction, check RoB, run leave-one-out |
| Lower-right (high Q, low influence) | An outlier in effect, but too imprecise to move the pooled estimate | Explain it, but excluding it will not change conclusions |
| Upper-left (low Q, high influence) | Consistent with the rest but very heavily weighted (large trial) | Result depends on one trial — report a leave-one-out sensitivity analysis |
| Lower-left | Unremarkable | No action |

Reporting template: *"Baujat analysis identified Study X and Study Y in the upper-right quadrant, contributing the largest share of Q. Leave-one-out exclusion of these studies changed the pooled OR from a.aa to b.bb and reduced I² from p% to q%."*

Always follow a Baujat finding with an actual leave-one-out or subgroup analysis — the plot only generates hypotheses.

## 6. Common Misreadings — Warn the User

- **"Outlier" is not a licence to delete.** Excluding a study because it disagrees is data dredging. Exclude only for a pre-specified, documented methodological reason, and always report both analyses.
- **The `y > 2 × mean(y)` outlier rule used upstream is an ad-hoc heuristic**, not a validated cut-off. Report it as a screening device, and describe the rule explicitly if you use it.
- **Axis orientation is not standardised across packages/papers.** Always read the axis labels; never assume. (See the correction in §3.)
- **A high-influence study is not a biased study.** Large, well-conducted trials are supposed to be influential.
- **Baujat says nothing about the direction of bias**, only about contribution magnitude.
- **Do not use Baujat as evidence of publication bias** — that is what `funnel-plot.md` is for.
- **With small k, every point looks extreme.** Do not report quadrant findings when k < 5.
- **Removing the top-right study usually lowers I²** — that is arithmetic, not a discovery, and must not be presented as resolving heterogeneity.
- Baujat is a supplementary figure. Leading a results section with it signals that the primary synthesis was unstable.
