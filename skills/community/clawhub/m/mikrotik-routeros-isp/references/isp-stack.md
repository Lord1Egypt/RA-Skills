# ISP Stack Reference — OLT → MikroTik → RADIUS

Full end-to-end configuration for a FTTH ISP using VSOL OLT + MikroTik PPPoE concentrator + MK-Auth RADIUS.

---

## Architecture

```
[ONT/CPE] ─── GPON ──→ [VSOL OLT]
                           │ VLAN 500–507 per PON port (tagged)
                           ▼
                    [MikroTik RB4011 / CCR]
                    PPPoE Server (per VLAN)
                    CGNAT Pool: 100.64.0.0/10
                    RADIUS → MK-Auth
                           │ SNAT via loopback
                           ▼
                    [MikroTik CCR1009]
                    Border / BGP / Transit
```

---

## MikroTik — VLAN Bridge Setup (per PON port)

```routeros
# Bridge for upstream (trunk)
/interface bridge add name=br-uplink

# VLAN interfaces per PON port
/interface vlan add name=vlan500 vlan-id=500 interface=ether2-olt comment="PON1"
/interface vlan add name=vlan501 vlan-id=501 interface=ether2-olt comment="PON2"
# ... repeat for 502–507

# PPPoE server on each VLAN
/interface pppoe-server server
add name=pppoe-pon1 interface=vlan500 service-name=internet authentication=pap,chap disabled=no
add name=pppoe-pon2 interface=vlan501 service-name=internet authentication=pap,chap disabled=no
```

---

## MikroTik — RADIUS (MK-Auth)

```routeros
/radius
add address=<mkauth-ip> secret=<shared-secret> service=ppp timeout=3000ms

/ppp profile
set default use-radius=yes

/ppp aaa
set use-interim-update=yes interim-update=5m
```

---

## MikroTik — CGNAT Pool

```routeros
/ip pool
add name=cgnat-pool ranges=100.65.62.0-100.65.63.255

/ppp profile
set default local-address=100.64.0.1 remote-address=cgnat-pool
```

---

## MikroTik — SNAT via Loopback (CCR1009)

```routeros
# Loopback IPs (one per CCR for SNAT source)
/ip address add address=10.255.0.1/32 interface=lo comment="SNAT-1"
/ip address add address=10.255.0.2/32 interface=lo comment="SNAT-2"

# SNAT rule on CCR border
/ip firewall nat
add chain=srcnat src-address=100.64.0.0/10 \
    action=src-nat to-addresses=10.255.0.1 \
    out-interface=ether1-transit comment="CGNAT SNAT"
```

---

## GenieACS / TR-069 Integration

- GenieACS runs on `<server>:7547` (CWMP) and `<server>:3000` (UI)
- CPEs must have ACS URL set to `http://<genieacs-ip>:7547`
- MikroTik can provision via `/tool fetch` or TR-069 on supported models

---

## MK-Auth Integration Notes

- MK-Auth runs PPPoE + Hotspot RADIUS
- Default RADIUS port: 1812 (auth) / 1813 (acct)
- Shared secret configured in MK-Auth → Configurações → RADIUS
- User plans map to MK-Auth "planos" with speed limits pushed via RADIUS attributes (Mikrotik-Rate-Limit)

---

## Dual-WAN Load Balance — PCC (Per-Connection Classifier)

Distribui conexões entre dois links simultaneamente (não é failover — é load balance real).
Usa `per-connection-classifier=src-address:2/0` e `2/1` para dividir tráfego pelo IP de origem.

