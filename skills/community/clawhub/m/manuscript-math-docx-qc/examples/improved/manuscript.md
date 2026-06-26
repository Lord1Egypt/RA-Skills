# Improved Manuscript Example

This synthetic example applies every best practice from the
`manuscript-math-docx-qc` skill. It is intentionally longer than the
minimal example (multiple sections, several display equations, two
tables, and figure cross-references) so the contact-sheet QC can
exercise page breaks, table overflow, and math-mode subscripts in
prose.

## 1. Inline Math Variables with Subscripts

All scientific variables with subscripts are written in math mode,
never as code spans.

The per-cell response variable is $Y_{ij}$ where $i$ indexes the
sample and $j$ indexes the feature. The corresponding weight is
$w_{ij}$. A reference value is $x_{i0}$ and the design matrix entry
is $x_{ij}$.

Code-style column names remain backticked: `metric_raw`,
`metric_processed`, `qc_score`, `n_cells`, `frac_expressing`.

Standard error is written as $\text{SE}_{\text{raw}}$ (math mode with
`\text{}` for the named subscript), not as `SE_raw` (which would lose
the subscript and read as "S E underscore raw").

## 2. Multi-Letter Quantities in Display Math

Multi-letter quantities always use `\operatorname{}` so Word does not
space the letters apart.

The primary effect decomposition is

$$
\Delta_{\text{total}} = \Delta_{\text{detection}} + \Delta_{\text{expression}} + \Delta_{\text{composition}}
$$

The bounded agreement score is

$$
\theta = \max\!\left(0,\ \min\!\left(1,\ \frac{\left|\operatorname{metric}_{\text{raw}} - \operatorname{metric}_{\text{processed}}\right|}{\left|\operatorname{metric}_{\text{raw}}\right|}\right)\right)
$$

The donor-aware bootstrap coverage is

$$
\widehat{\operatorname{Cov}}_{1-\alpha} = \Pr\!\left(\theta \in \bigl[\widehat{\theta}_{\text{lo}},\ \widehat{\theta}_{\text{hi}}\bigr]\right)
$$

All three formulas should render with consistent italic math letters
and no spurious spaces inside the multi-letter operator names.

## 3. Risky Patterns (Intentionally Avoided)

The following patterns, taken from the skill's common-failure-modes
list, are deliberately not used here:

- `\mathrm{metricValue}_{\mathrm{raw}}` would render with spaced
  letters in some DOCX-to-PDF paths. We use
  `$\operatorname{metric}_{\text{raw}}$` instead.
- `` `Y_ij` `` in prose would render as "Y_ij" with a literal
  underscore. We use `$Y_{ij}$` instead.
- A backtick-wrapped formula inside a long sentence would clip in
  Word. We split it into prose plus a display equation.

## 4. Wider Formula Page

To exercise page-break behaviour, here is a longer equation that
approaches the right margin:

$$
\mathcal{L}(\beta) = -\sum_{i=1}^{n} \left[ y_i \log \hat{p}_i + (1 - y_i) \log (1 - \hat{p}_i) \right] + \lambda \left\| \beta \right\|_2^2
$$

And a multi-line aligned equation that uses `aligned` rather than
hard-coded tabs:

$$
\begin{aligned}
\widehat{\Delta}_{\text{detection}} &= \frac{1}{n}\sum_{i=1}^{n} \bigl(\hat{p}_{i,\text{treated}} - \hat{p}_{i,\text{control}}\bigr) \\
\widehat{\Delta}_{\text{expression}} &= \frac{1}{n}\sum_{i=1}^{n} \hat{p}_{i,\text{shared}} \cdot \bigl(\hat{\mu}_{i,\text{treated}} - \hat{\mu}_{i,\text{control}}\bigr) \\
\widehat{\Delta}_{\text{composition}} &= \frac{1}{n}\sum_{i=1}^{n} \bigl(\hat{\pi}_{i,\text{treated}} - \hat{\pi}_{i,\text{control}}\bigr) \cdot \hat{\mu}_{i,\text{shared}}
\end{aligned}
$$

## 5. Table That Should Fit Comfortably

The following table is narrow enough to render without overflow or
truncated columns. Each row pairs a literal output column (code) with
its intended math rendering.

| Quantity | Source | Intended | QC note |
| --- | --- | --- | --- |
| Per-cell response | `$Y_{ij}$` | $Y_{ij}$ | Subscript preserved. |
| Per-cell weight | `$w_{ij}$` | $w_{ij}$ | Subscript preserved. |
| Reference value | `$x_{i0}$` | $x_{i0}$ | Two-char subscript preserved. |
| Standard error | `$\text{SE}_{\text{raw}}$` | $\text{SE}_{\text{raw}}$ | `\text{}` for named subscript. |
| Output column | `` `metric_raw` `` | `metric_raw` | Code font, not italic. |
| Output column | `` `qc_score` `` | `qc_score` | Code font, not italic. |

## 6. Figure Cross-Reference (Mock)

The decomposition diagram in `Figure 1` should be regenerated
before DOCX export, and the upload package must be re-synced.

$$
\text{Figure 1: effect architecture vector in 3D}\qquad \vec{a}_g = (\Delta_{\text{detection}},\ \Delta_{\text{expression}},\ \Delta_{\text{composition}})
$$

The next section demonstrates a paragraph that intentionally pushes
the content past one page so the contact sheet contains more than
one rendered image.

## 7. Multi-Page Stress

The following paragraphs are filler to push content to page 2 and
beyond. Real manuscripts should not be padded; this is a QC fixture
only.

Decomposition methods partition a total effect into additive
components. The exact identity holds when the partition is defined
as a Shapley value over the contributing factors. The donor-aware
bootstrap resamples whole donors, not individual cells, so the
inference respects the dependency structure of the assay. The
cluster-robust sandwich estimator handles small numbers of clusters
better than naive cell-level standard errors.

When the number of donors is large, donor-level and cell-level
confidence intervals converge. When the number of donors is small,
the donor-level interval is wider but has correct coverage under
exchangeability.

Pairwise decomposition between any two groups is obtained by
applying the same machinery to the two-group contrast. Compositional
decomposition adds a third factor whose contribution is measured as
the between-group difference in cell-type fractions, weighted by the
shared within-group expression profile.

The Wasserstein-distance variant replaces the mean contrast with
the full distribution contrast and is more sensitive to
multimodality.

## 8. Equation-Heavy Paragraph

The expected coverage of the donor-clustered bootstrap is

$$
\mathbb{E}\bigl[\widehat{\operatorname{Cov}}_{0.95}\bigr] \approx 0.93
$$

under the working exchangeability assumption. The naive cell-level
bootstrap has expected coverage of approximately $0.39$ on the same
fixture, which is why the skill flags donor-aware resampling as a
hard requirement for any manuscript that draws confidence intervals
from fewer than ten donors.

The invariant tests added in the v1.5.0 upgrade verify that

$$
\operatorname{architecture\_distance}(a,\ a) = 0
$$

and that

$$
\operatorname{architecture\_distance}(a,\ b) = \operatorname{architecture\_distance}(b,\ a)
$$

for every pair of effect-architecture vectors $a$ and $b$ in the
test fixture.

## 9. Closing Checklist

Before declaring the improved example ready, verify on the contact
sheet that:

- subscripts survive on every page that contains math,
- `\operatorname{}` quantities do not show spurious spaces,
- table columns do not wrap or truncate,
- figure cross-references render in a consistent style,
- no page is blank or clipped at the right margin.
