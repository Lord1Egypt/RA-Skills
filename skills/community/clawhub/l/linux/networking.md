# Networking — Reachability, DNS, Firewalls, and the Limits You Hit At Scale

Work outward in layers: is it listening → does the local firewall allow it → is there a route → does the name resolve → does the remote side answer. Each layer is one command, and the first failing layer is the whole answer.

## The Five-Layer Check

```bash
ss -tlnp                                   # 1. listening? on which ADDRESS? which pid?
sudo nft list ruleset  |  sudo iptables -S # 2. local filter (see "One Firewall, Several Front Ends")
ip route get 10.0.5.7                      # 3. chosen route AND source address for that destination
getent hosts api.internal                  # 4. resolution the way applications do it
nc -zv api.internal 5432                   # 5. remote side actually answering
```

- `ss -tlnp` binding: `127.0.0.1:5432` is unreachable from anywhere else no matter what the firewall says; `0.0.0.0:5432` listens on every IPv4 address; `[::]:5432` usually covers IPv4 too via v4-mapped addresses.
- `ip route get <dst>` is underused: it prints the route the kernel WILL take and the source IP it will use — instantly explaining asymmetric-routing and multi-homing failures.
- `ping` proves ICMP only. A host that pings with a dead service and a host that blocks ICMP while serving traffic are both routine.

## DNS

- Applications resolve through NSS (`/etc/nsswitch.conf`): `/etc/hosts` first on most systems, then DNS, then LDAP/SSSD if configured. **`dig` and `nslookup` bypass all of that and talk to a resolver directly** — "dig works but the app cannot resolve" is the signature of an `/etc/hosts`, nsswitch, or resolver-stub problem. Test with `getent hosts <name>`.
- systemd-resolved hosts: `/etc/resolv.conf` is a symlink to a stub listing `127.0.0.53`. Do not edit it — the real state is `resolvectl status` (per-link servers and search domains) and the config lives in `/etc/systemd/resolved.conf` or a `.network`/NetworkManager profile.
- Search domains multiply queries: with three search domains, a lookup of a short name can cost four round trips before the absolute name is tried. Use fully qualified names (with the trailing dot where the client honours it) in service configuration.
- Split-horizon and VPN: the internal zone resolves only through the VPN's resolver. `resolvectl query internal.corp` shows which link answered; per-link routing (`resolvectl domain <link> ~corp`) is the fix, not a global override.
- Caching lies: the negative cache holds an NXDOMAIN after you fix the record. `resolvectl flush-caches` (or restart the caching daemon) before concluding the fix failed.

## One Firewall, Several Front Ends

The kernel has one packet filter (nftables on current kernels; `iptables` on modern distros is a compatibility front end writing nft rules). Rules can arrive from four places at once, and reading only one of them is how you "prove" a port is open while it is blocked.

| Tool | Read state | Persist | Notes |
|---|---|---|---|
| nftables | `nft list ruleset` | `/etc/nftables.conf` + enable `nftables.service` | The ground truth on current systems |
| iptables (nft backend) | `iptables -S`, `iptables -L -n -v` | `iptables-save` + `netfilter-persistent`/`iptables-services` | Raw rules vanish on reboot unless saved |
| ufw | `ufw status verbose` | Persists by design | Debian/Ubuntu default front end |
| firewalld | `firewall-cmd --list-all` | `--permanent` then `--reload` | RHEL/Fedora default; a change without `--permanent` disappears at reload |
| else | Check all of the above plus the cloud security group | — | Cloud rules are invisible from inside the host |

- **`firewall-cmd` without `--permanent` is a runtime-only change** and `--reload` silently reverts it. The idiom is: apply runtime, verify, then re-apply with `--permanent`.
- Never `iptables -F` on a remote host with a DROP default policy — you flush your own access. Set policies to ACCEPT first, or schedule a rollback (→ `ssh.md`).
- Container runtimes insert their own chains ahead of the front-end's rules: a published container port can be world-reachable despite "deny all" (the `docker` skill covers this).
- Verify from OUTSIDE the host as the final step. A rule that passes `nft list ruleset` inspection and fails a real connection means a cloud security group, a network ACL, or a routing device.

## Connection Limits That Look Like Random Failures

