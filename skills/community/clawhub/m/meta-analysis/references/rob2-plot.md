# RoB 2 Plots — Traffic-Light & Summary Bar

> 中文摘要：Cochrane RoB 2 偏倚风险图（红绿灯图 + 汇总条形图）的产出规范——D1–D5 五域数据契约、robvis 与 ggplot2 两条实现路径、官方配色与符号、论文级排版，以及"加权 vs 未加权"等常见误读。
>
> **Adapted from**: `meta-rob2-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

See also: `revman_complete.md` §X (GRADE), `forest-binary.md` (RoB-stratified sensitivity analysis), `svg_editing.md`.

---

## 1. Purpose / When to Use

Two standard figures accompany a Cochrane RoB 2 assessment of **randomised trials**:

- **Traffic-light plot** — one row per study, one column per domain, showing the per-study judgement. Required for transparency.
- **Summary bar plot** — stacked proportions per domain across all studies. Gives the reviewer the overview.

Both are expected in a Cochrane review and in most journal submissions of an SR/MA.

| Study design | Correct tool |
|---|---|
| Randomised trials | **RoB 2** (this file) |
| Non-randomised studies of interventions | ROBINS-I (different domains — do not reuse this template) |
| Diagnostic accuracy studies | QUADAS-2 |
| Prognostic factor studies | QUIPS |

RoB 2 judgements are **human expert assessments**. This template only visualises them — never auto-generate or infer domain judgements from study metadata.

## 2. Input Data Requirements

One row per study, wide format:

| Column | Meaning |
|---|---|
| `study` | Study label (Author + Year) |
| `d1` | Bias arising from the randomisation process |
| `d2` | Bias due to deviations from intended interventions |
| `d3` | Bias due to missing outcome data |
| `d4` | Bias in measurement of the outcome |
| `d5` | Bias in selection of the reported result |
| `overall` | Overall risk of bias |

Allowed values (exact strings, case-sensitive): `Low`, `Some concerns`, `High`, `No information`.

Validation rules:
- Reject or warn on any value outside the four above — silent factor-level coercion will drop those cells from the plot.
- Enforce the RoB 2 **overall algorithm**: `Low` only if all domains are Low; `High` if any domain is High **or** multiple domains raise Some concerns; otherwise `Some concerns`. Flag rows that violate this rather than silently plotting them.
- RoB 2 is assessed **per outcome**, not per study. If multiple outcomes are assessed, produce one figure per outcome and name the file accordingly.
- Optional `weight` column enables the weighted summary bar (see §5).

## 3. R Implementation Essentials

**Preferred path — `robvis`** (the Cochrane-endorsed package; produces publication-ready output with correct colours and domain captions):

```r
library(robvis)
rob_traffic_light(data = df, tool = "ROB2")
rob_summary(data = df, tool = "ROB2", weighted = TRUE, overall = TRUE)
```

**Fallback path — ggplot2** (when `robvis` is unavailable), following the upstream script:

```r
library(ggplot2); library(reshape2)

long <- melt(df, id.vars = "study")
long$variable <- factor(long$variable, levels = c("d1","d2","d3","d4","d5","overall"))
long$value    <- factor(long$value,
                        levels = c("Low","Some concerns","High","No information"))

pal <- c("Low" = "#4daf4a", "Some concerns" = "#ff7f00",
         "High" = "#e41a1c", "No information" = "#999999")
shp <- c("Low" = 43, "Some concerns" = 45, "High" = 120, "No information" = 63) # + - x ?

# Traffic light
ggplot(long, aes(variable, study)) +
  geom_tile(fill = "white", colour = "black", linewidth = 0.6) +
  geom_point(aes(fill = value, shape = value), colour = "black", size = 8) +
  scale_fill_manual(values = pal, name = NULL) +
  scale_shape_manual(values = shp, name = NULL) +
  labs(x = NULL, y = NULL) +
  theme_minimal(base_size = 12) + theme(panel.grid = element_blank())

# Summary bar (unweighted proportions)
prop <- as.data.frame(prop.table(table(long$variable, long$value), margin = 1))
ggplot(prop, aes(Var1, Freq, fill = Var2)) +
  geom_col() + coord_flip() +
  scale_fill_manual(values = pal, name = NULL) +
  scale_y_continuous(labels = scales::percent) +
  labs(x = NULL, y = "Proportion of studies") + theme_bw(base_size = 12)
```

The symbol layer (`+ − × ?`) is not decorative — it is what makes the figure legible in greyscale and to colour-blind readers. Keep it.

Canvas height must scale with k: `height_px = max(400, 100 + 40 * k)`, otherwise rows collide.

## 4. Publication-Grade Output Specification

| Parameter | Requirement |
|---|---|
| Format | SVG master → EPS/TIFF/PDF |
| DPI | ≥ 300; 600 for line art |
| Traffic-light width | 170 mm (6 columns + study labels needs the full width) |
| Traffic-light height | Scales with k; cap at one page, otherwise split by outcome |
| Summary bar | 170 × 60–90 mm, horizontal stacked bars |
| Font | 9–11 pt; study labels never below 7 pt |
| Colours | `robvis` official: Low `#02C100` · Some concerns `#E2DF07` · High `#BF0000` · No information `#4EA1F7`. The upstream ColorBrewer set (`#4daf4a`/`#ff7f00`/`#e41a1c`/`#999999`) is acceptable and more colour-blind-safe — pick one and use it consistently across all figures |
| Domain captions | Spell out D1–D5 in the caption; never ship `d1…d5` unexplained |
| Legend | Bottom or right, single row, showing both colour and symbol |

## 5. Interpretation Rules

1. Report the overall distribution first: `n (%) Low`, `Some concerns`, `High`.
2. Then name the **worst-performing domain** and its likely cause (typically D2 deviations in open-label trials, or D5 selective reporting where no protocol exists).
3. Feed this into GRADE: a substantial proportion of High-risk studies justifies downgrading for risk of bias.
4. Run a **RoB-stratified sensitivity analysis** — pool Low-risk studies only and compare with the primary estimate. Report both.
5. If a domain is dominated by `No information`, that is a reporting-quality finding in its own right; say so rather than treating it as neutral.
6. State whether the summary bar is weighted or unweighted (see warnings below).

## 6. Common Misreadings — Warn the User

- **Weighted vs unweighted bars answer different questions.** Weighted bars (by study size or meta-analytic weight) show how much *evidence* is at risk; unweighted bars show how many *studies* are. The upstream script's `1/count` construction is **unweighted** — label it as such. Never compare a weighted figure with an unweighted one.
- **RoB 2 has no numeric score.** Do not sum domains, average them, or compute a "quality score" — that is RoB 1.0 thinking and is explicitly discouraged.
- **Overall is not the mode or majority of the domains.** It follows the RoB 2 algorithm and is often driven by the single worst domain.
- **`No information` is not `Low`.** Absence of reporting is not evidence of good conduct.
- **RoB is outcome-specific.** One figure covering all outcomes is a methodological error.
- **A green traffic-light grid does not validate the pooled effect** — internal validity says nothing about applicability, indirectness or imprecision.
- **Do not exclude High-risk studies from the primary analysis by default.** Prefer sensitivity analysis; if you do exclude, pre-specify it.
- **Colour alone fails accessibility review.** Always retain the `+ − × ?` symbols.
- Do not let an automated pipeline assign domain judgements. This visualisation consumes assessments produced by two independent human reviewers with a documented consensus procedure.
