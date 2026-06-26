# Extension Policy

Keep this skill small.

## Classify The Request

Four-region daily trends:

- Use `scripts/fetch_daily_trends.py`.
- Configure regions/platforms/limit first.
- Do not add push, schedule, database, or publishing features.

Vertical/custom-keyword hotspots:

- Use `scripts/fetch_keyword_hotspots.py`.
- Pass user-provided keywords through `--keywords`.
- Keep the keyword list user-configurable; do not hard-code product verticals unless the user asks.

Provider validity or platform quality:

- Run offline mode first to verify the runtime.
- Then run real mode and inspect explicit provider errors.
- Never replace real failures with sample data.

New platform/source:

- Add or extend a provider under `src/providers`.
- Keep the `TrendItem` contract.
- Add focused tests in `tests/test_basic_crawler.py` or a new provider test.

## Allowed Change Locations

Provider behavior:

```text
src/providers/
configs/providers.yaml
```

Basic orchestration:

```text
src/crawler.py
```

CLI entrypoints:

```text
scripts/fetch_daily_trends.py
scripts/fetch_keyword_hotspots.py
```

Tests:

```text
tests/
```

## Not Allowed In This Skill

Do not add these back into the bundled runtime:

- DingTalk webhook or Stream bot
- OSS upload/publish scripts
- ActionCard rendering
- lp-ads APIs or frontend workspace
- worker queue polling
- SQLite persistence
- LLM enrichment
- cron or scheduler management

Those belong in a larger product repository, not this basic crawler skill.

## Regression Checks

```bash
python -m pytest tests/test_basic_crawler.py -q
python -m compileall -q src scripts
python scripts/fetch_daily_trends.py --output out/daily_trends.md
python scripts/fetch_keyword_hotspots.py --keywords "乙游,短剧" --output out/keyword_hotspots.md
```
