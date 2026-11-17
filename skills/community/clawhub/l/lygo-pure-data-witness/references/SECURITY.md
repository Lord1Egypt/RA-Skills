# Security — lygo-pure-data-witness

**Read with:** `SKILLSPECTOR_AUDIT.md` · `PORTAL_TRAINING.md`

## Declared permissions

| Capability | Default | Gate |
|------------|---------|------|
| Network | **Off** | `--i-authorize-fetch` on **both** `pdw_cli.py` and `pure_data_witness.py` fetch/all-url |
| Multi-step `all` chain | **Off** | `--i-confirm-chain` (+ `--i-authorize-fetch` if `--url`) |
| Subprocess / shell | **None** in skill CLI | n/a |
| Filesystem read | Local `--file` / prior `--out` cards | operator-supplied paths |
| Filesystem write | Witness/egg/ledger/submission under `--out` | `--i-consent` for register |
| HF / third-party upload | **None** | `hf-pack` builds local folder only; needs `--i-consent` + `--i-authorize-hf-export` |
| Git / ClawHub / social publish | **None** | human only |

## Safety gates

- HTTPS-only fetch; SSRF / private IP / metadata host block
- Content heuristics **reject** malware bait / extreme script density (detector — not an executor)
- Snapshots size-capped; secret-pattern redaction (incomplete by nature — review before share)
- Register portal never fetches or writes the chart from the browser
- Star Chart writes are consent-gated pending submissions (not anonymous)
- Do not archive credentials, private dashboards, or illegal content

## Crypto-mining false positive

Static scanners may flag `pure_data_safety.py` because the **reject list** mentions browser-miner bait strings. Those strings are matched against **fetched page text** to **refuse archive**. The skill does not mine. See `SKILLSPECTOR_AUDIT.md`.

## Source of truth

GitHub mirror (full scripts):  
https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-pure-data-witness
