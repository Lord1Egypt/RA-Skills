# Common Homelab Device Power Draw Estimates

Reference values for `--power-watts` when adding assets. All figures are typical idle-to-load ranges; use the value that best represents your 24/7 baseline.

---

## Single-Board Computers

| Device | Idle (W) | Load (W) | Notes |
|--------|----------|----------|-------|
| Raspberry Pi Zero 2 W | 0.4 | 1.3 | No USB peripherals |
| Raspberry Pi 3B+ | 1.9 | 5.1 | |
| Raspberry Pi 4 (4GB) | 3.4 | 7.6 | Under sustained load |
| Raspberry Pi 4 (8GB) | 3.8 | 8.0 | |
| Raspberry Pi 5 (4GB) | 2.7 | 12.0 | Peak with PCIe NVMe |
| Orange Pi 5 | 5.0 | 15.0 | |
| Odroid N2+ | 3.0 | 12.0 | |

---

## Mini PCs / Desktops

| Device | Idle (W) | Load (W) | Notes |
|--------|----------|----------|-------|
| Mac Mini M1 | 7 | 39 | |
| Mac Mini M2 | 6 | 30 | |
| Mac Mini M4 | 5 | 28 | Ryan's Shaka machine |
| Intel NUC (12th gen) | 6 | 65 | |
| Beelink SER5 (Ryzen 5800H) | 8 | 65 | |
| Beelink EQ12 (N100) | 5 | 15 | Very efficient |
| HP EliteDesk 800 G5 (i5) | 12 | 65 | |
| Lenovo ThinkCentre M720q | 10 | 55 | |

---

## NAS / Storage

| Device | Idle (W) | Load (W) | Notes |
|--------|----------|----------|-------|
| Synology DS220+ (no disks) | 7 | 16 | |
| Synology DS920+ (no disks) | 9 | 26 | |
| Synology DS1522+ (no disks) | 17 | 40 | |
| TrueNAS Mini X+ (no disks) | 18 | 45 | |
| QNAP TS-464 (no disks) | 12 | 30 | |
| 3.5" HDD (spinning) | 4 | 8 | Per drive at load |
| 2.5" HDD (spinning) | 1.5 | 3 | Per drive |
| 2.5" SSD | 0.5 | 2 | Per drive |
| NVMe M.2 SSD | 0.5 | 3 | Per drive, varies widely |

---

## Networking

| Device | Idle (W) | Notes |
|--------|----------|-------|
| TP-Link TL-SG108E (8-port) | 4 | Unmanaged |
| TP-Link TL-SG116E (16-port) | 6 | |
| Netgear GS308E (8-port) | 4 | |
| Ubiquiti UniFi Switch Lite 8 PoE | 9 | Base, +PoE load |
| Ubiquiti UniFi Switch 24 | 33 | No PoE |
| MikroTik CRS305-1G-4S+IN | 12 | 10GbE SFP+ |
| Ubiquiti EdgeRouter X | 5 | |
| Ubiquiti Dream Machine SE | 33 | |
| pfSense on APU4 | 12 | |
| TP-Link EAP225 (AP) | 9 | |
| Ubiquiti UAP-AC-Pro (AP) | 9 | |
| Ubiquiti U6-Lite (AP) | 7 | |

---

## Servers / Rack

| Device | Idle (W) | Load (W) | Notes |
|--------|----------|----------|-------|
| Dell PowerEdge R720 | 120 | 350 | 2x E5-2670, 64GB RAM |
| Dell PowerEdge R730 | 95 | 380 | |
| Dell PowerEdge R420 | 60 | 200 | |
| HP ProLiant DL380 Gen9 | 100 | 400 | |
| SuperMicro X11SSH (i3-8100) | 25 | 75 | Low-power build |
| Intel N100 rack server | 8 | 20 | Very efficient |

---

## UPS / PDUs

| Device | Notes |
|--------|-------|
| APC Back-UPS 500 | ~5W overhead + battery maintenance |
| APC Back-UPS 1500 | ~8W overhead |
| APC Smart-UPS 1500 | ~12W overhead |
| CyberPower CP1500PFCLCD | ~10W overhead |
| PDU (basic, passive) | ~1W |

---

## Misc / Accessories

| Device | Idle (W) | Notes |
|--------|----------|-------|
| Raspberry Pi PoE+ HAT | +4W | Added to Pi power draw |
| USB hub (powered, 7-port) | 2 | No load |
| KVM switch (2-port) | 1 | |
| Raspberry Pi Touchscreen (7") | 2.5 | |
| Zigbee USB dongle | 0.3 | |
| Z-Wave USB dongle | 0.3 | |
| USB Bluetooth adapter | 0.25 | |

---

## Tips

- **Use idle power** for 24/7 always-on devices as your baseline.
- **NAS total** = chassis idle + (disks × per-disk idle) + spinup spikes.
- **PoE switches** should be measured at their device PoE draw, not rated max.
- When unsure, use a smart plug with energy monitoring (e.g., Kasa EP25, Shelly PM) and measure directly.
- Rule of thumb for rough estimates: NAS ~20-40W, Pi cluster ~5-10W/node, managed switch ~5-15W.
