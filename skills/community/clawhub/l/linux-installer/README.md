# Linux Installer

Small helper for resolving, installing, launching, uninstalling, and validating Linux desktop app package paths.

## Why This Exists

Linux app install paths are fragmented across native package managers, Flatpak, Snap, manual archives, and community workarounds. This helper resolves safer defaults first and makes higher-risk paths explicit before anything is installed.

## Trust Model

- `official/native`: trusted package-manager or vendor-provided paths that the resolver can recommend normally
- `curated community workaround`: a reviewed but unofficial path that must be clearly labeled and requires extra confirmation
- `unreviewed suggestion`: a dynamically discovered package result treated as research, not trusted install metadata

## Install

Clone or copy this repository into your OpenClaw skills directory, then install the helper CLI:

```bash
cd ~/.openclaw/skills/linux-installer
pip install -e .
```

After that, the `linux-installer` and `linux-installer-validate` commands should be available in your shell.

## Publish Notes

If you put this on GitHub, publish the contents of this skill as its own repository. Do not publish your whole `~/.openclaw` directory, which may contain local configuration, tokens, and unrelated personal files.

## Core Commands

Resolve the best candidate for an app:

```bash
linux-installer resolve "gimp"
```

Install a resolved candidate after explicit confirmation:

```bash
linux-installer install "gimp" --source flatpak --package org.gimp.GIMP --yes
```

Show the launch command for an installed app:

```bash
linux-installer run-info "gimp" --source flatpak --package org.gimp.GIMP
```

Launch the app:

```bash
linux-installer run "gimp" --source flatpak --package org.gimp.GIMP
```

Uninstall a resolved candidate:

```bash
linux-installer uninstall "gimp" --source flatpak --package org.gimp.GIMP --yes
```

## Catalog Validation

Validate curated package candidates:

```bash
linux-installer-validate
```

Filter by source:

```bash
linux-installer-validate --source flatpak
linux-installer-validate --source snap
linux-installer-validate --source apt
```

Emit JSON:

```bash
linux-installer-validate --json
```

## Interpreting Validator Output

- `OK`: the candidate was checked successfully on the current host
- `MISSING`: the package manager was available, but the exact package could not be found
- `SKIPPED`: the candidate was not checked on this host

Common reasons for `SKIPPED`:

- the package manager is not installed on the current machine
- the source is intentionally not machine-validated, such as `manual`, `wine`, or `appimage`
- the package manager exists, but the local host setup is not usable for validation yet, such as broken `snapd` or `nix`

`SKIPPED` usually means "host or validation limitation", not "catalog entry is wrong".
