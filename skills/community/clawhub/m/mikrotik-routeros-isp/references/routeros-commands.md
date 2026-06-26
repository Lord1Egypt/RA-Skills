# RouterOS Command Reference
> Source: https://help.mikrotik.com/docs — RouterOS official documentation

## Table of Contents
1. [System & Diagnostics](#1-system--diagnostics)
2. [Interfaces & Bridge](#2-interfaces--bridge)
3. [IP Routing](#3-ip-routing)
4. [Firewall — Filter](#4-firewall--filter)
5. [Firewall — NAT](#5-firewall--nat)
6. [Firewall — Mangle](#6-firewall--mangle)
7. [PPPoE Server & PPP AAA](#7-pppoe-server--ppp-aaa)
8. [DHCP](#8-dhcp)
9. [Queues & QoS](#9-queues--qos)
10. [OSPF (v7)](#10-ospf-v7)
11. [BGP (v7)](#11-bgp-v7)
12. [VRRP](#12-vrrp)
13. [Scripting](#13-scripting)
14. [User & Services](#14-user--services)

---

## 1. System & Diagnostics

```routeros
/system resource print
/system identity print
/system identity set name="router-01"
/system routerboard print
/system clock print
/system backup save name=pre-change
/export compact
/export file=config-backup
/log print
/log print where topics~"error"
/log print where topics~"pppoe"
/ip neighbor print
/ip arp print
/tool ping 8.8.8.8 count=5
/tool traceroute 8.8.8.8
/tool bandwidth-test address=<ip> direction=both
/tool torch interface=ether1
/tool sniffer quick interface=ether1 ip-address=1.2.3.4
```

---

## 2. Interfaces & Bridge

```routeros
/interface print stats
/interface ethernet set ether1 speed=1Gbps full-duplex=yes

# VLANs
/interface vlan add name=vlan500 vlan-id=500 interface=ether2

# Bridge
/interface bridge add name=br-wan protocol-mode=rstp
/interface bridge port add bridge=br-wan interface=ether2

# IMPORTANT: Simple Queues / Queue Trees on bridged/VLAN/PPPoE traffic
# require these settings (disabled by default):
/interface bridge settings set use-ip-firewall=yes
/interface bridge settings set use-ip-firewall-for-vlan=yes
/interface bridge settings set use-ip-firewall-for-pppoe=yes
# Without this, bridge traffic bypasses postrouting -> queues won't work

# Bonding
/interface bonding add slaves=ether1,ether2 mode=802.3ad name=bond0

# PPPoE client (WAN uplink to ISP)
/interface pppoe-client add name=pppoe-wan interface=ether1 \
    user=user@isp password=pass add-default-route=yes use-peer-dns=yes disabled=no
# After connecting, WAN = pppoe-wan (not ether1)
```

---

## 3. IP Routing

```routeros
/ip address print
/ip address add address=192.168.1.1/24 interface=ether1
/ip address remove [find interface=ether2]

/ip route print
# Flags: D=dynamic A=active C=connect S=static b=bgp o=ospf d=dhcp
# ECMP: multiple routes same dst, flagged with +

/ip route add dst-address=0.0.0.0/0 gateway=1.2.3.1
/ip route add dst-address=10.0.0.0/8 gateway=192.168.1.254 distance=10

# v7: /routing/route shows all address families + filtered routes
/routing route print
/routing route print detail where dst-address=0.0.0.0/0
```

---

## 4. Firewall — Filter

> Chains: input (->router), forward (through router), output (from router)
> Best practice: accept established/related FIRST to offload CPU

```routeros
/ip firewall filter print

# Protect router (input chain)
/ip firewall address-list add list=mgmt address=10.0.0.0/8
/ip firewall filter
add chain=input connection-state=established,related action=accept
add chain=input connection-state=invalid action=drop
add chain=input src-address-list=mgmt action=accept
add chain=input protocol=icmp action=accept
add chain=input action=drop

# RFC6890 not-in-internet list (for forward chain protection)
/ip firewall address-list
add list=not_in_internet address=10.0.0.0/8 comment=RFC6890
add list=not_in_internet address=172.16.0.0/12 comment=RFC6890
add list=not_in_internet address=192.168.0.0/16 comment=RFC6890
add list=not_in_internet address=100.64.0.0/10 comment="CGNAT RFC6890"
add list=not_in_internet address=169.254.0.0/16 comment=RFC6890
add list=not_in_internet address=0.0.0.0/8 comment=RFC6890
add list=not_in_internet address=224.0.0.0/4 comment=Multicast
add list=not_in_internet address=240.0.0.0/4 comment=RFC6890

# Protect LAN clients (forward chain)
/ip firewall filter
add chain=forward action=fasttrack-connection connection-state=established,related
add chain=forward action=accept connection-state=established,related
add chain=forward action=drop connection-state=invalid log=yes log-prefix=invalid
add chain=forward action=drop dst-address-list=not_in_internet \
    in-interface=br-lan out-interface=!br-lan log=yes log-prefix="!public_from_LAN"
add chain=forward action=drop connection-nat-state=!dstnat \
    connection-state=new in-interface=ether1-wan log=yes log-prefix="!NAT"
add chain=forward action=drop in-interface=ether1-wan \
    src-address-list=not_in_internet log=yes log-prefix="!public"
```

---

## 5. Firewall — NAT

> masquerade: dynamic public IP (PPPoE/DHCP WAN). Clears conntrack on reconnect.
> src-nat: static public IP. Conntrack survives link failure (better for stable links).
> ALWAYS clear conntrack after NAT changes: /ip firewall connection remove [find]

```routeros
/ip firewall nat print

# Masquerade (dynamic — ISP PPPoE)
/ip firewall nat add chain=srcnat out-interface=pppoe-wan action=masquerade

# SNAT via loopback (CGNAT, static)
/ip firewall nat add chain=srcnat src-address=100.64.0.0/10 \
    action=src-nat to-addresses=<loopback-ip> out-interface=ether1-wan

# Port forward
/ip firewall nat add chain=dstnat protocol=tcp dst-port=3389 \
    in-interface=ether1-wan action=dst-nat to-addresses=192.168.1.10

# DNS redirect (force all DNS through router)
/ip firewall nat add chain=dstnat dst-port=53 protocol=tcp action=redirect to-ports=53
/ip firewall nat add chain=dstnat dst-port=53 protocol=udp action=redirect to-ports=53

# Clear connection tracking (after rule changes)
/ip firewall connection remove [find]
```

---

## 6. Firewall — Mangle

> Max 4096 unique packet marks. Exceeding -> error "bad new packet mark"
> MSS clamping is REQUIRED for PPPoE (MTU=1492 < ethernet 1500)

```routeros
/ip firewall mangle print

# MSS clamp for PPPoE (mandatory)
/ip firewall mangle add chain=forward out-interface=pppoe-wan protocol=tcp \
    tcp-flags=syn tcp-mss=1301-65535 action=change-mss new-mss=1300

# Connection + packet mark for queues (efficient: only inspects new connections)
/ip firewall mangle
add chain=forward in-interface=br-lan src-address=192.168.1.100 \
    connection-state=new action=mark-connection new-connection-mark=client_conn
add chain=forward connection-mark=client_conn \
    action=mark-packet new-packet-mark=client_p
```

---

## 7. PPPoE Server & PPP AAA

> RFC 2516. Handshake: PADI -> PADO -> PADR -> PADS -> session established.
> Do NOT assign DHCP or static IPs on same interface as PPPoE server.
> RADIUS attributes override profile. Missing attributes fall back to profile.
> Mikrotik-Rate-Limit RADIUS attribute applies speed limits per user.

```routeros
# PPPoE server (one per VLAN/interface)
/interface pppoe-server server
add service-name=internet interface=vlan500 authentication=pap,chap disabled=no
add service-name=internet interface=vlan501 authentication=pap,chap disabled=no

# PPP profile
/ppp profile
add name=plano-50M local-address=100.64.0.1 remote-address=cgnat-pool \
    rate-limit=50M/50M use-radius=yes

# IP pool for CGNAT
/ip pool add name=cgnat-pool ranges=100.65.62.0-100.65.63.255

# PPP secrets (local, optional when RADIUS active)
/ppp secret add name=user01 password=pass service=pppoe profile=plano-50M

# Active sessions
/ppp active print
/ppp active print count-only

# RADIUS
/radius add address=<mkauth-ip> secret=<secret> service=ppp timeout=3s
/ppp aaa set use-interim-update=yes interim-update=5m
# interim-update sends accounting packets to MK-Auth every 5 min
```

---

## 8. DHCP

```routeros
/ip dhcp-server lease print
/ip dhcp-server lease print where address=192.168.1.50
/ip dhcp-server lease make-static [find address=192.168.1.50]
/ip pool add name=dhcp-pool ranges=192.168.1.100-192.168.1.200
/ip dhcp-server add name=dhcp1 interface=br-lan address-pool=dhcp-pool lease-time=1h
/ip dhcp-server network add address=192.168.1.0/24 \
    gateway=192.168.1.1 dns-server=8.8.8.8,1.1.1.1
```

---

## 9. Queues & QoS

> Simple Queues / Queue Trees work in postrouting chain.
> Bridge traffic: MUST enable use-ip-firewall=yes on bridge (see section 2).

```routeros
# Simple queue (rate limit per IP)
/queue simple add name=cliente-01 target=192.168.1.100 max-limit=10M/10M
/queue simple set [find name=cliente-01] max-limit=20M/20M

# Queue Tree (per packet-mark, from mangle)
/queue tree add name=dl-cliente parent=global packet-mark=client_p max-limit=50M

/queue type print
```

---

## 10. OSPF (v7)

> v7 filter syntax: script-like "if...then". Default chain action = reject.
> originate-default=if-installed: advertise default only if present in routing table.
> OSPF is CPU/memory intensive — use areas and summarization on large networks.

```routeros
# Instance + Area
/routing ospf instance add name=ospf-main router-id=1.1.1.1
/routing ospf area add name=backbone area-id=0.0.0.0 instance=ospf-main
/routing ospf interface-template add area=backbone interfaces=ether1,ether2

# Status
/routing ospf neighbor print
/routing ospf lsa print

# Routing filter (v7 syntax)
/routing filter rule
add chain=ospf-out rule="if (dst in 192.168.0.0/16) { accept }"
add chain=ospf-in  rule="if (dst-len > 24) { reject } else { accept }"

# Redistribute default + static
/routing ospf instance set ospf-main \
    originate-default=if-installed redistribute=static
```

---

## 11. BGP (v7)

> v7 redesign: no /routing bgp instance or /routing bgp peer.
> Menus: /routing/bgp/template, /routing/bgp/connection, /routing/bgp/session
> peer-role is MANDATORY (ebgp or ibgp).
> input.accept-nlri: filter prefixes BEFORE storing in memory (reduces RAM usage).

```routeros
# Template (BGP params, reusable)
/routing bgp template set default as=65001 router-id=1.1.1.1

# Connection (per peer)
/routing bgp connection add name=transit \
    remote.address=1.2.3.4/32 remote.as=65000 local.role=ebgp template=default

# Memory-efficient input filter
/ip firewall address-list add list=bgp-prefixes address=0.0.0.0/0
/routing bgp template set default \
    input.filter=bgp-in \
    input.accept-nlri=bgp-prefixes

/routing filter rule
add chain=bgp-in rule="if (dst in 0.0.0.0/0) { accept } else { reject }"

# Session monitoring
/routing bgp session print
/routing stats process print interval=1

# v7 note: route visible in /routing/route, not only /ip/route
/routing route print where protocol=bgp
```

---

## 12. VRRP

```routeros
/interface vrrp add name=vrrp1 interface=ether1 vrid=1 priority=150
/interface vrrp set vrrp1 authentication=ah password=secret preemption-mode=yes
/ip address add address=192.168.1.1/24 interface=vrrp1  # virtual IP
/interface vrrp print
```

---

## 13. Scripting

> Full reference: https://help.mikrotik.com/docs/spaces/ROS/pages/139067404/Scripting+examples

```routeros
# Backup with date in name
/system script add name=backup-daily source={
    /system backup save name=("auto-" . [:pick [/system clock get date] 0 10])
}
/system scheduler add name=daily interval=1d on-event=backup-daily

# Detect PPPoE events via log buffer
/system logging action add name="pppoe-log"
/system logging add action=pppoe-log topics=pppoe,info,!ppp,!debug
# Then script checks if new log entry added to buffer

# Dynamic queue per active PPPoE session
:foreach s in=[/ppp active find] do={
    :local name [/ppp active get $s name]
    :local addr [/ppp active get $s address]
    :if ([:len [/queue simple find name=$name]] = 0) do={
        /queue simple add name=$name target=$addr max-limit=10M/10M
    }
}

# RADIUS IP resolver (run every 5 min)
/system scheduler add name=resolveRadius interval=5m on-event={
    :local resolved [resolve "mkauth.local"]
    /radius set [find service=ppp] address=$resolved
}

# Scripting basics
:local x 10
:if ($x > 5) do={ :log info "maior que 5" }
:foreach i in={1;2;3} do={ :log info ("item: " . $i) }
:local arr {a=1; b=2}; :put ($arr->"a")
```

---

## 14. User & Services

```routeros
/user add name=monit group=read password=senha
/user set admin password=nova-senha

# Restrict services to management subnet
/ip service set ssh    port=22   address=10.0.0.0/8
/ip service set winbox port=8291 address=10.0.0.0/8
/ip service disable telnet
/ip service disable ftp
/ip service disable api

# Harden SSH (use ed25519, enforce strong crypto)
/ip ssh set strong-crypto=yes host-key-type=ed25519

# Brute-force protection
/ip firewall filter add chain=input protocol=tcp dst-port=22 \
    connection-state=new src-address-list=!mgmt \
    action=add-src-to-address-list address-list=ssh-block \
    address-list-timeout=1h log=yes log-prefix="SSH-BLOCK"
/ip firewall filter add chain=input protocol=tcp dst-port=22 \
    src-address-list=ssh-block action=drop
```
