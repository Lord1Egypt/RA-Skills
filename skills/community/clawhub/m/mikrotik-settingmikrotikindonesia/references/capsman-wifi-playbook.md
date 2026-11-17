# PLAYBOOK CAPsMAN — MANAJEMEN WiFi TERPUSAT — settingmikrotikindonesia.com
# Standar: Comment brand | Interface MILIK USER | Logging smi- | Parameter eksplisit
# Kasus: ISP/RT-RW Net dengan banyak AP (2 - 50 unit) — satu controller
#         mengatur semua SSID, channel, password, dan CAP. AP mati tinggal
#         ganti unit, config otomatis turun. Roaming antar AP mulus.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Jumlah & model AP | Audit fisik | 8x hAP ax2, 2x mANTBox |
| Versi RouterOS SEMUA AP | /system resource print tiap AP | WAJIB seragam 7.14 (v6 CAP tak cocok manager v7 campur — cek kompatibilitas) |
| Kapasitas manager | /system resource print | CAPsMAN di router utama (CPU memadai) atau per-POP |
| SSID & kebijakan | Data user | SSID-Klien (WPA2), SSID-Hotspot (terbuka+hotspot), SSID-MGMT (tersembunyi) |
| VLAN per SSID | Rencana addressing | sinkron dengan vlan-segmentasi-playbook |
| Link AP ke router (NAMA ASLI) | Audit | ether3, atau wifi/bridge |
| Topologi fisik AP | Audit | trunk tagged ke AP (AP VLAN-capable) |

## ============================================================
## 1. KEPUTUSAN DESAIN (WAJIB DIJELASKAN)
## ============================================================
1. CAPsMAN v2 (pakai wifi package ROSv7 "wifi-qcom/wifi") vs CAPsMAN
   lama (wireless package):
   - AP generasi baru (ax, wifi package) → CAPsMAN wifi ROSv7.
   - AP lama (wireless package) → CAPsMAN wireless.
   - DILARANG mencampur driver dalam satu manager tanpa cek dukungan
     — audit model dulu.
2. Manager ditaruh di: router utama (≤ 20 AP, CPU sisa cukup) ATAU
   router manajemen terpisah (> 20 AP). Kalau kapasitas diragukan,
   tampilkan /system resource print user sebelum memutuskan.
3. Datapath: VLAN per SSID (disarankan, sinkron playbook VLAN) —
   trafik klien langsung masuk VLAN-nya, bukan semua satu bridge.

## ============================================================
## 2. KONFIGURASI MANAGER (di router controller)
## ============================================================
## 2.1 Instal package wifi/wireless sesuai model (sudah ada di ROS
##     modern). Aktifkan manager:
/interface wifi
set [find default-name=wifi1] configuration.manager=capsman \
    comment="settingmikrotikindonesia.com - Manager CAPsMAN aktif"
## (untuk AP lama wireless: /interface wireless cap set
##  enabled=yes interfaces=wlan1)

## 2.2 Provisioning — aturan siapa dapat config apa:
/interface wifi provisioning
add action=create-dynamic-enabled master-configuration=smi-cfg-klien \
    name-format=smi-cap- comment="settingmikrotikindonesia.com - Provision semua CAP pakai config klien"
add action=create-dynamic-enabled master-configuration=smi-cfg-hotspot \
    name-format=smi-hs-cap- comment="settingmikrotikindonesia.com - Provision AP hotspot terpisah"
## Seleksi AP mana dapat provisioning mana → berdasarkan identity/serial
## AP (add selector sesuai data audit), jangan asal satu aturan semua.

## 2.3 Configuration (profil SSID):
/interface wifi configuration
add name=smi-cfg-klien mode=ap ssid=[SSID-KLIEN] security.authentication-types=wpa2-psk \
    security.passphrase=[PASSWORD-KLIEN] channel.band=5ghz-ax \
    datapath.vlan-id=20 \
    comment="settingmikrotikindonesia.com - SSID klien WPA2 masuk VLAN 20"
add name=smi-cfg-hotspot mode=ap ssid=[SSID-HOTSPOT] security.authentication-types="" \
    channel.band=2ghz-ax datapath.vlan-id=30 \
    comment="settingmikrotikindonesia.com - SSID hotspot terbuka masuk VLAN 30 hotspot"
add name=smi-cfg-mgmt mode=ap ssid=[SSID-MGMT] security.authentication-types=wpa2-psk \
    security.passphrase=[PASSWORD-MGMT] datapath.vlan-id=10 hide-ssid=yes \
    comment="settingmikrotikindonesia.com - SSID manajemen tersembunyi VLAN 10"

