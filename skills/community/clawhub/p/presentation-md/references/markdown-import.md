# Markdown → Deck JSON

Bridge Marp / md-slides authoring into presentation-md without abandoning schema.

## CLI

```bash
presentation-md-render --from-md ./deck.md -o deck.json --theme signal
```

## MCP

`import_markdown` with `{ markdown, theme?, title?, output_path? }`.

## Export Markdown

```bash
presentation-md-render deck.json --format md -o deck.md
```

MCP `export_deck` with `{ format: "md" }` returns the Markdown string (or writes `output_path`).

Studio: **Source ▾ → Download Markdown**. Round-trips with Open `.md` / Paste MD / `import_markdown`.

## Front matter

```yaml
---
title: Acme Pitch
theme: signal
company: Acme
description: Optional
---
```

## Slide splits

Separate slides with a line that is exactly `---`.

## Layout mapping

| Markdown | Layout |
|----------|--------|
| `#` / first slide | `title` |
| lone `##` | `section` |
| bullets | `feature-grid` (or `stat-row` when `Value — Label`) |
| numbered list | `timeline` |
| markdown table | `data-table` |
| `>` quote | `quote` |
| ` ```lang ` fence | `code` |
| ` ```chart bar ` CSV | `chart` |
| ` ```html ` | `custom-html` |
| thank/next CTA last slide | `closing` |

## Craft heuristics

Wrap / present-mode layouts the bridge also detects (best-effort):

| Trigger | Layout |
|---------|--------|
| Heading/body matches `streak`, `days straight`, `habit grid` (+ optional `N days`) | `streak-grid` |
| `top N` / `percentile` / `completion` / `progress ring` **and** a `%` | `metric-ring` |
| Heading matches `rank` / `leaderboard` / `top N` + `Label — value` / `Label · NN%` bullets | `ranked-list` |
| Heading matches `logo` / `partner` / `trusted by` + ≥3 short bullets (≤28 chars) | `logo-wall` |
| Last slide heading matches thank/next/share/download **and** ≥2 CTA labels | `closing` with dual `actions[]` (solid + outline) |

Example streak beat:

```markdown
## 47 days straight

Habit grid for the launch week.
```

Example ranked beat:

```markdown
## Top sessions

1. Focus — 42%
2. Deep work — 31%
3. Standup — 18%
```

### Chart fence

````markdown
```chart bar
Quarter,Enterprise,Mid-market
Q1,38,14
Q2,41,16
```
````

### HTML fence

````markdown
```html
<div style="color:var(--accent)">One-off art</div>
```
````

Always `audit_deck` + `judge_deck` after import — heuristics are best-effort. Prefer dual `actions[]` with icons on launch/investor closings once you polish the imported JSON.
