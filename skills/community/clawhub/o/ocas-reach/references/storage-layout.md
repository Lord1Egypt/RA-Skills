# Storage Layout

```
{agent_root}/commons/data/ocas-reach/
  config.json        — optional skill configuration (currently empty)
  usage.jsonl        — append-only call log; quota counts derive from this
  accounts.json      — account ledger (one entry per registered source)
  intents.jsonl      — append-only log of query intents (source, action, params, timestamp)
  evidence.jsonl     — append-only evidence log for recovery contract (all runs including no-ops)
{agent_root}/commons/journals/ocas-reach/
  YYYY-MM-DD/{run_id}.json   — Observation Journal per query (Action Journal for registrations)
```

No data is stored inside the skill package. The package is read-only at runtime.
