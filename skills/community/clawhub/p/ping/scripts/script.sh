#!/usr/bin/env bash
# ping skill — Network Connectivity Tool
# Version: 1.0.0
# Author: BytesAgain | https://bytesagain.com

set -euo pipefail

COMMAND="${1:-help}"
DATA_DIR="$HOME/.ping"
DATA_FILE="$DATA_DIR/data.jsonl"
CONFIG_FILE="$DATA_DIR/config.json"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

# Initialize config if missing
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << 'EOF'
{"count": 4, "timeout": 5, "interval": 5, "duration": 60}
EOF
fi

# Read config defaults
_get_config() {
    python3 << 'PYEOF'
import json, os
config_file = os.path.join(os.environ.get("HOME", ""), ".ping", "config.json")
try:
    with open(config_file) as f:
        cfg = json.load(f)
    print(json.dumps(cfg))
except:
    print('{"count": 4, "timeout": 5, "interval": 5, "duration": 60}')
PYEOF
}

case "$COMMAND" in

check)
    python3 << 'PYEOF'
import subprocess, json, os, time, re, sys

target = os.environ.get("PING_TARGET", "")
if not target:
    print("Error: PING_TARGET is required", file=sys.stderr)
    sys.exit(1)

config_file = os.path.join(os.environ.get("HOME", ""), ".ping", "config.json")
try:
    with open(config_file) as f:
        cfg = json.load(f)
except:
    cfg = {}

count = int(os.environ.get("PING_COUNT", cfg.get("count", 4)))
timeout = int(os.environ.get("PING_TIMEOUT", cfg.get("timeout", 5)))

print(f"🏓 Pinging {target} with {count} packets (timeout: {timeout}s)...")

try:
    result = subprocess.run(
        ["ping", "-c", str(count), "-W", str(timeout), target],
        capture_output=True, text=True, timeout=count * timeout + 10
    )
    output = result.stdout + result.stderr
    success = result.returncode == 0

    # Parse stats
    stats = {"target": target, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "success": success, "count": count, "type": "check"}

    # Parse packet loss
    loss_match = re.search(r'(\d+)% packet loss', output)
    if loss_match:
        stats["packet_loss"] = int(loss_match.group(1))

    # Parse rtt
    rtt_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
    if not rtt_match:
        rtt_match = re.search(r'min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', output)
    if rtt_match:
        stats["rtt_min"] = float(rtt_match.group(1))
        stats["rtt_avg"] = float(rtt_match.group(2))
        stats["rtt_max"] = float(rtt_match.group(3))
        stats["rtt_mdev"] = float(rtt_match.group(4))

    # Save to JSONL
    data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
    with open(data_file, "a") as f:
        f.write(json.dumps(stats) + "\n")

    if success:
        print(f"✅ {target} is reachable")
        if "rtt_avg" in stats:
            print(f"   RTT: min={stats['rtt_min']}ms avg={stats['rtt_avg']}ms max={stats['rtt_max']}ms")
        if "packet_loss" in stats:
            print(f"   Packet loss: {stats['packet_loss']}%")
    else:
        print(f"❌ {target} is unreachable")
        if "packet_loss" in stats:
            print(f"   Packet loss: {stats['packet_loss']}%")

    print(f"\n📝 Result saved to history")

except subprocess.TimeoutExpired:
    print(f"❌ Ping to {target} timed out")
    record = {"target": target, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
              "success": False, "count": count, "type": "check", "error": "timeout"}
    data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
    with open(data_file, "a") as f:
        f.write(json.dumps(record) + "\n")
except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF
    ;;

trace)
    python3 << 'PYEOF'
import subprocess, json, os, time, sys, shutil

target = os.environ.get("PING_TARGET", "")
if not target:
    print("Error: PING_TARGET is required", file=sys.stderr)
    sys.exit(1)

print(f"🔍 Tracing route to {target}...")

# Try traceroute first, fallback to tracepath
trace_cmd = None
if shutil.which("traceroute"):
    trace_cmd = ["traceroute", "-m", "30", "-w", "3", target]
