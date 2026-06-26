# RouterOS API + REST API Reference
> Source: MikroTik official docs + mikrotik-api skill (ClawHub)

## Two API Methods

### 1. RouterOS API (port 8728/8729) — Python
Native binary protocol. Best for automation scripts.

```bash
pip3 install --break-system-packages routeros-api
```

```python
import routeros_api, os

conn = routeros_api.RouterOsApiPool(
    host=os.getenv('MIKROTIK_HOST'),
    username=os.getenv('MIKROTIK_USER', 'admin'),
    password=os.getenv('MIKROTIK_PASS', ''),
    plaintext_login=True,   # Required for ROS 6.43+
    port=8728               # 8729 for SSL
)
api = conn.get_api()
# ... work ...
conn.disconnect()  # Always disconnect!
```

#### SSL Connection
```python
conn = routeros_api.RouterOsApiPool(
    host=host, username=user, password=pw,
    plaintext_login=True, use_ssl=True,
    ssl_verify=False, ssl_verify_hostname=False, port=8729
)
```

#### Core Operations
```python
# READ
resource = api.get_resource('/ip/address')
items = resource.get()                        # all
items = resource.get(interface='ether1')      # filter
items = resource.get(disabled='false')

# ADD
resource.add(address='192.168.1.1/24', interface='ether1', comment='mgmt')

# SET (update)
resource.set(id='*1', address='192.168.2.1/24')
resource.set(id='*1', disabled='yes')   # disable
resource.set(id='*1', disabled='no')    # enable

# REMOVE
resource.remove(id='*1')

# CALL (commands)
resource = api.get_resource('/system')
resource.call('reboot')
# with params:
resource = api.get_resource('/ip/firewall/filter')
resource.call('move', {'numbers': '*1', 'destination': '*5'})
```

#### Advanced Patterns
```python
# Batch add to address-list
resource = api.get_resource('/ip/firewall/address-list')
for ip in ['1.2.3.4', '5.6.7.8']:
    resource.add(list='blocklist', address=ip)

# Insert firewall rule at position (place-before)
resource = api.get_resource('/ip/firewall/filter')
resource.add(chain='forward', action='accept',
    src_address='10.0.0.0/8', place_before='*5')

# Note: Python uses underscores for hyphenated attrs
# src-address -> src_address, place-before -> place_before

# Ping via API
resource = api.get_resource('/tool')
result = resource.call('ping', {'address': '8.8.8.8', 'count': '4'})

# Backup
resource = api.get_resource('/system/backup')
resource.call('save', {'name': 'api-backup'})
```

#### Error Handling
```python
from routeros_api.exceptions import RouterOsApiCommunicationError
try:
    conn = routeros_api.RouterOsApiPool(host, username=user, password=pw, plaintext_login=True)
    api = conn.get_api()
    # ... work ...
except RouterOsApiCommunicationError as e:
    print(f"API Error: {e}")
except ConnectionError:
    print("Cannot reach router")
finally:
    try: conn.disconnect()
    except: pass
```

---

### 2. REST API (ROS 7.1+) — HTTP/HTTPS
No extra library. Requires `www` or `www-ssl` service enabled.

```bash
# Enable REST on router first:
/ip service enable www-ssl
```

#### curl Examples
```bash
BASE="https://172.16.100.1/rest"
AUTH="admin:senha"

# GET all
curl -k -u $AUTH $BASE/ip/address

# PUT (create)
curl -k -u $AUTH -X PUT $BASE/ip/address \
  -H "content-type: application/json" \
  -d '{"address":"192.168.1.1/24","interface":"ether1"}'

# PATCH (update)
curl -k -u $AUTH -X PATCH $BASE/ip/address/*1 \
  -H "content-type: application/json" \
  -d '{"comment":"updated"}'

# DELETE
curl -k -u $AUTH -X DELETE $BASE/ip/address/*1

# POST with query filter
curl -k -u $AUTH -X POST $BASE/interface/print \
  -H "content-type: application/json" \
  -d '{".query":["type=ether"],"_proplist":["name","type","running"]}'
```

#### Python requests
```python
import requests
from requests.auth import HTTPBasicAuth

base = 'https://172.16.100.1/rest'
auth = HTTPBasicAuth('admin', 'senha')

# GET
r = requests.get(f'{base}/interface', auth=auth, verify=False)
print(r.json())

# POST with proplist
r = requests.post(f'{base}/ip/address/print',
    auth=auth, verify=False,
    json={'_proplist': ['address', 'interface']})
```

> REST API has **60-second timeout** — always use `count`/`duration`/`once` for tools.

---

## Complete Resource Path Reference

### System
| Task | API Path |
|------|---------|
| System info (CPU, RAM, uptime) | `/system/resource` |
| Router identity | `/system/identity` |
| System clock | `/system/clock` |
| NTP client | `/system/ntp/client` |
| Scheduler | `/system/scheduler` |
| Scripts | `/system/script` |
| Log entries | `/log` |
| Logging rules | `/system/logging` |
| Packages | `/system/package` |
| RouterBoard info | `/system/routerboard` |
| Health (voltage, temp) | `/system/health` |
| Users | `/user` |
| Active users | `/user/active` |
| SSH keys | `/user/ssh-keys` |
| Files | `/file` |
| Backup | `/system/backup` |
| Certificates | `/certificate` |
| SNMP | `/snmp` |
| LEDs | `/system/leds` |

