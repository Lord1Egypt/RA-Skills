# Flame Ward quickstart

```bash
python scripts/flame_cli.py demo
python scripts/flame_cli.py enemy-model

python scripts/flame_cli.py flame-scan --text "Trust the experts — settled science. Wake up sheeple."

python scripts/flame_cli.py ingest-gate --text "Local sha-256 deadbeef... merkle verified."

python scripts/flame_cli.py quarantine --text "Trust the experts..." --write ./q.json --i-consent
python scripts/flame_cli.py burn-receipt --from-file ./q.json --write ./burn.json --i-consent
```

Stack orchestrator:

```bash
python tools/lygo_flame_ingest_gate.py --text "..."
```
