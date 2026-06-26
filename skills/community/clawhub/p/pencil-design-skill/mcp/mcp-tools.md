# MCP Tool Quick Reference

> **Applies to**: Mode B (MCP Tools)
> **See also**: [image-reuse.md](image-reuse.md) · [screenshot-qa.md](screenshot-qa.md)

Quick reference for the Pencil MCP tools used in Mode B. For the full Mode B workflow, see the "Mode B — MCP tool-based" section in `SKILL.md`.

---

## Tool Overview

| Tool | Use |
|------|-----|
| `pencil_get_editor_state` | First call — get file state and `.pen` schema |
| `pencil_batch_get` | Read nodes, find `reusable: true` components |
| `pencil_batch_design` | Insert / copy / update / delete / move / generate-image |
| `pencil_get_variables` / `pencil_set_variables` | Read / write design tokens |
| `pencil_get_screenshot` | Visual verification |
| `pencil_snapshot_layout` | Detect clipping, overflow, overlap (`problemsOnly: true`) |
| `pencil_get_guidelines` | Topics: `code`, `tailwind`, `landing-page`, `design-system`, `table` |
| `pencil_find_empty_space_on_canvas` | Place new screens |
| `pencil_search_all_unique_properties` / `pencil_replace_all_matching_properties` | Audit & bulk-edit properties |
| `pencil_open_document` | Open / create document |

---

## Typical Call Order

```
1. pencil_get_editor_state        -> get .pen schema, current state
2. pencil_batch_get reusable=true -> discover existing components (REUSE > recreate)
3. pencil_get_variables           -> read tokens; pencil_set_variables to create new
4. pencil_find_empty_space        -> place new artboards
5. pencil_batch_design            -> build ONE section at a time
6. pencil_get_screenshot + pencil_snapshot_layout(problemsOnly:true) -> verify each section
7. Fix issues -> re-screenshot -> re-check (verify loop)
8. Final full-file layout audit -> problemsOnly MUST be empty before declaring done
```

## Verification Discipline

- Always screenshot and run `pencil_snapshot_layout(problemsOnly: true)` after **each** section, not only at the end. See [screenshot-qa.md](screenshot-qa.md).
- Before generating new images/logos, search existing nodes with `pencil_batch_get` and copy/resize rather than regenerate. See [image-reuse.md](image-reuse.md).
- For bulk property audits or token migrations, prefer `pencil_search_all_unique_properties` + `pencil_replace_all_matching_properties` over manual per-node edits.
