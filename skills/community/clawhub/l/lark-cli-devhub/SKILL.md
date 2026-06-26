---
name: lark-cli-devhub
description: Use when a developer needs lark-cli or feishu-cli workflows to turn Feishu/Lark into a project knowledge hub for bugfix memory, task clarity, release evidence, pitfall lookup, AI run summaries, or main-branch writeback discipline.
metadata:
  requires:
    bins: ["lark-cli", "python3", "git"]
---

# Lark CLI Dev Hub

Lark CLI Dev Hub is a development knowledge system backed by Feishu Base, Docs/Wiki, Tasks, and Whiteboard. Use it to prevent repeated bug investigation, keep task state explicit, and preserve release evidence.

Discovery aliases: `feishu-cli`, `飞书 CLI`, `lark-cli`, `Lark CLI`, `Feishu Dev Hub`, `Lark Dev Hub`, `Codex Feishu`, `Claude Code Feishu`.

## Core Boundaries

- Agent memory stores collaboration preferences and workflow style.
- Lark CLI Dev Hub stores project facts, tasks, bug evidence, pitfalls, playbooks, decisions, releases, artifacts, and AI run summaries.
- Do not write secrets, access tokens, app secrets, private keys, raw credentials, or full environment files.
- Treat Base as the structured source of truth. Docs hold long-form context. Whiteboard is a visual aid with a text summary linked back to Base.

## Local Entry Points

```bash
export DEVHUB_HOME="${DEVHUB_HOME:-$HOME/.codex/devhub}"

python3 "$DEVHUB_HOME/bin/devhub.py" search --project "$(basename "$PWD")" --query "symptom area keywords"
python3 "$DEVHUB_HOME/bin/devhub.py" record-bugfix --payload /tmp/devhub-bugfix.json
python3 "$DEVHUB_HOME/bin/devhub.py" record-ai-run --payload /tmp/devhub-ai-run.json
python3 "$DEVHUB_HOME/bin/devhub.py" record-release --payload /tmp/devhub-release.json
python3 "$DEVHUB_HOME/bin/devhub.py" sync-outbox --cwd "$PWD"
```

Config defaults to:

```text
$HOME/.codex/devhub/config.json
```

Project-local receipts and outbox:

```text
.devhub/receipts/
.devhub/outbox/
```

## When Working On Bugs

Before investigation:

1. Extract project, area/module, symptom, error keywords, and relevant file paths.
2. Run `devhub.py search` with a concise query.
3. Read relevant Pitfalls, Bugfixes, Playbooks, Decisions, and Areas from the output.
4. Let old records influence the fix, but only mention them in the final summary when they materially changed the work.

After a meaningful fix:

1. Write a Bugfix record.
2. Write an AI Run record.
3. Create or update a Pitfall or Playbook when the lesson is reusable.
4. Keep long narratives in Docs only when they are worth reading later.

See [`references/writeback-flows.md`](references/writeback-flows.md).

## Before Main Pushes

Before pushing `main` or `master`, write a Release record or leave an outbox item. The hook chain accepts one of:

- `# kb-updated`
- a receipt under `.devhub/receipts/`
- an outbox item under `.devhub/outbox/`
- `# kb-skip: reason` for a justified skip

The default mode is Shadow Mode: warn first, then tighten to enforced mode after the workflow is trusted.

See [`references/hook-policy.md`](references/hook-policy.md).

## Domain Routing

Use the split domain skills when the work needs deeper Feishu CLI behavior:

- `lark-cli-devhub-base` for Base schema, records, views, dashboards, and structured AI search.
- `lark-cli-devhub-docs-wiki` for Docs, Wiki spaces, long-form pages, and node organization.
- `lark-cli-devhub-taskflow` for task lists, bug/feature tasks, owners, and status discipline.
- `lark-cli-devhub-whiteboard` for architecture maps, workflow maps, dependency graphs, and visual summaries.
- `lark-cli-devhub-drive` for Drive files, imports, exports, folder sync, comments, permissions, and artifact registration.
- `lark-cli-devhub-sheets` for spreadsheet reports, QA matrices, release checklists, and human-editable trackers.
- `lark-cli-devhub-calendar` for agenda, freebusy, scheduling, rooms, review blocks, and release windows.
- `lark-cli-devhub-communications` for IM and Mail search, summaries, drafts, replies, announcements, and sharing artifacts.
- `lark-cli-devhub-meetings` for VC, Minutes, meeting notes, recordings, action items, and decision extraction.
- `lark-cli-devhub-approvals-okr` for formal approvals, OKR progress, release governance, and goal alignment.
- `lark-cli-devhub-slides` for project briefings, release review decks, retrospectives, and stakeholder updates.
- `lark-cli-devhub-events` for event consumers, watchers, automation triggers, and writeback loops.

See [`references/domain-map.md`](references/domain-map.md) and [`references/knowledge-model.md`](references/knowledge-model.md).
