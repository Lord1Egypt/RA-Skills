---
name: neomano-internet-speed
description: Measure current internet connection speed (download + upload) from this machine using a lightweight HTTP-based speed test (Cloudflare speed endpoints). Use when the user asks for subida/bajada speed, bandwidth, or "speedtest".
metadata: {"clawdbot":{"emoji":"🚦","requires":{"bins":["python3"]}}}
---

## What it does

- Runs a simple download + upload throughput test against Cloudflare's speed test endpoints.
- Reports Mbps for download and upload.

## Run

```bash
python3 {baseDir}/scripts/speedtest.py
python3 {baseDir}/scripts/speedtest.py --download-bytes 50000000 --upload-bytes 10000000
```

## Notes

- Results depend on current network conditions and routing.
- This is not as feature-rich as Ookla Speedtest, but has zero external deps.
