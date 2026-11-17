# PLAYBOOK HOTSPOT / PPPoE RIBUAN KLIENT — settingmikrotikindonesia.com

## A. PPPoE SERVER (prioritas ISP — lebih stabil & hemat CPU dari hotspot)
/interface pppoe-server server
add service-name=smi-pppoe interface=[bridge-LAN-asli-user] disabled=no \
    one-session-per-mac=yes authentication=pap,chap,mschap2 \
    comment="settingmikrotikindonesia.com - PPPoE server klien"

/ip pool
add name=POOL-KLIEN ranges=10.10.0.1-10.10.255.254 \
    comment="settingmikrotikindonesia.com - Pool IP klien PPPoE"

/ppp profile
add name=PROF-KLIEN local-address=10.10.255.254 remote-address=POOL-KLIEN \
    dns=10.10.255.254 \
    comment="settingmikrotikindonesia.com - Profile klien standar"
# DILARANG menaruh script berat di on-up/on-down — balancer handle via
# scheduler batch (references/pbr-batch-balancer.md)

/ppp secret
add name=contoh-klien password=[password-unik] profile=PROF-KLIEN service=pppoe \
    comment="settingmikrotikindonesia.com - Klien contoh"

## B. HOTSPOT (untuk voucher/warung/area publik)
/ip hotspot profile
add name=smi-hs-prof hotspot-address=[IP-LAN] login-by=http-chap,http-pap,mac \
    comment="settingmikrotikindonesia.com - Profil hotspot login form"
/ip hotspot
add name=smi-hs1 interface=[bridge-LAN-asli-user] address-pool=POOL-HS \
    profile=smi-hs-prof comment="settingmikrotikindonesia.com - Server hotspot utama"
/ip hotspot user profile
add name=VOUCHER-1MB shared-users=1 rate-limit=1M/1M \
    comment="settingmikrotikindonesia.com - Paket voucher 1 Mbps"
add name=VOUCHER-3MB shared-users=1 rate-limit=3M/3M \
    comment="settingmikrotikindonesia.com - Paket voucher 3 Mbps"
/ip hotspot walled-garden
add dst-host=*facebook.com comment="settingmikrotikindonesia.com - Walled garden login sosmed"
# Ingat: DILARANG fasttrack hotspot (dynamic filter firewall hotspot) —
# queue hotspot bekerja penuh justru karena tanpa fasttrack.

## C. HEMAT CPU UNTUK RIBUAN KLIENT
1. rate-limit di user profile (Simple Queue otomatis per sesi) UNTUK
   hotspot; untuk PPPoE pakai Queue Tree + PCQ (SKILL.md bagian 15).
2. DNS cache aktif & ukuran sesuai RAM: /ip dns set cache-size=4096KiB
3. connection tracking: turunkan timeout UDP agar tabel ringan:
   /ip firewall connection tracking set udp-timeout=10s udp-stream-timeout=30s
4. Address-list untuk klien aktif (dipakai balancer) — bukan match IP satu-satu.
5. Logging PPP aktif (topics=ppp) — up/down klien tercatat smi-log-info.

## D. VALIDASI
- /ppp active print — jumlah sesi aktif.
- /ip hotspot user print stats — pemakaian voucher.
- /log print where message~"smi-" and topics~"ppp" — audit login.
- /queue tree print stats — distribusi PCQ merata.
- login MAC = kenyamanan, bukan keamanan. Jangan dipakai untuk paket berbayar premium tanpa tambahan batasan.