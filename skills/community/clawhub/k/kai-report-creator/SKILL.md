---
name: kai-report-creator
description: Use when the user wants to CREATE or GENERATE a report, business summary, data dashboard, or research doc — 报告/数据看板/商业报告/研究文档/KPI仪表盘. Handles Chinese and English equally. Supports generating from raw notes, data, URLs, or an approved plan file. Use for --plan (structure first), --generate (render to HTML), --review (one-pass automatic refinement), --themes (preview styles), --from FILE, --bundle, --export-image flags. Does NOT apply to exporting finished HTML to PPTX/PNG (use kai-html-export) or creating slide decks (use kai-slide-creator).
version: 1.23.3
user-invocable: true
metadata: {"openclaw": {"emoji": "📊"}}
---

# kai-report-creator

Generate single-file HTML reports from source notes or `.report.md` IR. Keep this file as a thin router: load only the references needed for the current path.

## Core Principles

1. **Zero Dependencies** — generated reports are self-contained HTML, with CDN or bundled assets only when needed.
2. **User Provides Data, AI Provides Structure** — never fabricate facts or numbers; use `[数据待填写]` / `[INSERT VALUE]` when data is missing.
3. **Plan Before Generate** — complex reports should become `.report.md` IR first, then HTML.
4. **Progressive Disclosure for AI** — output keeps `report-summary`, section annotations, and component data machine-readable.
5. **Thin Routing Over Prompt Growth** — `SKILL.md` routes work; detailed rules live in references.
6. **Contracts and Gates Beat Prompt Soup** — prefer IR, guard validation, shell tests, and post-render review over adding more prose to this hot path.

## Command Routing

When invoked as `/report [flags] [content]`, parse flags first:

| Flag | Action |
|------|--------|
| `--plan "topic"` | Write `.report.md` IR only. Stop after saving it. |
| `--generate [file]` | Render one `.report.md` IR to HTML. With no file given, treat as IR from context: extract exactly one valid IR block from context. Never render the surrounding conversation. |
| `--review [file]` | Refine an existing HTML report with `references/review-checklist.md`. |
| `--themes` | Write the themes preview HTML. |
| `--from <file>` | If the file starts with frontmatter, treat as IR; otherwise create IR, then render. |
| `--theme <name>` | Override the theme. Built-ins: `corporate-blue`, `minimal`, `dark-tech`, `dark-board`, `data-story`, `newspaper`, `regular-lumen`, `fangsong`. |
| `--template <file>` | Use a custom HTML template. See `references/toc-and-template.md`. |
| `--output <file>` | Save to this path instead of the default. |
| `--bundle` | Inline CDN assets where supported. |
| `--export-image [mode]` | After HTML generation, run `scripts/export-image.py`; mode is `im`, `mobile`, `desktop`, or `all`. |
| no flags + text | Create IR internally, then render HTML. |
| no flags + IR in context | Treat as `--generate` from context. |

Default output filename: `report-<YYYY-MM-DD>-<slug>.html`. Slug: lowercase ASCII, non-alphanumeric to hyphens, collapse hyphens, trim, max 30 chars.

## Reference Loading

Load reference files minimally by route; do not read every reference by default. In short: load only the references that materially help the current render path.

| Route | Always load | Conditional load |
|-------|-------------|------------------|
| `--plan` | `references/spec-loading-matrix.md`, `references/plan-flow.md`, `references/theme-routing.md` | `references/regular-report-content-rules.md` for periodic reports |
| `--generate` | `references/generate-flow.md`, `references/html-shell-template.md` + every `references/html-shell/*.md`, `references/theme-css.md`, `references/review-checklist.md` | `references/rendering-rules.md` then only the `references/rendering/*.md` files required by the IR; `references/anti-patterns.md` for visual anchors; `references/diagram-decision-rules.md` for diagrams; `references/regular-report-content-rules.md` for periodic reports |
| `--review` | `references/review-checklist.md` | `references/review-report-template.md` if a structured change summary is requested |
| custom theme/template | `references/theme-css.md`, `references/toc-and-template.md` | custom theme `reference.md` or `theme.css` |

Load `references/spec-loading-matrix.md` before `--plan` and `--generate` as a silent classifier. It covers optional archetypes: `brief`, `research`, `comparison`, `update`.

Always load `references/anti-patterns.md` before `--generate`. Load `references/diagram-decision-rules.md` whenever a diagram or diagram-like structure is being considered.

## IR Contract

Load `references/ir-contract.md` for the full frontmatter spec, validity terms, and compatibility anchors.

