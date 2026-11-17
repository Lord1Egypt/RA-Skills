# Internal notes (private test skill)

Kept minimal. Owner-only. Not for marketing.

## Behaviour

- Scripts under `scripts/` perform auth refresh (WeChat QR image) and list/detail collect for the owner's configured source.
- Env: `QIANLIMA_TOKEN`, `QIANLIMA_OPENID`, optional analysis keys; load from `$QIANLIMA_WORKDIR/.env`.
- Workdir default: `~/.my-halala-sales-vp`.
- Business auth failure → client exit code `2`.

## Storage

| Path under workdir | Role |
| --- | --- |
| `data/*.sqlite3` | de-dupe / detail status |
| `output/` | list + detail artifacts |
| `runtime/` | temporary QR image |

## Regions

Built-in sample mapping includes `广西` → `6`. Other areas: pass numeric `--area-id`.

## Rate limits

Single-threaded HTTP with random delay ~2.5–5.5s; do not parallelize collect.
