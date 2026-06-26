---
name: notebooklm-py-skill
description: "Manage Google NotebookLM notebooks, sources, chats, artifacts, and exports through the notebooklm-py CLI with safe workflows."
homepage: https://github.com/Suidge/notebooklm-py-skill
license: MIT
metadata:
  openclaw: {"skillKey": "notebooklm-py-skill", "emoji": "📓"}
---

# notebooklm-py-skill

Use this skill when the user asks to operate Google NotebookLM through the local `notebooklm` CLI: notebooks, sources, chat, research, notes, sharing, artifacts, or exports.

## Core Rules

1. Verify auth with `notebooklm auth check --test --json` before any workflow that depends on account access.
2. Prefer explicit notebook IDs (`-n NOTEBOOK_ID` or `--notebook NOTEBOOK_ID`) in automation; avoid shared `notebooklm use` context in parallel workflows.
3. Prefer `--json` for commands whose output will be parsed, cited, or used as evidence.
4. Ask before destructive or long-running work: notebook delete, source delete/clean, artifact delete, generation, downloads, saved notes, and waits in the main conversation.
5. Put one-off prompt/source/output files under a temporary directory and clean them up unless the user asked to keep them.
6. Never run `notebooklm doctor --fix` without explicit confirmation.

## Common Commands

```bash
notebooklm auth check --test --json
notebooklm list --json
notebooklm metadata -n NOTEBOOK_ID --json
notebooklm source list -n NOTEBOOK_ID --json
notebooklm source add "https://example.com" -n NOTEBOOK_ID --json
notebooklm source add ./file.pdf -n NOTEBOOK_ID --json
notebooklm source add - --type text --title "notes.md" -n NOTEBOOK_ID --json < /tmp/openclaw-attachments/notes.md
notebooklm ask "Question" -n NOTEBOOK_ID --json
notebooklm ask --prompt-file /tmp/openclaw-attachments/question.txt -n NOTEBOOK_ID --json
notebooklm artifact list -n NOTEBOOK_ID --json
```

## Workflows

### Query A Notebook

1. Run auth verification.
2. Locate the notebook with `list --json`, or use the provided ID/URL.
3. Ask with `ask ... -n NOTEBOOK_ID --json`.
4. If the answer is incomplete, ask focused follow-ups and synthesize.

### Add Sources Then Query

1. Create or identify the notebook.
2. Add URL/file/text sources with `source add ... --json`.
3. If the next step depends on indexing, wait for returned source IDs with `source wait SOURCE_ID -n NOTEBOOK_ID --json`.
4. Ask or generate only after required sources are ready.

## References

Load `references/notebooklm-py-cli.md` for command groups, 0.5.0 compatibility notes, artifact examples, and troubleshooting.
