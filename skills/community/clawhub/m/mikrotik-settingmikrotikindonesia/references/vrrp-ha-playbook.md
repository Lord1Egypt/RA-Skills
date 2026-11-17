# PLAYBOOK HIGH AVAILABILITY VRRP — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit
# Kasus: dua router di satu lokasi — kalau gateway utama mati, cadangan
# otomatis ambil alih dalam hitungan detik. Untuk klien yang jual SLA
# uptime / jaringan yang putus gateway = kerugian nyata.
# KEJUJURAN: VRRP melindungi KEGAGALAN GATEWAY SAJA. Tidak melindungi:
# fiber upstream putus (itu netwatch/multihoming), bridge/AP mati,
# power gedung mati (itu UPS/genset). Jangan jual VRRP sebagai "anti
# semua mati".

## ============================================================
## 0. DATA WAJIB
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Dua router tersedia + model & versi ROS SAMA | Audit | sama-sama 7.14 |
| Subnet LAN gateway | Audit | 10.10.10.0/24 |
| IP virtual (VIP) yang dipakai klien | Rencana | 10.10.10.1 (gateway klien!) |
| IP asli router A & B | Audit | 10.10.10.2 / 10.10.10.3 |
| VRID (unik per grup di segmen) | Rencana | 10 |
| Prioritas & preemption | Desain | A=200 master, B=150 backup |
| Interface LAN asli kedua router | Audit | bridge-lan (SAMA nama logis) |

## PRASYARAT: kedua router WAJIB config dasar identik (firewall, NAT,
## routing) — VRRP hanya menukar identitas gateway; kalau config
## backup router beda, failover jalan tapi layanan rusak. Backup
## router = clone config utama (bandingkan /export kedua sisi dulu!).

## ============================================================
## 1. KOMPONEN A — IP DASAR (RED-DESIGN GATEWAY)
## ============================================================
## Router A (utama):
/ip address
add interface=bridge-lan address=10.10.10.2/24 \
    comment="settingmikrotikindonesia.com - IP asli router A"
## Router B (cadangan):
/ip address
add interface=bridge-lan address=10.10.10.3/24 \
    comment="settingmikrotikindonesia.com - IP asli router B"
## Klien TIDAK memakai .2/.3 — klien memakai VIP (langkah 2).

## ============================================================
## 2. KOMPONEN B — VRRP (kedua router, prioritas beda)
## ============================================================
## Router A (master):
/interface vrrp
add name=smi-vrrp-lan interface=bridge-lan vrid=10 priority=200 \
    preemption-mode=yes authentication=ah password=[PASS-VRRP] \
    comment="settingmikrotikindonesia.com - VRRP master A"
/ip address
add interface=smi-vrrp-lan address=10.10.10.1/24 \
    comment="settingmikrotikindonesia.com - VIP gateway klien"
## Router B (backup):
/interface vrrp
add name=smi-vrrp-lan interface=bridge-lan vrid=10 priority=150 \
    preemption-mode=yes authentication=ah password=[PASS-VRRP] \
    comment="settingmikrotikindonesia.com - VRRP backup B"
/ip address
add interface=smi-vrrp-lan address=10.10.10.1/24 \
    comment="settingmikrotikindonesia.com - VIP gateway klien"
## Catatan disiplin: vrid SAMA (10) di kedua router = satu grup;
## priority tinggi = menang. preemption=yes = A kembali jadi master
## saat pulih (default layanan kembali normal — sampaikan pilihannya:
## yes = konsisten; no = tak ada preemption kedua).
## DHARATAN: authentication di VRRPv2 (v4 subnet) ok; bila
## IPv6/VRRPv3 ikut, verifikasi dukungan auth di versi ROS user.

## ============================================================
## 3. KOMPONEN C — PENJAGA UPSTREAM (VRRP TIDAK MENANGANI INI!)
## ============================================================
## Masalah klasik: A hidup tapi fiber upstream-nya mati → VRRP tetap
## di A = klien "gateway hidup, internet mati". Solusi: netwatch cek
## upstream, bila gagal → turunkan priority A (failover tetap terjadi):
/tool netwatch
add host=[IP-CEK-UPSTREAM-MIS-8.8.8.8] interval=10s up-script="\
  /interface vrrp set [find name=\"smi-vrrp-lan\"] priority=200" \
  down-script="\
  /interface vrrp set [find name=\"smi-vrrp-lan\"] priority=100; \
  :log error \"smi-ha: upstream A gagal - priority diturunkan, B ambil alih\"" \
  comment="settingmikrotikindonesia.com - Netwatch upstream atur prioritas VRRP"
