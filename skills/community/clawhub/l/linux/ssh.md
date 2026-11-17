# SSH — Access, Keys, and Not Locking Yourself Out

Two jobs live here: making SSH work when it silently refuses, and changing a remote host without losing the ability to reach it. The second one has a fixed procedure — use it every time, including the time it feels unnecessary.

## The Lockout-Proof Change Procedure

1. Keep your current session open. It stays open even if the daemon restarts — an established connection survives `systemctl restart sshd`.
2. Schedule the undo BEFORE applying the change:
   `systemd-run --on-active=10min --unit=ssh-rollback systemctl restart sshd` (or with a config restore in front of it). `echo 'cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config; systemctl restart sshd' | at now + 10 minutes` if `at` is installed.
3. Validate the syntax offline: `sshd -t` (add `-T` to dump the effective config). Same idea for the other lockout-class files: `visudo -c`, `nft -c -f`, `mount -a`.
4. Apply, then open a **new** connection from a second terminal and authenticate fully.
5. Only after the new session works: cancel the rollback (`systemctl stop ssh-rollback.timer`, `atrm <job>`) and close the old session.

The same five steps apply to firewall changes, sudoers edits, PAM edits, and network reconfiguration. On cloud hosts, know your out-of-band console (serial console, provider web console) before you need it — that is the only path back when step 4 fails and the timer misfires.

## "Server Refused Our Key" With No Useful Error

The server rejects for reasons the client is never told. In order of frequency:

| Cause | Check on the server | Fix |
|---|---|---|
| Permissions | `ls -ld ~ ~/.ssh ~/.ssh/authorized_keys` | Home not group/world-writable, `~/.ssh` 700, `authorized_keys` 600, owned by the user. `StrictModes yes` (default) rejects otherwise |
| Wrong user's file | `getent passwd <user>` for the real home | The key must be in the home of the account you log in AS |
| SELinux label | `ls -Z ~/.ssh` | `restorecon -Rv ~/.ssh` — the classic after restoring a home directory from backup |
| Key type disabled | `sshd -T \| grep -i pubkeyacceptedalgorithms` | `ssh-rsa` with SHA-1 is refused by OpenSSH >=8.8; regenerate as ed25519 |
| Account state | `passwd -S <user>`, `chage -l <user>` | Expired account or `nologin` shell (→ `users.md`) |
| AllowUsers/AllowGroups | `sshd -T \| grep -iE 'allow|deny'` | The user is not in the allowed set |
| else | `journalctl -u sshd -f` during the attempt | The server log names the real reason; the client never will |

Debug from both ends simultaneously: `ssh -vvv user@host` on the client, `journalctl -u sshd -f` (`ssh` on Debian/Ubuntu, `sshd` on RHEL) on the server. The client's last "Offering public key" line before the failure tells you which key it tried.

## Client Configuration That Pays For Itself

```
Host bastion
    HostName bastion.example.com
    User ops
    IdentityFile ~/.ssh/id_ed25519_ops
Host 10.0.*.*
    ProxyJump bastion
    ServerAliveInterval 60
    ServerAliveCountMax 3
Host *
    IdentitiesOnly yes
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m
```

- **First match wins** in `ssh_config` (and in `sshd_config`): specific hosts go ABOVE wildcards, and a `Host *` block at the top silently overrides everything under it.
- `IdentitiesOnly yes` stops the agent from offering every key it holds; without it, a server with `MaxAuthTries 3` (a common hardened value) disconnects before reaching the right key — the "too many authentication failures" error.
- `ControlMaster` reuses one TCP connection for subsequent sessions: near-instant reconnects, and a single authentication for a batch of commands. It also means killing the master drops every multiplexed session.
- `ServerAliveInterval 60` keeps NAT and load balancers from silently dropping idle sessions.

## Keys And Agents

