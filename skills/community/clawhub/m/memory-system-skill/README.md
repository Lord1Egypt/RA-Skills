# Memory System Protocol

A practical, battle-tested memory protocol for **long-running AI agents** that need to survive session resets without losing continuity.

Hardened by real incidents: encoding corruption, backup drift, and multi-agent desync. Every rule in this protocol exists because something broke in production.

## Why

Long-lived agents (chat assistants, background daemons, multi-agent setups) lose continuity every time a session ends. The usual fixes — "just keep a big context file" — rot: files grow stale, encodings get corrupted, backups drift out of sync, and nobody notices until data is gone.

This protocol is a small, concrete operating manual:

- **Dual per-day logs** — a summary + a verbatim transcript, so both "what happened" and "exactly what was said" survive.
- **Encoding safety rules** — corruption is silent and permanent; these rules prevent it.
- **Backup + checksum verification** — "copied" is not "identical"; every sync is verified.
- **Multi-agent shared facts** — one authoritative file, checksum-verified mirrors.
- **Startup checklist** — every session resumes with context instead of a blank slate.

## Directory layout

```
memory/
├── logs/YYYY-MM-DD/            # one directory per day
│   ├── YYYY-MM-DD.md           # summary (events, "## time — topic" sections)
│   └── YYYY-MM-DD-verbatim.txt # verbatim transcript (MUST be exact)
├── knowledge-base.txt          # optional: topic index + event digests
├── scripts/                    # helper scripts
└── body/                       # optional: agent state / sensory layer
```

## Quick start

1. Create the directory layout above.
2. Log daily: a summary `.md` + a verbatim `-verbatim.txt` (exact transcript, no summarizing).
3. Append each conversation turn after every reply; backfill if the log lags the conversation.
4. Mirror logs to an external backup after every write, then verify with checksums.
5. Read today's log at session startup before doing anything else.

Full protocol: see [`SKILL.md`](SKILL.md) (also installable as an agent skill).

## Highlights

- **Verbatim logs are sacred.** Summaries can be wrong; verbatim transcripts are the personal-history record. Never summarize, omit, or rewrite them.
- **Append, don't rewrite.** Reading a mixed-encoding file and writing it back "loosely" permanently destroys data (U+FFFD replacement). Always append with explicit UTF-8.
- **BOM matters on Windows.** A UTF-8 file without BOM is read as ANSI (GBK on zh-CN) by Windows PowerShell 5.1 — garbled strings, broken paths, mojibake filenames.
- **Verify every sync.** MD5 after every copy. A stale mirror looks identical until you checksum it.

## License

MIT