elif shutil.which("tracepath"):
    trace_cmd = ["tracepath", target]
else:
    print("Error: Neither traceroute nor tracepath found. Install traceroute.", file=sys.stderr)
    sys.exit(1)

try:
    result = subprocess.run(trace_cmd, capture_output=True, text=True, timeout=120)
    output = result.stdout
    print(output)

    record = {
        "target": target,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "type": "trace",
        "success": result.returncode == 0,
        "hops": output.count("\n") - 1,
        "output_preview": output[:500]
    }

    data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
    with open(data_file, "a") as f:
        f.write(json.dumps(record) + "\n")

    print(f"\n📝 Trace saved to history")

except subprocess.TimeoutExpired:
    print(f"❌ Traceroute to {target} timed out (>120s)")
except Exception as e:
    print(f"❌ Error: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF
    ;;

sweep)
    python3 << 'PYEOF'
import subprocess, json, os, time, sys, ipaddress, concurrent.futures

subnet = os.environ.get("PING_SUBNET", "")
if not subnet:
    print("Error: PING_SUBNET is required (e.g., 192.168.1.0/24)", file=sys.stderr)
    sys.exit(1)

try:
    network = ipaddress.ip_network(subnet, strict=False)
except ValueError as e:
    print(f"Error: Invalid subnet: {e}", file=sys.stderr)
    sys.exit(1)

hosts = list(network.hosts())
if len(hosts) > 256:
    print(f"Warning: Subnet has {len(hosts)} hosts, limiting to first 256")
    hosts = hosts[:256]

print(f"🔍 Sweeping {subnet} ({len(hosts)} hosts)...")

def ping_host(ip):
    try:
        r = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            capture_output=True, text=True, timeout=5
        )
        return (str(ip), r.returncode == 0)
    except:
        return (str(ip), False)

alive = []
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(ping_host, ip): ip for ip in hosts}
    for future in concurrent.futures.as_completed(futures):
        ip_str, is_up = future.result()
        if is_up:
            alive.append(ip_str)
            print(f"  ✅ {ip_str}")

alive.sort(key=lambda x: ipaddress.ip_address(x))
print(f"\n📊 Results: {len(alive)}/{len(hosts)} hosts alive")

record = {
    "type": "sweep",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "subnet": subnet,
    "total_hosts": len(hosts),
    "alive_count": len(alive),
    "alive_hosts": alive
}

data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(f"📝 Sweep results saved to history")
PYEOF
    ;;

monitor)
    python3 << 'PYEOF'
import subprocess, json, os, time, re, sys

target = os.environ.get("PING_TARGET", "")
if not target:
    print("Error: PING_TARGET is required", file=sys.stderr)
    sys.exit(1)

interval = int(os.environ.get("PING_INTERVAL", "5"))
duration = int(os.environ.get("PING_DURATION", "60"))

print(f"📡 Monitoring {target} every {interval}s for {duration}s...")

start_time = time.time()
results = []
data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")

while time.time() - start_time < duration:
    try:
        r = subprocess.run(
            ["ping", "-c", "1", "-W", "3", target],
            capture_output=True, text=True, timeout=10
        )
        success = r.returncode == 0
        rtt = None
        rtt_match = re.search(r'time=([\d.]+)', r.stdout)
        if rtt_match:
            rtt = float(rtt_match.group(1))

        ts = time.strftime("%H:%M:%S")
        if success and rtt is not None:
            print(f"  [{ts}] ✅ {target} — {rtt}ms")
        elif success:
            print(f"  [{ts}] ✅ {target} — OK")
        else:
            print(f"  [{ts}] ❌ {target} — unreachable")

        results.append({"time": time.time(), "success": success, "rtt": rtt})
    except:
        ts = time.strftime("%H:%M:%S")
        print(f"  [{ts}] ❌ {target} — timeout")
        results.append({"time": time.time(), "success": False, "rtt": None})

    remaining = duration - (time.time() - start_time)
    if remaining > interval:
        time.sleep(interval)
    else:
        break

# Summary
total = len(results)
ok = sum(1 for r in results if r["success"])
rtts = [r["rtt"] for r in results if r["rtt"] is not None]

