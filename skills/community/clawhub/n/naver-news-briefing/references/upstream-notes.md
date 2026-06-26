# Upstream notes: `navernews-tabsearch`

Use these notes when extending or debugging the skill.

## Reused patterns

- `core.query_parser.py`
  - Preserve the upstream split between:
    - API query = all positive keywords joined by spaces
    - tab/db keyword = first positive keyword only
    - exclude words = `-단어` tokens
  - Preserve `build_fetch_key(search_query, exclude_words)` normalization.
- `core.config_store.py`
  - Reuse Windows-first credential handling with DPAPI-encrypted `client_secret_enc` and atomic config writes.
- `core.workers.ApiWorker`
  - Reuse request shape: `https://openapi.naver.com/v1/search/news.json`
  - Use headers `X-Naver-Client-Id`, `X-Naver-Client-Secret`
  - Use `sort=date`, clean `<b>` tags, prefer `news.naver.com` links when present, filter exclude words on title/description.
- Repo persistence style
  - Keep state on local disk inside the skill (`data/`), use atomic JSON for config and SQLite for watch state / dedupe.

## Intentional simplifications vs upstream GUI app

- No PyQt UI, tabs, bookmarks, tray, or backup rotation UI.
- No full article database; only persistent watch rules, keyword groups, and seen-link dedupe for cron-style monitoring.
- Adapt the upstream tab-search/bookmark mindset into CLI-friendly persistent keyword groups (`group-*`) plus combined briefing templates (`brief-multi`) instead of recreating GUI tabs.
- Focus on CLI/stdout output that OpenClaw can relay into chat or scheduled jobs.

## Relevant upstream files

- `README.md`
- `core/query_parser.py`
- `core/config_store.py`
- `core/workers.py`
- `core/database.py`
- `tests/test_query_parser_search_policy.py`
