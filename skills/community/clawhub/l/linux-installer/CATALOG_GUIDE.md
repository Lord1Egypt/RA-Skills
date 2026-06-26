# Catalog Guide

The catalog should cover the awkward 10% to 20% of apps that need human judgment, not every package on Linux.

For the easy 80% to 90%, the resolver already does useful work by:

- preferring curated catalog entries when present
- discovering official/native package matches dynamically
- surfacing unreviewed Flatpak or Snap suggestions only as an unsafe fallback

That means a new catalog entry is worth adding when at least one of these is true:

- the app has multiple install paths and one is clearly safer or more stable
- the Linux package name does not match the app name well
- the app only works through a curated community workaround
- the app only has a manual archive or AppImage path
- the app needs special warnings, manual steps, or a custom launch command
- the app is popular enough that users will hit the edge case repeatedly

## Fast Triage

Use this decision order to avoid spending hours on every app:

1. Check whether the app is already handled well by dynamic discovery.
2. If dynamic discovery would return a safe and obvious package name, do not add a catalog entry yet.
3. Add a curated entry only when it improves safety, naming, launch reliability, or user guidance.
4. Prefer one strong candidate over many speculative candidates.
5. Only add manual or community entries when you can clearly label risk and source.

## Recommended Entry Shapes

Keep entries small. Most apps should fit one of these patterns.

### 1. Official package with a stable launcher

Use this when the Linux package is trustworthy and the launch command is obvious.

```json
{
  "source": "flatpak",
  "package": "org.example.App",
  "install": [
    ["flatpak", "install", "-y", "flathub", "org.example.App"]
  ],
  "launch": ["flatpak", "run", "org.example.App"],
  "reason": "Official Flatpak app ID with a stable launcher."
}
```

### 2. Native package fallback

Use this when the package manager name is straightforward and no extra warning is needed.

```json
{
  "source": "apt",
  "package": "example-app",
  "install": [
    ["sudo", "apt-get", "install", "-y", "example-app"]
  ],
  "launch": ["example-app"],
  "reason": "Native Debian-family package fallback when Flatpak is unavailable."
}
```

### 3. Official manual archive fallback

Use this when the vendor publishes Linux builds but not a package-manager install.

```json
{
  "source": "manual",
  "package": "example-linux",
  "source_url": "https://example.com/download/linux",
  "manual_steps": [
    "Download the official Linux build from the source URL.",
    "Extract or place it into ${HOME}/.local/opt/example/.",
    "Launch the binary from that folder."
  ],
  "launch": ["${HOME}/.local/opt/example/example-app"],
  "reason": "Curated official manual fallback using the vendor's Linux download.",
  "warnings": [
    "This path is manual and should not be auto-installed by the helper."
  ],
  "recipe": {
    "kind": "official_archive",
    "install_location": "${HOME}/.local/opt/example",
    "binary_name": "example-app"
  }
}
```

### 4. Curated Wine fallback

Use this only when there is no reasonable Linux-native path.

```json
{
  "source": "wine",
  "package": "exampleapp",
  "install": [
    [
      "env",
      "WINEPREFIX=${HOME}/.local/share/linux-installer/exampleapp",
      "winetricks",
      "-q",
      "corefonts"
    ]
  ],
  "launch": [
    "env",
    "WINEPREFIX=${HOME}/.local/share/linux-installer/exampleapp",
    "wine",
    "C:\\\\Program Files\\\\ExampleApp\\\\example.exe"
  ],
  "source_url": "https://example.com/download",
  "manual_steps": [
    "Download the official Windows installer from the source URL.",
    "Run the installer inside the configured WINEPREFIX.",
    "Launch the app through the configured Wine command."
  ],
  "reason": "Curated Wine fallback for systems without a usable package wrapper.",
  "warnings": [
    "This fallback requires the user to download and run the official installer manually.",
    "Wine-based installs are higher risk and may require manual follow-up."
  ],
  "recipe": {
    "kind": "manual",
    "installer_source": "Official installer from the vendor website",
    "wineprefix": "${HOME}/.local/share/linux-installer/exampleapp"
  }
}
```

### 5. Curated community workaround

Use this when the app has no official Linux version but a widely known workaround exists.

```json
{
  "source": "flatpak",
  "package": "org.example.Workaround",
  "install": [
    ["flatpak", "install", "-y", "flathub", "org.example.Workaround"]
  ],
  "launch": ["flatpak", "run", "org.example.Workaround"],
  "reason": "Curated community workaround distributed on Flathub.",
  "warnings": [
    "This is not official vendor software.",
    "The workaround is community-maintained and may break or be discontinued."
  ],
  "community": true,
  "community_label": "Community workaround",
  "upstream_name": "Workaround"
}
```

## Minimal Safety Standard

Before adding an entry, try to satisfy this checklist:

- `display_name` is human-friendly
- `aliases` cover the common user spellings
- `search_terms` cover the names people will actually type
- every candidate has a short `reason`
- manual entries include `manual_steps`
- community entries include `community: true` and clear warnings
- Wine entries include both warnings and a scoped `WINEPREFIX`
- `launch` is explicit whenever the package name is not the launcher name

## What Not To Add

Skip or postpone entries like these:

- obscure apps with no clear official source
- entries that only duplicate obvious native package names
- community packages you have not personally reviewed enough to label safely
- package-manager variants that add no practical value
- manual entries with vague install directions like "extract and run somehow"

## Suggested Backlog Order

If you want to reach broad coverage quickly, add entries in this order:

1. Popular Windows-first apps that need aliases or curated fallbacks
2. Popular apps with official Linux downloads but no package-manager package
3. Apps with misleading package names or non-obvious launch commands
4. High-demand community workarounds that need extra confirmation
5. Lower-traffic apps only after users actually ask for them

## Working Rule Of Thumb

If an entry takes more than about 10 to 15 minutes to verify, it usually belongs in one of these buckets:

- leave it to dynamic discovery for now
- add a minimal manual/community fallback with strong warnings
- skip it until a real user asks for it

## Validation Loop

For ongoing maintenance, use two layers:

1. Structural validation:

```bash
python -m py_compile skills/linux-installer/main.py skills/linux-installer/validate_catalog.py
python skills/linux-installer/main.py resolve "gimp"
```

2. Package existence validation for curated candidates:

```bash
python skills/linux-installer/validate_catalog.py
```

Useful focused checks:

```bash
python skills/linux-installer/validate_catalog.py --source flatpak
python skills/linux-installer/validate_catalog.py --source snap
python skills/linux-installer/validate_catalog.py --json
```

The validator intentionally skips `manual`, `wine`, and `appimage` entries because those sources are not reliably machine-verifiable in the same way.

When reading validator output:

- `OK` means the package was confirmed through the source available on the current host
- `MISSING` means the package manager was available and the exact package could not be found
- `SKIPPED` usually means a host limitation, missing package manager, or intentionally unvalidated source rather than a broken catalog entry
