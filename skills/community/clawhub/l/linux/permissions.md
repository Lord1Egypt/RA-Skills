# Permissions — Why "Permission Denied" Is Almost Never About chmod

Six independent layers can deny the same open(): mode bits, ownership, ACLs, mount options, MAC (SELinux/AppArmor), and unit sandboxing. `chmod` only touches the first. Walk the layers in this order — each check is one command.

## The Denial Ladder

| # | Layer | Check | Fix |
|---|---|---|---|
| 1 | Path traversal | `namei -l /full/path` | Every directory needs `x` for the running uid; the first failing component is the bug |
| 2 | Owner/group vs the real uid | `ps -o user,group -p <pid>` vs `ls -ln` | Compare NUMERIC ids — names lie across containers, NFS, and LDAP |
| 3 | ACLs | `getfacl <path>` (`+` in `ls -l`) | The `mask` line caps every named entry; a grant of `rwx` under `mask::r--` is effectively `r--` |
| 4 | Mount options | `findmnt -T <path>` | `noexec` (EACCES on execute), `nosuid`, `ro`, `nodev` — invisible to `ls` |
| 5 | MAC | `ls -Z`, `ausearch -m avc -ts recent`, `aa-status` | SELinux label or AppArmor profile (below) |
| 6 | Unit sandboxing | `systemd-analyze security <unit>` | `ProtectSystem=strict`/`ProtectHome`/`PrivateTmp` deny a service what root can do by hand |
| else | Immutable / capability | `lsattr <path>`, `getcap <binary>` | `chattr -i`; caps replace root entirely |

Rule of thumb for triage: works as root by hand but fails as the service → layers 5 and 6. Fails for root too → layer 4 or `chattr +i`.

## Mode Bits That Are Not Obvious

- Directory `x` = traverse, `r` = list names, `w` = create/delete entries. `w` on a directory lets a user delete files they do not own — unless the sticky bit (`chmod +t`, as on `/tmp`) is set.
- Recursive fix without breaking directories: `chmod -R u=rwX,go=rX <dir>` — capital `X` sets execute only on directories and on files that already had it. `chmod -R 644` strips directory `x` and locks the whole tree.
- Setuid is ignored on scripts by kernel policy (the shebang race). Only binaries honour it — use a sudoers rule or a file capability.
- Setgid on a directory (`chmod 2775`) makes new entries inherit the directory's group; without it every file lands in the creator's primary group and shared work breaks one file at a time.
- Default umask 022 makes every new file world-readable. 077 on multi-user or sensitive hosts; set it in `/etc/login.defs` (`UMASK`) plus the service's unit (`UMask=`), because a daemon never reads your shell profile.

## ACLs

```bash
setfacl -m u:deploy:rwx  /srv/app          # one user, this directory
setfacl -d -m g::rwx     /srv/app          # DEFAULT acl: applies to entries created later, not existing ones
setfacl -R -m g:web:rX   /srv/app          # existing entries; capital X again
getfacl /srv/app                            # read the mask line before believing any grant
```

- Shared team directory, complete recipe: `chmod 2775 dir` (setgid) + `setfacl -d -m g::rwx dir`. Setgid fixes the group, the default ACL fixes the mode.
- `chmod` on a file WITH ACLs rewrites the mask — a `chmod 640` silently neuters every named ACL entry. Re-run `getfacl` after any chmod on an ACL'd tree.
- Not every filesystem carries ACLs: check `findmnt -o TARGET,OPTIONS` for `acl` (ext4 has it by default since 3.x kernels; some NFS and tmpfs mounts do not).

## SELinux (RHEL, Fedora, CentOS Stream — enforcing by default)

- Denial signature: the operation fails with EACCES while mode bits and owner are perfect, and `ausearch -m avc -ts recent` prints an AVC line naming source context, target context, and the class.
- `mv` preserves the source context, `cp` inherits the destination's. A file moved into `/var/www` keeps `user_home_t` and the web server is denied; `restorecon -v <file>` re-labels it from policy.
- Persistent custom paths need the policy updated, not just the label: `semanage fcontext -a -t httpd_sys_content_t "/srv/app(/.*)?" && restorecon -Rv /srv/app`. A bare `chcon` is lost at the next relabel.
- Many denials are a boolean, not a label: `getsebool -a | grep httpd` then `setsebool -P httpd_can_network_connect on`. Reach for booleans before writing policy.
- `audit2allow -a -M mypol` generates a module from the actual denials — read the generated `.te` before installing it; it will happily grant far more than you meant.
- `setenforce 0` is a diagnostic, not a fix: it proves SELinux is the layer, does not survive reboot, and leaves the real label bug in place. Put it back with `setenforce 1` in the same session.
- Bulk relabel after restoring files from a backup: `touch /.autorelabel && reboot` (→ `boot.md`).

