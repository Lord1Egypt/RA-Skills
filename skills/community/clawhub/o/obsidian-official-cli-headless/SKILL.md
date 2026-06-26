---
name: obsidian-official-cli-headless
description: Install and adapt the official Obsidian CLI for headless Linux servers by using a non-root user, Xvfb virtual display, ACL-based vault access, and an obs wrapper command. Use when the user wants the official Obsidian CLI (not notesmd-cli) on a Debian/Ubuntu-like machine without a normal desktop session, or when root/GUI/display constraints break native CLI use.
---

# Obsidian Official CLI Headless

Treat the official Obsidian CLI as a **desktop-first app adaptation problem**, not a normal CLI install.

## Core rules

- Use this skill only for the **official** Obsidian CLI.
- Assume headless Linux needs a dedicated non-root user, `Xvfb`, and a wrapper command.
- Prefer ACLs over ownership changes when the vault lives under `/root`.
- Prefer one target vault.
- Keep the user away from `su - obsidian` and display details by exposing `/usr/local/bin/obs`.

## Fast path

1. Confirm the vault path. Default to `/root/obsidian-vault` only if the user does not specify another path.
2. Run `scripts/install_official_obsidian.sh` as root.
3. Run `scripts/configure_official_cli.sh <vault_path>` as root.
4. Run `scripts/verify_official_cli.sh [vault_path]`.
5. Report the wrapper path, active vault, verified commands, and remaining caveats.

## What this skill owns

- Official Obsidian `.deb` install
- Headless runtime dependencies needed for field use
- Dedicated `obsidian` user
- Official CLI enablement via `~/.config/obsidian/obsidian.json`
- Vault access via ACLs
- `/usr/local/bin/obs` wrapper
- Verification of `help`, `vault`, `daily:path`, `daily:append`, `daily:read`, and `search`

## What not to do

- Do not use this skill for `notesmd-cli` or lightweight markdown-only workflows.
- Do not expand into plugins, sync setup, theme tuning, or full desktop environment work unless the user explicitly asks.
- Do not broaden permissions more than needed.

## Wrapper model

The wrapper should effectively run:

```bash
su - obsidian -c 'cd <vault> && xvfb-run -a /usr/bin/obsidian --disable-gpu ...'
```

That is the stable operating model on a headless host.

## Verification commands

Use at minimum:

```bash
obs help
obs vault
obs daily:path
obs daily:append content="skill verification"
obs daily:read
obs search query="skill verification"
```

## References

- Read `references/architecture.md` when you need the rationale for non-root user, Xvfb, ACLs, or wrapper design.
- Read `references/troubleshooting.md` when the install works partially but CLI behavior still fails.

## Report format

Keep the result short:
- installed version
- wrapper path
- active vault path
- verified commands
- remaining limits