Quick reference:
- Three parts: YAML frontmatter, Markdown prose (`##`/`###`), component fences `:::tag [param=value]`.
- `:::kpi` uses `items:`; Use **ECharts** for ALL charts.
- Badges are optional visual enhancements, not a first-class IR tag.
- Validity taxonomy: `invalid_syntax`, `invalid_semantics`, `contract_conflict`, `auto_downgrade_target`.
- Timeline details live in rendering references; Allowed `Date` tokens must be real time markers, not decorative labels.
- Canonical component routing: `references/rendering-rules.md`; component details: `references/rendering/*.md`.

Minimal frontmatter example:
```yaml
theme: corporate-blue                  # Optional. Default: corporate-blue
report_class: mixed                    # Optional. Values: narrative, mixed, data
archetype: research                    # Optional lightweight archetype hint for silent classification.
```
Supported archetypes: `brief`, `research`, `comparison`, `update`.

## Language And Theme

Load `references/theme-routing.md` for the full theme-selection table and report-class rules.

Quick reference: auto-detect `zh` when CJK is material; apply to placeholders, TOC labels, date display, and shell labels.

## `--plan` Flow

Load `references/plan-flow.md` for the full 10-step procedure and narrative rhythm rules.

Key gates: save as `report-<slug>.report.md`; do not generate HTML; use real quantitative KPI values only.

Poster summary mode is opt-in. Do not infer `poster_title` or `poster_subtitle` from punctuation in `title`.

Narrative cadence blocks (`lead-block`, `section-quote`, `action-grid`) follow claim -> explanation -> scan anchor. These are optional prose upgrades, not default required blocks. If uncertain, keep normal paragraphs and add one clearer scan anchor instead of forcing a cadence block. Do not add more than one of `lead-block` / `section-quote` / `action-grid` by default inside the same section unless the source material clearly warrants it.

## `--generate` Flow

Load `references/generate-flow.md` for steps 1-8 (input parsing, guard validation, render, shell assembly, CSS).

Then run these quality gates in sequence — do not skip:

9. Run pre-write validation and fix all violations:
   - no raw `:::` in HTML
   - valid `ir-hash`
   - no generic/template h2 headings
   - short, real quantitative `.kpi-value` and `report-summary` KPI values; no placeholder or status-only KPI values
   - `.number` body numerals use tabular lining numerals
   - badges clarify status/category/entity, never quota-fill
   - timeline dates are real time markers
   - no U+FE0F
   - no `text-align: justify`, black-background flood, body letter-spacing > `0.05em`, or mobile-hidden critical controls
10. Run the final HTML quality gate with `scripts/html_quality_gate.py` on the rendered HTML. It must pass standard shell IDs, theme fidelity, and KPI value checks. If it fails, fix the HTML and rerun it before reporting success.
11. Run L2 shell checks. Required: `data-template="kai-report-creator"`, `data-version`, `data-theme`, `id="toc-toggle-btn"`, `id="toc-sidebar"`, `id="card-mode-btn"`, `id="sc-overlay"`, `id="export-btn"`, `id="export-menu"`, `id="export-print"`, `id="export-png-desktop"`, `id="export-png-mobile"`, `id="export-im-share"`, `id="report-summary"`, plus the JS bindings for print/desktop/mobile/IM export. If any export item or binding is missing, rebuild the whole export block from `references/html-shell/export.md`.
12. Run the silent final review pass from `references/review-checklist.md`, then write the HTML and report the path.

When the report is explicitly comparing named vendors, models, or tools, set `data-report-mode="comparison"` on the outer report container and use `.badge--entity-a/.badge--entity-b/.badge--entity-c` only for entity identity.

## `--review` Flow

1. Read the HTML file.
2. Load `references/review-checklist.md`.
3. Apply hard rules automatically; apply AI-advised rules only when confidence is high and factual accuracy is preserved.
4. One-pass automatic refinement; no confirmation window.
5. Use `references/review-report-template.md` when the user wants a structured summary.
6. Write back unless the user asked for diagnosis only.
7. Tell the user what changed and what was intentionally left untouched.

## `--themes` And `--export-image`

For `--themes`, read the theme preview template and write `report-themes-preview.html` verbatim.

For `--export-image`, after HTML generation run:

```bash
python <skill-dir>/scripts/export-image.py <output.html> --mode <mode>
```

If Playwright is unavailable, print install instructions and skip image export without failing HTML generation.

## Shell And Template Boundary

Generate complete self-contained HTML. Shell entry contract: `references/html-shell-template.md`; full shell structure, inline JS, export behavior, summary card, edit mode, TOC, print rules, Shell metadata, version/theme metadata, duplicate-date guard, and footer/watermark degradation rules: `references/html-shell/*.md`.

All scripts are inline in the shell template. Never load nonexistent files such as `templates/scripts/*.js`.

For custom templates and TOC slug rules, use `references/toc-and-template.md`.

## Final Output

Always end with the file path and a one-sentence summary. If a validation, guard, or export step could not run, say exactly which step was skipped and why.
