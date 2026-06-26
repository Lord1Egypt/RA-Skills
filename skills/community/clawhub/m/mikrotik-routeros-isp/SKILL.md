---
name: mikrotik-routeros-isp-br
description: >
  Expert-level management of MikroTik RouterOS devices and VSOL GPON OLTs via SSH or
  RouterOS API (port 8728/8729) and REST API (port 80/443).
  Use this skill whenever the user mentions MikroTik, RouterOS, RB, CCR, CRS, hAP,
  Winbox CLI, /ip route, /interface, /ppp, /queue, firewall rules, OSPF, BGP, VRRP,
  PPPoE, CGNAT, RADIUS, VLAN, OLT, GPON, ONT, PON port, or any ISP infrastructure task.
  Also triggers for: "show MikroTik routes", "configure PPPoE on RB4011",
  "check OLT uptime", "add firewall rule", "backup RouterOS config",
  "failover script", "notificação de link caído", "alerta Telegram MikroTik",
  "WhatsApp failover", "Evolution API RouterOS", "netwatch script",
  "script de failover com WhatsApp", "load balance actions",
  "conectar na API do MikroTik", "listar interfaces via API",
  "multi-device mikrotik", "TOOLS.md mikrotik",
  "netwatch-notify eworm", "backup upload mikrotik", "check-health routeros",
  "telegram-chat routeros", "dhcp-to-dns mikrotik", "eworm scripts routeros".
tags:
  - mikrotik
  - routeros
  - gpon
  - olt
  - isp
  - pppoe
  - cgnat
  - failover
  - api
requirements:
  binaries:
    - ssh
    - sshpass
  env:
    - MIKROTIK_HOST: "IP or hostname of the MikroTik device"
    - MIKROTIK_USER: "RouterOS username (default: admin)"
    - MIKROTIK_PASS: "(optional) password — prefer SSH key auth instead"
    - MIKROTIK_KEY: "(optional) path to SSH private key (default: ~/.ssh/mikrotik_key)"
    - OLT_HOST: "(optional) IP of VSOL/GPON OLT"
    - OLT_USER: "(optional) OLT SSH username"
    - OLT_PASS: "(optional) OLT SSH password"
security:
  credentials: >
    Prefer SSH key authentication over passwords. When password is needed,
    use MIKROTIK_PASS env var — never hardcode in scripts or TOOLS.md.
    Create a least-privilege management account on devices, not full admin.
  external_urls:
    - api.telegram.org — Telegram bot notifications (optional)
    - rsc.eworm.de — eworm RouterOS scripts (optional, audit before use)
    - Evolution API — WhatsApp notifications (optional, self-hosted)
---

# MikroTik RouterOS + VSOL OLT Skill

Expert-level management of MikroTik RouterOS devices and VSOL GPON OLTs.
Supports three access methods: **SSH CLI**, **RouterOS API (port 8728)**, and **REST API (port 443)**.
Covers ISP-grade infrastructure: PPPoE, CGNAT, RADIUS, VLAN, OSPF, BGP, VRRP, firewall,
queues, OLT/ONT provisioning, failover scripts, and WhatsApp/Telegram notifications.

---

## Access Method Selection

| Method | When to use | Port |
|--------|-------------|------|
| SSH CLI | Interactive config, scripts, export/import | 22 |
| RouterOS API | Automation, programmatic reads/writes, Python scripts | 8728/8729 |
| REST API | Modern ROS 7.1+, curl/HTTP clients, no extra library | 80/443 |

---

## Multi-Device Configuration

### Via TOOLS.md (recommended for multi-device setups)
Add to `~/.openclaw/workspace/TOOLS.md`:
```markdown
### MikroTik Devices
- **router1**: 192.168.88.1, admin, key:~/.ssh/mikrotik_key
- **router2**: 192.168.88.2, admin, key:~/.ssh/mikrotik_key
- **olt**: 192.168.88.3, admin, key:~/.ssh/olt_key
```
> **Security**: never store passwords in TOOLS.md. Use `key:<path>` for SSH key auth,
> or set `MIKROTIK_PASS` as an environment variable. Plaintext passwords in TOOLS.md
> expose credentials to any skill that reads that file.

