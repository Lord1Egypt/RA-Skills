---
name: privileged-operations
description: Safely perform Linux tasks that may require root privileges. Keep work unprivileged by default. When root is genuinely required, make the exact privileged action and reason visible to the user, then elevate only that narrow operation through an interactive authentication path the user can see and control. Prefer pkexec on graphical desktops; use sudo or doas only when their prompt is genuinely visible to the user. Never ask for, capture, pipe, cache, or automate a user's password, and never silently fall back to hidden or broad root execution.
---

# Privileged Operations

Safely handle Linux work that crosses the root privilege boundary.

## Core rule

> **Stay unprivileged until one specific operation genuinely requires root. Show the user what needs root and why, then elevate only that operation through a visible, interactive authentication path.**

Root access is not merely a technical capability. It is a human approval boundary.

The user should be able to notice:

- that an operation needs root;
- what exact operation is being authorised;
- why elevation is necessary;
- when authentication is being requested;
- whether they want to approve or cancel it.

Do not hide that boundary behind automation.

The default workflow is:

```text
inspect as user
→ diagnose as user
→ download/build/generate as user
→ validate as user
→ identify the exact privileged step
→ show the user the command/action and reason
→ request visible interactive authentication
→ run only that privileged step
→ verify as user
```

Do not become root first and then perform the task.

---

## 1. Decide whether root is actually required

Before elevating, be able to complete this sentence:

> "This exact operation needs root because ________, and the rest of the task does not."

If the reason is unclear, investigate first.

Operations that normally stay unprivileged include:

- editing files in `$HOME`;
- cloning, extracting, compiling, testing, and generating files;
- `make`, `cmake`, `meson`, `ninja`, `cargo`, Python, and Node project tooling;
- `systemctl --user ...`;
- `makepkg`, `yay`, and `paru` build/orchestration work that is designed to run as the normal user.

Root may legitimately be needed for:

- system package transactions;
- protected writes under `/etc`, `/usr`, `/opt`, `/boot`, and similar paths;
- system-level services;
- system-owned permissions or ownership;
- firewall, mount, kernel, boot, or device configuration;
- the final install step of a completed build into a protected prefix.

Even then, elevate only the protected operation.

---

## 2. Make the privilege boundary visible

Before a privileged mutation, surface the narrow action and reason to the user.

Good mental model:

```text
Needs root: install validated config into /etc/example/
Privileged action: /usr/bin/install -Dm644 ./example.conf /etc/example/example.conf
Why: destination is root-owned
```

The wording does not need to be ritualistic, but the user must have enough information to understand what the authentication request corresponds to.

Do not trigger a password/authentication prompt with no visible context when the environment lets you explain first.

Authentication is approval for the stated operation, not blanket approval for unrelated later root work.

---

## 3. Choose an interactive elevation path

### Graphical desktop: prefer `pkexec`

When a graphical polkit authentication agent is available, prefer:

```sh
pkexec <program> <arguments...>
```

This keeps the authentication step separate from the agent and normally gives the user a desktop approval/password dialog.

Prefer invoking the real executable directly:

```sh
pkexec /usr/bin/install -Dm644 ./example.conf /etc/example/example.conf
```

Avoid a privileged shell when a direct command works:

```sh
pkexec sh -c 'cp ./example.conf /etc/example/example.conf'
```

A privileged shell expands the authority and increases quoting and injection risk.

Before depending on `pkexec`, check that it exists. If no usable polkit authentication agent is available, report that rather than pretending the action was authorised.

### Visible terminal: `sudo` or `doas` may be acceptable

`sudo` or `doas` may be used only when all of the following are true:

- the command runs in a terminal/session the user can actually see;
- the user can see the command or has just been told exactly what privileged action is about to run;
- any authentication prompt is visible to the user;
- the user enters credentials directly into that trusted prompt;
- the privileged scope remains narrow.

Do not use `sudo` or `doas` merely because `pkexec` is unavailable if their prompt would be hidden from the user.

Do not treat cached authentication as permission for unrelated root work. If the chosen mechanism would make the elevation invisible, stop and re-establish a visible approval boundary.

### Never use hidden credential paths

Never:

