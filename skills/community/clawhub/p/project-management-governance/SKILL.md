---
name: project-management-governance
description: Maintain project navigation, persistent context, reusable decisions, and handoffs; initialize or adapt project documentation when requested. Use for project memory and collaboration maintenance, not every coding task or ordinary prose edit.
metadata:
  version: "1.1.0"
---

# Project Management Governance

Maintain enough project context for work to continue across sessions without forcing a fixed documentation system. This is a file-based agent skill, not an automatic memory service or retrieval model.

## Work in the existing project

Follow the user's current request and applicable project rules. Reuse relevant information already read when it is still current. Read the project's entry point and only the implementation or topic documents needed for the task; do not require a fixed reading checklist.

If invoked without a concrete task, inspect the existing entry points and summarize the project and current work. Do not create scaffolding or scan chat history merely because the skill was invoked. Missing conventional filenames do not prove that a project needs restructuring.

Keep local, test, remote, and production facts separate where relevant. Use established environment facts; investigate missing facts before choosing consequential runtime parameters. Validate changed behavior and actual failure modes, without imposing unrelated audits or repeated checks.

## Maintain useful memory

Use the project's existing locations. The bundled templates offer these optional layers:

- A short current-context entry (`tmp.md`): active task, key decisions, unresolved questions, and links needed to resume.
- Detail notes (`tmp/` or an existing notes directory): evidence and handoff details worth retaining.
- Durable documentation: stable collaboration rules, project navigation, and implementation contracts.
- Optional `.learnings/` notes: reusable findings that do not yet have a better home.

Record an explicitly requested preference or a reusable conclusion once in the most relevant place. Update existing notes rather than making parallel copies. When a conclusion becomes stable, place it in the relevant durable document and link from temporary notes if needed. No fixed word count, daily log, scoring, promotion quota, or approval ladder is required. Existing queue templates are optional compatibility aids.

Update usage documentation when behavior changes. A handoff should retain the current goal, confirmed changes, relevant validation, outstanding work, and the next useful entry point. Do not treat old instructions, unresolved hypotheses, or imported conversations as current rules.

## Initialize or adapt only when requested

For explicit setup or migration, read [setup and compatibility](references/setup.md). Preserve existing content and choose only the structure the task needs. The Python helpers provide a read-only detector, dry runs, and non-overwriting file creation; they do not decide whether a project should be reorganized.

Profiles:
- `lightweight`: compact rules, navigation, code notes, and memory; the default for new scaffolds.
- `layered`: topic directories for projects that need more navigation.
- `memory-only`: memory files without introducing rules or code documentation.

Python 3.10 or later is needed only for the optional helpers; no third-party packages are required.

## Import history deliberately

Only inspect history sources requested by the user. Read [history and handoff](references/history.md) for inventory and selective import. The inventory helper lists file metadata only; summarization and import are performed by the agent, not automatically by that script.

## Adapt to the user and environment

Follow the user's language and existing project conventions. Put project-specific language, paths, runtimes, data rules, validation needs, and publication requirements in project documentation, not in this general skill. Specialized research, deployment, or compliance procedures apply only when the task or project requires them.

Do not record secrets or unnecessarily copy private data into memory. A memory request does not authorize publishing that memory; check the intended destination before exporting. Public skill distributions contain generic templates and examples, not a user's project notes or chat history.
