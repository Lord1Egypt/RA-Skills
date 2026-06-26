# Markdown to HTML Example

This is a sample document to verify the `markdown-to-html` skill.

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
python3 scripts/markdown_to_html.py \
  --input-file sample.md \
  --output sample.html \
  --builtin-template docs-slate \
  --toc \
  --embed-assets
```
