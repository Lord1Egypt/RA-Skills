# Initialization Procedure

On first invocation of any Forge command, run `forge.init`:

1. Create `{agent_root}/commons/data/ocas-forge/` and subdirectories
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `build_log.jsonl`, `decisions.jsonl`
4. Create `{agent_root}/commons/journals/ocas-forge/`
5. Register cron job `forge:update` if not already present
6. Log initialization as a DecisionRecord in `decisions.jsonl`

See `references/storage_conventions.md` for storage layout details and `references/journal.md` for journal format.