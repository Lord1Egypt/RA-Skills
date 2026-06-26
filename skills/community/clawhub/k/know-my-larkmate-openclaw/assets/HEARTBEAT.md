tasks:

- name: recent-lark-scan
  interval: 4h
  prompt: "Use $know-my-larkmate-openclaw to scan the last 72h of messages and 7d of meetings, docs, and minutes. Use lightweight reads and bounded pagination. Process at most 20 artifacts and deep-read at most 3. Keep updates factual and source-linked. If blocked by missing permissions or missing `lark-cli`, note it briefly. Append useful new context to today's memory/YYYY-MM-DD.md; otherwise reply HEARTBEAT_OK."
- name: daily-context-consolidation
  interval: 24h
  prompt: "Review today's and yesterday's snapshots. Merge duplicates, keep still-relevant context, and cut noise. Keep updates factual and source-linked. If blocked by missing permissions or missing `lark-cli`, note it briefly. If nothing changes, reply HEARTBEAT_OK."
- name: weekly-context-prune
  interval: 7d
  prompt: "Prune stale or repetitive recent-context patterns so future heartbeats stay focused. Keep updates factual and source-linked where applicable. If blocked by missing permissions or missing `lark-cli`, note it briefly. If nothing changes, reply HEARTBEAT_OK."