print(f"\n📊 Monitor Summary:")
print(f"   Total pings: {total}")
print(f"   Success: {ok}/{total} ({ok*100//total if total else 0}%)")
if rtts:
    print(f"   RTT: min={min(rtts):.1f}ms avg={sum(rtts)/len(rtts):.1f}ms max={max(rtts):.1f}ms")

record = {
    "type": "monitor",
    "target": target,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "duration": duration,
    "interval": interval,
    "total_pings": total,
    "success_count": ok,
    "avg_rtt": round(sum(rtts)/len(rtts), 2) if rtts else None,
    "min_rtt": min(rtts) if rtts else None,
    "max_rtt": max(rtts) if rtts else None
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")

print(f"📝 Monitor session saved to history")
PYEOF
    ;;

report)
    python3 << 'PYEOF'
import json, os, sys
from collections import defaultdict

data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
target_filter = os.environ.get("PING_TARGET", "")

if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    print("📭 No ping history found. Run some checks first.")
    sys.exit(0)

records = []
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                r = json.loads(line)
                if target_filter and r.get("target") != target_filter:
                    continue
                records.append(r)
            except:
                continue

if not records:
    msg = f"for {target_filter}" if target_filter else ""
    print(f"📭 No records found {msg}")
    sys.exit(0)

# Group by target
by_target = defaultdict(list)
for r in records:
    t = r.get("target", r.get("subnet", "unknown"))
    by_target[t].append(r)

print("=" * 60)
print("📊 PING REPORT")
print("=" * 60)

for target, recs in sorted(by_target.items()):
    checks = [r for r in recs if r.get("type") == "check"]
    monitors = [r for r in recs if r.get("type") == "monitor"]
    traces = [r for r in recs if r.get("type") == "trace"]
    sweeps = [r for r in recs if r.get("type") == "sweep"]

    print(f"\n🎯 Target: {target}")
    print(f"   Total records: {len(recs)}")
    print(f"   Checks: {len(checks)} | Monitors: {len(monitors)} | Traces: {len(traces)} | Sweeps: {len(sweeps)}")

    if checks:
        success = sum(1 for c in checks if c.get("success"))
        rtts = [c["rtt_avg"] for c in checks if "rtt_avg" in c]
        print(f"   Check success rate: {success}/{len(checks)} ({success*100//len(checks)}%)")
        if rtts:
            print(f"   Avg RTT: {sum(rtts)/len(rtts):.1f}ms")

    if recs:
        timestamps = [r.get("timestamp", "") for r in recs if r.get("timestamp")]
        if timestamps:
            print(f"   First seen: {min(timestamps)}")
            print(f"   Last seen: {max(timestamps)}")

print(f"\n{'=' * 60}")
print(f"Total targets: {len(by_target)} | Total records: {len(records)}")
PYEOF
    ;;

latency)
    python3 << 'PYEOF'
import json, os, sys, math

data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
target = os.environ.get("PING_TARGET", "")

if not target:
    print("Error: PING_TARGET is required", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    print("📭 No ping history found.")
    sys.exit(0)

rtts = []
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
            if r.get("target") != target:
                continue
            if "rtt_avg" in r:
                rtts.append(r["rtt_avg"])
            if "avg_rtt" in r and r["avg_rtt"] is not None:
                rtts.append(r["avg_rtt"])
        except:
            continue

if not rtts:
    print(f"📭 No latency data found for {target}")
    sys.exit(0)

rtts.sort()
n = len(rtts)
avg = sum(rtts) / n
variance = sum((x - avg) ** 2 for x in rtts) / n
stddev = math.sqrt(variance)
jitter = sum(abs(rtts[i] - rtts[i-1]) for i in range(1, n)) / (n - 1) if n > 1 else 0

p50 = rtts[int(n * 0.50)] if n > 0 else 0
p90 = rtts[int(n * 0.90)] if n > 0 else 0
p95 = rtts[min(int(n * 0.95), n-1)] if n > 0 else 0
p99 = rtts[min(int(n * 0.99), n-1)] if n > 0 else 0

print(f"📊 Latency Analysis for {target}")
print(f"{'=' * 50}")
print(f"   Samples:  {n}")
print(f"   Min:      {min(rtts):.2f} ms")
print(f"   Max:      {max(rtts):.2f} ms")
print(f"   Average:  {avg:.2f} ms")
print(f"   Std Dev:  {stddev:.2f} ms")
print(f"   Jitter:   {jitter:.2f} ms")
print(f"   P50:      {p50:.2f} ms")
print(f"   P90:      {p90:.2f} ms")
print(f"   P95:      {p95:.2f} ms")
print(f"   P99:      {p99:.2f} ms")
PYEOF
    ;;

compare)
    python3 << 'PYEOF'
