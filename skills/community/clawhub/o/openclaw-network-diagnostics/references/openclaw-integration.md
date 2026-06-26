# OpenClaw Integration Options

## Option A: External background process (recommended)

Run the diagnostic worker as an independent process via `start/stop/status` commands.

### Pros
- Never blocks the main OpenClaw thread.
- Survives OpenClaw task restarts.
- Can be restarted independently.
- Clear process isolation for debugging.

### Cons
- Requires pid-file lifecycle management.
- Requires explicit start/stop orchestration in OpenClaw scripts.

## Option B: In-process async task (advanced)

Import `NetworkDiagnosticWorker` and create an asyncio task inside OpenClaw runtime.

### Pros
- Single process deployment.
- Direct access to in-memory OpenClaw status data.

### Cons
- Any blocking bug can impact OpenClaw runtime.
- Harder fault isolation.
- Runtime restarts stop diagnostics.

## Recommended default

Use Option A for production observability. Use Option B only when deep in-process coordination is required.

## Example OpenClaw shell hooks

```bash
# start
python3 /path/to/openclaw-network-diagnostics/scripts/netdiag.py start \
  --config /path/to/openclaw-network-diagnostics/references/config.example.json \
  --pid-file /path/to/openclaw-network-diagnostics/logs/netdiag.pid

# stop
python3 /path/to/openclaw-network-diagnostics/scripts/netdiag.py stop \
  --pid-file /path/to/openclaw-network-diagnostics/logs/netdiag.pid
```
