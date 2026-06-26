# Archetype: Windows host (HTTP-only probe)

For Windows machines that you want to probe without SSH. Common cases:

- Windows desktop running services like LM Studio, Plex, Jellyfin, Obsidian REST
- Windows server you administer via RDP, not SSH
- Any Windows machine where installing OpenSSH-server is unwanted

## When to use this archetype

- The target host runs Windows (any version)
- It exposes one or more HTTP/HTTPS services on the LAN
- You don't want hearth doing SSH-based system probes

## YAML

```yaml
- name: workstation
  address: 192.0.2.80
  auth: http-only
  apps:
    - name: lm-studio
      type: http
      url: http://workstation.lan:1234/v1/models
      expect_code: 200
    - name: obsidian-rest
      type: http
      url: https://workstation.lan:27124/
      auth_header_env: HEARTH_OBSIDIAN_TOKEN
      expect_code: 200
      verify_tls: false   # self-signed cert
```

## What the 5 layers will show

```
=== 192.0.2.80 workstation ===
  L1 ping:    OK
  L2 uptime:  unmanaged-host (no SSH)
  L3 mem:     unmanaged-host (no SSH)
  L4 svc:     unmanaged-host (no SSH/WMI access)
  L5 app:     lm-studio=HTTP 200 | obsidian-rest=HTTP 200
```

## Why honest reporting matters

L2-L4 are intentionally reported as `unmanaged-host (no SSH)` rather than skipped or hidden. This makes it visible at a glance that this device's only health signal is L5. If L5 reports green for both apps, you know the things you actually use are working. If they're not, you know the failure mode is at the app level, not at the OS level.

## Tweaks

- **Bearer-token-protected APIs**: set the env var (`HEARTH_OBSIDIAN_TOKEN`, `HEARTH_HA_TOKEN`, etc.) and reference it via `auth_header_env`.
- **Self-signed certs**: `verify_tls: false`. Common for local services like Obsidian REST.
- **Uses a hostname not in DNS**: use `resolve: name:port:ip` to bypass DNS:
  ```yaml
  url: https://my-app.local/
  resolve: my-app.local:443:192.0.2.80
  ```
- **Multiple apps**: list as many as you like — each becomes a `name=HTTP <code>` entry on the L5 line.

## What hearth WON'T do for Windows

- No CPU/memory/disk probing — that needs WMI or WinRM, out of scope
- No service status — same reason
- No process list — same reason

If you need those, use a separate Windows-native tool (Task Manager, perfmon, Resource Monitor) or set up SSH on the Windows host and use the `linux-systemd` archetype with adjustments.