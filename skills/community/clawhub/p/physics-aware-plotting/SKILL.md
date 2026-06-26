---
name: physics-aware-plotting
description: Physics-aware scientific plotting for research repositories. Use before making or updating Matplotlib figures to identify axis meanings, the comparison the figure supports, physically meaningful axis ranges, appropriate linear/log scaling, and publication-style visual choices inspired by ApJ/AAS figures.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📈"
    requires:
      anyBins:
        - python
        - python3
---

# Physics-Aware Plotting

Use this skill for scientific figures, diagnostic plots, and slide or paper plots in research repositories.

## Core Workflow

Before plotting, explicitly determine:

1. What physical quantity is on each axis.
2. What comparison or claim the figure is supposed to support.
3. Whether linear or log scaling is physically appropriate.

Do not treat plotting as a purely cosmetic task. The chosen limits, scaling, and overlays should reveal the physical behavior that matters.

## Publication Style

For paper or slide figures, use an ApJ/AAS-inspired scientific plotting style. Treat this as a set of principles, not a rigid rcParams block.

Prefer:

- clean white figure and axes backgrounds;
- readable serif or journal-compatible fonts, with consistent math text;
- compact figure proportions suitable for one-column or two-column paper layouts;
- inward ticks, visible minor ticks when they help interpretation, and ticks on the top/right when appropriate;
- moderate axis, tick, and line widths that remain legible after resizing;
- legends that explain the physical comparison without covering important data;
- high-resolution or vector output suitable for manuscript and slide reuse.

Avoid:

- decorative styles that obscure the data;
- overly large fonts or lines that make a figure look like a presentation mockup when it is meant for a paper;
- arbitrary color choices that make model families or observational datasets hard to distinguish;
- silently changing scientific units, scales, or limits to make a plot look nicer.

If the repository already defines a Matplotlib style such as `apj`, use it when it matches these principles. If no project style exists, implement only the minimal local styling needed for the requested figure, and keep those choices transparent in the code.

## Axis-Range Rules

If the user specifies axis limits, follow them.

If limits are not specified:

- Choose ranges from the data and the intended physical message.
- Avoid meaningless empty decades on log axes.
- Do not default to extremely small lower bounds such as `1e-20` unless the plotted quantity actually has meaningful structure there.
- On log y-axes, prefer a lower bound around the smallest meaningful nonzero signal, observational point, or modeled feature that the figure is intended to show.
- Set the upper bound slightly above the maximum relevant curve or data point so structure is visible without excessive empty space.
- If the figure compares multiple redshifts, models, or panels, use consistent limits when that improves interpretability.

## Interpretation Rules

- Prefer layouts that separate different physical concepts instead of overloading one panel.
- If a transformation changes the meaning of the plotted quantity, reflect that in labels and legends.
- Keep legends readable; increase legend size when the plot will be embedded in slides.
- When a figure is for slides or papers, prioritize clarity over showing every diagnostic variant.

## Output Placement

Use these conventions when the repository has no stronger local rule:

- draft or diagnostic figures: `outputs/`
- reusable tables behind figures: `data_save/`
- figures required by slide compilation: `slides/assets/`

## Slide And Paper Figure Quality

When a figure is intended for slides or papers:

- Treat the output as publication-quality by default.
- Prefer vector `.pdf` output for the figure actually inserted into the slide or manuscript.
- If a raster companion is generated for quick viewing, export it at `>=500 dpi`.
- Do not treat low-resolution `.png` output as the canonical asset unless the user explicitly requests that.

Always use `dpi=500` in `fig.savefig()` for figure outputs unless the user explicitly requests otherwise.

## Cleanup Rule

When a slide figure is replaced, keep only the currently used asset in `slides/assets/`. Move one-off or historical plot variants to `outputs/` instead of leaving stale slide assets in place.

## Usage Examples

Example 1:

User asks: "Plot the UV luminosity function comparison at z=8."

The agent should first identify the x-axis and y-axis physical quantities, decide whether the luminosity function axis should be log-scaled, choose an ApJ/AAS-inspired publication style, choose y-limits around the meaningful model and observational range, then save the figure with `dpi=500`.

Example 2:

User asks: "The log plot has too much empty space below the curves."

The agent should inspect the smallest meaningful nonzero values, avoid arbitrary tiny lower bounds such as `1e-20`, and set the lower limit near the physically relevant signal or observational threshold.

Example 3:

User asks: "Make this figure ready for slides."

The agent should prioritize readable labels and legends, export the canonical slide asset as vector PDF when possible, optionally create a high-DPI raster companion, and avoid leaving superseded files in `slides/assets/`.