### Via environment variables (single device)
```bash
export MIKROTIK_HOST=172.16.100.1
export MIKROTIK_USER=admin
export MIKROTIK_PASS=senha123
```

**Priority**: env vars > TOOLS.md > ask user

---

## Connection Methods

### SSH — preferred: key-based auth (no password in command line)
```bash
# Generate key once (on agent machine)
ssh-keygen -t ed25519 -f ~/.ssh/mikrotik_key -N ""

# Copy public key to router
ssh-copy-id -i ~/.ssh/mikrotik_key.pub admin@192.168.88.1
# Or paste manually: /user/ssh-keys/import public-key-file=key.pub user=admin

# Connect (no password exposure)
ssh -i ~/.ssh/mikrotik_key \
  -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 \
  admin@192.168.88.1 "/ip address print"
```

> If SSH key is not available, use password via env var only — never hardcode:
> ```bash
> sshpass -p "$MIKROTIK_PASS" ssh -o StrictHostKeyChecking=accept-new \
>   "$MIKROTIK_USER@$MIKROTIK_HOST" "/ip address print"
> ```

### RouterOS API (Python)
```bash
pip3 install --break-system-packages routeros-api
```
```python
import routeros_api, os

conn = routeros_api.RouterOsApiPool(
    host=os.getenv('MIKROTIK_HOST'),
    username=os.getenv('MIKROTIK_USER', 'admin'),
    password=os.getenv('MIKROTIK_PASS', ''),
    plaintext_login=True,  # Required for ROS 6.43+
    port=8728
)
api = conn.get_api()
resource = api.get_resource('/ip/address')
print(resource.get())
conn.disconnect()
```

### REST API (curl — ROS 7.1+)
```bash
# Use env vars — never hardcode credentials
curl -u "$MIKROTIK_USER:$MIKROTIK_PASS" \
  --cacert /path/to/router-cert.pem \
  https://$MIKROTIK_HOST/rest/ip/address

# Dev/lab only (skip cert verify):
curl -k -u "$MIKROTIK_USER:$MIKROTIK_PASS" https://$MIKROTIK_HOST/rest/ip/address
```

See `references/routeros-api.md` for complete API reference.

---

## Workflow (docs-first)

1. **Classify** — SSH task, API automation, or OLT work?
2. **Check references** — consult `references/` before acting
3. **Read before write** — always print/get current state first
4. **Confirm destructive ops** — show exact command, ask before remove/set/reboot
5. **Backup first** — `/system backup save` before major changes
6. **Verify** — read back after changes

---

## Quick Command Reference

### Diagnostics
```routeros
/system resource print
/system identity print
/system routerboard print
/interface print stats
/ip address print
/ip route print
/ip neighbor print
/log print
/tool ping 8.8.8.8 count=5
/tool traceroute 8.8.8.8
/tool torch interface=ether1
```

### Interfaces & VLANs
```routeros
/interface print detail
/interface vlan add name=vlan500 vlan-id=500 interface=ether2
/interface bridge add name=br-wan protocol-mode=rstp
/interface bridge port add bridge=br-wan interface=ether2
# IMPORTANT: for queues on bridged/PPPoE/VLAN traffic:
/interface bridge settings set use-ip-firewall=yes use-ip-firewall-for-vlan=yes use-ip-firewall-for-pppoe=yes
```

### PPPoE & ISP
```routeros
/interface pppoe-server server add service-name=internet interface=vlan500 authentication=pap,chap
/ppp secret add name=user01 password=pass service=pppoe profile=plano-50M
/ppp active print
/ip pool add name=cgnat-pool ranges=100.65.62.0-100.65.63.255
/ppp profile add name=plano-50M local-address=100.64.0.1 remote-address=cgnat-pool use-radius=yes
```

