# Home Router Security Auditor

**Your router ships with its doors keyed alike — this is the 30-minute fix.**

The home router is the perimeter for every device you own, and most run
factory settings: admin/admin logins, WPS enabled, remote management open,
firmware from years ago. Nobody attacks your router personally — automated
scanners find the defaults at internet scale. The hardening pass changes
every one of those doors, and takes half an hour once.

## What It Does

`scripts/router_audit.py` (read-only on your network — it never changes
router settings):

```bash
python3 scripts/router_audit.py --checklist --brand asus   # hardening pass + where to click
python3 scripts/router_audit.py --inventory --ping-sweep   # who is on your LAN
python3 scripts/router_audit.py --dict                     # admin-page dialect decoder
python3 scripts/router_audit.py --baseline --model "RT-AX3000" --fw "3.0.0.4.388"
```

- **The hardening checklist in priority order** (firmware → admin password
  → WPA3 → WPS off → remote admin off → UPnP off → guest isolation → DNS),
  each with the reason it matters, plus brand-family pointers (ASUS,
  TP-Link, Netgear, D-Link, Eero/Google app-managed) for where the setting
  actually lives.
- **Local device inventory**: ARP + ping sweep of your subnet (pure
  stdlib, no installs), listing IP/MAC/name per client with
  KNOWN/CHECK/INVESTIGATE verdicts — the visible symptom of freeloaders
  or compromise is an unknown client.
- **Router-speak dictionary**: WPS, UPnP/NAT-PMP, DNS rebind protection,
  Telnet, DMZ, hidden SSID, MAC filtering — what each actually means and
  the recommended state.
- **Baseline record**: model/firmware/date in JSON, so next year's audit
  compares against something.

## Who Needs This

- Anyone who just unboxed a router (the highest-value 15 minutes in home
  security)
- Homes that never changed the admin login (i.e., most homes)
- People whose IoT pile (cameras, bulbs, plugs) shares a network with
  their laptops — guest isolation is the fix
- Anyone who spotted an unknown device on Wi-Fi and wants the response
  protocol
- Yearly hygiene: firmware check + inventory diff

## Example

New router day: `--checklist --brand netgear` walks you through firmware
first (so settings don't get wiped after), admin password next, WPS off,
remote management off, UPnP off with a manual port forward for the one
game console that needed it, guest network for the smart bulbs. Then
`--baseline` records what you did, and `--inventory --ping-sweep` prints
the legitimate-device roster to compare against next time something feels
off.

## License

MIT — see LICENSE.
