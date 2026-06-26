---
name: obsidian-vault-curator
description: Cautious curation, classification, review, and migration planning for Obsidian or Markdown vaults. Use when the user wants to organize a messy vault, classify notes, define canonical reference pages, separate current vs historical vs future-state material, design review dashboards or Bases views, or plan safe cleanup and migration without losing historical context. This skill requires installed Python 3 on PATH.
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins: ["python3"]
    install:
      - id: brew-python
        kind: brew
        formula: python
        bins: ["python3"]
        label: "Install Python 3 (brew)"
        os: ["darwin"]
---

# Obsidian Vault Curator

Bring structure to a messy Obsidian vault without flattening its history. Start with inventory. Then run separate read-only analysis passes. Then propose one small, reviewable write slice.

For multi-note work, use read-only subagents by default. Keep the main agent as the only writer. Use one bounded slice per subagent and separate passes for inventory, comparison, classification, verification, and sensitive-content review.

## Runtime requirement

This skill declares `python3` on `PATH` as a host requirement.

- The requirement is surfaced in metadata as `requires.bins: ["python3"]`.
- On macOS, the metadata includes a Homebrew install hint.
- On Linux, install Python 3 with your distro package manager, for example `sudo apt install python3`, then verify `python3 --version`.
- On Windows, install Python from the official Python Install Manager or with `winget install Python.Python.3.14`, then open a new terminal and verify that `python3 --version` works. If only `python` works, add a `python3` alias or shim on `PATH` before using this skill.
- The bundled helper scripts in `scripts/` use only the Python standard library.
- No extra Python packages are required.
- No exact minor version is currently pinned. The helpers were validated with Python 3.11+ and tested locally on macOS against Python `3.14.4`.
- Windows support is documented, but the full workflow has not yet been live-validated on Windows.

## Core rules

- Default to read-only.
- Use subagents by default for multi-note or heterogeneous work.
- Keep inventory first, then read-only review, then writes.
- Never delete notes unless the user explicitly asks.
- Never rewrite more than one write slice at a time. A write slice must stay within 3-10 related notes. Multiple-slice content rewrites in one pass count as mass-rewrite and require explicit user approval.
- Never run parallel write agents.
- Treat findings of sensitive content (see `references/subagents.md` glossary) as hypotheses until the main agent verifies the exact note content.
- Never rely on a global forced subagent model. Reuse the main-agent model when it fits; change model only when a specific role clearly benefits.
- Prefer `superseded_by` over overwrite.
- Preserve historical context.
- Treat `doc_kind` and `status` as separate concerns.
- Prefer controlled YAML frontmatter over ad-hoc tags for lifecycle state.
- Verify links and metadata after each write slice.

## Subagent policy

- Keep the main agent in control. Use subagents as read-only orchestrator workers, not as handoffs.
- The main agent may handle the work alone only when the work fits in one explicit bounded 3-10 note slice with no cross-slice comparison and no sensitive-content risk. Otherwise inventory first.
- If the task spans multiple slices, split it. Do not keep multiple large slices in the main agent working memory when subagents can inspect them separately.
- If the task is heterogeneous, use separate passes instead of one mixed prompt.
- Use separate passes for inventory, duplicate clustering, classification, review, link verification, and sensitive-content review.
- Treat all subagent findings as candidates only; the main agent must verify exact note text before any write.
- Never start write work before inventory plus read-only review are complete.
- Never use subagents for deletes, moves, renames, write slices, or exact-text verification of sensitive content. Subagents may flag sensitive candidates as hypotheses; only the verbatim verification happens in the main agent.
- Never mix models within one slice unless there is a clear reason.
- Keep writes serialized and never parallelize write agents.
- Cap classifier-reviewer rounds at 2 per slice. If they still disagree after round 2, escalate to human review.
- Read-only slices must stay within 200 notes per subagent call. Write slices must stay within 3-10 related notes.
- Use the named roles from `references/subagents.md` (`inventory-agent`, `classifier-agent`, `curation-reviewer`, `link-verifier`, `migration-planner`, `duplicate-cluster-agent`, `sensitive-content-agent`, and threshold-based `structural-move-planner`) instead of ad-hoc subagent prompts.
- Use the return shape defined in `references/output-format.md` unless the parent task explicitly asks otherwise.

## Workflow

