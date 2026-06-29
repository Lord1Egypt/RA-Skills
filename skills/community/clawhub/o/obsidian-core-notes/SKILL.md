---
name: obsidian-core-notes
description: Maintain Obsidian vault core-file notes, topic synthesis notes, folder indexes, and graph links. Use when working in an Obsidian vault or document/code workspace and creating, editing, moving, deleting, scanning, summarizing, or organizing files that may need `.core.md`, `专题综合.core.md`, `资料索引.md`, or `核心文件索引.md`.
---

# Obsidian Core Notes

Keep source files, generated `.core.md` notes, topic-level `专题综合.core.md` notes, and Obsidian relationship indexes synchronized.

## Workflow

1. Confirm the vault/workspace root. Use the current working directory unless the user names another root.
2. Before writing, run a scan when scope is broad:
   ```bash
   python <skill-dir>/scripts/obsidian_core_notes.py scan --root <vault-root> --json
   ```
3. Decide the note type before writing:
   - File sidecar: one generated `.core.md` for a non-Markdown source attachment.
   - Folder index: `资料索引.md` for navigation and direct source lists.
   - Topic synthesis: `专题综合.core.md` only for high-value folders that can support V3-like synthesis.
4. For create/edit/move/rename/delete operations, update the matching `.core.md` note and nearest `资料索引.md` in the same turn.
5. For bulk refreshes, run:
   ```bash
   python <skill-dir>/scripts/obsidian_core_notes.py refresh --root <vault-root>
   ```
   `refresh` creates lightweight sidecars and indexes; it does not replace human/LLM synthesis for `专题综合.core.md`.
6. For broad topic work, screen candidates before writing:
   ```bash
   python <skill-dir>/scripts/obsidian_core_notes.py topic-candidates --root <vault-root> --json
   ```
7. Validate after any bulk operation:
   ```bash
   python <skill-dir>/scripts/obsidian_core_notes.py validate --root <vault-root>
   ```
8. Clean generated notes only when explicitly requested:
   ```bash
   python <skill-dir>/scripts/obsidian_core_notes.py clean-generated --root <vault-root>
   ```

## Rules

- Treat non-Markdown source files as attachments and generate distinct sidecar notes named `<source filename>.core.md`.
- Reference existing Markdown core files directly; do not duplicate them.
- Put folder navigation in `资料索引.md`; put the workspace entrypoint in `核心文件索引.md`.
- Do not make every folder look deeply summarized. Most `专题综合.core.md` files should remain lightweight source maps unless the folder passes topic-synthesis screening.
- V3-like topic synthesis must include source provenance, version/history cues, core judgments, content map, reusable patterns/templates/components, actions, and open questions.
- When a user asks for aggressive cleanup, back up overwritten/deleted generated notes outside the vault before deletion.
- Use only generated markers for safe overwrite or deletion:
  - `<!-- CORE_FILE_NOTE_V1 -->`
  - `<!-- CORE_FOLDER_INDEX_V1 -->`
  - `<!-- CORE_WORKSPACE_INDEX_V1 -->`
- Never delete hand-written Markdown notes unless the user explicitly asks.
- Exclude dependencies, caches, logs, build output, model artifacts, static vendor bundles, and temporary Office lock files.

## References

- Read `references/core-file-rules.md` before changing core-file classification.
- Read `references/obsidian-linking.md` before changing note names, tags, markers, or relationship link conventions.
- Read `references/topic-synthesis-core-notes.md` before screening folders for V3-like `专题综合.core.md` notes or rewriting many topic notes.

## Scripts

- `scripts/obsidian_core_notes.py scan`: count core candidates and summarize scope.
- `scripts/obsidian_core_notes.py refresh`: create or update `.core.md`, `资料索引.md`, and `核心文件索引.md`.
- `scripts/obsidian_core_notes.py topic-candidates`: rank folders whose direct sources may justify V3-like `专题综合.core.md`.
- `scripts/obsidian_core_notes.py validate`: verify generated marker counts and common corruption patterns.
- `scripts/obsidian_core_notes.py clean-generated`: remove only files with generated markers.

## Common Pitfall

If the user wants "像 V3 一样的专题综合", do not stop after `refresh`. `refresh` is a graph-maintenance pass; it can produce version/source statistics, but the V3-style note is a curated synthesis pass over selected folders.