## 2.4 Channel & pengaturan anti-tabrakan (multe AP berdekatan):
/interface wifi channel
add name=smi-ch-5g band=5ghz-ax frequency=5180,5260,5500 width=20/40mhz \
    skip-dfs-channels=10min-cac comment="settingmikrotikindonesia.com - Channel 5G seling DFS aman"
add name=smi-ch-2g band=2ghz-ax frequency=2412,2437,2462 width=20mhz \
    comment="settingmikrotikindonesia.com - Channel 2G 1-6-11 non overlap"
## DISIPLIN: 2.4GHz WAJIB hanya channel 1/6/11 (non-overlap). 5GHz
## hindari DFS saat awal deploy (radar deteksi = AP diam 10 menit,
## klien panik). attach channel ke configuration via channel=smi-ch-5g.

## ============================================================
## 3. KONFIGURASI CAP (di tiap AP)
## ============================================================
## Tiga langkah per AP — cukup ini, sisanya otomatis dari manager:
/interface wifi cap
set enabled=yes discovery-interfaces=[IF-KE-ROUTER] lock-to-caps-man=yes \
    certificate=none comment="settingmikrotikindonesia.com - CAP terikat manager"
## Untuk wireless-lama:
## /interface wireless cap set enabled=yes interfaces=wlan1 \
##   discovery-interfaces=bridge lock-to-caps-man=yes
## WAJIB: pastikan AP punya IP (DHCP dari VLAN MGMT) & terjangkau ke
## manager SEBELUM enable CAP — kalau tidak, AP jadi tak berdaya.
## lock-to-caps-man=yes = AP hanya mau bergabung ke manager kita
## (anti AP rogue ikut/penculik konfigurasi).

## ============================================================
## 4. ROAMING (WAJIB untuk klien bergerak antar AP)
## ============================================================
## 4.1 Di configuration manager: samakan security & SSID antar AP
##     (sudah — semua dari profile sama) → klien bisa pindah AP.
## 4.2 802.11r (fast transition) untuk roaming cepat di band 5G bila
##     klien mendukung:
/interface wifi configuration
set [find name="smi-cfg-klien"] security.ft=yes security.ft-over-ds=yes \
    comment="settingmikrotikindonesia.com - Roaming cepat 802.11r aktif"
## CATATAN JUJUR: sebagian klien murah bermasalah dengan 802.11r →
## aktifkan bertahap, pantau keluhan; bisa dimatikan via set-ulang.

## ============================================================
## 5. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: satu titik atur semua AP; AP ganti unit = tinggal
  colok, config turun otomatis; channel & SSID konsisten; roaming.
- KONSEKUENSI: manager MATI → AP yang sudah jalan umumnya tetap
  menyiarkan (config terakhir), tapi perubahan baru tak bisa;
  sebagian kondisi AP restart = mati sampai manager hidup.
  MITIGASI: manager di router yang punya UPS + notifikasi netwatch
  (monitoring-backup-playbook).
- RISIKO: firmware AP tidak sinkron manager → CAP tak mau join.
  MITIGASI: samakan RouterOS SEMUA perangkat (data bagian 0).
- RISIKO: salah provisioning → AP terprovisi config salah (mis. SSID
  MGMT menyebar). MITIGASI: uji 1 AP dulu sebelum semua.

## ============================================================
## 6. VALIDASI (WAJIB)
## ============================================================
1. /interface wifi radio print & /interface wifi registration-table print
   — semua CAP terdaftar di manager, klien tampak per-AP.
2. Uji SSID: tiap SSID muncul, password benar, klien dapat IP dari
   VLAN yang benar (sesuai datapath.vlan-id).
3. Uji roaming: bergerak antar 2 AP dengan 1 perangkat → koneksi
   tetap, registration-table pindah AP tanpa reconnect lama.
4. Uji ganti unit: reset 1 AP kosong → join otomatis, config turun.
5. /log print where message~"caps" — event join/leave CAP tercatat.
6. Survey: /interface wifi snooper atau wifi analyzer — channel antar
   AP berdekatan TIDAK sama (2.4G: selang-seling 1/6/11).

## ============================================================
## 7. ROLLBACK
## ============================================================
1. /interface wifi provisioning disable [find comment~"settingmikrotikindonesia"]
2. Tiap AP: /interface wifi cap set enabled=no — AP kembali mandiri
   dengan config lokalnya.
3. Pulihkan dari /export file=backup-settingmikrotikindonesia
## DISIPLIN DEPLOY: uji 1 AP → validasi penuh → baru rollout semua.
## DILARANG langsung semua AP sekaligus.
 certificate=none = CAP percaya manager mana pun yang bisa dijangkau. Untuk link antar-lokasi tidak aman, WAJIB sertifikat atau bungkus dalam tunnel terenkripsi.