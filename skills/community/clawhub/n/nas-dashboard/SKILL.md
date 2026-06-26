---
name: nas-dashboard
description: >-
  🏠 NAS Dashboard v3 — 环境感知的智能运维仪表盘。
  
  **适合谁**：自建 NAS / HomeLab / 家庭服务器用户，跑了 ZFS + Docker + 一堆自托管服务，需要一个"一眼看清问题、告诉你修什么"的每日健康报告。
  
  **做什么**：一键采集系统全貌（ZFS/磁盘SMART/Docker/Frigate摄像头/GPU/UPS/安全审计），环境感知评估（内网/公网分级），三级严重度（🔴紧急🟡关注🟢参考），每条告警附带评估原因+可执行修复命令。
  
  **最佳环境**：Ubuntu/Debian + ZFS + Docker，有 UPS 和 Frigate NVR 效果最佳。支持 Telegram 每日推送。
  
  **一句话**：不用天天盯着服务器，每天早上看一眼有没有🔴，有就照着修。

  Triggers: "nas status", "server status", "system dashboard", "文本仪表盘", "服务器状态", "系统健康".

# NAS Dashboard v3

Exception-driven, alert-first text dashboard for NAS/HomeLab monitoring. Prioritises problems over green lights — if everything is healthy you get a one-liner, if something is wrong you get a surgical report with **severity ratings** and **actionable fix commands**.

**Platform**: Linux (Ubuntu/Debian tested). Partial support: any Linux with ZFS. macOS/Windows: most sections unavailable (ZFS, SMART, systemd, apt, iostat, sensors are Linux-only).

## Design Principles

1. **Alerts First**: ❌/⚠️ always on top. No alerts → no ALERTS section.
2. **Normal is Invisible**: Don't list 15 healthy containers. Collapse to "X running (Y OK)".
3. **Contextual Correlation**: Disk ↔ ZFS vdev, container unhealthy + CPU process = zombie.
4. **Actionable Thresholds**: Timeshift >100 warns, SMART realloc>0 alarms, disk>45°C flags.
5. **Unified Timestamps**: All times in `YYYY-MM-DD HH:MM` or `XdXh` relative.

## Quick Start

### Configure (optional)

```bash
export ZPOOL="tank"              # default: auto-detect first pool
export DISK_LIST="sda sdb sdc"   # default: auto-detect all /dev/sd?
export FRIGATE_CAM_MAP="cam_d82e8e00:客厅,cam_ae7e3010:门口,cam_a24a20c0:车库"
export UPS_NAME="ups@localhost"  # default: ups@localhost
```

### Run

```bash
bash scripts/collect.sh
```

### Cron setup

```bash
openclaw cron add \
  --name "NAS仪表盘" \
  --schedule "0 9 * * *" \
  --agent main \
  --timeout 180 \
  --delivery "announce:telegram:YOUR_CHAT_ID" \
  --prompt "Run nas-dashboard skill: collect and format the dashboard report, then send to Telegram."
```

## Workflow

### 1. Collect data

Run `scripts/collect.sh`. Sections: SYSTEM, ZFS, VDEV_DISK (disk→pool mapping), DISKS (incl. SMART realloc/pending/udma), DISKIO, DOCKER, FRIGATE, GPU, NETWORK, PROCESSES, SERVICES, LOGS, SHARES, SECURITY, UPDATES, BOOT, UPS, TIMESHIFT.

### 2. Format output — Alert-First Layout

#### Step 0: Scan for Alerts (always do this first)

Scan ALL collected data against these thresholds and classify severity:

