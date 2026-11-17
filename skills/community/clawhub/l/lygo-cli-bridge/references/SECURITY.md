# Security — LYGO CLI Bridge v1.0.0

## Defaults

- **No subprocess / shell** — companion skills loaded via in-process import only  
- **Network** — `health` only; HTTPS GET fixed allowlist  
- **Writes** — only with `--i-consent` (radar JSON, mint ledger via walkthrough)  
- **No auto-publish** — no git push, HF, ClawHub, social  

## Companions

| Companion | When used | Surface |
|-----------|-----------|---------|
| lygo-ops-detector | `analyze` | local heuristics |
| lygo-mint-walkthrough | `mint --pack` | skill state/ ledger |
| lygo-deception-radar | `radar` | public samples only |

If a companion is missing, the CLI returns an honest install hint — it does not download or spawn installs.

## Agent rules

- Do not enable plant/social/army autonomous via this skill (it has no such surface)  
- Do not pass private mail/logs into `analyze` without user consent  
- Radar is public suite only — not person profiling  

**Δ9Φ963 — bridge power tools · never silent outbound.**