## (di Router A. Hasil: gateway ikut sehat upstream, bukan cuma router.)
## Sinkron: monitoring-backup-playbook untuk alert Telegram-nya.

##===========
## 4. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: gateway mati → B ambil alih dalam ~3 detik (interval
  default); klien tak perlu ubah setting apa pun (VIP konstan).
- KONSEKUENSI: B harus SENANTIASA siap (config identik, update ROS
  & rule sinkron dua sisi — pekerjaan ganda setiap perubahan).
  MITIGASI: jadwalkan sinkronisasi config berkala + bandingkan export.
- RISIKO: split-brain (kedua router merasa master) — umumnya karena
  kabel/link antar router bermasalah atau VRID bentrok dengan VRRP
  lain di segmen. MITIGASI: log monitoring + VRID unik + link langsung
  antar router sehat.
- RISIKO: failover OK tapi NAT/sesi koneksi putus (connection tracking
  tidak sinkron) → download/video call terputus sesaat saat failover,
  lalu pulih. Sampaikan ini ke user — VRRP bukan seamless penuh;
  bila butuh seamless: synchronised connection tracking (fitur
  tertentu) atau proyek lebih besar.
- RISIKO: DHCP server — pastikan HANYA SATU router yang DHCP aktif,
  atau DHCP failover disiapkan sadar (dua DHCP identik di satu
  segmen tanpa desain = pool konflik).

## ============================================================
## 5. VALIDASI (WAJIB, URUT — semua diuji SEBELUM dijual ke klien)
## ============================================================
1. /interface vrrp print — A: state MASTER; B: state BACKUP.
2. Cek klien: gateway 10.10.10.1 → internet jalan normal.
3. UJI FAILOVER (inti!): tarik power/kabel Router A →
   /interface vrrp print di B jadi MASTER ≤ 5 detik → klien ping
   terputus sesaat lalu JALAN LAGI tanpa ubah apa pun.
4. Nyalakan A lagi → preemption → A kembali MASTER.
5. Uji netwatch upstream: blok sementara akses upstream di A →
   priority turun → B ambil alih → log smi-ha muncul.
6. Uji aplikasi nyata: video call / download saat failover → putus
   sesaat lalu pulih (dokumentasikan ke user apa yang terjadi).
7. Bandingkan /export A vs B → perbedaan hanya IP asli & priority.

## ============================================================
## 6. ROLLBACK
## ============================================================
1. /interface vrrp disable [find comment~"settingmikrotikindonesia"]
   (di kedua router — B dulu bila A sedang master, agar tidak
   failover balik di saat salah konfig)
2. /tool netwatch disable [find comment~"Netwatch upstream"]
3. Kembalikan gateway klien bila sempat diubah (tidak perlu bila
   VIP tetap — itu justru keunggulan desain ini)
4. Pulihkan dari /export file=backup-settingmikrotikindonesia```

---

# UPDATE SKILL.md

Tambah di FILE REFERENCES:

```markdown
- references/bgp-filter-granular-playbook.md → perdalaman BGP: filter in/out, anti route-leak, max-prefix, multihoming
- references/user-manager-playbook.md → RADIUS User Manager: billing voucher hotspot/PPPoE multi-router terpusat
- references/queue-tree-game-playbook.md → prioritas trafik game anti-lag: mangle connection-mark hemat CPU + queue tree priority
- references/l2tp-ipsec-site-to-site-playbook.md → VPN lintas merek (perangkat non-MikroTik), PSK, NAT-T
- references/ipv6-hotspot-pppoe-playbook.md → IPv6 di layer akses: PPPoE dual-stack PD, hotspot v6 dengan firewall tahan
- references/vrrp-ha-playbook.md → dua router gateway HA, failover otomatis, netwatch atur priority
- references/telegram-integration-playbook.md → modul inti notifikasi Telegram: bot setup, script kirim retry, backup ke Telegram, diagnosis gagal kirim