| Scope | Condition | Severity |
|-------|-----------|----------|
| Pool health ≠ ONLINE | any pool | ❌ CRITICAL |
| Scrub errors > 0 | any pool | ❌ CRITICAL |
| ZFS_EVENT present | any event | ⚠️ WARNING |
| Disk health ≠ PASSED | any disk | ❌ CRITICAL |
| Disk realloc > 0 | any disk | ❌ CRITICAL |
| Disk pending > 0 | any disk | ⚠️ WARNING |
| Disk udma_crc > 100 | any disk | ⚠️ WARNING |
| Disk temp > 45°C | any disk | ⚠️ WARNING |
| Disk temp > 55°C | any disk | ❌ CRITICAL |
| Disk r_await > 20ms or w_await > 20ms | any disk | ⚠️ WARNING |
| Docker container Down/Unhealthy | any ctr | ⚠️ WARNING |
| Frigate camera skip > 1.0 | any camera | ⚠️ WARNING |
| Frigate camera fps = 0 | any camera | ❌ CRITICAL |
| Frigate storage > 80% | any storage | ⚠️ WARNING |
| Frigate storage > 95% | any storage | ❌ CRITICAL |
| Timeshift count > 100 | ts active | ⚠️ WARNING |
| Timeshift count > 300 | ts active | ❌ CRITICAL |
| CPU temp > 70°C | | ⚠️ WARNING |
| CPU temp > 85°C | | ❌ CRITICAL |
| GPU temp > 75°C | | ⚠️ WARNING |
| GPU temp > 85°C | | ❌ CRITICAL |
| ARC hit rate < 90% | | ⚠️ WARNING |
| ZFS capacity > 80% | | ⚠️ WARNING |
| ZFS capacity > 90% | | ❌ CRITICAL |
| Root disk > 85% | | ⚠️ WARNING |
| Root disk > 95% | | ❌ CRITICAL |
| Failed logins > 0 | today | ⚠️ WARNING |
| Failed systemd services | any | ⚠️ WARNING |
| UPS ≠ OL (not Online) | | ⚠️ WARNING |
| UPS battery < 50% | | ⚠️ WARNING |
| OOM events present | | ⚠️ WARNING |
| SSH pass auth on | sshd | ⚠️ WARNING |
| SSH root login on | sshd | ⚠️ WARNING |
| Firewall inactive | ufw/iptables | ⚠️ WARNING |
| Container image >6mo | Docker | ℹ️ INFO |
| APT updates available | | ℹ️ INFO |

If **0 alerts**: skip the `🚨 风险预警` section entirely.

If **alerts exist**: build `🚨 风险预警` section listing every alert, grouped by severity (❌ first, then ⚠️, then ℹ️). Format:

```
🚨 风险预警
❌ {description}
⚠️ {description}
```

#### Step 1: Build ALERTS Section (if any)

Sort by severity: ❌ CRITICAL → ⚠️ WARNING → ℹ️ INFO. One line per alert. Examples:
- `❌ sde (tank) Reallocated_Sector_Ct: 5 — 坏道增长，建议立即更换`
- `⚠️ cam_a24a20c0 skip:2.4 — 解码丢帧，检查 GPU 或降低分辨率`
- `⚠️ nextcloud (Docker) unhealthy — 容器异常`
- `⚠️ nfs-server (service) inactive — NFS 服务未运行`
- `⚠️ Timeshift: 430 snaps — 过多，建议清理 (>100)`
- `⚠️ sde udma_crc:29 — SATA 链路错误`
- `ℹ️ 0 APT updates pending`

**Correlation rules** (apply these when building alerts):
- If a Docker container is unhealthy AND a process with the same name has >1% CPU → append `(疑似僵死进程，建议重启容器)`
- If a Frigate camera has skip>1.0 AND GPU utilization is high → append `(GPU 编码瓶颈)`
- If a disk has udma>0 → mention potential SATA cable issue

#### Step 2: Build Dashboard Body

Use this compact layout. **Omit sections entirely if no data or all is healthy and not noteworthy.**

```
╭──────────────────────────────────╮
│  🏠 NAS Dashboard · {YYYY-MM-DD (周X)}  │
╰──────────────────────────────────╯
```

Then sections in order:

