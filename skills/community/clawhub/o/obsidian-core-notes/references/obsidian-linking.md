# Obsidian Linking Conventions

Use these conventions for generated graph support files.

## Generated file names

- Non-Markdown source note: `<source filename>.core.md`
  - Example: `AIGC Paas平台介绍V1.1.pptx.core.md`
- Topic synthesis note: `专题综合.core.md`
  - Use `core_note_schema: topic-synthesis-v3-like` for deep V3-like synthesis.
- Folder index: `资料索引.md`
- Workspace index: `核心文件索引.md`

These names keep source attachments and summary notes as distinct Obsidian graph nodes.

## Generated markers

Only overwrite or delete files with one of these markers near the top:

- `<!-- CORE_FILE_NOTE_V1 -->`
- `<!-- CORE_FOLDER_INDEX_V1 -->`
- `<!-- CORE_WORKSPACE_INDEX_V1 -->`

If a target Markdown file exists without a marker, choose a generated fallback name instead of overwriting it.

## Wikilinks

- Link source attachments with the full source filename:
  - `[[path/to/source.pptx|source.pptx]]`
- Link sidecar notes without `.md`:
  - `[[path/to/source.pptx.core|source.pptx]]`
- Link topic synthesis notes without `.md`:
  - `[[path/to/专题综合.core|专题综合.core]]`
- Link folder indexes as:
  - `[[path/to/资料索引|资料索引]]`

## Relationship rules

Prefer high-signal links:

- Same folder.
- Same normalized title or version family.
- Shared project/topic path.
- Source file to generated `.core.md`.
- High-value topic folder to `专题综合.core.md`.
- Folder index to direct core files and child folder indexes.

Avoid graph noise from dependencies, caches, generated outputs, media asset folders, and vendor resource bundles.
