# ALL-Sources

Updated: 2026-05-17

This package is a wiki-only release. It intentionally does not bundle raw source corpora.

## Compiled From

| Original source set | Compiled into | Count note |
|---|---|---|
| `n8n-io/n8n-docs` official docs mirror | `references/wiki/nodes/`, `references/wiki/concepts/`, `references/wiki/recipes/`, `references/wiki/api-cards/` | 518 node cards, 624 concept cards, 65 recipe cards, n8n Public API cards |
| Local Feishu/Lark API Markdown docs | `references/wiki/api-cards/`, `references/wiki/qa/` | Feishu API cards and one QA card |
| n8n official `.claude` references | `references/wiki/concepts/` and compiler guidance | Used as workflow generation guidance |

## Future Source Ingestion

When the user adds new raw docs later, create `references/source/<doc-set>/`, put the original files there, then use `references/compiler/ai-document-compiler.md` to compile them into wiki cards and update the relevant `ALL-*.md` indexes.
