# Bridge Health Check — LadybugDB HTTP Bridge (port 9192)

Before running the elephas pipeline (or any Chronicle-dependent skill), verify the bridge is healthy.

## Health Check

```bash
curl -s http://localhost:9192/health
```

Expected: `{"ok": true}`

## Restart Procedure

The bridge is NOT a systemd service — it's a persistent process that must be restarted manually when it fails.

### Terminal/Cron Mode (background=true)

```python
terminal(
    background=True,
    command="LBUG_C_API_LIB_PATH=/tmp/liblbug-v0171/liblbug.so.0.17.1 "
            "nohup python3 <hermes-home>/profiles/indigo/scripts/ladybug_bridge.py "
            "--db <hermes-home>/commons/db/ocas-elephas/chronicle.lbug "
            "--port 9192 "
            "> /tmp/ladybug_bridge_elephas.log 2>&1 &",
    notify_on_complete=True
)
```

Then verify:
```bash
sleep 5 && curl -s http://127.0.0.1:9192/health
```

### Foreground Mode (interactive)

```bash
pkill -f ladybug_bridge 2>/dev/null; sleep 2
LBUG_C_API_LIB_PATH=/tmp/liblbug-v0171/liblbug.so.0.17.1 \
  nohup python3 <hermes-home>/profiles/indigo/scripts/ladybug_bridge.py \
  --db <hermes-home>/commons/db/ocas-elephas/chronicle.lbug \
  --port 9192 \
  > /tmp/ladybug_bridge_elephas.log 2>&1 &
sleep 4
curl -s http://127.0.0.1:9192/health
```

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `LBUG_C_API_LIB_PATH` | `/tmp/liblbug-v0171/liblbug.so.0.17.1` | Points to LadybugDB C extension (v0.17.1+) |

## Critical Notes

- **`/tmp/liblbug-v0171/` is VOLATILE** — temp cleanup or reboots will delete it. If missing, re-download:
  ```bash
  cd /tmp && curl -sL -o liblbug-linux-x86_64.tar.gz \
    "https://github.com/LadybugDB/ladybug/releases/download/v0.17.1/liblbug-linux-x86_64.tar.gz" \
    && mkdir -p /tmp/liblbug-v0171 && cd /tmp/liblbug-v0171 && tar xzf /tmp/liblbug-linux-x86_64.tar.gz
  ```
- The bridge uses the DB path it was started with. The active DB is `<hermes-home>/commons/db/ocas-elephas/chronicle.lbug` (or `<hermes-home>/profiles/indigo/commons/db/ocas-elephas/chronicle.lbug` in profile-scoped deployments).
- The path `<commons>/db/ocas-elephas/chronicle.lbug` is a **stale/legacy copy** — do NOT point the bridge at it.
- Verify which DB path the bridge is using: `ps aux | grep ladybug_bridge | grep -v grep`

## Failure Mode

If the bridge is down when `elephas_cron_run.py` runs:
- Every `q()` call prints `BRIDGE URLError: <urlopen error ...>` and returns `[]`
- The pipeline completes with 0 entities extracted, 0 signals, 0 candidates
- Ingestion log entries are still written (with `reason: "no_entities"`)
- The run journal is written — the pipeline does NOT crash, it just produces empty results

**Action**: Restart the bridge and re-run the pipeline. The ingestion log deduplicates — re-running is safe.