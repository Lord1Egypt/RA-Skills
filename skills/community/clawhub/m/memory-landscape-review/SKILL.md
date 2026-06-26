---
name: "memory_landscape_review"
description: "Use when the user wants to review auto-memory, promote durable instructions into CLAUDE.md or local memory, and clean up duplicates or conflicts."
---


# Memory Landscape Review

Use this skill to review project memory, local memory, and auto-memory together.

## Workflow
1. Gather repo memory files and current auto-memory context.
2. Classify each entry as repo-wide, personal, team-wide, or temporary.
3. Detect duplicates, conflicts, and outdated instructions.
4. Present a grouped report before making any changes.
5. Only apply promotions or cleanup after explicit approval.

## Guardrails
- Propose first, edit second.
- Do not guess when an instruction might be personal vs shared.
- Keep transient notes out of durable memory files.

## Example Requests
- Review my auto-memory and tell me what belongs in durable memory.
- Find duplicate or conflicting instructions across memory layers.

## Inputs
- Repo memory files
- Auto-memory state
- User preference for shared vs local memory

## Outputs
- Promotion proposals
- Conflict cleanup report
- No-change recommendations

## Success Criteria
- Durable memory candidates are identified clearly.
- Duplicates and stale entries are surfaced.
- No edits happen before approval.

## Non-Goals
- Silently editing memory files
- Guessing personal vs shared intent when ambiguous

## Source Provenance
Derived from `src/skills/bundled/remember.ts`.
