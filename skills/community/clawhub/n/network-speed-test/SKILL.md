---
name: network-speed-test
description: Measure network download speed, upload speed, and latency from the command line. Uses Cloudflare speed test endpoints and public DNS for latency measurements. No external dependencies — pure Python with stdlib only. Use when checking internet speed, diagnosing slow connections, measuring latency/jitter, or benchmarking network performance.
---

# Network Speed Test

Measure download, upload, and latency with zero dependencies.

## Commands

All commands use `scripts/speed_test.py`.

### Run All Tests

```bash
python3 scripts/speed_test.py --all
python3 scripts/speed_test.py --all --json
```

### Individual Tests

```bash
python3 scripts/speed_test.py --download
python3 scripts/speed_test.py --upload
python3 scripts/speed_test.py --latency
```

### Custom Test Size

```bash
python3 scripts/speed_test.py --download --size 25   # 25 MB download test
python3 scripts/speed_test.py --all --size 50         # 50 MB download, 25 MB upload
```

### JSON Output

```bash
python3 scripts/speed_test.py --all --json
```

Returns structured JSON with timestamp, latency stats (avg/min/max/jitter per host), download speed (Mbps), and upload speed (Mbps).

## Latency Targets

Tests TCP connection latency to Cloudflare DNS (1.1.1.1), Google DNS (8.8.8.8), and Quad9 (9.9.9.9). Reports average, min, max, and jitter for each.

## Notes

- Download uses Cloudflare speed test endpoint
- Upload uses Cloudflare speed test endpoint
- Default test size: 10 MB download, 5 MB upload
- No API keys or accounts required
