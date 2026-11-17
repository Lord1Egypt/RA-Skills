# Router Hardening Field Reference

## Why defaults are the threat model

Home routers get attacked at scale by automated scanners, not targeted
geniuses. The scans look for: factory admin logins on the WAN side (or via
cross-site request forgery from a malicious page you visit while logged
in), open UPnP endpoints, WPS PINs, and known firmware exploits. Every item
in the hardening pass closes one of those specific, mechanically-exploited
doors. None of it requires skill to exploit — which is why closing them
works.

## The pass, in order, with reasons

1. **Firmware first** — many update flows reset settings; updating after
   configuring risks silently reverting your hardening.
2. **Admin password** — separate from Wi-Fi. It protects the config itself:
   port forwards, DNS, firmware. Default admin/admin on the LAN side is
   exploitable via CSRF from any compromised device or malicious webpage.
3. **WPA3 / WPA2-AES** — WPA3-SAE kills offline dictionary attacks. If
   legacy devices force WPA2, use AES-only (TKIP is 2008-era broken). WEP
   is breakable in minutes and should disqualify a router from service.
4. **WPS off** — the PIN variant is an 8-digit (effectively ~10^4) online
   brute-force on many models. Button-only mode is less bad but the
   setting usually kills both.
5. **Remote management off** — your admin page has no business being on
   the public internet. If you administer remotely, use a VPN or the
   vendor's authenticated cloud with MFA.
6. **UPnP off** — the protocol any LAN program can call to open inbound
   ports. Games and consoles love it; malware loves it more. Manual
   forwards for the specific device/port you actually need.
7. **Guest network with LAN isolation** — IoT devices (cameras, bulbs,
   plugs) are the most-compromised class of home device. Guest isolation
   means a pwned camera can't reach your laptop.
8. **DNS choice** — ISP resolvers vary in malware filtering; Quad9
   (9.9.9.9) filters malicious domains, Cloudflare (1.1.1.1) is fast and
   privacy-forward. Set at the router so every client inherits it.
9. **Admin-over-wired-only** (where supported) — shrinks the admin attack
   surface to physically-connected machines.
10. **Services** — Telnet off (plaintext, ever); SSH off unless used; DNS
    rebind protection ON (blocks DNS answers that resolve to your router's
    internal IP — a real phishing vector).

## Interpreting the inventory

- Every device on the list should map to something you can physically
  point at. Phones, laptops, TVs, printers, consoles, cameras, smart-home
  hubs.
- **MAC vendor prefix** (first three octets, e.g. `c4:d7:38`) identifies
  the manufacturer — search "<prefix> MAC lookup" to identify a mystery
  device.
- Dormant/no-name entries: identify by elimination — unplug a suspect
  device, re-run the inventory, see which row disappears.
- An active unknown that survives a Wi-Fi password change means either a
  device with a saved profile you forgot, or a wired freeloader — check
  the router's own client list page too.
- Sudden new devices at 3 AM that you can't account for = rotate the Wi-Fi
  PSK, check WPS state, review the router's logs if it has them.

## Admin page dialect cheat sheet

| Concept | ASUS | TP-Link | Netgear | App-managed |
|---|---|---|---|---|
| Wi-Fi security | Wireless → General | Wireless → Wireless Security | Wireless Settings | App Wi-Fi settings |
| Admin password | Administration → System | System Tools → Password | Set during setup | Vendor account password |
| Remote admin | Administration → System → "Web Access from WAN" | Security → Remote Management | Advanced → Remote Management | N/A (cloud) |
| UPnP | WAN → Virtual Server / UPnP | Forwarding → UPnP | Advanced → UPnP | Usually hidden |
| Guest net | Guest Network | Guest Network | Guest Network | App guest network |
| Firmware | Administration → Firmware Upgrade | System Tools → Firmware Upgrade | Router Update | App updates |

App-managed systems (Eero, Google Nest, Deco in app mode) trade the admin
password for a vendor cloud account: the hardening step becomes "strong
password + MFA on the vendor account," plus disabling unused cloud/integrations.

## Signs of compromise worth reacting to

- DNS settings changed to unknown servers (traffic hijack)
- New port forwards / DMZ entries you didn't create
- Admin password no longer works
- Unknown persistent clients
- Browser cert warnings on sites that shouldn't have them (SSL-strip
  middlebox)
- Router crashing/rebooting under load (some malware families brick
  routers by mistake)

Response: firmware reflash/factory reset → offline reconfigure with the
hardening pass → rotate the Wi-Fi PSK → change passwords for accounts used
on that network from a different connection.

## What this is not

- Not an enterprise NAC/802.1X design guide.
- Not wireless performance tuning (channel planning, mesh backhaul).
- Not a promise: security is layered; the router layer keeps out the
  automated 99%, and endpoint hygiene still matters.