**🖥 SYSTEM** — one line:
```
🖥 {hostname} · {OS_short} · up {uptime_simplified} · load:{load_1min}
   CPU:{cpu_used%} ██████░░░░ · RAM:{mem_used}/{mem_total} ({mem_pct}) · / {root_used}/{root_total} ({root_pct})
   CPU:{cpu_temp°C} · Mobo:{hottest_mobo_temp}°C
```
- `uptime_simplified`: convert "1 week, 2 days, 18 hours" → "1w2d18h"
- `OS_short`: "Ubuntu 24.04" from "Ubuntu 24.04.4 LTS"
- Only show the single highest mobo temp (not all sensors)
- CPU progress bar: 10 chars, cpu_used/10 → `█` count

**🗄 ZFS** — pool summary line + ARC line:
```
🗄 {pool} [{health_emoji} {health}] · {alloc}T/{size}T ({cap}%) ██████░░░░ · frag:{frag}%
   ARC:{arc_size}GiB/{arc_max}GiB · hit:{arc_hit}% · Scrub:{scrub_summary}
```
- Scrub summary: extract "repaired 0B, 0 errors" and date from SCRUB field
- If L2ARC size > 0: append `· L2ARC:{l2_size}GiB hit:{l2_hit}%`
- ZFS capacity bar: cap/10 → `█` count
- If ARC hit < 90%: add ⚠️ prefix
- Snapshots: `Snaps:{count} latest:{yyyy-mm-dd}`

**💾 DISKS** — fixed-width column layout, one line per disk.

Use a mini-table with `│` separators so all status emoji align vertically:

```
💾 DISKS ───────────────────────────────────
sda (tank) │ W1003ABYZ-011FA0 │  931G │ 42°C │ 10909h │              ✅
sdc (tank) │ WD10PURX-78D85Y0 │  931G │ 39°C │  6804h │ r_await:10ms ✅
sde (tank) │ ST1000DM003-1ER16 │  931G │ 36°C │ 10223h │  udma:29     ✅
```

Column widths (pad/crop each field to fit):
| Col | Field | Width | Align |
|-----|-------|-------|-------|
| 1 | `{disk} ({pool_role})` | 9 | left |
| 2 | model name | 18 | left, truncate if longer |
| 3 | size | 6 | right |
| 4 | temp | 5 | right |
| 5 | hours | 7 | right |
| 6 | alerts + status | 14 | right |

- Col 6 (alerts + status): padding is dynamic but right-aligned. Contents:
  - `realloc:X` if > 0 (else pad)
  - `pending:X` if > 0 (else pad)
  - `udma:X` if > 0 (else pad)
  - `r_await:Xms` if > 5ms (else pad)
  - Always end with `✅` (PASSED) or `❌` (FAIL)
- Use VDEV_DISK data to annotate pool role: `sda (tank)`, `sdb (tank-cache)` etc.
- Model: use full model string, crop to 18 chars if longer
- ⚠️ prefix the whole line if temp>45°C or realloc>0 or pending>0 or udma>100
- Serial is omitted (model provides enough identification for this view)

**Disk I/O** — only show disks with util>5% or await>10ms:
```
   IO: sda r2.5/w4.6ms util5.2% · sdc r10.5/w3.3ms
```

**🐳 DOCKER** — converged view:
```
🐳 {total} running ({healthy_count} healthy) · v{docker_ver} · {image_count} imgs · {volume_gb}GB
```
Then only list unhealthy containers explicitly:
```
   ⚠️ nextcloud: Up 2 days (no healthcheck)
   ℹ️ vaultwarden/server:latest: 4 months old (consider updating)
   ⚠️ xunlei: Up 2 days (no healthcheck) [CPU 11.2% — 疑似僵死]
```
- `healthy_count`: count of containers with "(healthy)" in status
- List containers WITHOUT "(healthy)" suffix under ⚠️
- If a container appears in TOP_CPU with same name → add `[CPU X% — 疑似僵死]`
- **Image staleness**: check IMG_AGE data; flag images older than 6 months with ℹ️
- Images: extract total size and reclaimable from DOCKER_DF
- If reclaimable > 10GB: `· {reclaimable} reclaimable ⚠️`
- If ALL containers are healthy: omit the detail lines, just show the summary

