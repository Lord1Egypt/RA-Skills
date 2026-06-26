# Polymarket Skill

Interact with Polymarket prediction markets via the official `polymarket` CLI.

## Installation

```bash
bash skills/polymarket/scripts/install.sh
```

This will:
1. Try installing pre-built binary
2. Fall back to building from source if GLIBC incompatible
3. Install to `~/.cargo/bin/polymarket`

## Quick Start

```bash
# Search markets (no wallet needed)
polymarket -o json markets search "bitcoin" --limit 5

# Get specific market
polymarket markets get will-trump-win-2024

# Check price
polymarket -o json clob midpoint TOKEN_ID

# See SKILL.md for full documentation
# See EXAMPLES.md for common patterns
```

## Files

- `SKILL.md` — Complete reference for OpenClaw agents
- `EXAMPLES.md` — Common usage patterns and scripts
- `scripts/install.sh` — Installation script
- `scripts/search.sh` — Search markets helper
- `scripts/get-market.sh` — Get market details
- `scripts/check-price.sh` — Check token price

## Requirements

- Rust (auto-installed by install.sh if missing)
- For trading: MATIC on Polygon for gas

## References

- [polymarket-cli GitHub](https://github.com/Polymarket/polymarket-cli)
- [Polymarket Docs](https://docs.polymarket.com)
