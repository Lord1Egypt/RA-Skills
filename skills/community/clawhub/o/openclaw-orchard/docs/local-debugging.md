# Orchard local debugging

Use local environment variables for debugging Orchard without changing published ClawHub defaults.

## Recommended local-safe profile

```bash
export ORCHARD_DEBUG=1
export ORCHARD_DEBUG_VERBOSE=1
export ORCHARD_DEBUG_LOG_ONLY=1
export ORCHARD_PRESERVE_SESSIONS=1
export ORCHARD_DISABLE_ARCHITECT_SPAWNS=1
export ORCHARD_CIRCUIT_BREAKER_ENABLED=1
export ORCHARD_CIRCUIT_BREAKER_FAILURE_THRESHOLD=3
export ORCHARD_CIRCUIT_BREAKER_COOLDOWN_MS=300000
export ORCHARD_QUEUE_INTERVAL_MS=900000
openclaw gateway restart
```

## UI access

### Local UI

Open the standalone UI at:

- `http://127.0.0.1:18790/`
- `http://localhost:18790/`

### SSH tunnel

If Orchard is running remotely, tunnel the standalone UI port:

```bash
ssh -N -L 18790:127.0.0.1:18790 <user>@<host>
```

Example:

```bash
ssh -N -L 18790:127.0.0.1:18790 leo@10.50.0.10
```

Then open `http://localhost:18790/` locally.

## Notes
- Keep plugin manifest defaults conservative and production-safe.
- Use env overrides for local debug and ClawHub development.
- If Orchard is wedging the machine, prefer `ORCHARD_DEBUG_LOG_ONLY=1` first.
- Use `ORCHARD_DB_PATH=/tmp/orchard-dev.db` to isolate local experiments.
- The gateway port `18789` is for authenticated API access; the standalone Orchard UI is on `18790`.
