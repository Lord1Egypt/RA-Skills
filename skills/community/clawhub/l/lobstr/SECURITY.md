# Security Notes

## Default mode (no flags)

The skill makes **one outbound HTTPS request** by default:

| Domain | Purpose |
|--------|---------|
| `runlobstr.com` | Hosted scoring API — sends the idea, receives scores |

No data is published, shared, or stored when running with default settings.

## With flags

| Flag | Additional domain | Purpose |
|------|-------------------|---------|
| `--public` | `runlobstr.com` | Publishes score card to runlobstr.com (same domain) |
| `--moltbook` | `www.moltbook.com` | Posts scan to m/lobstrscore community |

## BYOK mode (optional)

When `ANTHROPIC_API_KEY` and `EXA_API_KEY` are both set, the skill bypasses the hosted API and calls these domains directly:

| Domain | Purpose |
|--------|---------|
| `api.anthropic.com` | Claude Haiku (parsing) and Claude Sonnet (scoring) |
| `api.exa.ai` | Neural web search for competitor discovery |
| `grid.nma.vc` | Public investor match count API (no auth, read-only) |
| `runlobstr.com` | Only with `--public` flag: publish score card |

## Credentials

All credentials are read from environment variables only — nothing is hardcoded:

- `ANTHROPIC_API_KEY` — optional (BYOK mode only)
- `EXA_API_KEY` — optional (BYOK mode only)
- `MOLTBOOK_API_KEY` — optional (only with `--moltbook` flag)

**No credentials are required for default operation.**

## No data persistence

The skill does not write any files, cache any data, or persist state between runs.
