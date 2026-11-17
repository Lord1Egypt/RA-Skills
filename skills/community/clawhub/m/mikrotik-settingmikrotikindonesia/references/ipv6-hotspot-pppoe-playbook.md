# PLAYBOOK IPv6 DI LAYER AKSES (HOTSPOT & PPPoE) — settingmikrotikindonesia.com
# Standar: Comment brand | Logging smi- | Parameter eksplisit | Jujur
# POSISI: perdalaman ipv6-playbook.md (BACA DULU — khususnya bagian
# firewall v6 yang WAJIB). Playbook induk = distribusi prefix sampai
# router; yang ini = sampai ke klien hotspot & PPPoE.
# KEJUJURAN LAPANGAN: autentik hotspot MikroTik berbasis IPv4 — IPv6
# di hotspot butuh penanganan khusus (RA ke klien + firewall tahan
# sampai login). PPPoE dual-stack jauh lebih matang. Sampaikan
# realistis: jangan jual "hotspot v6 penuh" kalau kebutuhannya cuma
# internet biasa.

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG (DILARANG MENGARANG)
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Prefix milik ISP (dari playbook induk) | Register APNIC | 2001:db8:aaaa::/48 (PLACEHOLDER — WAJIB ganti prefix asli user!) |
| Interface hotspot & PPPoE server ASLI | /interface print | vlan30-hotspot, pppoe-server |
| Firewall v6 playbook induk SUDAH aktif? | /ipv6 firewall filter print | WAJIB SUDAH |
| Profile PPPoE existing | /ppp profile print | nama ASLI user |
| Versi ROS | /system resource print | 7.14+ |

## PRASYARAT KERAS: firewall IPv6 dari playbook induk SUDAH aktif dan
## LULUS UJI sebelum prefix disebarkan ke klien. Belum? = STOP,
## kerjakan playbook induk dulu. Deploy terbalik (prefix dulu, firewall
## belakangan) = semua klien exposed ke internet v6 — kesalahan fatal.

## ============================================================
## 1. KOMPONEN A — PPPoE DUAL-STACK (paling matang, mulai dari sini)
## ============================================================
## Pola teruji lapangan ISP: auth tetap IPv4 (PPP), prefix v6
## didelegasikan per pelanggan via PD — router pelanggan sebar sendiri
## ke rumahnya (end-to-end tanpa NAT: game host, CCTV, remote jalan).

## 1.1 Pool delegasi (satu /56 per pelanggan, dari /48 induk):
/ipv6 pool
add name=smi-pool-pd prefix=[PREFIX-INDUK-USER] prefix-length=56 \
    comment="settingmikrotikindonesia.com - Pool PD /56 per pelanggan PPPoE"
## Contoh bila induk 2001:db8:aaaa::/48 → prefix=2001:db8:aaaa::/48
## prefix-length=56 → muat 256 pelanggan /56.

## 1.2 Ikat pool ke profile PPPoE ASLI user (set-ulang, bukan re-add!):
/ppp profile
set [find name="[NAMA-PROFILE-PPPOE-ASLI]"] \
    remote-ipv6-prefix-pool=smi-pool-pd \
    comment="settingmikrotikindonesia.com - PPPoE dual-stack PD aktif"
## 1.3 RA: minta klien ambil DNS via DHCPv6 (other-configuration):
/ipv6 nd
set [find interface="[IF-PPPOE-ASLI]"] other-configuration=yes \
    managed-address-configuration=no \
    comment="settingmikrotikindonesia.com - RA minta DNS via DHCPv6"
## VERIFIKASI: /ipv6 nd print — jangan set-ulang entry "all"
## sembarangan bila ada interface lain yang pakai; pilih entry
## interface PPPoE yang tepat sesuai audit.

## ============================================================
## 2. KOMPONEN B — HOTSPOT DENGAN IPv6 (realistis, hati-hati)
## ============================================================
## Fakta: login page & auth hotspot tetap jalan via IPv4. IPv6 yang
## kita berikan = KONEKTIVITAS TAMBAHAN via RA, dengan KUNCI: klien
## v6 yang BELUM login TETAP DITAHAN firewall — tanpa ini, orang
## bisa internet gratis tanpa login lewat v6 (bocor klasik!).

## 2.1 Distribusi prefix ke VLAN hotspot (pola playbook induk 2.1):
/ipv6 address
add interface=[IF-HOTSPOT-ASLI] \
    address=[PREFIX-INDUK-USER]:30::/64 advertise=yes \
    comment="settingmikrotikindonesia.com - RA hotspot aktif"
## (ganti :30: sesuai VLAN ID hotspot user dari audit!)

## 2.2 KUNCI KEAMANAN — tahan v6 hotspot yang belum login:
/ipv6 firewall filter
add chain=forward action=drop \
    src-address=[PREFIX-INDUK-USER]:30::/64 \
    out-interface=[IF-WAN-ASLI] \
    log=yes log-prefix="smi-v6-hotspot-tahan" \
    comment="settingmikrotikindonesia.com - V6 hotspot belum auth ditahan"
add chain=forward action=accept \
    src-address-list=smi-v6-hotspot-ok out-interface=[IF-WAN-ASLI] \
    comment="settingmikrotikindonesia.com - V6 hotspot sah lewat"
