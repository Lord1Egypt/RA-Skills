# Initialization

On first invocation of any Taste command, run `taste.init`:

1. Create `{agent_root}/commons/data/ocas-taste/` and subdirectories
2. Write default `config.json` if absent (from `references/config.default.json`)
3. Create empty JSONL files: `signals.jsonl`, `items.jsonl`, `links.jsonl`, `decisions.jsonl`, `extractions.jsonl`, `intents.jsonl`, `evidence.jsonl`
4. Create `{agent_root}/commons/journals/ocas-taste/`
5. Register cron job `taste:update` if not already present
6. Log initialization as a DecisionRecord in `decisions.jsonl`