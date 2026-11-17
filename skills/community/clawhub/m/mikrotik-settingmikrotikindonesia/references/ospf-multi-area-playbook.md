# PLAYBOOK OSPF MULTI-AREA — settingmikrotikindonesia.com
# Standar: RouterOS v7 | Router-id = loopback | Filter WAJIB | Logging smi-
# Kasus: ISP multi-pop, core + beberapa POP, konsolidasi LSA & kontrol path

## ============================================================
## 0. DATA WAJIB SEBELUM CONFIG
## ============================================================
| Parameter | Sumber | Contoh |
|---|---|---|
| Topologi: router mana core, mana POP | Diagram user | Core1, Core2, POP-A, POP-B |
| IP loopback tiap router (UNIK!) | Rencana addressing | 10.255.0.1-.4 |
| Subnet link antar router | Rencana addressing | 10.0.12.0/30 dst. |
| Subnet LAN tiap POP (untuk advertise) | Audit | 10.10.0.0/16 |
| RouterOS versi semua router | /system resource print | 7.14 (WAJIB seragam/compatible) |

ATURAN EMAS ADDRESSING:
- Router-id = loopback /32, UNIK per router, tidak di-announce lewat
  network statement biasa tapi harus terjangkau (via OSPF) — kunci
  stabilitas peering antar-POP.
- Link antar router pakai /30 atau /31 — presisi, hemat.

## ============================================================
## 1. DESAIN AREA (JELASKAN KE USER)
## ============================================================
- AREA 0 (backbone): core routers + link antar core. WAJIB ada.
- AREA 1..N: masing-masing POP. Alasan multi-area:
  1. Ringkas LSA → SPF ringan → CPU rendah (sinergi hemat CPU standar kami).
  2. Perubahan di POP tidak memicu full SPF di seluruh jaringan.
  3. Kontrol ringkasan route antar area (inter-area filter).
- ATURAN: semua area WAJIB terhubung langsung ke area 0. POP yang
  tak bisa fisik ke area 0 → gunakan virtual-link (bagian 6) atau
  desain ulang — DILARANG area terisolasi "doang jalan dulu".

## ============================================================
## 2. KONFIGURASI CORE ROUTER (CONTOH CORE1)
## ============================================================
## 2.1 Loopback & router-id:
/interface
add name=loopback type=loopback comment="settingmikrotikindonesia.com - Loopback router-id core1"
/ip address
add address=10.255.0.1/32 interface=loopback \
    comment="settingmikrotikindonesia.com - Loopback router-id UNIK core1"

## 2.2 Instance & area:
/routing ospf instance
add name=smi-ospf-core router-id=10.255.0.1 \
    comment="settingmikrotikindonesia.com - Instance OSPF core router-id loopback"
/routing ospf area
add name=smi-area-0 area-id=0.0.0.0 instance=smi-ospf-core \
    comment="settingmikrotikindonesia.com - Backbone area nol"
add name=smi-area-pop-a area-id=0.0.0.1 instance=smi-ospf-core \
    comment="settingmikrotikindonesia.com - Area POP A"

## 2.3 Interface-template presisi (PASIF di mana tak perlu neighbor):
/routing ospf interface-template
add interfaces=loopback area=smi-area-0 passive=yes \
    comment="settingmikrotikindonesia.com - Loopback diiklankan tanpa neighbor"
add interfaces=[IF-KE-POP-A] area=smi-area-pop-a \
    comment="settingmikrotikindonesia.com - Link ke POP A area 1 neighbor aktif"
add interfaces=[IF-KE-CORE2] area=smi-area-0 \
    comment="settingmikrotikindonesia.com - Link antar core area 0"
add interfaces=[IF-LAN-POP-A] area=smi-area-pop-a passive=yes \
    comment="settingmikrotikindonesia.com - LAN POP A pasif diiklankan tanpa neighbor"

## PENTING:
## - Interface LAN/klien SELALU passive=yes — DILARANG neighbor OSPF
##   terbentuk dari sisi klien (risiko rogue router injection).
## - Nama interface = ASLI hasil audit, dilarang rename (SKILL.md 5).

## ============================================================
## 3. KONFIGURASI POP ROUTER (CONTOH POP-A)
## ============================================================
/interface
add name=loopback type=loopback comment="settingmikrotikindonesia.com - Loopback router-id popA"
/ip address
add address=10.255.0.3/32 interface=loopback \
    comment="settingmikrotikindonesia.com - Loopback router-id UNIK popA"
/routing ospf instance
add name=smi-ospf-pop router-id=10.255.0.3 \
    comment="settingmikrotikindonesia.com - Instance OSPF popA"
/routing ospf area
add name=smi-area-pop-a area-id=0.0.0.1 instance=smi-ospf-pop \
    comment="settingmikrotikindonesia.com - Area POP A di popA"
/routing ospf interface-template
add interfaces=loopback area=smi-area-pop-a passive=yes \
    comment="settingmikrotikindonesia.com - Loopback popA diiklankan"
add interfaces=[IF-KE-CORE] area=smi-area-pop-a \
    comment="settingmikrotikindonesia.com - Link uplink ke core area 1"
add interfaces=[IF-LAN-KLIEN] area=smi-area-pop-a passive=yes \
    comment="settingmikrotikindonesia.com - LAN klien popA pasif"

