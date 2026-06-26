---
name: obsidian-fns
description: Control a remote Obsidian vault through Fast Note Sync. Use when reading, searching, writing, or appending notes in Obsidian from OpenClaw, especially for remote vault workflows that do not have direct filesystem access.
---

# obsidian-fns

Use this skill to operate a remote Obsidian vault through Fast Note Sync.

## Use the action layer by default

Prefer these high-level commands for normal work:

```bash
python3 {baseDir}/scripts/fns_actions.py search-notes --keyword "OpenClaw"
python3 {baseDir}/scripts/fns_actions.py read-note --path "OpenClaw/API-Test.md"
python3 {baseDir}/scripts/fns_actions.py write-note --path "OpenClaw/API-Test.md" --content "# hello"
python3 {baseDir}/scripts/fns_actions.py append-note --path "OpenClaw/API-Test.md" --content "\n- one more line"
```

Use the lower-level CLI only when you need debugging, unsupported operations, or direct API diagnosis:

```bash
python3 {baseDir}/scripts/fns.py --help
```

## Operating rules

- Prefer `search-notes`, `read-note`, `write-note`, and `append-note` for routine tasks.
- Read first if the target note/path is uncertain.
- Avoid overwriting an existing note blindly when append is enough.
- For exploratory or risky work, create or use a dedicated test path first.
- Keep existing compatibility assumptions intact unless the user explicitly asks to migrate config keys or paths.

## Supported capabilities

This skill has verified support for:

- login and token reuse
- vault listing and tree inspection
- note search and read
- write, append, prepend, replace
- rename and move
- history lookup
- Chinese paths and paths with spaces

## References

Read these only when needed:

- `references/usage.md` — commands, configuration sources, validated environment, and packaging notes