## AppArmor (Debian, Ubuntu, SUSE)

- `aa-status` lists profiles in enforce vs complain mode; denials land in `dmesg`/`journalctl -k` as `apparmor="DENIED"` with the profile name and the exact path.
- Path-based, not label-based: moving a file changes nothing, but a symlink or a bind mount to a path outside the profile is denied.
- `aa-complain /etc/apparmor.d/usr.sbin.nginx` to log instead of block while you learn the rule set, then `aa-enforce` again. `apparmor_parser -r <profile>` reloads after editing.

## Capabilities (the root replacement)

- `setcap cap_net_bind_service=+ep /usr/local/bin/app` lets an unprivileged binary bind port 80 with no setuid. `getcap -r /usr/bin 2>/dev/null` audits what already has caps.
- Capabilities live in xattrs: **lost on package upgrade, on plain `cp`, and on any tar without `--xattrs`**. Re-apply after every upgrade of a binary you granted caps to, or move the grant into the unit (`AmbientCapabilities=CAP_NET_BIND_SERVICE` + `CapabilityBoundingSet=`).
- Prefer `AmbientCapabilities` in a systemd unit over setcap on disk: it survives upgrades and is visible in the unit file where the next admin will look.

## The Root-Is-Not-Omnipotent List

- `chattr +i file` blocks writes, renames, and deletes for root; `lsattr` shows it. Common on hardened hosts and on files a config-management tool wants to keep.
- SELinux denies root by policy — root running in `unconfined_t` is not root running in `httpd_t`.
- A read-only mount (`findmnt`) or a full filesystem produces errors that read like permission bugs; check both before touching modes.
- File capabilities can strip root: a binary with an empty bounding set cannot regain privileges even when euid is 0.

## Ownership Operations

- `chown -R` follows symlinks that point outside the target — use `-h`/`--no-dereference`, or `find <dir> -xdev -exec chown -h user:group {} +` for a bounded sweep.
- `chown` across filesystems does nothing surprising, but `mv` across filesystems is copy+delete: the new file gets a fresh inode, loses hardlinks, and re-derives its SELinux label from the destination.
- Numeric ids are the contract with containers and NFS: `chown 10001:10001` beats `chown appuser:appuser` when the same tree is mounted somewhere whose `/etc/passwd` differs.

## sudo Denials That Are Not Permission Bugs

- `sudo` resets PATH to `secure_path` from sudoers: a binary in `/opt/bin` runs fine in root's shell and returns "command not found" under `sudo`. Use the absolute path or extend `secure_path` in a sudoers drop-in.
- Files in `/etc/sudoers.d/` are ignored if the name contains a dot or ends in `~` — `myrule.conf` never loads and nothing warns you (→ `users.md`).
- Redirection happens in YOUR shell before sudo runs: `sudo echo x > /etc/f` fails. `echo x | sudo tee /etc/f`, or `sudo sh -c 'echo x > /etc/f'`.

## Record It

A denial that took six layers to find is worth exactly one file: the SELinux fcontext rule, the boolean, the ACL recipe, or the `ReadWritePaths=` set that finally worked goes to `~/Clawic/data/linux/artifacts/policy-<service>.md` — what it unblocked, the commands, and the date — with its `## Boxes` line in `memory.md`. Applying it is a change (`changes/<year>.md`, with `semanage fcontext -d` or the equivalent as the rollback). The second time the same class of denial appears on the same host, it is a pattern for `## Recurring Incidents` (`memory-template.md`).

Related: unit-level denials → `systemd.md` · SSH key permission rejections → `ssh.md` · users, groups, and sudoers structure → `users.md` · sandboxed desktop apps denied by confinement → `desktop.md`.