- ask the user to send their password in chat;
- read, store, log, echo, or capture a password;
- pipe a password to an elevation tool;
- use `sudo -S`;
- use `sshpass` or equivalent password automation for local root elevation;
- put a password in a command, script, environment variable, or temporary file;
- create passwordless privilege rules merely to avoid prompts;
- silently open a root shell;
- silently substitute one elevation mechanism for another when that changes what the user can see or approve.

The password belongs to the authentication system and the user, not to the agent.

---

## 4. Keep the privileged boundary narrow

Prefer one understandable root operation over a privileged command chain.

Good:

```sh
make
pkexec /usr/bin/make install
```

Riskier:

```sh
pkexec /bin/bash
make
make install
```

The second version unnecessarily gives the entire build root authority and can leave root-owned files in the user's work tree.

Avoid:

```sh
pkexec sh -c 'command1 && command2 && command3 && command4'
```

when only part of the chain needs root.

Do not start a persistent root shell by default. Treat an interactive root shell as exceptional and use it only when the user explicitly wants that mode and the work cannot reasonably be reduced to bounded commands.

The goal is not the fewest prompts. The goal is the smallest understandable privilege boundary.

---

## 5. Resolve paths and environment before elevation

Privilege tools often use a different or restricted environment. Do not assume preservation of:

- `PATH`;
- aliases or shell functions;
- virtual environments;
- custom library paths;
- project variables;
- `HOME`;
- desktop/session variables.

Resolve important paths before elevation and pass explicit arguments.

For sensitive commands, prefer known absolute executable paths where practical:

```sh
command -v systemctl
pkexec /usr/bin/systemctl restart example.service
```

Quote paths and variables, and use `--` before path operands where supported:

```sh
pkexec /usr/bin/rm -- "$file"
```

Do not trust a project-local executable merely because its name resembles a system program.

---

## 6. Build and generate as the normal user

Keep compilation, downloads, code generation, project scripts, extraction, and testing unprivileged.

Preferred pattern:

```text
build as user → test as user → validate → elevate final protected install → verify as user
```

This avoids root-owned build artefacts, poisoned user caches, and arbitrary build scripts running with full system access.

If a privileged operation unexpectedly creates root-owned files inside a user work tree, identify the exact affected paths and repair only those paths.

Never use a broad repair such as:

```sh
pkexec chown -R "$USER:$USER" "$HOME"
```

That can damage files intentionally owned by root or another user.

---

## 7. Package managers

Never run user-oriented build helpers as root merely to bypass their privilege model.

On Arch-family systems, for example:

- inspect/build AUR packages as the normal user;
- use the package manager for the final system transaction;
- elevate only that system transaction.

Example:

```sh
makepkg
pkexec /usr/bin/pacman -U ./package-name-*.pkg.tar.zst
pacman -Q package-name
```

A direct system package transaction may legitimately require root:

```sh
pkexec /usr/bin/pacman -S --needed package-name
```

If a visible terminal workflow is deliberately being used instead, the equivalent `sudo`/`doas` command is acceptable only under the interactive-visibility rules above.

Before broad installs, upgrades, or removals, inspect the proposed transaction. Do not add non-interactive confirmation flags by default to potentially destructive package operations.

---

## 8. Systemd

Determine whether a unit is user-level or system-level before elevating.

```sh
# user unit
systemctl --user restart example.service

# system unit on a desktop with polkit
pkexec /usr/bin/systemctl restart example.service
```

Do not elevate user services unnecessarily.

After changing a system unit, reload only when needed, then perform the exact intended action: start, stop, restart, reload, enable, disable, mask, or unmask. These are not interchangeable.

Verify afterwards:

```sh
systemctl status example.service
journalctl -u example.service -n 50 --no-pager
```

If reading the journal itself requires root, elevate only that read operation.

---

## 9. Edit protected files through staged replacement

Avoid launching a full editor as root.

Use this pattern:

1. read the existing file unprivileged where possible;
2. create a user-owned working copy or replacement;
3. edit and validate it as the normal user;
4. inspect the diff;
5. create a backup or rollback point when warranted;
6. install the final file with one narrow privileged command;
7. validate the installed result.

Example:

```sh
cp /etc/example.conf ./example.conf.new
# edit and validate ./example.conf.new

diff -u /etc/example.conf ./example.conf.new
pkexec /usr/bin/cp -a /etc/example.conf /etc/example.conf.bak
pkexec /usr/bin/install -m 644 ./example.conf.new /etc/example.conf
```

