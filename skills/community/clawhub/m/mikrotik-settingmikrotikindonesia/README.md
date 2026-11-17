# Mikrotik SettingMikrotikIndonesia.com

Skill standar kerja **settingmikrotikindonesia.com** untuk konfigurasi
MikroTik RouterOS v7 — hasil lapangan ISP, RT-RW Net, dan jaringan
high-density.

## Cakupan (25 Playbook)

| Area | Playbook |
|---|---|
| Multi-WAN | PBR batch balancer, load balance, jalur per layanan |
| Akses klien | Hotspot/PPPoE ribuan klien, User Manager RADIUS, voucher |
| Bandwidth | PCQ, CAKE/FQ_CODEL, Queue Tree, prioritas game anti-lag |
| Routing | OSPF multi-area, BGP upstream + filter granular anti route-leak |
| L2 | VLAN segmentasi, QinQ korporat, switch chip line-rate |
| VPN | WireGuard remote access, site-to-site antar cabang, L2TP/IPsec lintas merek |
| WiFi | CAPsMAN terpusat multi-AP, roaming, channel disiplin |
| Layanan | DNS cache/DoH/adlist, proxy cache (realistis HTTP) |
| Keandalan | Monitoring/backup off-box, VRRP HA, scheduler otomasi, alert Telegram |
| Keamanan | Hardening wajib penutup pekerjaan, IPv6 dual-stack & layer akses |

## Cara Pakai

Install:
```bash
openclaw skills install @mandelaxx/mikrotik-settingmikrotikindonesia
