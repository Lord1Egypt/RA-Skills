---
name: home-router-security-auditor
description: Use when setting up, auditing, or suspecting trouble with a home router — generates the civilian-grade hardening checklist (WPA3/WPA2 transition, WPS off, UPnP off, admin password + remote management, firmware freshness), decodes router-speak on the admin page, runs a local-network device inventory with flagging of unknown clients, and interprets the scary-sounding options (guest VLAN isolation, DNS rebinding protection) so defaults actually get changed instead of scrolled past.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [router, wifi, network-security, home-network, firmware, auditing]
---

# Home Router Security Auditor

## Overview

The home router is the perimeter of every device you own, and most run on
factory settings: admin/admin, WPS enabled, firmware from 2021, remote
management open to the internet. Attackers don't pick locks here — they
walk through defaults. This skill produces the hardening pass a
knowledgeable friend would do in 30 minutes: what to change, in what order,
what each scary admin-page word means, and how to verify the change took.
`scripts/router_audit.py` generates the checklist per router brand family,
runs a stdlib-only local device inventory (ARP + ping sweep of your
subnet) to flag unknown clients, and prints a verification protocol for
after each change.

## When to Use

- New router setup (the single highest-value moment — 15 minutes here
  changes everything downstream).
- Never changed the admin password / still on factory defaults.
- Suspected compromise: unknown devices on Wi-Fi, sudden DNS popups,
  router behaving strangely after a "support call".
- After moving, changing ISPs, or inheriting a router from a previous
  tenant/owner.
- Yearly hygiene pass (firmware, credentials, guest network review).

**Don't use for:** enterprise AP/controller configs, mesh backhaul tuning
for performance (not security), or law-enforcement-grade incident response
— this is the civilian layer: defaults, credentials, exposure, firmware.

## How It Works

### The hardening pass (priority order — do them in this sequence)

1. **Firmware first.** Updating after changing settings often resets them;
   update first, re-check after. Check the vendor's support page for the
   model, or the admin page's update section.
2. **Admin password** (not the Wi-Fi password — the router's own admin
   login). Unique, long, stored in a password manager. This is the #1
   factory default that matters.
3. **Wi-Fi encryption**: WPA3 if all devices support it; WPA2/WPA3
   transitional mode during the compatibility window; WPA2-AES minimum
   (never "WPA mixed" with TKIP, never WEP).
4. **WPS OFF.** The push-button/PIN pairing system has a broken PIN
   protocol on many routers; it's a default-on backdoor.
5. **Remote management OFF** (also: "Web Access from WAN", "Cloud
   management" unless you deliberately use the vendor app over the
   internet — and if you do, it needs a strong vendor-account password).
6. **UPnP OFF.** Convenience that lets any LAN device (including malware
   on a laptop) open inbound ports on your perimeter. Port-forward
   manually for the 1-2 things that need it.
7. **Guest network ON** for IoT/visitors, with "allow guest to see LAN"
   OFF — isolates the devices most likely to be compromised (cameras,
   bulbs, vacuums) from your laptops.
8. **DNS**: note what the router hands out; consider explicit
   Quad9/Cloudflare (malware-filtering resolvers) instead of ISP defaults.
9. **Admin interface over Wi-Fi**: if the router allows restricting admin
   access to wired clients only, enable it.
10. **Reboot cadence + note**: record firmware version and settings date
    (the script logs this) so next year's audit has a baseline.

### Brand-family notes

Admin-page location and wording drift by vendor: TP-Link
(tplogin.cn / 192.168.0.1, "Wireless Security"), ASUS (router.asus.com,
"Wireless" → "General"), Netgear (routerlogin.net, "Wireless Settings"),
D-Link, Eero/Google/Nova app-managed (hardening lives in the app: guest
isolation + no admin password = vendor account MFA instead). The script
prints per-family pointers so you find the right page.

### Device inventory (`--inventory`)

ARP table + ping sweep of the local subnet (pure stdlib), listing every
responding client with hostname where resolvable. Unknown persistent
clients are the visible symptom of both freeloaders and compromise.
Verdict per device: KNOWN (matches your mental list), CHECK (dormant or
unnamed — identify by MAC vendor prefix), INVESTIGATE (active unknown).

### Interpretation dictionary

The admin page says scary things in vendor dialect. The reference table
maps: "WPS", "UPnP", "NAT-PMP", "Remote/WAN management", "DNS rebind
protection" (keep ON — blocks malicious DNS answers targeting your
router), "IGMP snooping", "SSH/Telnet services" (Telnet OFF, always),
"mDNS" (fine on LAN, not forwarded).

## Using the Script

```
# the full hardening checklist with brand pointers
python3 scripts/router_audit.py --checklist --brand asus

# device inventory of the local subnet
python3 scripts/router_audit.py --inventory

# what each scary admin-page term means
python3 scripts/router_audit.py --dict

# baseline record after hardening
python3 scripts/router_audit.py --baseline --model "RT-AX3000" --fw "3.0.0.4.388"
```

## Common Pitfalls

1. **Changing the Wi-Fi password and calling it done.** The Wi-Fi PSK and
   the router admin login are different credentials; the admin one is the
   crown jewel and ships as admin/admin.
2. **Updating firmware after configuring.** Updates can factory-reset;
   firmware first, settings second.
3. **Leaving WPS "for guests".** Guests can type a Wi-Fi password. WPS's
   PIN mode is crackable on many models in hours.
4. **UPnP disabled, then re-enabled by a gamer "for NAT".** Forward the
   one port the game needs instead of reopening the perimeter-wide hole.
5. **Trusting MAC filtering as security.** MACs are spoofable in seconds;
   it's an inventory aid, not a lock.
6. **Hidden SSID as security.** Hiding the name changes nothing for
   attackers (probe frames leak it) and complicates your own devices.
7. **Ignoring the vendor cloud account.** App-managed routers (Eero,
   Google Wifi) move the attack surface to the vendor account: strong
   password + MFA there replaces the admin-password step.

## Verification Checklist

- [ ] Firmware current for the model; version recorded in baseline.
- [ ] Admin password unique + stored; factory login no longer works.
- [ ] WPA3 (or WPA2/WPA3 transitional; WPA2-AES floor), never WEP/TKIP.
- [ ] WPS disabled; remote/WAN admin disabled; Telnet off.
- [ ] UPnP off; needed ports forwarded manually.
- [ ] Guest network live with LAN isolation for IoT/visitors.
- [ ] Inventory reviewed: every client accounted for.
- [ ] Baseline saved (model, firmware, settings date) for next audit.
