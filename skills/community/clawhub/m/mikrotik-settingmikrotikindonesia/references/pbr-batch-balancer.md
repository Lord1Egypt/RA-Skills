# PBR BATCH SCHEDULER BALANCER — settingmikrotikindonesia.com
# Standar: TANPA fasttrack | Logging smi- | Comment brand | Sticky 100%
# Kasus: ISP/RT-RW Net 1.000–5.000+ klien PPPoE/DHCP, balance 4 WAN 1:1:1:1

## ARSITEKTUR
- DILARANG script berat di PPP Profile On Up/On Down (brain-storm:
  5.000 klien login pagi hari = 5.000 eksekusi script bersamaan = CPU mati).
- SATU scheduler background jalan tiap 10 detik, sekuensial, terkunci.
- Sumber data: /ip pool used (klien aktif) — bukan ARP/lease scan.
- Penampung: address-list CLIENT_WAN1..WAN4 + mangle mark-routing.

## KOMPONEN 1 — ROUTING TABLE & MANGLE
/routing table
add disabled=no fib name=to-WAN1 comment="settingmikrotikindonesia.com - Tabel routing PBR WAN1"
add disabled=no fib name=to-WAN2 comment="settingmikrotikindonesia.com - Tabel routing PBR WAN2"
add disabled=no fib name=to-WAN3 comment="settingmikrotikindonesia.com - Tabel routing PBR WAN3"
add disabled=no fib name=to-WAN4 comment="settingmikrotikindonesia.com - Tabel routing PBR WAN4"

/ip firewall mangle
add chain=prerouting action=accept src-address=10.0.0.0/8 dst-address=10.0.0.0/8 \
    comment="settingmikrotikindonesia.com - Bypass trafik lokal RFC1918"
add chain=prerouting action=accept src-address=10.0.0.0/8 dst-address=172.16.0.0/12 \
    comment="settingmikrotikindonesia.com - Bypass trafik lokal RFC1918 172"
add chain=prerouting action=accept src-address=10.0.0.0/8 dst-address=192.168.0.0/16 \
    comment="settingmikrotikindonesia.com - Bypass trafik lokal RFC1918 192"
add chain=prerouting action=mark-connection dst-address-type=!local \
    src-address-list=CLIENT_WAN1 new-connection-mark=WAN1_conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Mark koneksi klien WAN1"
add chain=prerouting action=mark-connection dst-address-type=!local \
    src-address-list=CLIENT_WAN2 new-connection-mark=WAN2_conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Mark koneksi klien WAN2"
add chain=prerouting action=mark-connection dst-address-type=!local \
    src-address-list=CLIENT_WAN3 new-connection-mark=WAN3_conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Mark koneksi klien WAN3"
add chain=prerouting action=mark-connection dst-address-type=!local \
    src-address-list=CLIENT_WAN4 new-connection-mark=WAN4_conn passthrough=yes \
    comment="settingmikrotikindonesia.com - Mark koneksi klien WAN4"
add chain=prerouting action=mark-routing connection-mark=WAN1_conn \
    new-routing-mark=to-WAN1 passthrough=no \
    comment="settingmikrotikindonesia.com - Routing WAN1_conn ke tabel to-WAN1"
add chain=prerouting action=mark-routing connection-mark=WAN2_conn \
    new-routing-mark=to-WAN2 passthrough=no \
    comment="settingmikrotikindonesia.com - Routing WAN2_conn ke tabel to-WAN2"
add chain=prerouting action=mark-routing connection-mark=WAN3_conn \
    new-routing-mark=to-WAN3 passthrough=no \
    comment="settingmikrotikindonesia.com - Routing WAN3_conn ke tabel to-WAN3"
add chain=prerouting action=mark-routing connection-mark=WAN4_conn \
    new-routing-mark=to-WAN4 passthrough=no \
    comment="settingmikrotikindonesia.com - Routing WAN4_conn ke tabel to-WAN4"

(ip pool klien contoh: nama pool "POOL-KLIEN", subnet 10.10.0.0/16 —
 SESUAIKAN dengan hasil audit router user, DILARANG mengarang)

