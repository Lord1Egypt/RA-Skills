# Storage Layout

```
{agent_root}/commons/data/ocas-bower/
  config.json
  folder_index.json           -- full folder tree with paths, depths, permissions
  drive_digest.json           -- lightweight holistic Drive summary
  scan_progress.json          -- scan state: folders done/pending, resume point
  scans/                      -- one file per top-level folder tree
    {folder_id}.json
    _root.json                 -- files at Drive root with no parent folder
  preference_profile.json     -- inferred preferences, domains, patterns, class precision
  proposals.jsonl             -- all proposals: pending, approved, executed, failed, skipped, expired
  move_log.jsonl              -- record of every executed operation with previous_value
  undo_log.jsonl              -- record of every executed undo
  feedback_log.jsonl          -- user undo and reject events for suppression/demotion learning
  scan_events.jsonl           -- scan run history
  analysis_events.jsonl       -- analysis run history
  health_history.jsonl        -- weekly Drive health score snapshots
  decisions.jsonl             -- DecisionRecords
  intents.jsonl               -- durable intent queue (append-only)
  evidence.jsonl              -- execution evidence log (append-only)
  reports/                    -- dated apply digest Markdown files

{agent_root}/commons/journals/ocas-bower/
  YYYY-MM-DD/{run_id}.json
```
