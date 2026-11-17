# PLAYBOOK L2TP/IPSEC SITE-TO-SITE — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit
# POSISI: pelengkap vpn-antar-cabang-playbook.md. WireGuard/EoIP lebih
# disukai antar MikroTik; L2TP/IPSEC dipilih bila SALAH SATU sisi
# perangkat NON-MikroTik / klien enterprise minta standar IPsec.
# Prinsip: PSK kuat atau lebih baik sertifikat; NAT-T standar.

## ============================================================
## 0. DATA WAJIB
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| IP publik statik kedua sisi (atau DDNS) | Audit /ip cloud | pusat statik, cabang DDNS |
| Subnet LAN kedua sisi (TIDAK BOLEH sama!) | Audit | 10.10.0.0/24 vs 10.20.0.0/24 |
| Perangkat sisi lawan & dukungan IPsec | Data user | MikroTik↔vendor lain |
| Metode auth: PSK / sertifikat | Keputusan+user | PSK kuat (min 24 karakter acak) |
| Pool IP tunnel L2TP | Rencana | 10.99.1.0/24 |
| Versi ROS | Audit | 7.14 |

## ATURAN: subnet LAN ANTAR SISI WAJIB BERBEDA — sama = routing kacau
## permanen. Audit DULU sebelum lanjut; bila sama, beritahu user
## harus readdress salah satu (jangan diakali dulu).

## ============================================================
## 1. KOMPONEN A — L2TP SERVER (sisi pusat)
## ============================================================
/interface l2tp-server server
set enabled=yes use-ipsec=yes ipsec-secret=[PSK-KUAT] \
    authentication=mschap2 default-profile=smi-l2tp \
    comment="settingmikrotikindonesia.com - L2TP server IPsec aktif"
/ppp profile
add name=smi-l2tp local-address=10.99.1.1 remote-address=pool-l2tp \
    comment="settingmikrotikindonesia.com - Profil tunnel L2TP"
/ppp secret
add name=smi-site-cabang1 password=[PASS-KUAT] profile=smi-l2tp \
    comment="settingmikrotikindonesia.com - Kredensial cabang1"
/ip pool
add name=pool-l2tp ranges=10.99.1.10-10.99.1.99 \
    comment="settingmikrotikindonesia.com - Pool tunnel L2TP"

## ============================================================
## 2. KOMPONEN B — FIREWALL UNTUK L2TP/IPSEC (DARI WAN)
## ============================================================
/ip firewall filter
add chain=input action=accept protocol=udp dst-port=1701 \
    src-address=[IP-PUBLIK-CABANG] \
    comment="settingmikrotikindonesia.com - L2TP dari cabang sah saja"
add chain=input action=accept protocol=udp dst-port=500 \
    src-address=[IP-PUBLIK-CABANG] \
    comment="settingmikrotikindonesia.com - IKE dari cabang sah"
add chain=input action=accept protocol=udp dst-port=4500 \
    src-address=[IP-PUBLIK-CABANG] \
    comment="settingmikrotikindonesia.com - NAT-T dari cabang sah"
add chain=input action=accept protocol=ipsec-esp \
    src-address=[IP-PUBLIK-CABANG] \
    comment="settingmikrotikindonesia.com - ESP dari cabang sah"
## DISIPLIN: src-address dibatasi IP cabang — DILARANG membuka L2TP
## untuk seluruh internet (brute force PSK/password nyata terjadi).
## POSISI: di atas rule drop WAN (hardening-playbook). Verifikasi urutan!

## ============================================================
## 3. KOMPONEN C — SISI CABANG (client)
## ============================================================
/interface l2tp-client
add name=smi-l2tp-cabang1 connect-to=[IP-PUBLIK-PUSAT] user=smi-site-cabang1 \
    password=[PASS-KUAT] use-ipsec=yes ipsec-secret=[PSK-KUAT] \
    add-default-route=no disabled=no \
    comment="settingmikrotikindonesia.com - Tunnel ke pusat"

## ============================================================
## 4. KOMPONEN D — ROUTING ANTAR SITUS
## ============================================================
## Pusat: rute ke LAN cabang via IP tunnel cabang:
/ip route
add dst-address=10.20.0.0/24 gateway=10.99.1.10 \
    comment="settingmikrotikindonesia.com - Rute LAN cabang1 via tunnel"
## Cabang: rute ke LAN pusat via IP tunnel lokal:
add dst-address=10.10.0.0/24 gateway=10.99.1.1 \
    comment="settingmikrotikindonesia.com - Rute LAN pusat via tunnel"
## FIREWALL FORWARD: izinkan antar-LAN eksplisit (dua sisi):
/ip firewall filter
add chain=forward action=accept src-address=10.10.0.0/24 dst-address=10.20.0.0/24 \
    comment="settingmikrotikindonesia.com - Forward pusat ke cabang"
add chain=forward action=accept src-address=10.20.0.0/24 dst-address=10.10.0.0/24 \
    connection-state=established,related \
    comment="settingmikrotikindonesia.com - Balasan cabang ke pusat"
## (percikan balikan dua arah sesuai kebijakan bisnis — tanya user
## siapa boleh akses apa; jangan open semua port antar situs.)

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: interoperabel lintas merek; standar enterprise; NAT-T
  jalan di belakung NAT umum.
- KONSEKUENSI: L2TP/IPsec lebih berat CPU dari WireGuard (enkripsi
  userland); jumlah tunnel terbatas kemampuan board.
- RISIKO #1: subnet sama antar situs → routing rusak. AUDIT DULU.
- RISIKO: PSK lemah / port 1701 terbuka umum → brute force. MITIGASI:
  src-address filter + PSK panjang acak + log smi-.
- RISIKO: NAT ganda di salah satu sisi → tunnel deg-degan. MITIGASI:
  NAT-T (4500) aktif; bila bisa, minta IP statik tanpa NAT berlapis.
- RISIKO: MTU (L2TP overhead) → beberapa situs/web lambat. MITIGASI:
  mss-clamp di mangle (1450-1460) bila gejala muncul.

## ============================================================
## 6. VALIDASI (WAJIB, URUT)
## ============================================================
1. /interface l2tp-client print — status: connected (sisi cabang).
2. /ppp active print — tunnel tampak di pusat.
3. Ping lintas situs: LAN pusat ↔ LAN cabang (bukan cuma IP tunnel!).
4. Aplikasi nyata: akses file server / kamera antar situs.
5. /log print where message~"l2tp|ipsec" — tanpa error berulang.
6. Uji NAT-T: cabang di belakang ISP NAT → tunnel tetap stabil.
7. Reconnect: restart tunnel → kembali sendiri <1 menit.

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /interface l2tp-client disable [find comment~"settingmikrotikindonesia"]
2. Pusat: /interface l2tp-server server set enabled=no
3. /ip firewall filter disable [find comment~"L2TP|IKE|NAT-T|ESP"]
4. /ip route remove [find comment~"Rute LAN (pusat|cabang) via tunnel"]
5. Pulihkan dari /export file=backup-settingmikrotikindonesia
