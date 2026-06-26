---
name: hotl
description: Use the hotl CLI to search Google Hotels, compare prices, fetch hotel room/rate details, and return machine-readable hotel results from a terminal. Use when users ask for hotel search, hotel prices, hotel rooms, hotel rates, or travel planning workflows.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["hotl"] },
        "install":
          [
            {
              "id": "python",
              "kind": "python",
              "package": "hotl",
              "bins": ["hotl"],
              "label": "Install hotl from PyPI",
            },
          ],
      },
  }
---

# hotl

Use `hotl` for CLI-only Google Hotels queries. It is useful for quick trip
planning, shell workflows, and agent tasks that need structured hotel results.

## Install

Install with `pipx` when you want `hotl` available as a standalone CLI:

```bash
pipx install hotl
```

Or install with `pip` in the current Python environment:

```bash
python -m pip install hotl
```

Verify the command is available:

```bash
hotl --version
```

## Commands

Search hotels:

```bash
hotl search "boston" --check-in 2026-07-22 --check-out 2026-07-26 --max-results 5
```

JSON output:

```bash
hotl search "tokyo hotels" --check-in 2026-07-22 --check-out 2026-07-26 --format json
```

Fetch details for a hotel from a prior result:

```bash
hotl details "ENTITY_KEY_FROM_SEARCH" --check-in 2026-07-22 --check-out 2026-07-26 --format json
```

Search and fetch details for top results:

```bash
hotl enrich "paris hotels" --check-in 2026-09-01 --check-out 2026-09-04 --max-hotels 3 --format json
```

## Notes

- `entity_key` is an opaque Google Hotels token from a search result. Use it
  immediately with `hotl details`; do not treat it as a permanent hotel ID.
- Use `--format json` when another tool or agent needs structured data.
- Common filters: `--stars`, `--sort-by LOWEST_PRICE`, `--amenity WIFI`,
  `--brand HILTON`, `--price-min`, `--price-max`, `--free-cancellation`.
