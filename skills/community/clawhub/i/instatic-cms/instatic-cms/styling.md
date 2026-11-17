# Styling

## Core Framework engine
- Design data lives as tokens: color tokens generate tint/shade scales from one base color, type is one fluid ramp that tracks viewport, spacing is a ratio-based scale, utility classes compile into a single small framework.css.
- Changing a token repaints every consumer. Site-level style changes trigger a republish of affected pages (server republish pass), so the canvas preview and the published output stay in step.

## Output pipeline
- Production pages link up to four hashed CSS bundles: reset (cross-browser baseline), framework (tokens/utilities), style (module + class CSS collected during render), userStyles (page-scoped author stylesheets kept verbatim).
- Module CSS is deduped per moduleId. Hidden nodes are pruned before render and contribute no CSS.

## Author classes and ambient rules
- Class registry holds named author classes; bare selectors (a:hover, nav > li) become ambient rules. Inline style attributes land per node.
- Pasted CSS and the agent's `site_apply_css` share one classifier: class-bearing selectors become registry classes, class-free selectors become ambient. Exact selector identity and !important survive the round trip.

## Token portability
Module CSS ships to published pages where editor tokens are absent; site framework tokens (the `--site-*` layer) are the portable surface. Hardcoded hex inside module code is exempt from the admin token policy but should stay token-referenced where possible.

## Import fidelity limits
@layer, conditional local @imports, and arbitrary external @imports are not modelable; Super Import surfaces them as warnings rather than dropping them silently. Everything else (unconditional local import graphs, @keyframes, @font-face, var()/clamp()/min()/max() values via the substitution encoder) round-trips into editable rules or page-scoped files.
