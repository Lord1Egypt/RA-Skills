# Execution Constraints & Phased Execution

Moved from main SKILL.md to keep it concise.

## Hard Limits

1. **Self-Check Limit:** Max 1 self-check per Markdown generation. No repeat self-checks.
2. **Auto-Patch Limit:** Max 1 auto-patch after failed self-check. If still failing, stop and report.
3. **No Recursive Self-Invocation:** Do not re-trigger analysis from within analysis. Prompt user to initiate new round manually.
4. **PDF Read Limit:** Max 2 reads of same PDF per round. Beyond that, split into phases.
5. **Chat Output Limit:** File-first — chat only shows path + 3–5 core summaries + self-check result + manual-review items.
6. **Context/Call Overflow:** Stop immediately, prompt user to split into phases. Do not brute-force through overflow.

## Long PDF: Phased Execution Mode

When PDF > ~20 pages Methods+Results or context is tight, default to phased execution:

| Phase | Content | Output |
|-------|---------|--------|
| Phase 1 | Generate Study Profile | Study Profile table |
| Phase 2 | Generate Module A–B | Module A + B |
| Phase 3 | Generate Module C–D | Module C + D |
| Phase 4 | Generate Module E–G | Module E + F + G |
| Phase 5 | Merge all Phase outputs + final self-check | Complete Markdown file |

**Phase merge rules:**
- Each Phase writes to `temp/{FirstAuthor}_{Year}/Phase{N}.md` or `intermediate/{FirstAuthor}_{Year}/Phase{N}.md` (NOT `outputs_md/`).
- Phase 5 merge: delete all Phase-level titles (e.g., `# Phase 1`), replace with single `# 论文 Results 反向拆解`, then `## Metadata` / `## Study Profile` / `## Module A–G` / `## Revision log`. No Phase N titles in final file.
- If any Phase self-check fails after patch, stop subsequent Phases.
- **Default cleanup:** After successful merge, delete/move Phase temp files. Only preserve if `debug_mode: true`.
- Phase files only in `temp/{AuthorYear}/`; `outputs_md/` only keeps final Markdown.
- **Cleanup verification:** Report `cleanup failed` in chat if delete/move operations fail. Revision log must not claim cleanup that didn't execute.

## Output File Policy

1. Long papers may use phased generation; Phase files are temporary.
2. Phase files → `temp/{FirstAuthor}_{Year}/` or `intermediate/{FirstAuthor}_{Year}/`, not main output directory.
3. Final user-facing file: `outputs_md/reverse_engineer/{FirstAuthor}_{Year}_Results_Reverse_Analysis.md`.
4. Default: no Phase1–Phase4 files in main output directory.
5. `debug_mode: true` → preserve Phase files; otherwise delete/move to temp after successful merge.
6. Chat: only final Markdown path, no intermediate file paths.
7. **Merge format hard rule:** Final file has exactly one H1 (`# 论文 Results 反向拆解`), zero Phase N titles.

## Desktop Folder Mode

| OS | Desktop path |
|----|-------------|
| macOS | `~/Desktop/OpenClaw_Paper_Analysis/` |
| Linux | `~/Desktop/OpenClaw_Paper_Analysis/` |
| Windows | `%USERPROFILE%\Desktop\OpenClaw_Paper_Analysis\` |

Fallback if desktop inaccessible: `./OpenClaw_Paper_Analysis/`. Report fallback in chat.

Folder tree:
```
OpenClaw_Paper_Analysis/
├── outputs_md/
│   ├── reverse_engineer/
│   └── results_writer/
├── logs/
├── figures_notes/
└── templates/
```

File naming: `{FirstAuthor}_{Year}_Results_Reverse_Analysis.md`