- **Ephemeral port exhaustion**: the default range is 32768-60999 (28232 ports) and each closed outbound connection sits in TIME_WAIT for 60 seconds. Ceiling to a single destination ≈ 28232 / 60 ≈ 470 new connections per second. Above that, `connect()` fails intermittently under load and recovers when traffic dips. Fix with connection pooling or keep-alive; `net.ipv4.tcp_tw_reuse=1` helps outbound (the old `tcp_tw_recycle` broke NAT clients and was removed in kernel 4.12).
- **Accept-queue drops**: `ss -ltn` shows `Recv-Q` (pending) against `Send-Q` (the backlog size) for listening sockets; a `Recv-Q` at the backlog means the app is not accepting fast enough. Confirm with `nstat -az TcpExtListenOverflows`. Raising `net.core.somaxconn` only helps if the application also asks for a larger backlog.
- **conntrack table full**: `nf_conntrack: table full, dropping packet` in `dmesg` means silent drops under load. Compare `sysctl net.netfilter.nf_conntrack_count` with `nf_conntrack_max` and alarm at 80%; raising the max costs little memory, the drops cost requests.
- **Retransmissions**: `ss -tin` per-socket shows `rtt`, `retrans`, and cwnd; `nstat -az | grep -i retrans` aggregates. Retransmits climbing with CPU idle points at the network path, not the host.

## MTU: The Hang That Only Hits Large Transfers

- Signature: handshakes and small requests succeed, large uploads/downloads stall forever. Cause: a tunnel (VPN, WireGuard, GRE, some cloud overlays) lowers the effective MTU and PMTU-discovery ICMP is blocked somewhere.
- Probe the real limit: `ping -M do -s 1472 <host>` — 1472 payload + 28 bytes of headers = 1500. Halve until it passes to find the ceiling.
- Fix at the interface (`ip link set dev eth0 mtu 1400`, persisted in the network config) or enable `net.ipv4.tcp_mtu_probing=1` so the stack discovers it without ICMP.

## Capture, When Logs Are Not Enough

```bash
tcpdump -ni any -c 200 'host 10.0.5.7 and port 5432'      # quick look, bounded
tcpdump -ni eth0 -s 0 -w /tmp/cap.pcap 'port 443'          # to file for Wireshark
tcpdump -ni any 'tcp[tcpflags] & (tcp-syn|tcp-rst) != 0'   # who resets whom
```

- Read the first packets, not the whole capture: SYN with no reply = filtered upstream; SYN then RST = nothing listening or an active reject; retransmitted SYNs = packet loss or asymmetric routing.
- Always bound the capture (`-c` or a small `-W`/`-C` ring). An unbounded `-w` on a busy interface fills the disk (→ `disk-space.md`).

## Addresses And Routes

- `ip a`, `ip r`, `ip neigh` replace `ifconfig`, `route`, and `arp` — the old tools omit secondary addresses and modern attributes.
- Interface configuration is distro-specific (netplan, NetworkManager, systemd-networkd, `/etc/network/interfaces`) → `distros.md`. Whatever the front end, `ip` shows the result and only the front end makes it survive a reboot.
- Dual stack: `localhost` may resolve to `::1` first while the service listens only on `127.0.0.1`, producing "connection refused" on a running service. Test both literals; bind `::` with `net.ipv6.bindv6only=0` (the default) to cover both.
- Ports below 1024 do not require root: `setcap cap_net_bind_service=+ep <binary>` or `AmbientCapabilities=` in the unit (→ `permissions.md`).
- Proxy environment variables are read case-sensitively by different tools; set both `http_proxy` and `HTTP_PROXY`, and put internal ranges in `no_proxy` (comma-separated, no wildcards in most clients).

## Persistence

Every runtime networking change is gone at reboot unless paired with its persistence mechanism: `ip`/`sysctl -w` → a file in `/etc/sysctl.d/` and the distro's network config; `iptables` → `iptables-save`; `nft` → `/etc/nftables.conf`; `firewall-cmd` → `--permanent`. Verify the pairing the same day, not at the next unplanned reboot (→ `SKILL.md` rule 5).

## Record It

Firewall state is the change most likely to be undone accidentally and the hardest to reconstruct: every rule added or removed goes to `~/Clawic/data/linux/changes/<year>.md` with its front end, its persistence step (`--permanent`, `iptables-save`, `/etc/nftables.conf`), its rollback, and how it was verified from OUTSIDE the host. The set of listening ports a host is supposed to have belongs in `## Listening` in `baselines/<host>.md`, because a new listener is only visible as a diff. Which firewall front end this host actually uses goes on its row in `## Hosts` — checking all four again next session is wasted work (`memory-template.md`).

Related: SSH specifics and lockout safety → `ssh.md` · sysctl tuning and persistence → `kernel.md` · exposure baseline for public hosts → `hardening.md` · unexpected outbound connections → `compromise.md`.