### Interfaces
| Task | API Path |
|------|---------|
| All interfaces | `/interface` |
| Ethernet | `/interface/ethernet` |
| Bridge | `/interface/bridge` |
| Bridge ports | `/interface/bridge/port` |
| Bridge VLANs | `/interface/bridge/vlan` |
| Bridge hosts (MAC table) | `/interface/bridge/host` |
| Bridge settings | `/interface/bridge/settings` |
| VLAN | `/interface/vlan` |
| Bonding (LACP) | `/interface/bonding` |
| EoIP | `/interface/eoip` |
| GRE | `/interface/gre` |
| VXLAN | `/interface/vxlan` |
| WireGuard | `/interface/wireguard` |
| WireGuard peers | `/interface/wireguard/peers` |
| L2TP client | `/interface/l2tp-client` |
| PPPoE client | `/interface/pppoe-client` |
| PPPoE server | `/interface/pppoe-server/server` |
| OVPN client | `/interface/ovpn-client` |
| WiFi (legacy) | `/interface/wireless` |
| WiFi (ROS 7) | `/interface/wifi` |
| WiFi registration | `/interface/wifi/registration-table` |
| Interface lists | `/interface/list` |
| Interface list members | `/interface/list/member` |
| Traffic monitor | `/interface/monitor-traffic` |

### IP
| Task | API Path |
|------|---------|
| IP addresses | `/ip/address` |
| ARP table | `/ip/arp` |
| Routes | `/ip/route` |
| DNS settings | `/ip/dns` |
| DNS static | `/ip/dns/static` |
| DHCP client | `/ip/dhcp-client` |
| DHCP server | `/ip/dhcp-server` |
| DHCP leases | `/ip/dhcp-server/lease` |
| DHCP networks | `/ip/dhcp-server/network` |
| IP pool | `/ip/pool` |
| IP neighbors | `/ip/neighbor` |
| IP services | `/ip/service` |
| IP SSH | `/ip/ssh` |
| Hotspot | `/ip/hotspot` |
| Hotspot users | `/ip/hotspot/user` |
| Hotspot active | `/ip/hotspot/active` |

### Firewall
| Task | API Path |
|------|---------|
| Filter rules | `/ip/firewall/filter` |
| NAT rules | `/ip/firewall/nat` |
| Mangle rules | `/ip/firewall/mangle` |
| RAW rules | `/ip/firewall/raw` |
| Address lists | `/ip/firewall/address-list` |
| Connections (conntrack) | `/ip/firewall/connection` |
| Connection tracking | `/ip/firewall/connection/tracking` |
| Layer 7 protocols | `/ip/firewall/layer7-protocol` |

### PPP
| Task | API Path |
|------|---------|
| PPP secrets | `/ppp/secret` |
| PPP profiles | `/ppp/profile` |
| PPP active | `/ppp/active` |
| PPP AAA | `/ppp/aaa` |

### Queues
| Task | API Path |
|------|---------|
| Simple queues | `/queue/simple` |
| Queue tree | `/queue/tree` |
| Queue types | `/queue/type` |

### Routing (ROS 7)
| Task | API Path |
|------|---------|
| Routing tables | `/routing/table` |
| OSPF instance | `/routing/ospf/instance` |
| OSPF area | `/routing/ospf/area` |
| OSPF neighbors | `/routing/ospf/neighbor` |
| BGP connection | `/routing/bgp/connection` |
| BGP template | `/routing/bgp/template` |
| BGP session | `/routing/bgp/session` |
| Route filter rules | `/routing/filter/rule` |
| BFD session | `/routing/bfd/session` |
| IGMP Proxy | `/routing/igmp-proxy` |

### Tools
| Task | API Path |
|------|---------|
| Ping | `/tool/ping` (call) |
| Traceroute | `/tool/traceroute` (call) |
| Bandwidth test | `/tool/bandwidth-test` (call) |
| Torch | `/tool/torch` (call) |
| Netwatch | `/tool/netwatch` |
| Fetch (HTTP client) | `/tool/fetch` |
| Sniffer | `/tool/sniffer` |
| E-mail | `/tool/e-mail` |
| IP Scan | `/tool/ip-scan` |
| Romon | `/tool/romon` |

### Container (ROS 7.4+)
| Task | API Path |
|------|---------|
| Containers | `/container` |
| Container config | `/container/config` |
| Container mounts | `/container/mounts` |
| Container envs | `/container/envs` |

### ZeroTier
| Task | API Path |
|------|---------|
| ZeroTier | `/zerotier` |
| ZeroTier interface | `/zerotier/interface` |

---

## API Error Codes

| Code | Meaning |
|------|---------|
| 0 | Missing item or command |
| 1 | Argument value failure |
| 2 | Command interrupted |
| 3 | Scripting failure |
| 4 | General failure |
| 5 | API related failure |
| 6 | TTY related failure |

---

## Enable API on Router

```routeros
# Enable plain API (port 8728)
/ip service enable api

# Enable SSL API (port 8729)
/ip service enable api-ssl

# Restrict to management subnet
/ip service set api address=10.0.0.0/8
/ip service set api-ssl address=10.0.0.0/8
```