import subprocess, json, os, time, re, sys

targets_str = os.environ.get("PING_TARGETS", "")
if not targets_str:
    print("Error: PING_TARGETS is required (comma-separated)", file=sys.stderr)
    sys.exit(1)

targets = [t.strip() for t in targets_str.split(",") if t.strip()]
count = int(os.environ.get("PING_COUNT", "4"))
data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")

print(f"🔄 Comparing {len(targets)} targets with {count} pings each...\n")

results = []
for target in targets:
    try:
        r = subprocess.run(
            ["ping", "-c", str(count), "-W", "3", target],
            capture_output=True, text=True, timeout=count * 5 + 10
        )
        success = r.returncode == 0
        rtt_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', r.stdout)
        if not rtt_match:
            rtt_match = re.search(r'min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', r.stdout)

        loss_match = re.search(r'(\d+)% packet loss', r.stdout)

        entry = {"target": target, "success": success}
        if rtt_match:
            entry["min"] = float(rtt_match.group(1))
            entry["avg"] = float(rtt_match.group(2))
            entry["max"] = float(rtt_match.group(3))
        if loss_match:
            entry["loss"] = int(loss_match.group(1))
        results.append(entry)
    except:
        results.append({"target": target, "success": False, "error": "timeout"})

# Display table
print(f"{'Target':<25} {'Status':<10} {'Avg RTT':<12} {'Min RTT':<12} {'Max RTT':<12} {'Loss':<8}")
print("-" * 79)
for r in results:
    status = "✅ UP" if r["success"] else "❌ DOWN"
    avg = f"{r['avg']:.1f}ms" if "avg" in r else "N/A"
    mn = f"{r['min']:.1f}ms" if "min" in r else "N/A"
    mx = f"{r['max']:.1f}ms" if "max" in r else "N/A"
    loss = f"{r.get('loss', 'N/A')}%"
    print(f"{r['target']:<25} {status:<10} {avg:<12} {mn:<12} {mx:<12} {loss:<8}")

# Rank by avg RTT
ranked = sorted([r for r in results if "avg" in r], key=lambda x: x["avg"])
if ranked:
    print(f"\n🏆 Fastest: {ranked[0]['target']} ({ranked[0]['avg']:.1f}ms)")

# Save comparison
record = {
    "type": "compare",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "targets": targets,
    "results": results
}
with open(data_file, "a") as f:
    f.write(json.dumps(record) + "\n")
PYEOF
    ;;

history)
    python3 << 'PYEOF'
import json, os, sys

data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
target_filter = os.environ.get("PING_TARGET", "")
limit = int(os.environ.get("PING_LIMIT", "50"))

if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    print("📭 No ping history found.")
    sys.exit(0)

records = []
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
            if target_filter and r.get("target") != target_filter:
                continue
            records.append(r)
        except:
            continue

records = records[-limit:]

print(f"📋 Ping History (showing {len(records)} records)")
print("=" * 70)

for r in records:
    ts = r.get("timestamp", "unknown")
    rtype = r.get("type", "unknown")
    target = r.get("target", r.get("subnet", "N/A"))
    success = "✅" if r.get("success") else "❌"

    detail = ""
    if "rtt_avg" in r:
        detail = f"avg={r['rtt_avg']}ms"
    elif "avg_rtt" in r and r["avg_rtt"] is not None:
        detail = f"avg={r['avg_rtt']}ms"
    elif "alive_count" in r:
        detail = f"{r['alive_count']}/{r['total_hosts']} alive"

    print(f"  [{ts}] {success} {rtype:<8} {target:<25} {detail}")
