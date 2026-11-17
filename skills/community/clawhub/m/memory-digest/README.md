# Memory Digest

**Weekly reports from your AI agent's memory — for the human who owns it.**

[English](./README.md) | [中文](./README_CN.md)

---

Agents that keep long-term memory produce daily logs nobody reads. Memory Digest turns that corpus into a one-page report: what happened, which projects moved, what is still pending, and which numbers changed.

Most memory tooling stores and retrieves *for the agent*. This reads the same files *for the owner*.

## What it produces

| Section | Meaning |
|---|---|
| **Activity timeline** | Per-day entry with section count, topics, and a one-line summary |
| **Projects in motion** | Project/topic names with momentum: 🆕 new, ▶️ ongoing, ⏸️ stalled |
| **Open threads** | Pending / to-confirm items with their source date |
| **Numbers in motion** | Metrics (downloads, users, stars, …) mentioned in the window |

## Quick start

```bash
git clone https://github.com/Thomaszhou22/memory-digest.git
python3 memory-digest/scripts/memory_digest.py --memory-dir /path/to/agent/workspace --days 7
```

Flags: `--days N` (window, default 7) ｜ `--out report.md` (save to file) ｜ `--json` (machine-readable).

Works with any corpus of date-named daily logs (`memory/YYYY-MM-DD.md`). The script is **read-only**.

## Real-world validation

Developed against a live agent workspace with 130+ memory files. On its first real run it correctly surfaced: a seven-day activity timeline, a stalled project untouched for six days, and every pending to-confirm item still awaiting an owner reply — including ones recorded five days earlier that would otherwise have been forgotten.

## Cron-friendly

```bash
# weekly Monday 09:00 report
0 9 * * 1 python3 /path/to/memory-digest/scripts/memory_digest.py --memory-dir ~/agent --days 7 --out ~/reports/week.md
```

## Using as an OpenClaw / Claude Code skill

Copy or symlink this folder into your skills directory. `SKILL.md` triggers on "weekly digest", "what did my agent do", "记忆周报", "述职报告". The skill procedure adds a verification step before delivering: open threads are extracted heuristically, so the agent confirms pending items are genuinely unresolved before presenting.

## Design notes

- **Read-only.** Reports never mutate memory.
- **Language-agnostic extraction.** Pending markers (待办/待确认/pending/TODO) and metric units (下载/users/星/stars) in English and Chinese.
- **Heuristics, not truth.** Momentum and open threads are candidates for review; the skill's job is to compress a week into one page, not to be infallible.

## Companion skills

- [memory-checkup](https://github.com/Thomaszhou22/memory-checkup) — consistency audit: stale numbers, dangling references, dead daily flushes
- Together: checkup finds what's wrong, digest shows what happened.

## File structure

```
├── SKILL.md                    # Skill instructions for the agent
├── scripts/
│   └── memory_digest.py        # Read-only digest generator
├── README.md
└── README_CN.md
```

## Limitations

- Section/heading conventions are assumed (Markdown `#`-`##` headings per day file)
- Project extraction is keyword-based; exotic naming may need tuning
- No vector search; it reads text, not embeddings

## License

MIT