```routeros
# Interface lists para WAN
/interface list
add name=wan comment=wan
/interface list member
add list=wan interface=ether1
add list=wan interface=ether2

# Address lists
/ip firewall address-list
add address=10.0.0.0/8 list=private
add address=100.64.0.0/10 list=private
add address=192.168.0.0/16 list=private
add address=172.16.0.0/12 list=private
add address=192.168.88.0/24 list=lan

# Firewall filter — FastTrack conexões estabelecidas
/ip firewall filter
add chain=input connection-state=invalid action=drop
add chain=forward connection-state=invalid action=drop
add chain=forward connection-state=established,related connection-mark=no-mark action=fasttrack-connection
add chain=forward connection-state=established,related connection-mark=no-mark action=accept
add chain=output connection-state=invalid action=drop

# NAT — masquerade saindo pelas WAN
/ip firewall nat
add chain=srcnat src-address-list=private dst-address=!private out-interface-list=wan action=masquerade

# Mangle — marcar conexões por interface de entrada (retorno de tráfego)
/ip firewall mangle
add chain=prerouting in-interface=ether1 connection-mark=no-mark \
    new-connection-mark=mark-connection-ether1 action=mark-connection passthrough=yes
add chain=prerouting in-interface=ether2 connection-mark=no-mark \
    new-connection-mark=mark-connection-ether2 action=mark-connection passthrough=yes

# Forçar IPs específicos em uma interface (opcional)
add chain=prerouting connection-mark=no-mark new-connection-mark=mark-connection-ether1 \
    passthrough=yes src-address-list=force-ether1 action=mark-connection
add chain=prerouting connection-mark=no-mark dst-address-list=force-ether1 \
    new-connection-mark=mark-connection-ether1 passthrough=yes action=mark-connection
add chain=prerouting connection-mark=no-mark new-connection-mark=mark-connection-ether2 \
    passthrough=yes src-address-list=force-ether2 action=mark-connection
add chain=prerouting connection-mark=no-mark dst-address-list=force-ether2 \
    new-connection-mark=mark-connection-ether2 passthrough=yes action=mark-connection

# PCC — divide tráfego LAN entre as duas interfaces (50/50 por IP de origem)
add chain=prerouting comment=PCC connection-mark=no-mark src-address-list=private \
    dst-address-list=!private dst-address-type=!local in-interface-list=lan \
    new-connection-mark=mark-connection-ether1 passthrough=yes \
    per-connection-classifier=src-address:2/0 src-address-list=lan action=mark-connection
add chain=prerouting comment=PCC connection-mark=no-mark src-address-list=private \
    dst-address-list=!private dst-address-type=!local in-interface-list=lan \
    new-connection-mark=mark-connection-ether2 passthrough=yes \
    per-connection-classifier=src-address:2/1 src-address-list=lan action=mark-connection

# Routing marks por conexão marcada
add chain=prerouting connection-mark=mark-connection-ether1 in-interface-list=lan \
    new-routing-mark=mark-routing-ether1 passthrough=yes action=mark-routing
add chain=prerouting connection-mark=mark-connection-ether2 in-interface-list=lan \
    new-routing-mark=mark-routing-ether2 passthrough=yes action=mark-routing
add chain=output connection-mark=mark-connection-ether1 \
    new-routing-mark=mark-routing-ether1 action=mark-routing passthrough=yes
add chain=output connection-mark=mark-connection-ether2 \
    new-routing-mark=mark-routing-ether2 action=mark-routing passthrough=yes

# RAW — bloqueia portas de ataque comuns na WAN
/ip firewall raw
add chain=prerouting in-interface-list=!wan protocol=tcp action=drop dst-port=25
add chain=prerouting in-interface-list=wan protocol=udp action=drop dst-port=1-1024,3389
add chain=prerouting in-interface-list=wan protocol=tcp action=drop \
    dst-port=1-1024,1900,2049,3389,5353
```

> **Nota:** Requer rotas estáticas por routing-mark:
> ```routeros
> /ip route add dst-address=0.0.0.0/0 gateway=<gw-ether1> routing-table=mark-routing-ether1
> /ip route add dst-address=0.0.0.0/0 gateway=<gw-ether2> routing-table=mark-routing-ether2
> ```

---

## OSPF Watchdog — Reinicia OSPF quando rota default some

Script pra detectar quando a rota default OSPF desaparece e reiniciar o processo automaticamente + alertar via Telegram.

```routeros
/system script add name=ospf-watchdog source={
  :local HOSTNAME ([/system identity get name])
  :if ([/ip route print count-only where dst-address=0.0.0.0/0 ospf]=0) do={
    /routing ospf instance set 0 disabled=yes
    /routing ospf instance set 0 disabled=no
    /log error "$HOSTNAME NO OSPF"
    :delay 4000ms
    /tool fetch url=("https://api.telegram.org/bot" . $BOT_ID . \
      "/sendMessage?chat_id=" . $CHAT_ID . \
      "&text=" . $HOSTNAME . " NO OSPF, OSPF RESTARTING") keep-result=no
  }
}

# Rodar a cada 1 minuto
/system scheduler add name=ospf-watchdog interval=1m \
  on-event="/system script run ospf-watchdog" start-time=startup
```

> Para RouterOS v7, trocar `/routing ospf instance set 0` por:
> `/routing ospf instance set ospf-main disabled=yes` (use o nome da instância)