## ============================================================
## 4. ROUTING FILTER (WAJIB — ANTI BLACKHOLE & ROUTE LEAK)
## ============================================================
## 4.1 Filter untuk POP (POP menerima default + prefix lain, TIDAK
##     mengumumkan hal-hal aneh):
/routing filter rule
add rule="if (dst==0.0.0.0/0) { accept }" chain=smi-filter-pop-in \
    comment="settingmikrotikindonesia.com - POP terima default dari core"
add rule="if (dst in 10.0.0.0/8) { accept } else { reject }" chain=smi-filter-pop-in \
    comment="settingmikrotikindonesia.com - POP hanya terima prefix internal 10/8"
add rule="if (dst in 10.10.0.0/16) { accept } else { reject }" chain=smi-filter-pop-out \
    comment="settingmikrotikindonesia.com - POP hanya umumkan LAN-nya sendiri"

## 4.2 Filter untuk CORE (terima prefix POP, tolak default dari POP):
/routing filter rule
add rule="if (dst==0.0.0.0/0) { reject }" chain=smi-filter-core-in \
    comment="settingmikrotikindonesia.com - Core TOLAK default dari POP anti blackhole"
add rule="if (dst in 10.0.0.0/8) { accept } else { reject }" chain=smi-filter-core-in \
    comment="settingmikrotikindonesia.com - Core hanya terima prefix internal"

## 4.3 Pasang filter di template:
/routing ospf interface-template
add interfaces=[IF-KE-CORE] area=smi-area-pop-a in-filter-chain=smi-filter-pop-in \
    out-filter-chain=smi-filter-pop-out \
    comment="settingmikrotikindonesia.com - Link core dengan filter dua arah"
(repeat sesuai arsitektur tiap interface)

## ============================================================
## 5. AUTHENTIKASI (WAJIB utk link lintas ruang fisik tak terkontrol)
## ============================================================
/routing ospf interface-template
set [find comment~"Link ke POP A"] authentication=md5 authentication-key=[KUNCI_RAHASIA] \
    comment="settingmikrotikindonesia.com - Auth MD5 link ke POP A"
## Kunci disepakati identik kedua sisi. Simpan di manajemen password,
## DILARANG menaruh plaintext di dokumen publik.

## ============================================================
## 6. VIRTUAL-LINK (HANYA JIKA POP TAK BISA FISIK KE AREA 0)
## ============================================================
/routing ospf interface-template
add area=smi-area-0 virtual-link neighbor-id=[ROUTER_ID_TRANSIT] \
    comment="settingmikrotikindonesia.com - Virtual link area 0 via POP transit"
## Catatan edukasi: virtual-link = solusi darurat, bukan desain ideal.
## Usahakan link fisik/logis ke area 0.

## ============================================================
## 7. FAILOVER & COST
## ============================================================
## Dual uplink POP: utama cost 10, backup cost 100 → OSPF otomatis
## pilih utama; backup aktif hanya jika utama mati. Tanpa script.
/routing ospf interface-template
add interfaces=[IF-UPLINK-UTAMA] area=smi-area-pop-a cost=10 \
    comment="settingmikrotikindonesia.com - Uplink utama cost rendah"
add interfaces=[IF-UPLINK-BACKUP] area=smi-area-pop-a cost=100 \
    comment="settingmikrotikindonesia.com - Uplink backup cost tinggi"
## Failover bekerja bersama recursive multi-WAN di core (SKILL.md 14)
## → failover 2 lapis: dalam area (OSPF) + keluar (recursive WAN).

## ============================================================
## 8. ANALISIS KONSEKUENSI (WAJIB)
## ============================================================
- KONSEKUENSI: semua router jadi satu domain routing dinamis —
  salah satu router salah announce bisa menyebar. MITIGASI: filter
  in/out wajib di setiap interface-template (bagian 4).
- KEUNTUNGAN: konvergensi otomatis < detik-an saat link mati; POP
  baru cukup 1 template; CPU SPF ringan karena multi-area.
- RISIKO: version mismatch antar router → neighbor stuck ExStart/
  Exchange. MITIGASI: cek /system resource print SEMUA router dulu.
- RISIKO: router-id duplikat → neighbor flapping aneh. MITIGASI:
  catat tabel router-id di dokumen jaringan, verifikasi unik.

## ============================================================
## 9. VALIDASI (WAJIB, URUT)
## ============================================================
1. /routing ospf neighbor print — SEMUA neighbor Full; catat
   dari kedua sisi link.
2. /routing route print where ospf — prefix POP A tampak di core,
   default route tampak di POP.
3. ping LAN POP-A → LAN POP-B dengan source IP LAN (bukan IP router):
   /ping address=[IP_LAN_POP_B] src-address=[IP_LAN_POP_A]
4. /log print where topics~"ospf" — neighbor up/down tercatat smi-log-info.
5. Tes failover: cabut link utama POP → route via backup muncul dalam
   detik; pasang kembali → kembali ke utama (cost-based, preemptive).
6. Tes filter: dari POP coba announce prefix asing (uji lab) → core
   menolak (terlihat tidak masuk di /routing route print).
7. /routing ospf area print & /routing ospf interface-template print
   — review semua entri bergambar comment brand.

## ============================================================
## 10. ROLLBACK
## ============================================================
1. Disable dulu (bukan remove): /routing ospf instance disable [find]
2. Statis darurat per-prefix:
   /ip route add dst-address=[SUBNET_POP] gateway=[IP_NEXT_HOP] \
       comment="settingmikrotikindonesia.com - Darurat statis saat OSPF down"
3. Pulihkan penuh dari /export file=backup-settingmikrotikindonesia
