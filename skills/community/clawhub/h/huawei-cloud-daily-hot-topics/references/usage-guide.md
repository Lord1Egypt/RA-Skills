# Usage Guide — huawei-cloud-daily-hot-topics

## Quick start

```bash
python3 scripts/fetch_hot_topics.py
```

Prints a Markdown ranking table of today's hot topics (top 10 by default).

## Common recipes

| Goal | Command |
|------|---------|
| Markdown table (default) | `python3 scripts/fetch_hot_topics.py` |
| Top 20 | `python3 scripts/fetch_hot_topics.py --top 20` |
| Plain text | `python3 scripts/fetch_hot_topics.py --format text` |
| Machine-readable JSON | `python3 scripts/fetch_hot_topics.py --format json --top 5` |
| Pin a provider | `python3 scripts/fetch_hot_topics.py --source zhihu` |
| Skip the network | `python3 scripts/fetch_hot_topics.py --offline` |
| List providers | `python3 scripts/fetch_hot_topics.py --list-sources` |
| Write to a file | `python3 scripts/fetch_hot_topics.py --output hot.md` |

## Output shape

Markdown (default) is a table with columns `排名 | 标题 | 热度 | 来源`. When the
fallback is used, the result is explicitly labelled **示例数据** and a warning
trail is printed at the bottom.

JSON output is a single object:

```json
{
  "source": "weibo",
  "source_label": "微博热搜",
  "is_sample": false,
  "note": "",
  "date": "2026-10-26",
  "top": 10,
  "warnings": [],
  "items": [
    {"rank": 1, "title": "...", "hot": 1081263, "source": "微博热搜", "url": "https://..."}
  ]
}
```

`items` is always constrained to `--top` entries.

## Provider chain and degradation

- The default chain is `weibo → zhihu → douyin`. The first provider that returns
  a non-empty list wins.
- `--source <name>` moves that provider to the front of the chain; the remaining
  providers stay as fallbacks.
- If every provider fails (or `--offline` is set), the skill loads
  `scripts/sample_data.json`, sets `is_sample=true`, labels the source as
  **示例数据**, and records why each provider failed in `warnings`. The command
  still exits `0`.

## Error handling

- `--top 0` (or a negative value) and an unknown `--source` print an error and
  exit `2`.
- A failure to write `--output` prints an error and exits `2`.
- A non-zero code is otherwise never returned: the bundled sample data is the
  guaranteed final fallback.

## Extending providers

Providers live in the `PROVIDERS` registry at the top of
`scripts/fetch_hot_topics.py` (`name -> {label, url}`). Add a public, keyless,
read-only endpoint there; normalisation already understands the common field
names (`title`/`name`/`word`, `hot_value`/`hot`/`index`, `link`/`url`/`href`).