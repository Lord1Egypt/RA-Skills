# Spot — Recovery Behavior

When Spot encounters failures — bot blocks, VPN disconnects, platform timeouts, or data corruption — it follows these principles:

1. **Idempotency** — All recovery actions are idempotent.
2. **Graceful degradation** — If a platform is unreachable, log the failure, mark the record, and continue. Partial results are never discarded.
3. **VPN reconnection** — If `tun0` drops mid-sweep, pause, reconnect via `ocas-vpn`, and resume from the last completed entry.
4. **Data repair** — Quarantine corrupt JSONL lines to `.quarantine/` and reconstruct last valid state from journal outputs.
5. **Audit continuity** — Every recovery action is recorded in `intents.jsonl` and `evidence.jsonl`.