- Generate `ssh-keygen -t ed25519 -C "purpose"`. RSA only where an old server requires it, and then 4096 bits.
- Distribute with `ssh-copy-id`; it gets the permissions right, which manual appends often do not.
- Passphrase-protect every private key and unlock it through the agent (`ssh-add -t 8h` sets a lifetime). An unencrypted key file is a credential anyone with read access owns forever.
- **Never use agent forwarding (`-A`) to a host you do not fully trust**: root on that host can use your agent socket to authenticate as you anywhere. `ProxyJump` (`-J bastion`) tunnels through without exposing keys and is the correct default.
- Restrict what a key may do, on the server side, in `authorized_keys`: `restrict,command="/usr/local/bin/backup-only",from="10.0.0.0/8" ssh-ed25519 AAAA...` — `restrict` disables forwarding, agent, pty, and X11, then you add back only what is needed. This is how a deploy key stops being a shell.
- Host key changed after a rebuild: `ssh-keygen -R <host>` removes the stale entry. Distinguish the legitimate rebuild from an actual interception by checking the new fingerprint against the console output of the host itself.

## Server Configuration

- Modern OpenSSH reads `/etc/ssh/sshd_config.d/*.conf` via an `Include` at the TOP of the main file — a setting you add at the bottom of `sshd_config` can be overridden by a drop-in that was parsed first. Always confirm with `sshd -T | grep -i <setting>`, which prints the effective value.
- The hardening baseline (`PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no`, `AllowGroups ssh-users`) belongs in a drop-in file, applied through the procedure at the top of this file → `hardening.md`.
- Changing the port is obscurity, not security; it does cut log noise from opportunistic scanners. If you do it, update SELinux (`semanage port -a -t ssh_port_t -p tcp 2222`) and the firewall in the same change, or the daemon will not bind.
- `Match` blocks are evaluated after the global section and apply until the next `Match` — an indentation-free file makes their scope easy to misread. Verify per-user results with `sshd -T -C user=alice,host=...,addr=...`.

## Tunnels And File Transfer

- Local forward (reach a remote-only service from your laptop): `ssh -L 5432:db.internal:5432 bastion` → connect to `localhost:5432`.
- Remote forward (expose a local service to the server): `ssh -R 8080:localhost:3000 host`; the server needs `GatewayPorts` for anything beyond its own loopback.
- SOCKS proxy for a browser: `ssh -D 1080 bastion`.
- Copy through the same jump path: `scp -J bastion file host:/tmp/`, or `rsync -e 'ssh -J bastion'` (→ `files.md`).
- Long operations over SSH belong in `tmux`: a dropped connection during `apt full-upgrade` or a database migration leaves a half-finished transaction (→ `packages.md`).

## Connection Failures Before Authentication

- `Connection refused` — nothing listening on that port: the daemon is down, or bound elsewhere (`ss -tlnp | grep :22` from the console).
- `Connection timed out` — a filter is dropping packets: host firewall, cloud security group, or routing (→ `networking.md`).
- `Permission denied (publickey)` — the daemon answered and rejected you: the table above.
- `Too many authentication failures` — the agent offered too many keys: `IdentitiesOnly yes`.
- `Broken pipe` after idle — missing keepalives: `ServerAliveInterval`.
- `kex_exchange_identification: read: Connection reset` — commonly a rate limiter or intrusion-prevention tool (fail2ban, sshguard) that has banned your address; check its status on the server before touching sshd.

## Record It

How you reach a host is inventory, not memory: put the access reference — and only the reference — in the `Access reference` column of `~/Clawic/data/servers/servers.md` (`file:~/.ssh/id_ed25519_web01`, `keychain:web01-console`, `1password:Infra/web01`). Never a private key, a passphrase, or a password, and never the contents of an `authorized_keys` file the user pastes: public keys are fine, everything alongside them usually is not. Jump-host topology and the out-of-band console for a host belong in the same row's notes or in `## Hosts`. Every `sshd_config` change goes to `changes/<year>.md` with its rollback and how it was verified (`memory-template.md`).

Related: firewall rules and reachability → `networking.md` · account state and sudo → `users.md` · exposure baseline → `hardening.md` · unknown keys in `authorized_keys` → `compromise.md`.