## POSISI WAJIB: rule accept DI ATAS rule drop (firewall dibaca atas
## ke bawah — bila terbalik, drop menang = tidak ada yang bisa v6).

## 2.3 Buka untuk yang sudah login:
## Script hotspot on-login menambahkan alamat v6 klien ke address-list
## smi-v6-hotspot-ok, on-logout menghapus:
/system script
add name=smi-hotspot-v6 source={
# dipanggil dari hotspot user profile on-event / atau scheduler polling
# (mechanisme final tergantung versi ROS user — WAJIB uji di LAB:
#  API hotspot mengembalikan alamat v6 klien beda perilaku antar
#  versi. Verifikasi dengan data router user, jangan asal tempel!)
:do {
  /ip hotspot active
  :foreach i in=[find] do={
    :local u [/ip hotspot active get $i user]
    :local a [/ip hotspot active get $i address]
    ## alamat v6 klien didapat dari binding/RA — implementasi
    ## disesuaikan hasil uji LAB di versi ROS user
    :log info ("smi-hotspot-v6: sinkron user " . $u)
  }
} on-error={
  :log error "smi-hotspot-v6: gagal sinkron address-list"
}
} comment="settingmikrotikindonesia.com - Sinkron v6 hotspot ke address-list"
## DILARANG pasang produksi sebelum lulus uji LAB bagian 5 #2-#3.

## 2.4 KEPUTUSAN JUJUR WAJIB DISAMPAIKAN: bila kebutuhan user cuma
## "pelanggan bisa internet", hotspot IPv4 SUDAH CUKUP. Pasang IPv6
## hotspot HANYA bila ada alasan nyata: permintaan pelanggan korporat,
## aplikasi v6-only, kebijakan regulator. Tidak ada alasan = tidak
## dipasang (config tak terpakai = sampah config + risiko bocor baru).

## ============================================================
## 3. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KEUNTUNGAN: pelanggan PPPoE dapat PD /56 penuh (game host, CCTV,
  remote tanpa NAT); siap masa depan; nilai jual "IPv6 ready".
- KONSEKUENSI: dua jalur kebijakan (v4 billing + v6 firewall) harus
  sinkron — LIMIT BANDWIDTH v4 TIDAK OTOMATIS MEMBATASI v6! Queue v6
  perlu aturan sendiri target prefix (sinkron
  bandwidth-management-playbook: buat mangle/queue untuk v6 atau
  tandai di dua stack).
- RISIKO #1: hotspot v6 lolos tanpa login (firewall tahan salah urutan
  / tak jalan) → internet gratis bocor. MITIGASI: uji #2 bagian 5
  WAJIB lulus; urutan accept di atas drop diverifikasi.
- RISIKO: pelanggan pakai alamat v6 acak (privacy extensions) → sulit
  ditelusuri per alamat. MITIGASI: identifikasi per PREFIX PD (tiap
  pelanggan /56 unik) untuk keperluan abuse/troubleshoot.
- RISIKO: pemakaian v6 tak tercatat billing → edukasi owner sejak
  awal bahwa billing v4 ≠ batas v6.
- RISIKO: pool PD habis bila pelanggan > kapasitas /48 → hitung
  kebutuhan dulu; bila kurang, minta prefix lebih besar sejak awal.

## ============================================================
## 4. VALIDASI (WAJIB, URUT — TES #2 PALING PENTING!)
## ============================================================
1. PPPoE: klien konek → cek /ipv6 pool — prefix terpakai tercatat;
   router pelanggan dapat /56; perangkat di rumah dapat alamat global;
   test-ipv6.com skor tinggi.
2. HOTSPOT (TES KRITIS): perangkat BARU tanpa login → browsing v6
   DITAHAN + log smi-v6-hotspot-tahan naik. Gagal tahan = STOP,
   perbaiki firewall — DILARANG produksi.
3. HOTSPOT: setelah login → v6 lewat (address-list smi-v6-hotspot-ok
   terisi; log sinkron muncul).
4. Firewall v6 playbook induk tetap lulus semua ujinya (rule baru
   tidak merusak rule induk — cek urutan print).
5. Speedtest dua stack → keduanya sesuai paket yang dijual (v6 tidak
   jadi celah unlimited).
6. Logout klien → alamat keluar dari address-list → v6 tertahan lagi.

## ============================================================
## 5. ROLLBACK
## ============================================================
1. Hentikan distribusi DULU (kebalikan urutan deploy):
   /ipv6 nd set [find interface="[IF-PPPOE-ASLI]"] other-configuration=no
   /ipv6 address disable [find comment~"RA hotspot"]
2. /ipv6 firewall filter disable [find log-prefix~"smi-v6-hotspot"]
3. /ppp profile set [find name="[NAMA-PROFILE-PPPOE-ASLI]"] \
       remote-ipv6-prefix-pool=""
4. /system script remove [find name="smi-hotspot-v6"]
5. Pulihkan dari /export file=backup-settingmikrotikindonesia
## DISIPLIN: hentikan DISTRIBUSI dulu, baru bedah firewall & binding —
## rollback terbalik sempurna dari urutan deploy.
