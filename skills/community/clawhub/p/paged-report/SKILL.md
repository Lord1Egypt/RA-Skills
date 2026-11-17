---
name: paged-report
description: "Generate client HTML reports with A4 print via WebBridge. Triggers: client report, 发给客户, 报价, 进度汇报, 确认函."
version: 1.2.1
status: development
stability: review-pending
author: Ming Fang
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [reports, html, client, print, a4]
---

# Paged Report

Generate professional client-facing HTML reports with A4-oriented print styles and self-contained HTML. Browser/PDF pagination and physical page count require verification. Works for any client/project — not tied to a specific brand. The current catalog documents 14 entries (10 typed renderer components plus structural hero, TOC, section, and footer); the 5 family labels are accepted metadata values, not family-specific rendering policies.

## Trigger

Any of: "client report", "send report to client", "发给客户", "报价方案", "进度汇报", "确认函", "数据报告", "导入报告", "make a report for", "生成报告", "paged report"

## How it works

1. Identify template family + client/project name
2. Put report content in the structured JSON contract below
3. Render HTML from the paged-report repository root with `python3 -m generator.paged_report input.json --output report.html`
4. Kimi WebBridge (recommended for interactive/PDF preview): `navigate(http://127.0.0.1:...)` + `save_as_pdf(paper_format: "a4")`; verify the resulting PDF
5. Optional: `artifact-delivery` to publish a reviewed preview

**One reusable tab**: `session: "report-gen"` — navigate → save_as_pdf → repeat.

## Structured JSON generator

The repository includes a standard-library renderer and the canonical input schema at `schemas/report.schema.json`. Use it for repeatable reports instead of hand-editing a copied HTML file.

Minimal shape:

```json
{
  "family": "confirmation",
  "toc": true,
  "meta": {
    "language": "zh-CN",
    "title": "运费规则确认",
    "client": "客户名称",
    "category": "运营确认",
    "subtitle": "一句话说明",
    "date": "2026-09-07",
    "version": "v1.0"
  },
  "pages": [
    {
      "label": "规则与确认",
      "sections": [
        {
          "id": "rules",
          "title": "规则变更对比",
          "components": [
            {
              "type": "compare_table",
              "columns": ["项目", "变更前", "变更后"],
              "rows": [["免运门槛", "$200", "$150"]]
            }
          ]
        }
      ]
    }
  ]
}
```

Supported component types are `table`, `compare_table`, `callout`, `tag`, `kpi`, `progress`, `status_row`, `checklist`, `grid`, and `divider`; hero, TOC, sections, pages, and footer are generated structurally. Text is escaped by default. Do not put raw HTML, secrets, or unverified customer facts in the JSON.

`data_appendix` and package-level delivery manifests are proposed follow-up contracts, not supported input features in v1.2.1. Do not claim that the renderer provides searchable relational appendices, CSV export, or package registration until a later implementation passes its contract tests; see the review-pending design under `docs/reports/`.

## Accepted family labels (5 metadata values; family-specific rendering policies are not enforced)

| Family | Use when | Planning range (not enforced) |
|--------|----------|---------------|
| **proposal** | Quote, pricing, service proposal, 报价, 方案 | 3-7 |
| **data-audit** | Data quality, catalog audit, CSV analysis, 数据审计 | 5-10 |
| **progress** | Status update, milestone, 项目进展, 周报 | 2-5 |
| **confirmation** | Rule change, shipping, delivery, 确认函, 变更通知 | 1-2 |
| **handoff** | Technical delivery, import prep, 验收, 交付 | 2-8 |

Invoice excluded (accounting standards apply separately).

## CSS: load linked file

```
skill_view(name='paged-report', file_path='templates/base.css')
```

Inline entire CSS into `<style>` tag. Self-contained HTML, no external deps.

## HTML skeleton

```html
<!DOCTYPE html>
<html lang="zh-CN">  <!-- or lang="en" for English -->
<head>
<meta charset="UTF-8">
<title>{report title}</title>
<style>{full base.css content}</style>
</head>
<body>
<div class="page">
  <!-- COVER: hero + optional toc -->
  <div class="report-page cover">
    <div class="hero">
      <p class="eyebrow">{client} · {category}</p>
      <h1>{title}</h1>
      <p class="subtitle">{description}</p>
      <div class="meta">
        <span>{date}</span><span>{version}</span><span>{project}</span>
      </div>
    </div>
    <!-- optional TOC if 3+ sections -->
    <nav class="toc">
      <h2>目录</h2>
      <ol><li><a href="#s1">{section}</a></li></ol>
    </nav>
  </div>

  <!-- CONTENT PAGES: one logical authoring boundary per .report-page -->
  <div class="report-page flex-col">
    <div class="content-area">
      <section id="s1">
        <h2>{section title}</h2>
        {components: tables, callouts, cards, kpis, etc.}
      </section>
    </div>
    <div class="footer-area">
      <div class="footer"><p>{client} · {report type} · {date}</p></div>
    </div>
  </div>
</div>
</body>
</html>
```

