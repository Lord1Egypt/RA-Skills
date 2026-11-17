# Users, Groups, And sudo — Accounts That Behave Predictably

Account state, group membership, and sudo rules fail in ways that read like permission bugs. Check the account before you check the filesystem.

## Reading An Account's Real State

```bash
getent passwd alice          # covers LDAP/SSSD too; /etc/passwd alone does not
id alice                     # uid, gid, and ALL group memberships
passwd -S alice              # P = usable password, L = locked, NP = no password
chage -l alice               # expiry dates — an expired account fails login with no useful message
grep alice /etc/shadow       # `!` or `*` prefix = no password login possible
loginctl user-status alice   # active sessions and lingering
```

- `getent` respects `nsswitch.conf` and therefore sees directory-backed users; every script that greps `/etc/passwd` breaks the day the host joins LDAP or SSSD.
- **`passwd -l alice` locks the PASSWORD only — her SSH key still logs in.** To actually disable an account: `usermod --expiredate 1 alice` (and remove or move `~/.ssh/authorized_keys` if you must be certain). Getting this wrong is a real offboarding incident, not a theoretical one.
- `usermod -s /usr/sbin/nologin` blocks interactive shells but still allows SSH port forwarding and command execution unless the key is restricted (→ `ssh.md`).

## Creating Accounts

- `useradd -m -s /bin/bash -G sudo alice` — `-m` creates the home directory (its absence is why a new user lands in `/` with a broken shell), `-G` adds supplementary groups.
- **`usermod -G` REPLACES the supplementary group list; `usermod -aG` appends.** One missing `-a` removes a user from every group they had, including sudo. Print `id alice` before and after, every time.
- Group changes take effect at the next login. An existing shell keeps its old set: `newgrp <group>` opens a subshell with it, or reconnect. "I added them to the docker group and it still fails" is almost always this.
- UID ranges: system accounts below 1000, humans at 1000 and above (`/etc/login.defs`). Service accounts get `--system --shell /usr/sbin/nologin --no-create-home` unless the service genuinely needs a home.
- Keep numeric UIDs consistent across hosts that share storage (NFS, rsync'd trees, container bind mounts): ownership travels as numbers, never as names (→ `permissions.md`).
- Deleting: `userdel alice` leaves the home directory and every file elsewhere. `userdel -r` removes the home and mail spool; files outside it become orphaned by UID, and the next user created with that UID inherits them. Sweep with `find / -xdev -uid <old-uid>` before reusing.

## Groups

- Primary group (from `/etc/passwd`) owns newly created files; supplementary groups grant access. A setgid directory overrides the primary group for files created inside it (→ `permissions.md`).
- `getent group docker` shows members from all sources; `/etc/group` alone misses directory-backed and primary-only members (a user whose PRIMARY group is `docker` does not appear in the group's member list at all).
- The admin group differs by distro: `sudo` on Debian/Ubuntu, `wheel` on RHEL/Fedora/Arch (→ `distros.md`).
- Membership in the `docker` group (or any group with write access to a container socket) is root-equivalent. Treat granting it as granting root, because it is.

## sudo

- Edit only with `visudo` (or `visudo -f /etc/sudoers.d/ops`): it validates before saving. A syntax error in a file that is already saved means nobody can use sudo, and the fix requires a root shell or single-user boot (→ `boot.md`).
- **Files in `/etc/sudoers.d/` are ignored if the filename contains a dot or ends in `~`.** `ops.conf` never loads; `ops` does. Nothing warns you — the rule just does not exist.
- `sudo -l` prints the effective rules for the current user; `sudo -l -U alice` for someone else. This is the answer to "why can she run that", not a reading of the raw files.
- `env_reset` is on by default and `secure_path` overwrites PATH: a binary in `/opt/bin` works in root's shell and returns "command not found" under sudo. Use an absolute path, or extend `secure_path` in a drop-in.
- Narrow rules are worth the effort, but a rule is only as narrow as the command allows: `alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx` is fine; granting `vim`, `less`, `find`, `awk`, `tar`, or anything with a shell escape (or a `*` in the command path) is granting full root with extra steps.
- `Defaults:alice !requiretty` and `Defaults logfile=/var/log/sudo.log` are the two settings most often needed for automation and for audit, respectively. Command output already lands in the journal via `authpriv` (→ `logs.md`).
- `sudo -i` runs a full login shell as root (root's environment); `sudo -s` keeps yours; `sudo -u www-data -H command` runs as another service account with that account's HOME.

## PAM And Login Limits

- `/etc/security/limits.conf` applies to PAM sessions only — logins and SSH. **systemd services never read it**; their limits come from the unit (→ `processes.md`).
- Order matters in `/etc/pam.d/*`: a misplaced `sufficient` can grant access, a broken `required` line can lock every account out. Test in a second session, always (→ `ssh.md` procedure).
- Lockout policies (`pam_faillock` on RHEL, `pam_tally2`/`faillock` elsewhere) lock accounts after failed attempts; `faillock --user alice --reset` clears it. A user who "suddenly cannot log in with the right password" is often locked, not misconfigured.
- Password policy lives in `pam_pwquality`/`pam_unix` plus `chage` defaults in `/etc/login.defs`; expiry set on service accounts is a scheduled outage nobody scheduled.

## Directory-Backed Users (LDAP / AD / SSSD)

- `nsswitch.conf` decides the order and the sources; `sss_cache -E` invalidates a stale cache after a directory change.
- Offline caching keeps logins working when the directory is unreachable — and also keeps a de-provisioned account working locally until the cache expires. Know the cache lifetime before you rely on central offboarding.
- `getent passwd alice` returning nothing while the directory has the user means the client, not the directory: check `sssd` status and its log before touching the server side.

## Offboarding Checklist

- `usermod --expiredate 1 <user>` (blocks login through every path, unlike `passwd -l`)
- Remove or archive `~/.ssh/authorized_keys`, and check for keys in other accounts' files and in deploy targets
- Revoke sudo: remove from the admin group AND from any `/etc/sudoers.d/` rule naming them
- Terminate live sessions: `loginctl terminate-user <user>`; kill lingering services (`loginctl disable-linger`)
- Reassign or archive files they own: `find / -xdev -user <user>` before the UID is recycled
- Rotate any shared credential they could read — the account is closed, the secret is not (→ `hardening.md`)

## Record It

Account work is change work: every account created or disabled, every sudo rule added, and every group grant that is root-equivalent (docker, wheel, sudo) goes to `~/Clawic/data/linux/changes/<year>.md` with its rollback. An offboarding gets its own row with the checklist items actually completed, because "we removed the account" and "we rotated what she could read" are different claims and only one of them is usually true. If the person is someone the user tracks, they belong in the shared `~/Clawic/data/contacts/contacts.md` — the person keyed by email or handle, with role, channel and one line of context, and never their credentials, hashes, or key material, which are not written anywhere under `~/Clawic/data/`. Their Unix accounts and group grants stay in the change rows here and point at them by name (`memory-template.md`).

Related: filesystem denials → `permissions.md` · SSH key rejection → `ssh.md` · audit and exposure baseline → `hardening.md` · unexpected UID 0 accounts → `compromise.md`.
