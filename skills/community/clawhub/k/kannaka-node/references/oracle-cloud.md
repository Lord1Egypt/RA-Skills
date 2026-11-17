# Oracle Cloud free tier, for a Kannaka node

The Always Free shapes are enough for a member node. The Ampere A1 (`VM.Standard.A1.Flex`,
up to 4 OCPU / 24 GB shared across the tenancy) is `aarch64`; the AMD micro
(`VM.Standard.E2.1.Micro`, 1 GB) is `x86_64` and is tight: it runs a member node, not
`serve`, and not a local brain.

**Login.** Oracle Linux images: user `opc`. Ubuntu images on OCI: user `ubuntu`. Root
login is disabled; `sudo` is passwordless for that user. The key is the one the human
chose when creating the instance.

**Outbound only.** A node needs outbound TCP 443 and 4222. OCI's default security list
allows all egress, and the image's own `iptables`/`firewalld` allows all outbound too.
You do not touch the security list, `firewalld`, or `iptables`. If someone later wants
this box to *serve* something inbound (a dashboard, a NATS leaf), that is when both the
security list ingress rule and the host firewall need a port, and the image's built-in
`REJECT` rule near the bottom of the `INPUT` chain is the one that bites; not this
skill's problem.

**SELinux is Enforcing** on Oracle Linux. Two consequences the script already handles:
the unit executes `/usr/local/bin/kannaka` (label `bin_t`), never `~/.local/bin/kannaka`
(`home_bin_t`, which lands the process in a confined domain that cannot read
`~/.kannaka`); and after copying a binary into `/usr/local/bin`, `restorecon` it. If
you ever see `Permission denied` on a file whose mode and owner are obviously right,
`getenforce` and `ls -Z` before anything else.

**Packages.** `dnf`. `curl`, `tar`, `awk`, `sha256sum` are present on the base image.
Nothing else is required for a member node.

**Updates.** `sudo dnf -y upgrade --refresh` replaces `sshd` mid-transaction; your
session may drop with a `kex_exchange_identification` error. That is not a failure; wait
and reconnect. Kernel updates need a reboot; `needs-restarting -r` tells you.

**fail2ban** is not on the base image, but operators often add it. Many rapid ssh
sessions from one address trip the sshd jail (typical: 5 in 10 minutes, one-hour ban)
even when every login succeeded. Use one multiplexed session.

**Disk.** The free-tier boot volume is 47 GB by default. The Kannaka store grows with
what the node hears; a node that absorbs audio or a busy swarm can reach hundreds of MB.
A full disk strands atomic saves as `kannaka.hrm.tmp.*` files. Keep 5 GB free, and if
the store is large, set retention rules in `config.toml` (`[retention]`, per content
prefix, cap and ttl) so it forgets on purpose instead of by accident.

**Time.** `chronyd` is on and correct by default. The swarm's epochs assume roughly
synchronised clocks; check `timedatectl` if the node's phase looks wrong to its peers.
