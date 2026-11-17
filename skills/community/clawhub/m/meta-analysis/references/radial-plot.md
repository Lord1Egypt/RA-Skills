# Radial (Galbraith) Plot — Heterogeneity & Outlier Screening

> 中文摘要：Radial/Galbraith 图以精度(1/SE)为横轴、标准化效应(z)为纵轴，通过 ±2 置信带快速识别偏离研究并目视判断异质性。含 metafor::radial() 与 ggplot2 实现、论文级排版、解读规则与常见误读。
>
> **Adapted from**: `meta-radial-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

See also: `baujat-plot.md` (influence diagnostics), `funnel-plot.md` (the radial plot is a rotated funnel), `tsa_diagnostics.md`.

---

## 1. Purpose / When to Use

The radial plot (Galbraith 1988) rescales every study to a common variance so that heterogeneity becomes visually assessable without the funnel's precision distortion.

- **x = precision = 1/SE** — larger studies sit to the right.
- **y = standardised effect = θᵢ/SEᵢ** (a z-score).
- The fitted line passes through the **origin** with slope = pooled effect.
- Under homogeneity, ~95% of points fall inside a **±2 band** around that line.

| Situation | Use |
|---|---|
| Screening for studies inconsistent with the pooled effect | Yes |
| Visual heterogeneity check that is less size-biased than a funnel | Yes |
| Publication-bias assessment | **No** — use `funnel-plot.md` |
| k < 3, or all studies with near-identical SE | No — the x-range collapses |

Because it uses the same coordinates as Egger's regression, the radial plot is the natural visual companion to that test — but it is a **heterogeneity** tool, not a bias tool.

## 2. Input Data Requirements

Any `meta`/`metafor` object. Upstream supports `Binary` / `Continuity` / `Survival` CSV shapes — see `funnel-plot.md` §2.

Essential: pooling must occur on the **log scale** for ratio measures (log OR, log RR, log HR). Plotting raw OR on the radial axes is invalid because the null is not at 0.

Minimum k = 3; interpret cautiously below k = 10.

## 3. R Implementation Essentials

Canonical implementation — prefer this over a hand-built version:

```r
library(metafor)
res <- rma(yi, vi, data = df, method = "FE")   # radial plots assume a common effect
radial(res, main = "Radial (Galbraith) Plot",
       xlab = "Precision (1/SE)", ylab = "Standardised effect (z)")
```

`metafor::radial()` draws the arc scale on the right, which reads off the effect size directly — keep it; it is the feature that distinguishes a radial plot from a plain scatter.

ggplot2 version when a custom style is required:

```r
d <- data.frame(study = m$studlab,
                prec  = 1 / m$seTE,
                z     = m$TE / m$seTE)
b <- m$TE.common                      # slope = pooled effect (fixed-effect)
d$expected <- b * d$prec
d$inside   <- abs(d$z - d$expected) <= 2

xmax <- max(d$prec) * 1.1
band <- data.frame(x = c(0, xmax, xmax, 0),
                   y = c(2, b * xmax + 2, b * xmax - 2, -2))

ggplot() +
  geom_polygon(data = band, aes(x, y), fill = "lightblue", alpha = 0.3) +
  geom_abline(intercept = 0,  slope = b, colour = "darkblue", linewidth = 0.9) +
  geom_abline(intercept =  2, slope = b, colour = "darkblue", linetype = "dashed") +
  geom_abline(intercept = -2, slope = b, colour = "darkblue", linetype = "dashed") +
  geom_hline(yintercept = 0, colour = "grey50", linetype = "dotted") +
  geom_point(data = d, aes(prec, z, colour = inside), size = 3) +
  ggrepel::geom_text_repel(data = d, aes(prec, z, label = study), size = 2.8) +
  scale_colour_manual(values = c(`TRUE` = "#2166ac", `FALSE` = "#b2182b"),
                      labels = c("Outside band", "Inside band"), name = NULL) +
  xlim(0, xmax) + theme_bw(base_size = 11)
```

Notes: the band must start at x = 0 (the origin anchors the regression). Use the **fixed-effect** pooled estimate for the slope — under a random-effects model the ±2 band no longer has its nominal coverage. `ggplot2` ≥ 3.4 requires `linewidth =` rather than `size =` for lines.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG master → EPS/PDF/TIFF |
| DPI | ≥ 300 (upstream 150 dpi is below journal minimum) |
| Size | 100–170 mm wide; keep near-square so the band angle is not distorted |
| Font | 9–11 pt axes, 7–8 pt study labels |
| Colour | `#2166ac` inside / `#b2182b` outside; add shape coding for greyscale |
| Axis | x must start at 0 — a truncated x-axis breaks the geometry |
| Band | ±2 (or ±1.96) shaded, with dashed boundaries and a legend entry |

Report the companion table (`study, precision, z, expected z, inside/outside`) as CSV or a supplement.

## 5. Interpretation Rules

1. **Slope** = pooled effect. A slope near 0 means no overall effect.
2. **Scatter width** = heterogeneity. Tight around the line → homogeneous; fanning out → heterogeneous.
3. **Points outside the ±2 band** are inconsistent with the common-effect model. Expect ~5% outside by chance alone.
4. Quantify: report `n outside / k (%)`. Rough reading — ≤5% consistent with homogeneity · 5–20% mild · 20–40% moderate · >40% substantial heterogeneity.
5. **Right-hand points** (high precision) dominate the fit; a single large study far from the line is more consequential than several small ones.
6. Always report I², τ² and Q alongside — the radial plot supplements, never replaces, the numeric statistics.

## 6. Common Misreadings — Warn the User

- **This is not a publication-bias plot.** Asymmetry here reflects heterogeneity; use a contour-enhanced funnel plot for bias.
- **~5% of points lie outside the band under perfect homogeneity.** One outlying study out of 20 is expected, not a finding.
- **Do not delete "outside-band" studies.** Investigate them (population, dose, follow-up, RoB); exclusion requires a pre-specified reason and a reported sensitivity analysis.
- **The band assumes a fixed-effect model.** If a random-effects model is the primary analysis, state that the band is a diagnostic device with no inferential coverage.
- **Precision on the x-axis is not sample size.** A small trial with a very common outcome can out-rank a large trial with a rare one.
- **Ratio measures must be on the log scale.** Plotting OR directly puts the null at 1 and invalidates the origin-anchored line.
- **Radial plots become unreadable above ~25 studies.** Label only the outside-band points.
- **A tight radial plot does not validate the pooled estimate** — consistent studies sharing the same bias will look perfectly homogeneous.
- Verify the legend mapping when customising colours; the upstream script's label ordering depends on factor level order and is easy to invert silently.
