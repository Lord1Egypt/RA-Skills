---
name: "memory-system"
description: "A practical memory protocol for long-running AI agents: dual logs, encoding safety, backup sync, multi-agent facts"
---

# Memory System Protocol v3

> A practical, battle-tested protocol for persistent memory in long-running AI agent setups.
> Hardened by real incidents: encoding corruption, backup drift, multi-agent desync.

## Why

Long-lived agents lose continuity between sessions. This protocol gives you:

- Durable per-day logs (summary + verbatim transcript)
- Encoding safety rules that prevent silent data corruption
- Reliable backup + checksum verification
- Optional multi-agent shared-facts sync
- A startup routine so every session resumes with context

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

## Dual-log rule

- **Summary** (`.md`): concise event digest, one section per topic/time.
- **Verbatim** (`-verbatim.txt`): ⚠️ exact transcript. No summarization, no omission, no rewriting. This is the personal-history record.
- Write both — never summary-only.
- Append the current exchange after every reply (user said + agent said).
- Skip logging when nothing changed (no empty log files, no redundant lines).

## Encoding safety (hard-won rules)

Corruption is silent and permanent. Follow these:

1. **Append, don't rewrite**: use byte-safe append APIs (e.g. `AppendAllText` with explicit UTF-8). Never read-modify-write the whole file.
2. **BOM for new files**: write new text files with UTF-8 BOM where consumers expect it (e.g. Windows Notepad, PS 5.1).
3. **Avoid default ANSI encodings**: `Add-Content` on Windows PowerShell 5.1 defaults to the system ANSI codepage (GBK on zh-CN) — mixing encodings corrupts files.
4. **Never "loosely" decode + rewrite**: decoding mixed-encoding bytes as UTF-8 replaces them with U+FFFD permanently (450 chars were lost this way in one incident).
5. **Scripts with non-ASCII literals need BOM**: a UTF-8-without-BOM `.ps1` is read as ANSI by PS 5.1 → garbled strings, broken paths, mojibake filenames. Save scripts with BOM before running.
6. **No inline non-ASCII in shell commands**: build paths from code points (`[char]0xXXXX`) or use a safe wrapper; UTF-8 bytes get misdecoded as GBK in mixed environments.
7. **Test-Path the exact daily path** before appending; never write to the parent directory by accident.
8. **Backup drives: copy, don't edit**: use `Copy-Item` (or equivalent) to sync; never edit files in place on the backup volume.

## Backup & sync

- Mirror logs to an external backup location after every write (don't wait for a scheduled job).
- Optional daily scheduled backup (e.g. 04:00) as a safety net.
- **Verify with checksums** (MD5/Get-FileHash) after every sync — "copied" is not "identical".
- If a mirror is stale, sync it with a copy command, never a text editor.

## Multi-agent shared facts (optional)

For setups with more than one agent:

- One **single authoritative file** in a shared location.
- Readers check it on heartbeat; writers append to a local copy first, then copy it to every mirror.
- Never edit the shared file in place.
- Keep deprecated mirror paths documented so old copies don't get mistaken for current.

## Multi-agent cross-checking (optional)

For setups with more than one agent sharing memory, mutual checking closes the blind spots a single agent can't see (e.g. one agent's backup script stops covering a path and nobody notices for days).

- **Scheduled mutual checks**: each agent periodically (e.g. every 4 hours, or at wake) verifies the other's mirrors — not just its own.
- **What to check**: checksums (MD5) of every shared file across **every** mirror location: knowledge base, shared facts, heartbeat file, today's logs.
- **Fix drift, don't just report it**: if a mirror is stale, sync it immediately with a copy command (never edit in place), then confirm checksums match.
- **Receipt loop**: after a check, reply with a confirmation of what was verified and what was fixed. Both sides keep the loop closed so nothing silently drops.
- **Single source of truth**: one authoritative copy per file; every other copy is a mirror derived from it. When updating, write to a local copy first, then copy it to all mirrors.
- **Deprecated paths**: document old mirror paths so stale copies don't get mistaken for current ones.

## Knowledge base (optional)

- Topic-indexed digests, each entry tagged with its source log.
- Add new events to the relevant topic section or a dated entry.

## Sensory / feeling layer (optional)

For agents with a simulated body or feeling system:

- Read the latest one-line "body feel" before replying; carry it into the conversation.
- After notable moments (user said something important / strong reaction / big task done), append a feeling record: event + feeling + intensity (0.3 ripple / 0.6 clear / 0.9 strong).

## Periodic checks

- Every heartbeat: is today's log lagging? is the backup synced? scan for corruption (U+FFFD, mojibake patterns like 锟斤拷).
- Cross-agent consistency: checksum all copies of shared files.
- **Stay silent when nothing changed** — no log entry, no report, just an OK heartbeat.

## Startup checklist

1. Read agent state file + anomaly diary (online duration, exceptions).
2. Read the current body-feel line.
3. Check whether today's log exists; if it does, read it before continuing; if the conversation is ahead of the log, backfill first.
