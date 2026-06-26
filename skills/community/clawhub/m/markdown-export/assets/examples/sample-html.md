# Markdown Export HTML Example

This is a sample document to verify the `markdown-export` skill in `html` mode.

## Supported Capabilities

- Markdown file input
- Markdown string input
- Custom Pandoc HTML templates
- Custom CSS overrides
- Built-in four style templates

## Example Table

| Template | Visual Direction | Use Case |
| --- | --- | --- |
| docs-slate | Documentation | Internal docs, Tech guides |
| magazine-amber | Editorial | Columns, Long forms, Content pages |
| product-midnight | Release | Release notes, Product updates |
| serif-paper | Paper | Articles, Essays, Whitepapers |

## Quote

> Templates handle the skeleton, CSS handles the visuals. Custom templates take priority over built-in ones.

## Code

```bash
python3 scripts/export_markdown.py \
  --format html \
  --input-file sample.md \
  --output sample.html \
  --builtin-template docs-slate \
  --toc \
  --embed-assets
```

## Full-Width Article Without TOC

```bash
python3 scripts/export_markdown.py \
  --format html \
  --input-file sample.md \
  --output sample-no-toc.html \
  --builtin-template docs-slate \
  --embed-assets
```

## Plain Body Without Article Card Background

```bash
python3 scripts/export_markdown.py \
  --format html \
  --input-file sample.md \
  --output sample-plain.html \
  --builtin-template docs-slate \
  --embed-assets \
  --no-body-background
```