PYEOF
    ;;

export)
    python3 << 'PYEOF'
import json, os, sys, csv, io

data_file = os.path.join(os.environ.get("HOME", ""), ".ping", "data.jsonl")
fmt = os.environ.get("PING_FORMAT", "json").lower()
output = os.environ.get("PING_OUTPUT", "")

if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    print("📭 No data to export.")
    sys.exit(0)

records = []
with open(data_file) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except:
                continue

if fmt == "csv":
    all_keys = set()
    for r in records:
        all_keys.update(r.keys())
    all_keys = sorted(all_keys)

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=all_keys, extrasaction='ignore')
    writer.writeheader()
    for r in records:
        row = {}
        for k in all_keys:
            v = r.get(k, "")
            if isinstance(v, (list, dict)):
                v = json.dumps(v)
            row[k] = v
        writer.writerow(row)
    content = buf.getvalue()
elif fmt == "json":
    content = json.dumps(records, indent=2)
else:
    print(f"Error: Unknown format '{fmt}'. Use 'csv' or 'json'.", file=sys.stderr)
    sys.exit(1)

if output:
    with open(output, "w") as f:
        f.write(content)
    print(f"✅ Exported {len(records)} records to {output} ({fmt})")
else:
    print(content)
PYEOF
    ;;

config)
    python3 << 'PYEOF'
import json, os, sys

config_file = os.path.join(os.environ.get("HOME", ""), ".ping", "config.json")
key = os.environ.get("PING_KEY", "")
value = os.environ.get("PING_VALUE", "")

try:
    with open(config_file) as f:
        cfg = json.load(f)
except:
    cfg = {"count": 4, "timeout": 5, "interval": 5, "duration": 60}

if not key:
    print("⚙️  Ping Configuration:")
    for k, v in sorted(cfg.items()):
        print(f"   {k}: {v}")
    sys.exit(0)

if not value:
    if key in cfg:
        print(f"{key}: {cfg[key]}")
    else:
        print(f"Key '{key}' not found. Available: {', '.join(cfg.keys())}")
    sys.exit(0)

# Try to parse value as number
try:
    value = int(value)
except ValueError:
    try:
        value = float(value)
    except ValueError:
        pass

cfg[key] = value
with open(config_file, "w") as f:
    json.dump(cfg, f, indent=2)

print(f"✅ Set {key} = {value}")
PYEOF
    ;;

help)
    cat << 'HELPEOF'
🏓 Ping — Network Connectivity Tool v1.0.0

Usage: bash scripts/script.sh <command>

Commands:
  check     Check connectivity to a target host
  trace     Trace network route to a target
  sweep     Sweep a subnet for responsive hosts
  monitor   Continuously monitor a host over time
  report    Generate summary report from history
  latency   Analyze latency statistics for a target
  compare   Compare latency between multiple hosts
  history   View stored ping history
  export    Export data to CSV or JSON
  config    View or update configuration
  help      Show this help message
  version   Show version

Environment Variables:
  PING_TARGET    Target host/IP
  PING_TARGETS   Comma-separated targets (compare)
  PING_COUNT     Number of packets (default: 4)
  PING_TIMEOUT   Timeout in seconds (default: 5)
  PING_INTERVAL  Monitor interval (default: 5)
  PING_DURATION  Monitor duration (default: 60)
  PING_SUBNET    CIDR subnet (sweep)
  PING_LIMIT     Max history records (default: 50)
  PING_FORMAT    Export format: csv|json (default: json)
  PING_OUTPUT    Export output file path

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
    ;;

version)
    echo "ping v1.0.0 — Network Connectivity Tool"
    echo "Powered by BytesAgain | bytesagain.com"
    ;;

*)
    echo "Unknown command: $COMMAND"
    echo "Run 'bash scripts/script.sh help' for usage."
    exit 1
    ;;

esac
