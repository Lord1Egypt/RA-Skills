---
name: linux-installer
description: Installs, launches, and uninstalls Linux desktop apps by resolving the safest supported source first, then running a local helper CLI. Use when the user asks to install software like GIMP, Notepad++, or other desktop apps on Linux and wants the install command plus the command to launch or remove it.
---

# Linux Installer

## What This Skill Does

Resolves the best supported install path for a Linux desktop app, explains the recommendation briefly, asks for confirmation before any system change, performs the install, and returns the exact launch or uninstall command.

If the chosen source needs missing tooling like `snapd`, `flatpak`, `wine`, or `winetricks`, the helper can bootstrap that tooling first through the host's native package manager.

It can also return curated community workarounds when no official Linux package exists. These must be clearly labeled and require an extra explicit confirmation before install.

When no curated or official path exists, the helper may surface unreviewed community suggestions from public package metadata. These are research results, not trusted install metadata.

Default source preference is:

1. Flatpak
2. Snap
3. Native package manager
4. openSUSE `zypper`
5. Arch `pacman`
6. Native Arch AUR helper
7. Nix profile install
8. AppImage
9. Curated official manual/archive fallback
10. Curated Wine/manual fallback

Community workarounds are only allowed when they are explicitly curated in the catalog.

Unreviewed community suggestions may be installed only when:

1. `skills.entries.linux-installer.unsafeCommunityInstalls` is enabled in `openclaw.json`
2. the user explicitly confirms the unreviewed install
3. the install command includes `--allow-unsafe`

## Prerequisites

Before using this skill, ensure the helper CLI is installed:

```bash
cd ~/.openclaw/skills/linux-installer
pip install -e .
```

## Workflow

If you are expanding curated coverage, use [CATALOG_GUIDE.md](./CATALOG_GUIDE.md) to decide which apps belong in `catalog.json` and which should rely on dynamic discovery.

When the user asks to install an app:

1. Resolve the best path:

```bash
linux-installer resolve "gimp"
```

2. Summarize the result:
   - chosen source
   - package id
   - whether it is an official package, fallback, or community workaround
   - whether it is curated or unreviewed
   - missing tooling, if any
   - tooling bootstrap command, if any
   - source URL, if available
   - public summary and any best-effort review note
   - exact install command
   - launch command
   - warnings or fallbacks

3. Ask for confirmation before installing.

4. If the selected result is a community workaround, ask for a second explicit confirmation that acknowledges it is unofficial/community-maintained.

5. If the selected result is an unreviewed suggestion, explain that:
   - it was discovered dynamically from public package metadata
   - it is not maintainer-reviewed
   - opt-in support for unreviewed suggestions must be enabled first
   - it requires a separate unreviewed-install confirmation

6. After confirmation, run:

```bash
linux-installer install "gimp" --source flatpak --package org.gimp.GIMP --yes
```

For a community workaround, include `--allow-community`:

```bash
linux-installer install "roblox" --source flatpak --package org.vinegarhq.Sober --yes --allow-community
```

For an unreviewed suggestion, include `--allow-unsafe` and ensure opt-in support for unreviewed suggestions is enabled in `openclaw.json`.

7. Return the launch command:

```bash
linux-installer run-info "gimp" --source flatpak --package org.gimp.GIMP
```

8. Optionally launch the installed app:

```bash
linux-installer run "gimp" --source flatpak --package org.gimp.GIMP
```

9. For removal, prefer the helper's uninstall command. If the result is a manual or unsafe removal path, return the command or manual steps instead of improvising:

```bash
linux-installer uninstall "gimp" --source flatpak --package org.gimp.GIMP --yes
```

## Rules

- Never install anything before the user confirms.
- Never install a community workaround without a second explicit confirmation.
- Never install an unreviewed suggestion unless opt-in support is enabled and the user explicitly accepts the unreviewed path.
- Prefer the helper CLI output over ad hoc shell reasoning.
- If `resolve` says no safe automated path was found, do not invent install steps.
- Manual/archive fallbacks may surface curated `manual_steps`, but the helper must not auto-download or auto-run them.
- Manual/archive and other unsafe removal flows may surface `manual_steps`, but the helper must not auto-delete them unless the uninstall path is explicitly curated and safe.
- Wine/manual flows are higher risk and should be presented as fallback options, not defaults.
- Community workarounds must be presented as unofficial, curated alternatives.
- Unreviewed suggestions must be presented as research findings, not trusted recommendations.
- Always tell the user the exact command to launch the app after install.
