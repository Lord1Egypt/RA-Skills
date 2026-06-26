---
name: net-detective
description: Run structured network diagnostics and produce a plain-English diagnosis explaining what's wrong and why. Goes beyond simple ping: tests DNS resolution across multiple providers, runs traceroute, detects MTU fragmentation, measures speed, and compares results against historical baselines. Use when the user reports "network slow", "internet problems", "diagnose network", "why is my internet slow", "DNS issues", "packet loss", "network diagnostic", connection issues, or wants to understand what's wrong with their network.
---

# Net Detective

Run structured network diagnostics and explain findings in plain English.

## Scripts

- `scripts/diagnose.py` — orchestrates all tests, outputs unified JSON
- `scripts/dns_check.py` — tests DNS resolution across Google, Cloudflare, and system resolvers
- `scripts/speedtest.py` — measures download throughput via curl (no external packages)
- `scripts/history.py` — records results over time, detects anomalies vs baseline
- `scripts/report.py` — converts diagnostic JSON into a plain-English markdown report

All scripts use Python stdlib only. Cross-platform: macOS and Linux.

Reference `references/diagnostic-guide.md` for what each test measures and common failure patterns.

## Standard Workflow

### 1. Run the full diagnostic

```bash
python3 scripts/diagnose.py > /tmp/net-diag.json
```

Add `--speed` to include a bandwidth test (adds ~20s):
```bash
python3 scripts/diagnose.py --speed > /tmp/net-diag.json
```

Skip traceroute or MTU if time-constrained:
```bash
python3 scripts/diagnose.py --no-traceroute --no-mtu > /tmp/net-diag.json
```

### 2. Compare against history (if available)

```bash
python3 scripts/history.py --compare /tmp/net-diag.json > /tmp/net-history.json
```

If no history exists yet, skip this step.

### 3. Generate the report

Without history:
```bash
python3 scripts/report.py /tmp/net-diag.json
```

With history comparison:
```bash
python3 scripts/report.py /tmp/net-diag.json --history-compare /tmp/net-history.json
```

### 4. Record result to history

```bash
python3 scripts/history.py --record /tmp/net-diag.json
```

Do this after every diagnostic run to build a baseline over time.

## Flags Reference

| Script | Flag | Effect |
|--------|------|--------|
| `diagnose.py` | `--speed` | Include bandwidth test |
| `diagnose.py` | `--no-traceroute` | Skip traceroute (faster) |
| `diagnose.py` | `--no-mtu` | Skip MTU detection |
| `speedtest.py` | `--quick` | Only 100kb + 1mb tests |
| `history.py` | `--record <file>` | Save result to history |
| `history.py` | `--compare <file>` | Compare vs baseline |
| `history.py` | `--show` | Print current baseline |

## Interpreting Results

- **DNS failures/slowness** — websites appear down even when servers are up; most common cause of "internet is broken" when pings still work
- **Packet loss at early hops (1–3)** — local network issue (router, cable, Wi-Fi)
- **Packet loss at hops 3–6** — ISP problem, outside your control
- **High latency, no loss** — congestion, either local or upstream
- **MTU < 1472** — fragmentation; common with VPNs or PPPoE connections
- **Speed drop but latency fine** — possible ISP throttling

Read `references/diagnostic-guide.md` for full pattern descriptions and remediation steps.

## Presenting Findings to the User

- Lead with the headline finding, not raw numbers
- Reference baseline comparisons when available ("This is 3x slower than your normal")
- Give actionable next steps, not just observations
- If the issue is outside the user's control (ISP), say so clearly
