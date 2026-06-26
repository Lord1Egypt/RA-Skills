# Minimal Manuscript Example

This synthetic example demonstrates patterns that are commonly fragile in DOCX/PDF export.

## Safer Formula Style

Use math mode for scientific variables with subscripts, such as $Y_{ij}$ and $w_{ij}$.

Use `\operatorname{}` or `\text{}` for multi-letter quantities:

$$
\theta = \max\left(0, \min\left(1,
\frac{|\operatorname{metric}_{\text{raw}} - \operatorname{metric}_{\text{processed}}|}
{|\operatorname{metric}_{\text{raw}}|}
\right)\right)
$$

Literal column names should remain code spans, for example `metric_raw` and `qc_score`.

## Risky Formula Style

Avoid code spans when the intent is a mathematical subscript, for example `Y_ij` in prose.

Be cautious with `\mathrm{}` around multi-letter quantities:

$$
\mathrm{metricValue}_{\mathrm{raw}}
$$

Some DOCX-to-PDF conversion paths may render this as spaced letters.

## Table Stress Test

| Quantity | Source representation | Intended rendering | QC note |
| --- | --- | --- | --- |
| Row-by-column response | `$Y_{ij}$` | $Y_{ij}$ | Should preserve subscript. |
| Weight | `$w_{ij}$` | $w_{ij}$ | Should preserve subscript. |
| Literal output column | `` `metric_raw` `` | `metric_raw` | Should remain code text. |
