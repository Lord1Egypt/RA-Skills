---
name: meeting-to-kanban
description: Convert meeting notes or transcripts into a clean Kanban board with owners,
  due dates, blockers, and next actions.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Meeting to Kanban

## Purpose

Convert meeting notes or transcripts into a clean Kanban board with owners, due dates, blockers, and next actions.

## Trigger phrases

- 会议纪要转任务
- meeting notes to kanban
- 把会议变成看板
- action items from transcript
- 给我做项目任务板

## Ask for these inputs

- meeting notes/transcript
- board columns
- project context
- time horizon
- participants list if available

## Workflow

1. Extract decisions, action items, risks, and follow-ups.
2. Map actions into board columns such as Backlog, Next, Doing, Waiting, Done.
3. Assign owners and due dates when explicit; otherwise mark as unresolved.
4. Generate a CSV or Markdown board using the bundled columns schema.
5. Return a short manager summary and unresolved questions.

## Output contract

- kanban CSV
- manager summary
- owners and due dates table
- open questions list

## Files in this skill

- Script: `{baseDir}/scripts/tasks_to_kanban.py`
- Resource: `{baseDir}/resources/board-columns.yaml`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 会议纪要转任务
- meeting notes to kanban
- 把会议变成看板

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/tasks_to_kanban.py`.
- Bundled resource is local and referenced by the instructions: `resources/board-columns.yaml`.
