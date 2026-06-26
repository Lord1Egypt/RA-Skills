# md2pdf style guide

## Baseline choices

- Engine: XeLaTeX (best CJK + typography compatibility for mixed Chinese/English docs)
- Font strategy:
  - CJK main font: `Noto Sans CJK SC`
  - Latin serif: `DejaVu Serif`
  - Latin sans: `DejaVu Sans`
  - Monospace/code: `DejaVu Sans Mono`

## Recommended markdown authoring rules

1. Keep one H1 title only.
2. Use H2/H3 hierarchy consistently for TOC.
3. Always annotate fenced code language (e.g. ` ```bash `).
4. Keep tables concise; split very wide tables.
5. Use footnotes for dense annotations.

## Quality profiles

### Business report
- TOC: on
- Numbering: on
- Margin: 2.2cm
- Font size: 11pt

### Manual / print
- TOC: on
- Numbering: on
- Margin: 2.5cm
- Font size: 11pt or 12pt

### Dense technical appendix
- TOC: optional
- Numbering: on
- Margin: 2.0cm
- Font size: 10.5pt or 11pt

## If output still looks plain

- Add a custom LaTeX template and pass via defaults yaml
- Use a stricter markdown style guide for source authoring
- Normalize heading levels before conversion