Rules:
- Each `.report-page` is a logical authoring boundary with `min-height: 880px` on screen; it is not a guarantee of one physical A4 page
- `flex-col` + `.content-area` + `.footer-area` can push a footer after content when that logical page has spare space; overflow can reflow it
- Multiple `.report-page` divs provide authoring boundaries for multi-page reports
- `cover` class on the first page requests a print break after the cover; verify the target PDF
- Print-only `.page-label, .footer` horizontal padding (`4mm`) prevents left-edge glyph clipping when print mode resets report-page padding
- Self-contained: ALL CSS inline, no external links

## Component catalog (14 documented entries: 10 typed renderer components + 4 structural wrappers)

### Hero — required, cover page only
```html
<div class="hero">
  <p class="eyebrow">{client · category}</p>
  <h1>{main title}</h1>
  <p class="subtitle">{one-line summary}</p>
  <div class="meta"><span>{date}</span><span>{version}</span></div>
</div>
```

### TOC — when 3+ sections
```html
<nav class="toc"><h2>目录</h2>
<ol><li><a href="#s1">{title}</a></li></ol></nav>
```

### Section — logical content block
```html
<section id="s1"><h2>{title}</h2>{content}</section>
```

### Grid + Card — parallel items
```html
<div class="grid two">
  <div class="card"><h3>{title}</h3><p>{body}</p></div>
</div>
```

### Callout — 4 variants
```html
<div class="callout">{info}</div>
<div class="callout green">{success}</div>
<div class="callout amber">{warning}</div>
<div class="callout red">{error}</div>
```

### Table — header-repeat hint on page break; verify target PDF
```html
<table><thead><tr><th>A</th><th>B</th></tr></thead>
<tbody><tr><td>1</td><td><span class="tag green">Done</span></td></tr></tbody></table>
```

### Compare Table — before/after
```html
<table class="compare-table"><thead><tr><th>项目</th><th>旧</th><th>新</th></tr></thead>
<tbody><tr><td>X</td><td class="old">$200</td><td class="new">$150</td></tr></tbody></table>
```

### Tag — inline status
```html
<span class="tag green">完成</span>
<span class="tag amber">进行中</span>
<span class="tag red">待处理</span>
<span class="tag blue">信息</span>
```

### KPI — big number
```html
<div class="kpi">598 <span class="unit">产品</span></div>
```

### Progress Bar
```html
<div class="progress-bar green"><div class="fill" style="width:76%"></div></div>
```

### Status Row — compact list
```html
<div class="status-row">
  <span class="label">{what}</span>
  <span class="value"><span class="tag green">{status}</span></span>
</div>
```

### Checklist — action items
```html
<ul class="checklist">
  <li class="done">已完成</li><li>待完成</li>
</ul>
```

### Footer — generated per logical content page; verify physical placement
```html
<div class="footer"><p>{client} · {type} · {date}</p></div>
```

### Divider
```html
<hr>
```

## PDF via WebBridge

```bash
# Serve /tmp/report.html from a temporary localhost HTTP server first
python3 -m http.server 8765 --bind 127.0.0.1 --directory /tmp

# Navigate to the served file (reuses same tab)
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"http://127.0.0.1:8765/report.html"},"session":"report-gen"}'

# Save A4 PDF
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"save_as_pdf","args":{"paper_format":"a4","print_background":true,"path":"/tmp/report.pdf"},"session":"report-gen"}'
```

## Short page handling

- `.report-page { min-height: 880px }` — fills A4 on screen
- `.flex-col` + `.content-area { flex: 1 }` + `.footer-area { margin-top: auto }` — can push a footer toward the bottom when that logical page has spare space; verify print placement
- Content <30% of page: merge with next section
- Long table: the browser may split it; `thead` repetition is a print hint and must be verified in the target PDF

## Bilingual

Same template, swap text. `lang="zh-CN"` or `lang="en"`. Generate two files if needed.

## Pitfalls

- Always inline CSS — never `<link>` external stylesheet
- A `.report-page` is one logical authoring boundary; do not assume it maps to one printed page or nest page containers
- Hero only on first `.report-page.cover`
- **Long content overflow**: if a section is likely to exceed one A4 page, use the ~880px / ~45–50 line figure only as a rough screen-space planning heuristic, split it into multiple `.report-page` authoring boundaries when practical, and verify the resulting physical PDF. A single `.report-page` with `page-break-after: always` can spill onto a second physical page then force a break, leaving a mostly-blank page.
- WebBridge: reuse `session: "report-gen"`, don't create new session per report
- **Load kimi-webbridge skill** before using WebBridge curl commands — agents unfamiliar with the daemon will stall
- If WebBridge rejects `file://` because local-file access is disabled, serve the output from a temporary localhost HTTP server; do not change browser permissions just for report rendering
- Content that needs images: use `<img>` with max-width:100%, CSS handles sizing
- `lang="en"` reports: replace TOC heading `目录` with `Contents`, hero eyebrow with English labels
- Font weights 620/630/650 rely on Inter variable font; fallback stacks (PingFang SC, YaHei) will synthesize — acceptable but worth noting
