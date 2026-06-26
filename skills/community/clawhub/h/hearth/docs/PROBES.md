# Probe layers — what each layer checks and why

hearth's signature is its **5-layer probe pattern**. Every device gets the same layers, in the same order, with the same output format. This consistency is what makes a multi-device sweep scannable in seconds.

## The five layers

```
L1 — Reachability:   ICMP ping (1 packet, 2s timeout by default)
L2 — Uptime + load:  uptime -p, /proc/loadavg
L3 — Memory + disk:  free -h, df -h /
L4 — Services:       systemctl is-active <unit>...
L5 — App health:     varies per device — HTTP probes, command probes, JSON parsing
```

## Layer 1 — Reachability

**What it does:** sends 1 ICMP packet with a 2-second timeout.

**What "OK" means:** the device responded. The network path between bridgehead and device is intact.

**What "UNREACHABLE" means:** no ICMP response within the timeout. Could be network drop, host powered off, ICMP blocked by firewall, or just packet loss. **L2-L5 are skipped** when L1 fails — there's no point trying SSH on an unreachable host.

**Tweaks:**
- Hosts that block ICMP but accept TCP: bump `ping_count: 3` to reduce false positives. (TCP-SYN probe support is not currently implemented; contributions welcome.)

## Layer 2 — Uptime + load

**What it does:** runs `uptime -p` and reads `/proc/loadavg` on the device.

**Output format:**
```
L2 uptime:  3 days, 4 hours, load: 0.12 0.08 0.05
```

The three load numbers are 1-minute, 5-minute, 15-minute load averages. On a system with N CPU cores, sustained load above N indicates overload.

**Useful for catching:**
- Reboots (uptime resets to seconds/minutes)
- Sustained high load (1m and 5m both elevated)
- Load spikes (1m elevated but 5m normal)

## Layer 3 — Memory + disk

**What it does:** runs `free -h | grep Mem` and `df -h /`.

**Output format:**
```
L3 mem:     used 1.2Gi / 4.0Gi, 2.5Gi avail | disk: / 23% used, 75G free
```

The "avail" number is the third column of `free -h` — it accounts for buff/cache that can be reclaimed under memory pressure. This is the number that matters, not "free".

**Useful for catching:**
- Memory leaks (avail trending down across sweeps)
- Disk filling up (% used trending up)
- Just-in-time disaster recovery (disk full → systemd-journald fills → service crashes)

**Tweaks:**
- hearth probes only `/`. If you have separate `/var`, `/home`, `/data` partitions you care about, add command probes:
  ```yaml
  - name: data-disk
    type: command
    command: 'df -h /data | awk "NR==2 {print $5}"'
    expect_no_match: '^9[0-9]%|^100%'
  ```

## Layer 4 — Services

**What it does:** runs `systemctl is-active <unit>` for each unit in the device's `services:` list.

**Output format:**
```
L4 svc:     ssh=active nginx=active fail2ban=active
```

Possible per-service states:
- `active` — running normally
- `inactive` — not running
- `failed` — crashed (use `journalctl -u <unit>` to investigate)
- `activating` — still starting up
- `unknown` — unit doesn't exist (typo in your `services:` list)

**Special cases:**
- `no-systemd (chroot — N/A)` — device has `no_systemd: true`. Common for Kali NetHunter chroots, Termux, Alpine without OpenRC integration.
- `unmanaged-host (no SSH/WMI access)` — device has `auth: http-only`. L4 cannot be probed.

**Tweaks:**
- **`expected_failed_units`** lets you whitelist systemd units that are expected to be in a failed state — common for `lightdm` on a headless server, or `plymouth-quit` on a desktop install repurposed for server use. These will still appear in L4 output but not flagged.
- **Many units to check**: there's no hard limit, but each unit adds a small amount to the SSH round-trip. 10-15 units per device is the sweet spot.

## Layer 5 — App health

**What it does:** runs one or more app-specific probes.

**Why this matters:** L4 tells you a daemon is running. L5 tells you the daemon is doing what you want. The daemon could be running but returning HTTP 500. The database could be running but accepting no connections. The cache could be running but full of stale data.

**Probe types:**

### `http`
HTTPS or HTTP request, optionally with bearer auth, expected status code, and content match. Output:
```
L5 app:     web=HTTP 200 | api=HTTP 200 | health=HTTP 200
```

### `command`
User-defined read-only command on the device, with regex match against output. The command is taken verbatim from the user's own `devices.yaml` — hearth does not generate or fetch commands from any other source.
```
L5 app:     opensearch-cluster=OK (green) | indexers=OK (14) | tailscale=OK (100.64.0.10)
```

**Examples by app type:**

| App | Probe pattern |
|-----|---------------|
| Web app | HTTP 200 on `/`, optionally JSON-match a status field |
| API | HTTP 200 on `/health` or `/status`, parse JSON for "ok" |
| Database | command probe `mysqladmin ping`, expect `mysqld is alive` |
| Cache (Redis) | command probe `redis-cli ping`, expect `PONG` |
| Search (OpenSearch / ES) | curl `/_cluster/health`, expect `green` or `yellow` |
| Tailscale | command probe `tailscale ip -4`, expect a `100.x.x.x` |
| Magento indexers | command probe counts "Ready" lines from `bin/magento indexer:status` |

## Why these five and not six?

The five layers were chosen because each catches a *distinct, common* failure class:

| Failure class | Caught at |
|---------------|-----------|
| Host off / network broken | L1 |
| Reboot loop / runaway load | L2 |
| Disk full / OOM | L3 |
| Service crashed | L4 |
| Service running but app broken | L5 |

A sixth layer would risk overlap and noise. If you find yourself wanting one, it's usually better expressed as another L5 probe.

## Honest reporting

If a layer cannot be probed for a device, hearth says so explicitly:

- L4 on chroot/Termux: `no-systemd (chroot — N/A)`
- L2/L3/L4 on Windows: `unmanaged-host (no SSH)`
- SSH timed out: `SSH FAILED`
- Probe command returned nothing: `<name>=` (empty result)

Faking a green result on a layer that wasn't actually probed is dishonest — you wouldn't know the layer was lying when something silently broke. hearth chooses honesty.