### NAT & Firewall
```routeros
# masquerade (dynamic IP/PPPoE)
/ip firewall nat add chain=srcnat out-interface=pppoe-wan action=masquerade
# src-nat (static IP — CGNAT via loopback)
/ip firewall nat add chain=srcnat src-address=100.64.0.0/10 action=src-nat to-addresses=<loopback> out-interface=ether1-wan
# Flush conntrack after NAT changes:
/ip firewall connection remove [find]
# MSS clamping (mandatory for PPPoE):
/ip firewall mangle add chain=forward out-interface=pppoe-wan protocol=tcp tcp-flags=syn tcp-mss=1301-65535 action=change-mss new-mss=1300
```

### RADIUS / MK-Auth
```routeros
/radius add address=<mkauth-ip> secret=<secret> service=ppp timeout=3s
/ppp aaa set use-interim-update=yes interim-update=5m
```

### BGP / OSPF (v7)
```routeros
# BGP v7: peer-role mandatory
/routing bgp template set default as=65001
/routing bgp connection add name=transit remote.address=1.2.3.4/32 remote.as=65000 local.role=ebgp template=default
# OSPF v7
/routing ospf instance add name=ospf-main router-id=1.1.1.1
/routing ospf area add name=backbone area-id=0.0.0.0 instance=ospf-main
```

### Backup & Export
```routeros
/system backup save name=pre-change
/export compact
/export file=config-backup
```

---

## Failover & Notifications

```routeros
# Netwatch V6
/ip/netwatch/add host=8.8.8.8 interval=5s \
    down-script=":global comentario \"LINK1\"; :global LinkState 0; /system script run FAILOVER_ACTIONS" \
    up-script=":global comentario \"LINK1\"; :global LinkState 1; /system script run FAILOVER_ACTIONS"

# Netwatch V7 (execute{} obrigatório)
/ip/netwatch/add host=8.8.8.8 interval=5s \
    down-script=":global comentario \"LINK1\"; :global LinkState 0; execute {/system script run FAILOVER_ACTIONS}" \
    up-script=":global comentario \"LINK1\"; :global LinkState 1; execute {/system script run FAILOVER_ACTIONS}"
```

Scripts: FAILOVER_ACTIONS (Telegram + Google Sheets), FAILOVER_WPP (WhatsApp via Evolution API).
See `references/failover-notifications.md` for complete scripts and docker-compose.

> **Alternativa profissional**: `netwatch-notify` do repositório **eworm-de/routeros-scripts**
> oferece threshold de contagem, dependência pai/filho, múltiplos canais e auto-atualização.
> Ver `references/eworm-scripts.md`.
> **Atenção**: scripts de `rsc.eworm.de` são carregados diretamente nos dispositivos — revise
> o conteúdo antes de aplicar em produção. Prefira baixar, auditar e hospedar internamente.

---

## Critical Behaviors (from official docs)

- **NAT**: after rule changes → `/ip firewall connection remove [find]`
- **Bridge queues**: need `use-ip-firewall=yes` on bridge
- **PPPoE**: MSS clamping required (`change-mss new-mss=1300`)
- **BGP v7**: `peer-role` mandatory; use `input.accept-nlri` for RAM efficiency
- **Routing filter v7**: default action = reject; use `"if (cond) { accept }"`
- **Mangle**: max 4096 unique packet marks

---

## Safety Rules

- **Never** `/system reset-configuration` without double confirmation
- **Never** remove firewall input rules blindly — risk of SSH lockout
- **Always** export config before bulk changes
- **Warn** that PPPoE/NAT changes drop active sessions on live ISP routers

---

## Reference Files

| File | Contents |
|------|----------|
| `references/routeros-commands.md` | Full CLI command reference (firewall, NAT, PPPoE, BGP, OSPF, scripting) |
| `references/routeros-api.md` | RouterOS API + REST API — Python patterns + complete resource path table |
| `references/failover-notifications.md` | Failover scripts + Telegram + WhatsApp (Evolution API) + Google Sheets |
| `references/eworm-scripts.md` | eworm-de/routeros-scripts — netwatch-notify, backup, health, dhcp-to-dns, telegram-chat |
| `references/vsol-olt.md` | VSOL V1600G-series OLT SSH management |
| `references/isp-stack.md` | End-to-end ISP config: OLT → MikroTik → RADIUS |
| `scripts/ssh-exec.sh` | SSH helper script |
| `scripts/mikrotik_api.py` | Python API client (no external deps) |