Adapt ownership, permissions, ACLs, extended attributes, security labels, and other metadata to the actual target. `0644` is not universally correct.

Before overwriting a protected target, determine whether it is a file, directory, symlink, mount point, generated file, or package-owned file.

Prefer supported overrides, drop-ins, `/etc` configuration, or `/usr/local` installation over directly editing package-owned vendor files under `/usr`.

---

## 10. Protected redirection

Shell redirection may happen before the elevated program starts, so this is wrong:

```sh
pkexec echo "value" > /etc/example.conf
```

For a short stream, narrowly scoped `tee` may be appropriate:

```sh
printf '%s\n' "value" | pkexec /usr/bin/tee /etc/example.conf >/dev/null
```

For non-trivial files, generate and validate the file as the normal user, then install it with a narrow privileged command.

---

## 11. Downloads and third-party installers

Do not download changing remote content directly into protected system paths as root.

Prefer:

```text
download as user → verify → inspect/extract/build as user → elevate final install only
```

Avoid:

```sh
curl ... | pkexec sh
curl ... | sudo sh
```

If upstream documentation says the whole installer must run as root:

1. inspect the installer first;
2. determine which parts actually need root;
3. prefer a documented staged or non-root route where available;
4. never pipe a remote script directly into a privileged shell;
5. treat unavoidable full-root execution as materially higher risk and make that risk visible to the user.

An interactive password prompt does not make an opaque root installer safe.

---

## 12. Validate, back up, and define rollback

Do as much validation as possible before elevation: syntax checks, diffs, unit verification, package state, hashes/signatures where applicable, free space, binary tests, destination checks, and device/mount checks.

For configuration changes, prefer:

```text
generate → diff → validate → backup → privileged install → validate again
```

For risky changes, know the rollback path before applying them.

If rollback is difficult or impossible, say so before making the change.

---

## 13. Destructive operations need stronger checks

Treat privileged destructive commands as high risk, especially:

- `rm -rf`, recursive `chmod`, or recursive `chown`;
- `dd`, `mkfs.*`, `fdisk`, `sfdisk`, `parted`, or `wipefs`;
- mounts and unmounts;
- broad package removals;
- `systemctl disable` or `mask`;
- firewall changes;
- bootloader, initramfs, `/boot`, or EFI operations;
- kernel parameters and block-device changes.

Before running them:

- identify the exact target;
- surface the action to the user;
- resolve variables before elevation;
- reject empty or suspicious path values;
- inspect symlinks where relevant;
- verify device/mount state;
- understand what will be removed or overwritten;
- establish rollback or backup where practical.

Never construct a privileged recursive deletion from an unchecked variable.

Never guess between ambiguous destructive targets. If the target cannot be established confidently, stop rather than choosing one.

---

## 14. Do not weaken security to avoid prompts

Never solve privilege friction by permanently making the system less secure.

Do not:

- make protected files world-writable;
- give broad system directories to the user;
- add blanket passwordless polkit, sudo, or doas rules;
- disable authentication;
- set unsafe setuid bits;
- grant broad Linux capabilities when a narrower solution exists;
- run long-lived services as root unnecessarily.

A visible one-time authentication step is preferable to a permanent privilege hole.

---

## 15. Failure handling

Authentication success does not prove the command succeeded.

After every privileged change, inspect the exit status and verify the resulting state.

If a privileged operation fails:

1. stop;
2. inspect the actual error;
3. determine whether anything changed before the failure;
4. do not blindly rerun the same command;
5. roll back if a broken intermediate state was created and rollback is appropriate;
6. report what succeeded, what failed, and what remains uncertain.

Do not stack more privileged changes on top of an unknown partial state.

Prefer idempotent commands where practical, and check before appending settings that could duplicate on rerun.

---

## Operating rules

- **Root is a human approval boundary, not just a permission bit.**
- **Show the privileged action and reason before requesting authentication.**
- **Prefer `pkexec` when a graphical polkit prompt is available.**
- **Use `sudo`/`doas` only through a genuinely user-visible interactive terminal path.**
- **Never handle the user's password yourself.**
- **Never silently broaden or substitute the elevation mechanism.**
- **Elevate the smallest necessary operation.**
- **Build, inspect, download, and test unprivileged.**
- **Authentication is not proof of successful mutation; verify afterwards.**
- **If the approval boundary cannot be made visible, report the blocker instead of hiding it.**