**📹 FRIGATE** — cameras, only expand problem ones:
```
📹 3 cams · detection:{det_fps}fps · infer:{infer_ms}ms
   ✅ cam_d82e8e00: 5.1fps · ✅ cam_ae7e3010: 5.1fps
   ⚠️ cam_a24a20c0: 4.9fps · skip:2.4 (丢帧 49%)
```
- Map camera IDs to friendly names via `FRIGATE_CAM_MAP` env var
- Show ALL camera names with fps (even healthy, but compact inline)
- Cameras with skip>0.5: show skip value + calculated drop percentage `(skip/fps*100)`
- Cameras with skip≤0.5: just show `✅ name: fps`
- Storage: `📀 {path}: {used}G/{total}G ({pct}%)` for each FRIGATE_STORAGE line. ⚠️ if >80%.
- If Frigate unreachable: `📹 Frigate: no response ❌`

**🎮 GPU** — one line:
```
🎮 {gpu_model} · {temp}°C · {util}% · VRAM:{used}M/{total}M · {proc_count} procs
```
- VRAM bar: 10 chars proportional
- Omit GPU entirely if nvidia-smi not available or no GPU detected

**🌐 NETWORK** — one line per active interface:
```
🌐 enp4s0: {ip} · ↓{total_rx} ↑{total_tx}
```
- Skip DOWN interfaces
- Traffic: use TRAFFIC data, convert to human-readable (GB/MB)

**📊 PROCESSES** — top 3 CPU only (compact):
```
📊 CPU: xunlei 11.2% · ffmpeg 3.6% · python3 3.1%
   MEM: python3 3.6% · node 2.8% · gnome-shell 1.4%
```

**⚙️ SERVICES** — only show non-active or failed:
```
⚙️ ⚠️ nfs-server: inactive · 1 failed unit: snap.firmware-updater
```
- If all services active and no failed units: omit this section entirely

**🔒 SECURITY** — compact with full audit:
```
🔒 Failed logins: {count} · Boot: {boot_time_YYYY-MM-DD HH:MM} ({Xd} ago)
   SSH: port:{port} · root:{yes/no} · pass:{yes/no} · key:{yes/no}
   FW: {ufw/iptables status} ({n} rules) · Ports: {open_ports_list}
```
- SSH_PASS_AUTH=yes → ⚠️ alert (建议禁密码仅用密钥)
- SSH_ROOT_LOGIN=yes → ⚠️ alert (建议禁root直接登录)
- FW_UFW=inactive or FW_TYPE=none → ⚠️ alert (防火墙未启用)
- Convert OPEN_PORTS comma list to compact format: "22,80,443,8972,8973"
- Last logins: extract latest entry, reformat to "user from ip at YYYY-MM-DD HH:MM"
- If failed_logins = 0 → `Failed logins: 0`
- If fail2ban active → append `· f2b active`

**🔋 UPS** — one line:
```
🔋 {status_icon} {status_text} · charge:{batt_charge}% · load:{ups_load}% · in:{input_v}V · batt:{batt_v}V
```
- `OL` → ⚡Online, `OB` → 🪫Battery, `OB DISCHRG` → 🪫Discharging

**💾 TIMESHIFT** — one line with health check:
```
💾 Timeshift: {count} snaps · latest:{YYYY-MM-DD HH:MM}
```
- If 100 < count ≤ 300: append `⚠️ 过多，建议清理`
- If count > 300: append `❌ 严重过多 (>300)，立即清理！`

**📦 UPDATES** — only if > 0:
```
📦 {count} APT updates available
```

**🔧 OOM / Logs** — only if data present:
```
🔧 OOM: {oom_line_truncated}
```

#### Step 3: Final Assembly — Compact Mode

1. Title line (single row with date)
2. 🚨 ALERTS (if any) — combined, no section header duplication
3. `━━━━` divider (4 chars, not full-width)
4. Body sections — **merge related sections inline**:
   - 🖥 SYSTEM + 🌐 NETWORK on one block (host info → IP inline)
   - 🗄 ZFS + 💾 DISKS as one storage block
   - 🐳 DOCKER + 📹 FRIGATE as one container block
   - 🔒 SECURITY as standalone (important)
   - 📊 PROCESSES: only show if CPU>50% or unusual
   - ⚙️ SERVICES: only show failed
   - 🔋 UPS + 💾 TIMESHIFT + 📦 UPDATES as footer row
