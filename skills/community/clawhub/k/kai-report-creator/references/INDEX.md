# References Index

Use this index to load only the reference files needed for the current route. `SKILL.md` is intentionally a thin router; detailed contracts live here.

| File | Load When | Owns |
|------|-----------|------|
| `html-shell-template.md` | Every `--generate` render | Shell entry contract, required IDs, child shell load map, duplicate-date guard, export and footer/watermark red lines |
| `html-shell/core-structure.md` | Every standard `--generate` render | Document skeleton, head/meta, report-summary JSON, section wrapper, footer/watermark body |
| `html-shell/shared-component-css.md` | Every standard `--generate` render | Shared component CSS and rhythm helper CSS |
| `html-shell/toc-edit-summary.md` | Every standard `--generate` render | TOC overlay, edit mode, and motion JS |
| `html-shell/summary-card.md` | Every standard `--generate` render | Summary card controls, poster-mode CSS, HTML, and JS |
| `html-shell/export.md` | Every standard `--generate` render | Export menu/buttons and print/desktop/mobile/IM image JS bindings |
| `html-shell/print-responsive.md` | Every standard `--generate` render | Print rules and mobile critical-control constraints |
| `theme-css.md` | Every `--generate` render and custom themes | CSS assembly order, post-shared theme overrides, custom theme fallback |
| `rendering-rules.md` | IR contains structured components | Directive parsing, no-raw-`:::` rule, component selection guard, child rendering load map |
| `rendering/plain-markdown.md` | Any rendered prose or headings | `##`/`###` section wrappers, `data-summary`, prose rhythm anchors |
| `rendering/kpi.md` | IR contains `:::kpi` | KPI contract, value-length limits, summary-card KPI constraints, badges |
| `rendering/chart.md` | IR contains `:::chart` | ECharts-only chart contract and chart schema rules |
| `rendering/table-list.md` | IR contains `:::table` or `:::list` | Table/list rendering contracts and single-line list compatibility |
| `rendering/timeline-diagram.md` | IR contains `:::timeline` or `:::diagram` | Timeline/diagram contracts, date whitelist, diagram schemas |
| `rendering/media-code-callout.md` | IR contains `:::image`, `:::code`, `:::callout`, or custom blocks | Media/code/callout rendering and custom block expansion |
| `anti-patterns.md` | Before `--generate` when visual anchors or components are chosen | Fake KPI, decorative chart, pseudo timeline, template heading, badge quota, color flood, weak summary/action patterns |
| `diagram-decision-rules.md` | Diagram or diagram-like content is being considered | Diagram go/no-go checks and safer downgrades |
| `regular-report-content-rules.md` | Weekly/daily/monthly/periodic reports or `regular-lumen` | Periodic report extraction, KPI selection, timeline narrative, next-period plan |
| `review-checklist.md` | `--review` and silent final review pass | Content/design review checkpoints and auto-fix boundaries |
| `review-report-template.md` | User asks for structured review summary | Review report output format |
| `spec-loading-matrix.md` | Before `--plan` and `--generate` | Silent classifier for `brief`, `research`, `comparison`, and `update` archetypes |
| `toc-and-template.md` | TOC, custom template, or theme override work | TOC link rules, custom template placeholders, theme override injection |
| `design-quality.md` | Design judgment is needed beyond deterministic shell/component rules | Visual quality baseline, typography, color discipline, rhythm guidance |
