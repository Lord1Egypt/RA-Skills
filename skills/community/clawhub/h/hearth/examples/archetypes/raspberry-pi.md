# Archetype: Raspberry Pi

For Pi Zero / Pi 3 / Pi 4 / Pi 5 running Raspberry Pi OS or Debian for ARM.

## When to use this archetype

- Resource-constrained device (single-core, low RAM)
- Has `vcgencmd` (Pi-specific CPU temp probe)
- Often Wi-Fi only, sometimes flaky

## YAML

```yaml
- name: pi-charger
  address: 192.0.2.40
  auth: ssh-pass
  user: pi
  password_env: HEARTH_PASS_PI
  ssh_connect_timeout: 6        # Pi Zero W single-band Wi-Fi can be slow
  services: [ssh, cron, openeo, wifi-guardian, wpa_supplicant]
  apps:
    - name: charger-api
      type: http
      url: http://pi-charger.lan/api
      expect_code: 200
    - name: cpu-temp
      type: command
      command: 'vcgencmd measure_temp 2>/dev/null | sed "s/temp=//"'
```

## What the 5 layers will show

```
=== 192.0.2.40 pi-charger ===
  L1 ping:    OK
  L2 uptime:  3 days, 9 hours, load: 0.40 0.40 0.27
  L3 mem:     used 152Mi / 427Mi, 274Mi avail | disk: / 22% used, 22G free
  L4 svc:     ssh=active cron=active openeo=active wifi-guardian=active wpa_supplicant=active
  L5 app:     charger-api=HTTP 200 | cpu-temp=51.9'C
```

## Tweaks

- **Pi Zero W**: 427 MiB total RAM. Don't over-pack with services. Set `ssh_connect_timeout: 8` if Wi-Fi is unreliable.
- **CPU temp watch**: anything sustained >70°C means thermal trouble (no heatsink, in a case, summer). Throttle at 80°C.
- **SD card wear**: watch disk usage. Above 70% on a Pi means you should consider a bigger card or migrating to SSD.
- **Wi-Fi resilience**: a `wifi-guardian.service` (or similar daemon that pings a known host and resets the interface on failure) is highly recommended for headless Pi Zero deployments.

## Common Pi services

| Use | Typical services |
|-----|------------------|
| Pi-hole DNS | `ssh pihole-FTL` |
| Home Assistant container | `ssh docker containerd` |
| OctoPrint | `ssh octoprint` |
| Sensor / IoT | `ssh cron <your-app>` |
| Tailscale | append `tailscaled` |