1. Always read `references/status-schema.md` and `references/classification-rubric.md` before classifying any note, including a single-note task.
2. If the task spans multiple notes or requires cross-note comparison, read `references/workflow.md`.
3. If the user wants dashboards or views, read `references/bases-views.md`.
4. If the task spans multiple notes, multiple folders, cross-note comparison, duplicate risk, or heterogeneous material, read `references/subagents.md` and start with an inventory subagent. Only skip that when the work is already one explicit bounded 3-10 note slice with no cross-slice comparison. Keep subagents read-only by default. Keep all writes in the main agent. Subagents never write, even with user approval. If the user asks a named subagent to write, refuse the delegation and execute the write yourself in the main agent.
5. If findings need to be merged across slices or reviewed by a human, read `references/output-format.md`.
6. For larger areas, split the work into bounded slices by note cluster, topic cluster, or review queue. Use folder boundaries only when they are the natural boundary of a bounded slice.
7. Inventory the target area before proposing edits. Use `scripts/inventory_slice.py` when repeated folder scans would otherwise waste context.
8. Suggest canonical pages, status changes, supersession links, and the smallest safe write slice. Use `scripts/generate_migration_plan.py` with the JSON output of `scripts/inventory_slice.py` when the user wants a structured migration slice proposal.
9. Before structural writes and after every write slice, verify metadata with `scripts/validate_frontmatter.py`, verify links with `scripts/check_links.py`, and reassess whether the chosen canonical pages still make sense.
10. If a migration touches more than 50 notes or spans more than 3 vault top-level directories, use `structural-move-planner` instead of a normal migration-planner pass.
11. When spawning a subagent, use the labeled packet structure from `references/subagents.md` and the concrete examples from `references/subagent-packets.md`.

## Output shape

When curating a vault area, use the context router and shapes defined in `references/output-format.md` unless the user asks for a different format.

## Decision rules

- If a note is still useful but no longer leading, mark it `historical` and point to a successor.
- If a note describes a desired future state, mark `status: concept` and choose `doc_kind` separately.
- If validity is unclear, mark it `needs-review` first instead of guessing.
- If an old note may become useful again, prefer `reactivatable` over burying it.
- If multiple notes cover the same topic, nominate one canonical page and propose the rest as supporting or historical pages.
- If the vault already has a schema, adapt to it instead of forcing a new one.
- If a subagent flags sensitive content (see `references/subagents.md` glossary), verify the exact text in the main agent before escalating or editing.

## Safe operating mode

Use small, reviewable steps:

- classify before moving or merging
- move before rewriting when structure is the real problem
- create indexes and canonical pages before cleanup
- keep historical pages reachable
- ask before touching attachments, `.obsidian/`, or folder restructures that touch more than one folder or more than 10 notes

## Built-in helpers (require installed `python3`)

If `python3` is unavailable, the bundled helper scripts cannot run. Continue with the manual workflow and do not pretend a helper script ran.

- `scripts/inventory_slice.py` — scan one vault slice and summarize note counts, missing metadata, status/doc_kind coverage, title duplicates, exact-content duplicate clusters, and high-signal sensitive candidates that still require main-agent verification.
- `scripts/validate_frontmatter.py` — verify the controlled frontmatter shape on one slice before or after edits.
- `scripts/generate_migration_plan.py` — turn the JSON output of `scripts/inventory_slice.py` into a small, reviewable migration plan.
- `scripts/check_links.py` — inspect wikilinks in one slice and flag unresolved targets before or after moves. Treat results as slice-local unless the checked slice includes every possible target note.

## Large-section strategy

When the user wants work on a broader vault area or any task involving multiple notes:

1. keep one main agent as orchestrator
2. split the area into bounded slices
3. use read-only subagents for inventory, duplicate clustering, classification, contradiction checks, link review, and sensitive-content review, one bounded slice per subagent
4. merge findings in the main agent
5. execute one write slice at a time in the main agent

Prefer this over giving one agent the whole vault context at once. If the area cannot be answered confidently from the current instructions and one bounded slice of material, inventory first, then fan out into separate slices.

## References

- `references/status-schema.md` — controlled fields, values, and examples
- `references/classification-rubric.md` — note-by-note classification heuristics
- `references/workflow.md` — end-to-end curation and migration flow
- `references/bases-views.md` — suggested Bases views and review queues
- `references/subagents.md` — safe delegation model for larger vault jobs
- `references/subagent-packets.md` — concrete subagent packet examples for deterministic read-only delegation
- `references/output-format.md` — standard subagent return shape, merge rules, and human-review gates
