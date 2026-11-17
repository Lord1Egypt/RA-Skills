# Directory Index — {{PROJECT_NAME}}

Record time: {{DATE}}
Authority: `AGENTS.md` directory rules + `governance.py index`
Changes: {{CHANGES}}

## Root layout
```
{{PROJECT_ROOT}}
├── 🔴 Core spec zone
│   ├── [AGENTS.md](AGENTS.md) — project protocol
│   ├── [ARCHITECTURE.md](ARCHITECTURE.md) — system architecture
│   ├── [PROJECT.md](PROJECT.md) — project card
│   └── [index.md](index.md) — this file (authoritative map)
├── 🟡 Core code zone
│   └── ...
├── 🟢 Agent workspace
│   ├── [LESSONS.md](LESSONS.md) — AI error & correction log
│   └── [session_handoff.md](session_handoff.md) — end-of-session handoff
├── 📂 Reference / assets (read-only)
└── 🗑️ Archived (read-only)
```

> Run `python scripts/governance.py index --project-dir .` to regenerate this
> section from the filesystem. Short descriptions come from `index_notes.json`.

## Change log
| Time | Change | Notes |
|---|---|---|
| {{DATE}} | Initial record | ... |
