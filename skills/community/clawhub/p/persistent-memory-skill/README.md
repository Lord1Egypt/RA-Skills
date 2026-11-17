# persistent-memory

**One reviewed local memory layer for compatible AI agents.**

Claude does not automatically know what you told Codex, and Codex does not automatically know what you saved elsewhere. Persistent Memory gives compatible agents a shared, readable source of context instead of asking you to paste it again.

It complements platform memory; it does not replace it, import your old chats, or run in the background.

## What It Does

- **Loads baseline context** — `load memory` reads your core files and index, not every project file.
- **Saves with review** — the AI proposes the content and destination; you approve before it writes.
- **Loads details on demand** — relevant project or note files are read only when the topic needs them.
- **Uses optional Summary-first loading** — for an active file with a reviewed `## Summary`, the agent reads the short summary first and opens the full file only when the request needs more detail. Files without a summary keep the existing behavior.
- **Manages lifecycle safely** — archive, trash, recovery, and memory health are confirmation-based.
- **Stays transparent** — memory is plain local Markdown you can inspect and edit.

## Quick Start

1. Install the skill for an agent that can discover Skills.
2. Start with an explicit command: `remember this` or `记住这个`.
3. Review the AI's proposed file and wording, then confirm it.
4. In a later compatible conversation, say `load memory` or `加载记忆`.

If you already have a memory folder created before lifecycle support, run `memory upgrade` / `升级记忆` before using archive, delete, recover, or memory health.

## How It Works

```text
~/.persistent-memory/
├── _core/                 # Baseline identity and collaboration context
├── _index.md              # One-line routes to active on-demand memory
├── projects/              # Active project context
├── notes/                 # Active knowledge and decisions
└── _archive/              # Excluded from normal loading
    ├── _index.md          # Archive and trash records
    └── _trash/            # 30-day recoverable deletion buffer
```

`load memory` loads **baseline context**: `_core/` and `_index.md`. When a topic matches an index entry, the agent reads only the related active file. Archived files stay out of normal loading.

## Summary-first Files

Summary-first loading is optional for active on-demand files. Put `## Summary` or `## 摘要` immediately after the title and any optional introductory metadata:

```markdown
# Project title

> Optional introductory metadata

## Summary

- Current status or scope
- Key decision or result
- Important constraint or uncertainty

## Full Details
```

Use three to six factual bullets. When the summary is enough, the agent answers from it; when it is not, the agent says the summary is insufficient and reads the full file. Existing files without a valid summary keep the normal full-file behavior. You do not need to bulk-migrate old files. When a reviewed update changes a summarized fact, the same proposed change updates the affected summary before you confirm it.

## Compatibility Contract

Cross-agent sharing works only when all of these are true:

- Each **compatible agent** can discover this skill or has an equivalent fallback instruction.
- The agents use the **same local filesystem** and resolve `~/.persistent-memory/` to the same location.
- The active user has read/write permission for that location.

Two agents do not automatically share every historical conversation. They share only memory files saved into this folder and only when the conditions above hold.

If an agent cannot discover Skills automatically, add an equivalent instruction in that agent's configuration. The minimum fallback is: when the user says `load memory`, read `~/.persistent-memory/_core/` and `~/.persistent-memory/_index.md`.

## Commands

| Say this | What happens |
|---|---|
| `load memory` | Loads baseline context: core files and the active index. |
| `remember this` / `save this` | Proposes a reviewed memory update. |
| `update memory` | Separates proposed facts and inferred patterns for approval. |
| `memory status` | Lists active memory structure and summaries. |
| `memory upgrade` | Previews and, after confirmation, creates missing lifecycle folders for an older memory root. |
| `archive <relative-path>` | Moves a completed low-frequency active file to archive after confirmation. |
| `delete <relative-path>` | Moves an already archived file to the 30-day trash after confirmation. |
| `recover <relative-path>` | Restores an archived or trashed file after confirmation. |
| `memory health` | Proposes lifecycle actions; it never executes them automatically. |

Lifecycle paths must be relative, such as `projects/old.md`. The skill rejects absolute paths, `..`, `_core/`, and control files. A path collision stops the operation before any file or index changes; it never overwrites a destination automatically.

## What Belongs in Memory

Keep stable identity, preferences, decisions, concise project state, and pointers to source material here.

Keep raw repositories, downloads, media files, and datasets in their original project workspaces. A memory note should point to them and explain why they matter; it should not become a general-purpose file warehouse.

## Privacy

All memory is stored as local Markdown files. Do not put passwords, API keys, or secrets in it. The v0.8 lifecycle and summary rules protect core files and require explicit confirmation before filesystem changes.

## Release Status

v0.8.0 adds optional Summary-first loading for active on-demand files. It does not add section-level loading, automatic summary creation, or bulk migration. See [CHANGELOG.md](CHANGELOG.md) for release details.

## License

MIT
