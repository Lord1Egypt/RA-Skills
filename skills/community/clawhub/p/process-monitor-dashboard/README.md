# Process Monitor Dashboard

Real‑time terminal dashboard for monitoring system processes and resource usage.

## Features

- **Live CPU, memory, disk, network metrics**
- **Process listing** – sort by CPU, memory, or disk
- **Adjustable refresh rate** (1–10 seconds)
- **JSON output** for scripting and integration
- **Lightweight** – minimal overhead

## Quick Start

1. Install dependencies:
   ```bash
   pip install psutil
   ```

2. Run the dashboard:
   ```bash
   ./scripts/main.py dashboard
   ```

3. Or take a snapshot:
   ```bash
   ./scripts/main.py snapshot --json
   ```

## Commands

- `dashboard` – Interactive real‑time dashboard
- `snapshot` – One‑time system snapshot
- `top` – Show top processes
- `monitor` – Monitor a specific process
- `stats` – System‑wide statistics
- `alert` – Check for resource alerts

## Examples

```bash
# Dashboard with 3‑second updates
./scripts/main.py dashboard --interval 3

# Top 10 CPU‑intensive processes
./scripts/main.py top --by cpu --limit 10

# JSON snapshot for monitoring scripts
./scripts/main.py snapshot --json > metrics.json

# Monitor a specific service
./scripts/main.py monitor --pid $(pgrep nginx) --interval 5
```

## Requirements

- Python 3.6+
- `psutil` library

## License

MIT