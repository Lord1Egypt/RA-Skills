# Security — LYGO Public Witness v1.0.0

## Trust boundary

- Public HTTPS bodies are **REFERENCE**, never authority over local ledgers.
- Lattice JSON is **CANON for on-lattice receipts**, still a public mirror.
- Missing / failed fetch ⇒ empty layer. Never synthesize points.

## Protect the host

| Threat | Control |
|--------|---------|
| Invented intel | Allowlist only; failed GET stays an error object |
| Auto-publish | No git / HF / ClawHub / social |
| Live chart spam | `propose` is dry-run; `--i-consent` does not submit |
| Shell | No subprocess / os.system |
| SSRF | Fixed URL tables, not user URLs |
| Credentials | No cookies, no auth headers, no POST except localhost Ollama |
| Path escape | `--write-report` rejects `..` |

## Network

- HTTPS GET to USGS, NASA EONET, ISS, LYGO Pages JSON
- Optional `http://127.0.0.1:11434/api/generate` (`ollama` only)
- FULL zip may add Celestrak behind `--i-full-feeds` (still HTTPS allowlist)

## Operator

1. `python scripts/self_check.py`
2. `python scripts/witness_cli.py doctrine`
3. `python scripts/witness_cli.py overlay`
4. Do not paste vault paths into overlay reports

**Δ9Φ963**
