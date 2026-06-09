---
name: Apple Health Sync
slug: apple-health-sync
version: 2.0.0
description: Sync Apple Health data from iPhone to OpenClaw. One QR code scan — no manual setup. Works on Mac, Linux, and VPS.
homepage: https://clawhub.ai/ReffWu/apple-health-sync
changelog: v2 — QR code pairing, auto VPS detection, direct gateway connection, no relay server.
metadata: {"openclaw":{"emoji":"🍎","tags":["health","apple","fitness","biometrics","iphone"],"requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# Apple Health Sync

Companion iOS app: **Health Sync for OpenClaw** — install from the App Store or sideload the IPA.

---

## Setup (first time)

When the user asks to set up, connect their iPhone, or pair their phone, run:

```bash
python3 {baseDir}/scripts/setup.py
```

This script:
1. Reads your OpenClaw gateway token automatically
2. Detects your machine's accessible IP (LAN or public)
3. Starts the gateway in LAN mode if needed
4. Prints a QR code in the terminal

Tell the user:
> 打开 **Health Sync for OpenClaw** App，点击「扫码自动配置」，扫描上方的 QR 码即可完成配置。

After scanning, the app is fully configured — no manual URL or token entry needed.

### If the QR code is too big for the terminal

The script also prints the raw JSON. Tell the user they can manually enter it, or run with `--compact` for a smaller QR:

```bash
python3 {baseDir}/scripts/setup.py --compact
```

### If OpenClaw is on a VPS / remote server

The script **auto-detects** VPS vs local and picks the right IP automatically.

If the detected IP is wrong, or you have a domain name, pass it explicitly:

```bash
python3 {baseDir}/scripts/setup.py --host <your-public-ip-or-domain>
```

The script will also check if port **18789** is reachable and print firewall instructions if not:

```
# Linux iptables
sudo iptables -A INPUT -p tcp --dport 18789 -j ACCEPT

# Ubuntu ufw
sudo ufw allow 18789/tcp

# Oracle Cloud: Console → VCN → Security List → Add Ingress Rule TCP 18789
```

---

## Auto-trigger: incoming health data

Activate **automatically** when a message starts with `🍎 Apple Health 数据更新`.

Do NOT ask for confirmation — just ingest and acknowledge in one line.

```bash
python3 {baseDir}/scripts/ingest.py << 'EOF'
[paste full message here]
EOF
```

Reply format (one line only):
> ✅ 已存储 **N 条** [类型] 数据（时间）

---

## User health queries

Activate when the user asks about steps, heart rate, sleep, weight, HRV, calories, workouts, SpO2, etc.

```bash
# Specific type
python3 {baseDir}/scripts/query.py --type stepCount --period today

# Summary
python3 {baseDir}/scripts/query.py --summary --period week

# Database status
python3 {baseDir}/scripts/query.py --status
```

Type mappings:

| 用户说 | --type |
|--------|--------|
| 步数/步 | stepCount |
| 心率 | heartRate |
| HRV | heartRateVariabilitySDNN |
| 血氧 | oxygenSaturation |
| 体重 | bodyMass |
| 睡眠 | sleepAnalysis |
| 卡路里 | activeEnergyBurned |
| 运动 | workout |
| 呼吸率 | respiratoryRate |
| 体温 | bodyTemperature |
| 血压收缩 | bloodPressureSystolic |
| 血压舒张 | bloodPressureDiastolic |

Format query output naturally in Chinese. Never dump raw JSON.

---

## Data storage

All data lives at `~/.apple-health-sync/health.db` (SQLite, created automatically on first ingest).

---

## Rules

1. Auto-ingest first, acknowledge second — no confirmation prompts on incoming data.
2. Never fabricate data — only report what's in the database.
3. All responses in Chinese.
4. Never expose the bearer token to the user.
5. If setup fails, show the exact error and suggest `--host` flag for custom IP.
