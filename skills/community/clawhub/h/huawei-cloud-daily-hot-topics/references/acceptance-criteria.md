# Acceptance Criteria — huawei-cloud-daily-hot-topics

## In scope

- Full skill directory: `SKILL.md`, `scripts/`, `references/`, `templates/`,
  `tests/`.
- `scripts/fetch_hot_topics.py` performs a single query and prints today's hot
  topics ranked by `rank / title / hot value / source`.
- Output formats: Markdown (default), plain text, and JSON.
- `--top N` constrains the number of entries shown.
- `--source <name>` selects a preferred provider; multiple providers are tried
  in order and the chain degrades on failure.
- When the network or every provider is unavailable, the skill falls back to the
  bundled sample dataset, labels it **示例数据**, and still exits `0`.
- `--output` writes the result to a file.
- Offline unit tests (HTTP mocked) under `tests/`.

## Acceptance checklist

- [ ] Directory structure is complete and passes the Huawei Cloud Skill
      structure validation.
- [ ] `python3 scripts/fetch_hot_topics.py` runs once and prints a hot-topic
      ranking with exit code `0` and no traceback.
- [ ] Default output is readable Markdown; `--format json` is parseable JSON.
- [ ] `--top N` limits the number of entries correctly.
- [ ] When data sources are unavailable, the skill degrades to fallback sources
      or the bundled sample data without crashing.
- [ ] New unit tests pass (`python3 -m unittest discover -s tests -v`).

## Out of scope

- No Huawei Cloud CLI/SDK/REST integration; no cloud resources; no AK/SK.
- No persistence of fetched data, historical archiving, trend analysis, charts,
  or push/subscription.
- No guarantee of the content or availability of third-party public endpoints;
  providers are replaceable.

## Safety

Pure read-only query of public, keyless endpoints. No resource creation or
deletion, no write operations, no dangerous scenes.