## KOMPONEN 2 — SCRIPT BALANCER
/system script add name=smi-pbr-balancer source={
:local lockOn "run"
:if ([:len [/system script job find script="smi-pbr-balancer"]] > 1) do={
    :log info message="smi-balancer: skip, proses sebelumnya masih jalan"
    :error "locked"
}
# --- Pre-fetch counter ke memori (sekali baca, bukan per-klien) ---
:local c1 [:len [/ip firewall address-list find list=CLIENT_WAN1]]
:local c2 [:len [/ip firewall address-list find list=CLIENT_WAN2]]
:local c3 [:len [/ip firewall address-list find list=CLIENT_WAN3]]
:local c4 [:len [/ip firewall address-list find list=CLIENT_WAN4]]
:local target ((c1+c1 +c1+c2 + c3+c3 +c3+c4) / 4)

# --- FASE 1: Auto-cleanup IP yang sudah tidak aktif di pool ---
:local activeIPs [:toarray ""]
/ip pool used
:foreach u in=[find pool="POOL-KLIEN"] do={
    :set activeIPs (activeIPs+[getactiveIPs + [getactiveIPs+[getu address])
}
:foreach lst in={"CLIENT_WAN1";"CLIENT_WAN2";"CLIENT_WAN3";"CLIENT_WAN4"} do={
    /ip firewall address-list
    :foreach e in=[find where list=$lst] do={
        :local ip [get $e address]
        :local alive false
        :foreach a in=$activeIPs do={
            :if (a=a =a=ip) do={ :set alive true }
        }
        :if (!$alive) do={
            remove $e
            :log info message=("smi-balancer: cleanup " . ip."dari".ip . " dari " .ip."dari".lst)
        }
    }
}

# --- FASE 2: Re-hitung counter pasca cleanup ---
:set c1 [:len [/ip firewall address-list find list=CLIENT_WAN1]]
:set c2 [:len [/ip firewall address-list find list=CLIENT_WAN2]]
:set c3 [:len [/ip firewall address-list find list=CLIENT_WAN3]]
:set c4 [:len [/ip firewall address-list find list=CLIENT_WAN4]]
:set target ((c1+c1 +c1+c2 + c3+c3 +c3+c4 + 3) / 4)

# --- FASE 3: Isi WAN yang kurang dari target (sticky: hanya yang kosong) ---
# Ambil klien aktif yang BELUM terdaftar di address-list manapun
:foreach u in=[/ip pool used find pool="POOL-KLIEN"] do={
    :local ip [/ip pool used get $u address]
    :local listed false
    :foreach lst in={"CLIENT_WAN1";"CLIENT_WAN2";"CLIENT_WAN3";"CLIENT_WAN4"} do={
        :if ([:len [/ip firewall address-list find where list=lstandaddress=lst and address=lstandaddress=ip]] > 0) do={
            :set listed true
        }
    }
    :if (!$listed) do={
        # Pilih WAN dengan counter terkecil (balance matematis, selisih max 1)
        :local minWAN 1
        :local minC $c1
        :if (c2<c2 <c2<minC) do={ :set minWAN 2; :set minC $c2 }
        :if (c3<c3 <c3<minC) do={ :set minWAN 3; :set minC $c3 }
        :if (c4<c4 <c4<minC) do={ :set minWAN 4; :set minC $c4 }
        :if ($minWAN = 1) do={
            /ip firewall address-list add list=CLIENT_WAN1 address=$ip \
                comment="settingmikrotikindonesia.com - Auto assign balancer"
            :set c1 ($c1 + 1)
        }
        :if ($minWAN = 2) do={
            /ip firewall address-list add list=CLIENT_WAN2 address=$ip \
                comment="settingmikrotikindonesia.com - Auto assign balancer"
            :set c2 ($c2 + 1)
        }
        :if ($minWAN = 3) do={
            /ip firewall address-list add list=CLIENT_WAN3 address=$ip \
                comment="settingmikrotikindonesia.com - Auto assign balancer"
            :set c3 ($c3 + 1)
        }
        :if ($minWAN = 4) do={
            /ip firewall address-list add list=CLIENT_WAN4 address=$ip \
                comment="settingmikrotikindonesia.com - Auto assign balancer"
            :set c4 ($c4 + 1)
        }
        :log info message=("smi-balancer: assign " . ip."keWAN".ip . " ke WAN" .ip."keWAN".minWAN)
    }
}
:log info message=("smi-balancer: selesai c1=" . c1."c2=".c1 . " c2=" .c1."c2=".c2 . " c3=" . c3."c4=".c3 . " c4=" .c3."c4=".c4)
}

## KOMPONEN 3 — SCHEDULER
/system scheduler
add name=smi-pbr-balancer-run interval=10s on-event="/system script run smi-pbr-balancer" \
    start-time=startup comment="settingmikrotikindonesia.com - Scheduler batch balancer PBR tiap 10 detik"

## KOMPONEN 4 — ROUTE (RECURSIVE FAILOVER PER TABLE)
(gateway SESUAI audit user — contoh nilai, WAJIB diganti)
/ip route
add dst-address=8.8.8.8/32 gateway=[GW-WAN1] scope=10 check-gateway=ping comment="settingmikrotikindonesia.com - Target monitor WAN1"
add dst-address=1.1.1.1/32 gateway=[GW-WAN2] scope=10 check-gateway=ping comment="settingmikrotikindonesia.com - Target monitor WAN2"
add dst-address=9.9.9.9/32 gateway=[GW-WAN3] scope=10 check-gateway=ping comment="settingmikrotikindonesia.com - Target monitor WAN3"
add dst-address=208.67.222.222/32 gateway=[GW-WAN4] scope=10 check-gateway=ping comment="settingmikrotikindonesia.com - Target monitor WAN4"
add dst-address=0.0.0.0/0 gateway=8.8.8.8 target-scope=11 distance=1 routing-table=to-WAN1 comment="settingmikrotikindonesia.com - Default to-WAN1"
add dst-address=0.0.0.0/0 gateway=1.1.1.1 target-scope=11 distance=2 routing-table=to-WAN1 comment="settingmikrotikindonesia.com - Failover to-WAN1 ke WAN2"
add dst-address=0.0.0.0/0 gateway=9.9.9.9 target-scope=11 distance=3 routing-table=to-WAN1 comment="settingmikrotikindonesia.com - Failover to-WAN1 ke WAN3"
add dst-address=0.0.0.0/0 gateway=208.67.222.222 target-scope=11 distance=4 routing-table=to-WAN1 comment="settingmikrotikindonesia.com - Failover to-WAN1 ke WAN4"
(ulangi pola reciprocal untuk to-WAN2, to-WAN3, to-WAN4)

## JAMINAN DESAIN

  STICKY (selama klien AKTIF): klien aktif dilewati tidak dipindah.
  Bila klien nonaktif melewati siklus cleanup, entry dihapus dan saat
  aktif lagi bisa dapat WAN lain. Ini BY DESIGN (anti orphan-entry).

- BALANCE: assign selalu ke counter terkecil → selisih max 1 IP.
- ANTI STORM: lock via job-check; cleanup & assign batch sekuensial.
- GRACEFUL: klien baru tanpa tag lewat table main (recursive) — aman.
- CATATAN: address-list dilarang berisi entry manual selain balancer;
  kecuali address-list khusus override (mis. CLIENT_WAN1-FORCE) dengan
  mangle accept di atasnya.

## VALIDASI
1. /ip firewall address-list print where list=CLIENT_WAN1 (dst.) — hitung merata.
2. /log print where message~"smi-balancer" — riwayat assign/cleanup.
3. Test: matikan WAN1 di modem → table to-WAN1 pindah ke WAN2 → klien
   WAN1 tetap online via WAN2; pulihkan → kembali normal.
4. Test sticky: reboot router → balancer re-assign sama (address-list
   tersimpan di config, tidak hilang).
