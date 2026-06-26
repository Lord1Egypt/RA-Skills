# IR Contract

`.report.md` has three parts:

1. YAML frontmatter between `---` delimiters.
2. Markdown prose with `##` / `###` headings.
3. Component fences: `:::tag [param=value]` ... `:::`.

## Minimal Frontmatter

```yaml
---
title: Report Title
theme: corporate-blue                  # Optional. Default: corporate-blue
date: YYYY-MM-DD
lang: zh
report_class: mixed
archetype: research                    # Optional lightweight archetype hint for silent classification.
audience: "Busy decision-maker"
decision_goal: "Decide next move"
must_include:
  - Source truth that must survive compression
must_avoid:
  - Decorative placeholder chart
charts: cdn
toc: true
animations: true
abstract: "One-sentence summary"
poster_title: "Optional stronger poster headline"
poster_subtitle: "Optional poster subtitle"
poster_note: "Optional short closing sentence"
template: ./my-template.html
theme_overrides:
  primary_color: "#E63946"
custom_blocks:
  my-tag: |
    <div class="my-class">{{content}}</div>
---
```

For trivial reports, omit optional fields. For high-stakes or complex reports, keep `report_class`, `audience`, `decision_goal`, `must_include`, and `must_avoid` so review/evals can detect drift.

Poster summary mode is opt-in. Do not infer `poster_title` or `poster_subtitle` from punctuation in `title`.

## Validity Terms

`invalid_syntax`, `invalid_semantics`, `contract_conflict`, `auto_downgrade_target`.

## Compatibility Anchors

- `:::kpi` canonical body uses `items:`.
- Timeline Allowed `Date` tokens: `YYYY-MM-DD`, `YYYY-MM`, `YYYY`, `Q[1-4] YYYY`, `Day N`, `Week N`, `Month N`.
- Use **ECharts** for ALL charts.
- Badges are optional visual enhancements, not a first-class IR tag.

Canonical component routing lives in `references/rendering-rules.md`; component details live in `references/rendering/*.md`.
