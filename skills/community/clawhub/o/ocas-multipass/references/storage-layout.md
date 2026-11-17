# Storage Layout

```
{agent_root}/commons/data/ocas-multipass/
  config.json
  search_log.jsonl
  decisions.jsonl
  intents.jsonl
  evidence.jsonl
  sessions/
    {session_id}/
      manifest.json
      log.jsonl
      status.txt
      replay.md
      checkpoints/
      skills/
      workspace/
      output/
{agent_root}/commons/journals/ocas-multipass/
  YYYY-MM-DD/{run_id}.json
```
