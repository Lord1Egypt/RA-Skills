# Output Contract

The primary artifact is a structure-preserving, doctor-readable translation. It is not a summary report and it does not require a document-level metadata table.

## Core Output Rules

- Emit blocks in source reading order.
- Emit one translated block per source block and preserve the source anchor, such as `P2-B4`.
- Chinese appears first. The original source text appears immediately below the Chinese for the same block.
- Do not add information-summary, terminology-reference, rewrite, or commentary sections to the primary artifact.
- Only add a trailing `需重点核对项` section when clinically important low-confidence items remain after translation.

## Allowed Rendering Forms By Block Type

- `title`: Heading line with anchor, Chinese first, original immediately below.
- `paragraph`: Paragraph block preserving paragraph boundaries. Do not merge or split paragraphs.
- `list`: List block preserving item count, order, and list nesting depth when present.
- `key_value`: Stable structured table with consistent field/value columns. Do not rewrite field blocks as prose.
- `table`: Table structure preserved. Markdown tables are allowed when they faithfully represent the grid.
- `table`: Embedded HTML is allowed when Markdown tables cannot preserve merged cells, multi-line cells, or clinically important alignment.
- `signature`: Short structured block or small table that preserves signatory and date relationships.
- `header_footer`: Compact block preserving the header/footer text near its anchor.
- `image_adjacent_text`: Local paired block that keeps the text with the relevant nearby image context.

## Rendering Examples

### Paragraph Block

```md
### [P2-B4] paragraph
中文：
患者近三天反复发热，最高体温 38.6°C，伴咳嗽及乏力。

原文：
The patient had recurrent fever for 3 days, with a peak temperature of 38.6°C, accompanied by cough and fatigue.
```

### Field Block (`key_value`)

```md
### [P1-B2] key_value
| 字段 | 中文 | 原文 |
| --- | --- | --- |
| 姓名 | 王某 | Wang, XX |
| 出生日期 | 1982-04-17 | 1982-04-17 |
| 入院诊断 | 社区获得性肺炎 | Community-acquired pneumonia |
```

### Simple Table Block

```md
### [P3-B1] table
| 项目 | 中文 | 原文 |
| --- | --- | --- |
| 白细胞计数 | 12.4 x10^9/L | WBC 12.4 x10^9/L |
| 血红蛋白 | 108 g/L | HGB 108 g/L |
| 血小板 | 256 x10^9/L | PLT 256 x10^9/L |
```

### Low-Confidence Cell Inside A Table

Use the smallest useful scope. Mark only the uncertain cell, not the whole block.

```html
<h3>[P4-B3] table</h3>
<table>
  <tr><th>项目</th><th>中文</th><th>原文</th></tr>
  <tr><td>用法</td><td>每日一次</td><td>once daily</td></tr>
  <tr><td>剂量</td><td><mark>疑似 0.25 mg，需核对原件</mark></td><td><mark>appears to read 0.25 mg</mark></td></tr>
</table>
```

### Optional Trailing Verification Section

Include this section only when clinically important low-confidence items exist.

```md
## 需重点核对项

- `[P4-B3]` 药物剂量单元格疑似为 `0.25 mg`，涉及用药安全，建议对照原件或向开具医生确认。
- `[P6-B2]` 过敏原名称字迹不清，可能影响临床判断，建议人工复核。
```

## Prohibited Forms

- No required cover page, executive summary, or report-style metadata table.
- No conversion of `table` or `key_value` blocks into prose summaries.
- No reordering, merging, or relocation across anchors.
- No standalone terminology appendix in the primary artifact.
