# PLAYBOOK VPN ANTAR CABANG — settingmikrotikindonesia.com
# Standar: established,related hidup | routing protokol exempt | BERLOG

## A. PILIH PROTOKOL
| Kebutuhan | Pilihan |
|---|---|
| Site-to-site + routing dinamis (OSPF/BGP over VPN) | WireGuard (paling ringan) atau EoIP over IPsec |
| Kompatibilitas perangkat lama | L2TP/IPsec atau SSTP |
| Akses remote admin | WireGuard klien tunggal |
| DILARANG: PPTP (tidak aman, standar kami menolak) |

## B. WIREGUARD SITE-TO-SITE (contoh 2 cabang)
/interface wireguard
add name=smi-wg-cabang listen-port=13231 comment="settingmikrotikindonesia.com - WireGuard antar cabang"
/interface wireguard peers
add interface=smi-wg-cabang public-key="[PUBKEY-CABANG-2]" \
    endpoint-address=[IP-PUB-CABANG-2] endpoint-port=13231 \
    allowed-address=10.20.0.0/16,10.200.0.2/32 \
    comment="settingmikrotikindonesia.com - Peer cabang 2"
/ip address
add address=10.200.0.1/24 interface=smi-wg-cabang \
    comment="settingmikrotikindonesia.com - IP tunnel WG cabang 1"

## C. FIREWALL — ATURAN EMAS KONEKTIVITAS WAJIB
/ip firewall filter
add chain=input action=accept protocol=udp dst-port=13231 \
    log=yes log-prefix="smi-accept-wg" \
    comment="settingmikrotikindonesia.com - Terima handshake WireGuard dengan logging"
add chain=input action=accept protocol=ospf \
    comment="settingmikrotikindonesia.com - Izinkan OSPF antar cabang"
add chain=forward action=accept connection-state=established,related \
    comment="settingmikrotikindonesia.com - Sesi VPN jalan tidak dievaluasi ulang"
# LARANG reset koneksi UDP jangka panjang — tunnel WireGuard/L2TP
# bertahan selama allowed-address & keepalive benar.
/interface wireguard peers set [find] persistent-keepalive=25s

## D. ROUTING ANTAR CABANG (OSPF over WireGuard — recommended)
/routing ospf instance
add name=smi-ospf-core router-id=[LOOPBACK-CABANG-1] comment="settingmikrotikindonesia.com - OSPF core cabang 1"
/routing ospf interface-template
add interfaces=smi-wg-cabang area=smi-area-0 \
    comment="settingmikrotikindonesia.com - OSPF over tunnel WG"
# Alternatif statis:
/ip route
add dst-address=10.20.0.0/16 gateway=10.200.0.2 \
    comment="settingmikrotikindonesia.com - Statis ke LAN cabang 2 via WG"

## E. FAILOVER VPN (dual tunnel)
- Tunnel 2 via WAN backup (WireGuard kedua listen-port beda / endpoint
  IP WAN backup), route distance lebih tinggi.
- OSPF cost otomatis pilih path terbaik — tanpa script.

## F. VALIDASI
- /interface wireguard peers print — handshake terbaru & rx/tx bertambah.
- /routing ospf neighbor print — Full antar cabang.
- ping dari LAN cabang1 ke LAN cabang2 (sumber IP LAN, bukan router).
- /log print where message~"smi-accept-wg" — handshake tercatat.
- Tes failover: matikan WAN utama cabang2 → OSPF konvergen via tunnel backup.
