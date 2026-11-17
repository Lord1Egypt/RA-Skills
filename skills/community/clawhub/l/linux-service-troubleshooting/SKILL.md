---
author: peterliu-512
license: MIT-0
name: linux-service-troubleshooting
description: Use when a Linux service is down or unreachable.
---

# Linux Service Troubleshooting

Diagnose "why is this service/port not working or reachable" on a Linux host. Applies to SSH reachability, Bluetooth, and other system services. Key principle: **don't blame the service until hardware + kernel driver + firewall/rfkill are all confirmed good** — the root cause is very often a config/firewall layer that was never synced.

## Core method: layered bottom-up check

Run in this order (cheapest/most-likely first):

1. **Hardware present?** `lsusb | grep -i <type>`, `lspci`
2. **Kernel driver loaded + initialized?** `lsmod | grep <mod>`, `dmesg | grep -i <subsys>`
3. **Radio/firewall unblocked?** `rfkill list` (bt/wifi), `firewall-cmd --list-all`, `nft list ruleset`
4. **Service running + enabled?** `systemctl status <svc>`, `systemctl is-active <svc>`, `is-enabled <svc>`
5. **Effective config value?** use the tool's OWN probe (`sshd -T`, `bluetoothctl show`), not manual `grep` of a config file.

## SSH reachability on a custom port — the firewalld trap

Symptom: SSH moved off 22 to a custom port (e.g. 50022); LAN access fails but Tailscale access works.

Root cause: firewalld's `ssh` service still maps to **22**; the custom port isn't in any allowed port/service, so LAN traffic (which traverses firewalld) is default-rejected. Tailscale traffic **bypasses firewalld entirely** via the `ts-input` chain (`iptables -S ts-input` → `-i tailscale0 -j ACCEPT`) — that's why the two entry points diverge.

Fix + verify:
```bash
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="50022" protocol="tcp" accept'
sudo firewall-cmd --reload
sudo firewall-cmd --list-rich-rules | grep 50022   # confirm persisted
sudo nft list ruleset | grep 50022                 # confirm in the live ruleset
sudo ss -tlnp | grep -E ':(22|50022)'              # confirm listening + no stale 22
```

**Verification gotcha:** testing `nc -zv <own-LAN-IP> <port>` FROM THE SAME HOST can return `ConnectionRefused` even when remote access works (local hairpin/route edge case — connect to your own physical NIC address). Verify from a real remote LAN host, or look for a live `ESTAB` entry: `sudo ss -tnp 'sport = :50022'`.

## OpenSSH config gotchas (durable, non-obvious)

- **Duplicate directive = FIRST value wins** (not last). If `sshd_config` has `PasswordAuthentication yes` then later `PasswordAuthentication no`, the effective value is **`yes`**. Never infer from reading the file.
- **`sshd -T` is authoritative** for the effective config:
  ```bash
  sudo sshd -T | grep -iE '^(permitrootlogin|passwordauthentication|port|pubkeyauthentication) '
  ```
  (`prohibit-password` may be reported as `without-password` — same meaning.)
- **`systemctl reload sshd`** applies per-connection settings (PermitRootLogin, PasswordAuthentication, etc.) WITHOUT dropping existing sessions (SIGHUP). Use `restart` only for `Port`/`ListenAddress`-class changes.
- **Remove dead firewalld services**: after moving off a port, `--remove-service=ssh` to avoid a "fake allow" for a port nothing listens on.
- Back up before editing: `sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)`.

## Bluetooth not working

Layered check: `lsusb` (hardware) → `dmesg | grep -i bluetooth` (driver/firmware) → `rfkill list` (radio block) → `systemctl status bluetooth` (service).

Common root cause: **everything fine except `bluetooth.service` is `disabled` + `inactive`**.

Signal: `bluetoothctl list` HANGS (40s+) when bluetoothd is down — the hang itself means "service down", not a bluetoothctl bug.

Fix:
```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
bluetoothctl list   # Controller <MAC> <host> [default]
bluetoothctl show   # Powered: yes  (and HCI/LMP version, supported profiles)
```

## Pitfalls

- Don't declare "firewall fixed" just because a rule was added — confirm BOTH `nft list ruleset | grep <port>` AND a real `ESTAB` connection.
- Don't lock yourself out: before tightening `PasswordAuthentication`→`no` or `PermitRootLogin`→`no`, confirm the user has working key auth (`ss -tnp` shows live sessions but not auth method).
- `who` shows login users; `ss -tnp 'sport = :<port>'` shows which remote IPs have live sessions and their sshd PIDs.
