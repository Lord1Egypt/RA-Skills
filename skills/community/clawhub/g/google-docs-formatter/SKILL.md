---
name: google-docs-formatter
description: Instruction-only workflow for formatting, editing, and creating Google Docs using the existing gog skill/CLI. Use when a user asks to format a Google Doc, convert Markdown into a Google Doc, update sections, preserve structure, or fix Google Docs formatting. Relies on gog for all Google Docs/Drive API operations; contains no scripts or direct API clients.
---

# Google Docs Formatter

Use this skill to format or update Google Docs through the existing `gog` skill/CLI. This skill is instruction-only: do not introduce new API clients, scripts, dependencies, or credential flows.

## Core rule

Rely on `gog` for all Google Docs and Drive operations. If the gog skill is not loaded and command details are needed, load the `gog` skill first.

Prefer Google Docs-native workflows over DOCX conversion. Avoid third-party proxy services unless the user explicitly requests them.

## Safety and approval

Before any write operation, state the target document and intended change, then get explicit user approval unless the user has already clearly approved that exact change.

Always ask before:
- `gog docs clear`
- replacing the full document body
- large multi-section replacements
- deleting text ranges
- changing a shared/work document whose ownership or audience is unclear

Safe to do without extra approval when already working on the user-approved doc:
- inspect metadata/structure
- export/read content
- prepare Markdown locally
- run dry-run style checks if supported

## Standard workflow

1. Identify the target doc.
   - Accept a Google Docs URL or document ID.
   - Extract the ID from URLs like `https://docs.google.com/document/d/<DOC_ID>/...`.

2. Inspect before editing.
   ```bash
   gog docs info <DOC_ID> --json
   gog docs structure <DOC_ID>
   gog docs export <DOC_ID> --format md --out /tmp/doc.md
   ```

3. Decide the edit strategy.
   - New document from Markdown: use `gog docs create --file`.
   - Replace a known placeholder or section: use `gog docs find-replace --format markdown`.
   - Small textual fix: use `gog docs edit` or `gog docs sed`.
   - Append content: use `gog docs write --append` or `gog docs insert`.
   - Full rewrite: only after explicit approval; prefer creating a copy first.

4. Prepare content as Markdown.
   - Use Markdown headings, bullets, numbered lists, tables, bold/italic, and links.
   - Keep semantic structure simple; Google Docs conversion is more reliable with clean Markdown.
   - For images, use supported Markdown image syntax only if `gog docs create` / `find-replace --format markdown` supports the source.

5. Apply the change with `gog`.

6. Verify after editing.
   ```bash
   gog docs structure <DOC_ID>
   gog docs export <DOC_ID> --format md --out /tmp/doc-after.md
   ```
   Compare the exported Markdown or structure against the intended result.

7. Report concisely.
   - What changed
   - Any limitations observed
   - Link or doc ID if useful

## Common operations

### Create a formatted Google Doc from Markdown

Prepare a local Markdown file, then:

```bash
gog docs create "Document title" --file /path/to/content.md
```

Use this instead of Markdown → DOCX → Drive upload unless the user specifically needs DOCX behavior.

### Replace a placeholder with formatted Markdown

Best when the document contains a marker such as `{{SECTION_DRAFT}}`.

```bash
gog docs find-replace <DOC_ID> '{{SECTION_DRAFT}}' --content-file /path/to/section.md --format markdown --first
```

Prefer `--first` when replacing a unique placeholder to avoid accidental repeated changes.

### Replace an existing section

If possible, first ask the user to add or approve stable markers around the section:

```text
<!-- START: SECTION_NAME -->
old content
<!-- END: SECTION_NAME -->
```

Then replace the bounded content with `gog docs find-replace --format markdown` using a prepared Markdown file.

If there are no stable markers, use `gog docs structure` to identify paragraphs and proceed carefully. Do not guess destructive ranges.

### Small text edits

```bash
gog docs edit <DOC_ID> "old text" "new text" --match-case
```

For regex-style replacements:

```bash
gog docs sed <DOC_ID> 's/old pattern/new text/g'
```

Use regex edits only when the match is unambiguous.

### Append content

```bash
gog docs write <DOC_ID> --file /path/to/content.md --append
```

If Markdown formatting is required, prefer placeholder replacement with `--format markdown` when available.

### Full document rewrite

Only after explicit approval. Prefer making a copy first:

```bash
gog docs copy <DOC_ID> "Backup before rewrite"
gog docs clear <DOC_ID>
gog docs write <DOC_ID> --file /path/to/content.md
```

Tell the user if the write path preserves only text rather than rich Markdown formatting; use `create --file` or `find-replace --format markdown` for rich Markdown conversion.

## Formatting guidance

Use simple, robust Markdown:

```markdown
# Title

## Section

Short paragraph.

- Bullet one
- Bullet two

| Column A | Column B |
| --- | --- |
| Value A | Value B |

**Bold** and *italic* text.
```

Avoid fragile formatting unless tested:
- deeply nested lists
- complex merged tables
- unusual HTML
- custom fonts/colors not expressible through Markdown

For advanced visual formatting not supported by `gog`, explain the limitation and propose the nearest `gog`-supported alternative.

## When to stop and ask

Ask the user before proceeding if:
- the document ID is ambiguous
- the requested formatting requires capabilities not exposed by `gog`
- the edit would delete or overwrite substantial content
- the exported/inspected structure does not match expectations
- `gog` reports auth/scope errors

Do not install other Google Docs skills just to complete formatting. This skill is meant to compose with `gog`, not replace it.
