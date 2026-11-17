# Security — Agent Lattice (Layer E)

## Threat model

| Threat | Control |
|--------|---------|
| Secret exfil via presence | Secret regex + size cap; reject card |
| Spam / resource exhaustion | Rate limit 12/min/agent; card ≤12KB |
| Quarantined agent joins | Alignment gate + validate_card |
| Stale / zombie agents | TTL + prune on directory save |
| Forged authority | Local A/B remains source of truth; remote is presence only |
| Open hub on internet | Optional `LYGO_AGENT_HUB_TOKEN`; prefer TLS (mesh-deploy Phase 9) |
| Auto-publish | Scripts never git/HF/ClawHub |

## Operator hardening

1. Bind hub to `127.0.0.1` unless intentionally public.  
2. Set `LYGO_AGENT_HUB_TOKEN` for shared hubs.  
3. Use TLS reverse proxy for wide-area.  
4. Never put tokens in agent cards.  
5. On `SENTINEL_QUARANTINE` — fix local lattice first.