5. Keep total output under 2000 chars
6. **Omitting rules**:
   - Omit DISKIO if all util<5%
   - Omit PROCESSES if CPU<50% and no anomalies
   - Omit SERVICES if all active
   - Omit LOGS if no errors
   - Omit UPDATES if 0 pending
   - Omit GPU if nvidia-smi unavailable

### 3. Deliver

Use `message` tool with `action=send` to the target channel.

## Prerequisites

| Tool | Required for | Package |
|------|-------------|---------|
| zpool/zfs | ZFS section | zfsutils-linux |
| smartctl | Disk health | smartmontools |
| docker | Docker section | docker-ce |
| nvidia-smi | GPU section | nvidia-driver |
| iostat | Disk I/O | sysstat |
| sensors | Temperatures | lm-sensors |
| upsc | UPS section | nut-client |
| journalctl | Logs | systemd (built-in) |

SMART, auth.log, and zpool events need `sudo -n` (passwordless sudo). Sections degrade gracefully if unavailable.

## Threshold Reference

| Metric | ⚠️ Warning | ❌ Critical |
|--------|-----------|-------------|
| Disk temp | >45°C | >55°C |
| CPU temp | >70°C | >85°C |
| GPU temp | >75°C | >85°C |
| ZFS capacity | >80% | >90% |
| Root disk | >85% | >95% |
| ARC hit rate | <90% | — |
| Disk r_await/w_await | >20ms | — |
| Frigate skip | >1.0fps | >3.0fps |
| Frigate storage | >80% | >95% |
| Frigate camera fps | <1.0 | =0 |
| Timeshift snaps | >100 | >300 |
| realloc (SMART 5) | — | >0 |
| pending (SMART 197) | >0 | >10 |
| udma_crc (SMART 199) | >100 | >1000 |
| UPS battery | <50% | <20% |
| Disk I/O util | >50% | >80% |

## Notes

- All personal data (hostname, IPs, disk serials) is read at runtime, not hardcoded.
- Camera name mapping is configurable via `FRIGATE_CAM_MAP` env var: `cam_id:Name,cam_id:Name`
- Pool name auto-detected from `zpool list`. Override with `ZPOOL` env var.
- Disk list auto-detected from `lsblk`. Override with `DISK_LIST` env var.
- Suitable for publishing to ClawHub — contains no credentials, tokens, or fixed identifiers.

## Changelog

### v3.0.0 (2026-05-31)
- **Environment-aware security assessment**: distinguishes LAN vs public internet, adjusts severity
- **Three-tier severity**: 🔴 Critical / 🟡 Warning / 🟢 Info with summary count in header
- **Action guide**: each alert now includes root cause explanation + concrete fix commands
- **Compact mode**: merged redundant sections, total output under 2000 chars
- **all-in-one.sh**: collect + format in single script (5s), agent only executes + sends
- **Container image age tracking**: flags Docker images older than 6 months
- **SSH config audit**: port, password auth, root login checks
- **Firewall + open ports audit**: ufw/iptables status, listening port enumeration
- **Fallback model chain**: Deepseek-Flash → MiniMax on timeout

### v2.0.0 (2026-05-19)
- Alert-first layout with 🚨 risk warning section
- Fixed-width DISKS table with SMART realloc/pending/udma columns
- ZFS ARC/L2ARC hit rate monitoring
- Docker healthcheck + zombie process correlation
- Frigate camera skip/drop detection with GPU bottleneck correlation

### v1.0.0 (2026-05-17)
- Initial release: 16-module text dashboard
- SYSTEM, ZFS, DISKS, DOCKER, FRIGATE, GPU, NETWORK, PROCESSES, SERVICES, LOGS, SHARES, SECURITY, UPDATES, BOOT, UPS, TIMESHIFT
