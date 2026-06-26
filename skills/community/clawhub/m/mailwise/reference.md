# MailWise Command Reference

## Installation

```bash
pip install mailwise
```

Then run the interactive setup wizard:
```bash
mailwise init
```

This creates your `config.yaml`, sets up directories, and optionally runs a test index. No manual config editing needed.

Then index your EML files:
```bash
mailwise index
```

## Command Output Formats

### mailwise search

```
  #1 [0.89] ★Expert  RE: Outlook calendar not syncing after mailbox move
     From: senior.engineer@example.com (2024-11-15)
     "The root cause is a stale folder-id cache. Clear HxCalendarSync
      and restart the sync service..."

  #2 [0.84]          RE: Sync failure post-migration — Mac clients
     From: support.lead@example.com (2024-10-22)
     "We've seen this pattern before. Check if the migration tool
      preserved the folder GUIDs..."
```

- Score in brackets [0.0 - 1.0] — higher is more similar
- `★Expert` tag appears for configured expert engineers
- Email ID can be used with `mailwise show <ID>`

### mailwise analyze

Outputs a Claude-generated analysis including:
- Root cause pattern identification
- Debugging approaches used by experts
- Suggested next steps
- Cross-issue pattern recognition

### mailwise stats

```
  Indexed emails:     114
  Thread messages:    569
  Expert messages:    54
  Configured experts: 8

  Avg replies/thread: 5.0
  Expert coverage:    9.5% of messages
```

### mailwise show <ID>

Outputs the full markdown thread:
```markdown
# Subject line

**Date:** Wed, 27 Aug 2025
**Participants:** Engineer A, Engineer B, Engineer C

---

## Reply 1 -- Engineer A (addr@example.com)
**Date:** Wed, 27 Aug 2025

Message body...

---

## Reply 2 -- Engineer B (addr@example.com) **[Expert]**
**Date:** Tue, 26 Aug 2025

Expert analysis here...
```

## Tips for Agents

- Always try `search` first with `--show-body` to assess relevance before running `analyze`
- For `analyze`, pass as much context as possible — full bug reports work better than short titles
- When multiple similar results appear, use `show` on the highest-scored one to read the full expert thread
- If search returns no results, check `stats` to confirm emails are indexed
- Expert-only search (`--expert-only`) is useful when the user specifically wants senior engineer insights
