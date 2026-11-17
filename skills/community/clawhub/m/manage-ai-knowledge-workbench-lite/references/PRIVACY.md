# Lite privacy boundary

Lite is fixed to Metadata-only and `model_transport: none`.

The local deterministic parser may read authorized Markdown files to extract allowed frontmatter, headings, tags, and links. It does not send bodies to a model. Generated indexes and the dashboard exclude note bodies, sensitive records, secrets, and absolute source paths.

Source files are facts and remain read-only. `.ai-workbench`, `AI-Knowledge`, and `AI-Dashboard` are derived outputs inside the selected workspace.
