---
name: mailwise
description: Search and analyze email issue threads from a local knowledge base. Use when the user asks about past bugs, incidents, or wants to find how experienced engineers solved similar issues. Triggers on questions like "have we seen this before", "similar issues", "how did we fix", "root cause analysis", "past incidents".
homepage: https://github.com/PetrGuan/MailWise
user-invocable: true
metadata: { "openclaw": { "emoji": "📧", "requires": { "bins": ["mailwise", "claude"], "env": { "ANTHROPIC_API_KEY": { "description": "Anthropic API key (only needed for the 'analyze' command; alternative: authenticate via 'claude' CLI login)", "required": false } } }, "install": [{ "id": "pip", "kind": "uv", "package": "mailwise", "bins": ["mailwise"], "label": "Install MailWise from PyPI" }] } }
---

# MailWise — Your Team's Email Memory

**Stop re-investigating issues your team already solved.** MailWise turns your email threads into a searchable knowledge base — index thousands of EML files locally, tag expert engineers, and use RAG to instantly surface how similar issues were debugged and resolved in the past.

> **"Have we seen this before?"** → MailWise searches 25,000+ emails in under a second and shows you exactly what your best engineers said about it.

## What you get

**Semantic search** — not keyword matching, but meaning-based retrieval across your entire email archive:

```
$ mailwise search "calendar sync fails after folder migration" --show-body

  #1 [0.89] ★Expert  RE: Outlook calendar not syncing after mailbox move
     From: senior.engineer@example.com (2024-11-15)
     "The root cause is a stale folder-id cache. Clear HxCalendarSync
      and restart the sync service..."

  #2 [0.84]          RE: Sync failure post-migration — Mac clients
     From: support.lead@example.com (2024-10-22)
     "We've seen this pattern before. Check if the migration tool
      preserved the folder GUIDs..."

  #3 [0.81] ★Expert  RE: Calendar items disappearing after move
     From: senior.engineer@example.com (2024-09-08)
     "This is the same class of bug as CASE-4521. The fix is..."
```

**RAG-powered analysis** — Claude reads the most relevant past threads and synthesizes debugging guidance:

```
$ mailwise analyze "User reports calendar events vanish after moving to a new folder"

  Based on 5 similar past issues, here's what your team has found:
  ● Root cause pattern: stale folder-id cache after migration (3 of 5 cases)
  ● Recommended first step: check HxCalendarSync logs for GUID mismatch
  ● Expert consensus: clearing the sync cache resolves ~80% of these cases
  ● Edge case: if GUIDs were not preserved during migration, a full re-sync is needed
```

## Get started in 3 steps

```bash
pip install mailwise        # 1. Install from PyPI
mailwise init               # 2. Interactive setup wizard — creates config, sets directories
mailwise index              # 3. Index your EML files (incremental, safe to re-run)
```

That's it. Now search with `mailwise search "..."` or get AI analysis with `mailwise analyze "..."`.

## Commands

### Search for similar issues

```bash
mailwise search "describe the issue here" --show-body
```

- `--show-body` — show a preview of each matching message
- `--expert-only` — only show replies from expert engineers
- `-k N` — number of results (default: 10)

### Deep analysis with RAG

```bash
mailwise analyze "paste full bug report or issue description here"
```

- `-k N` — number of similar issues to feed to Claude (default: 5)

**Tip:** Paste the FULL bug report — error codes, logs, environment details produce much better matches.

```bash
mailwise analyze "$(cat bug_report.txt)" -k 10
```

### View a full email thread

```bash
mailwise show <EMAIL_ID>
```

### Check index status

```bash
mailwise stats
```

### Manage expert engineers

```bash
mailwise experts list
mailwise experts add engineer@company.com --name "Jane Doe"
mailwise experts remove engineer@company.com
```

Expert engineers' replies get `★Expert` tags and boosted scores in search results.

## Typical workflow

1. User describes an issue or pastes a bug report
2. Run `mailwise search "..." --show-body` to find similar past issues
3. If promising results found, run `mailwise analyze "..."` for deep RAG analysis
4. Use `mailwise show <ID>` to read full threads of interest
5. Summarize findings: root cause patterns, debugging steps, and next actions

## Privacy & data handling

- **Local-only commands** (`index`, `search`, `show`, `stats`, `experts`): Everything runs on your machine. Embeddings generated locally via sentence-transformers. No data sent anywhere.
- **External LLM command** (`analyze`): Sends email excerpts to the Anthropic API via Claude Code CLI. Do not use on sensitive emails unless your org's data policy permits it.

## Authentication

- The `analyze` command requires [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) — run `claude` once to authenticate, or set `ANTHROPIC_API_KEY`
- No auth needed for local commands (`index`, `search`, `show`, `stats`, `experts`)
