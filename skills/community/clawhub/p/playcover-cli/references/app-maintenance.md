# App maintenance commands

Clear caches/PlayChain data, reveal apps or containers in Finder, and prune orphaned files.

These commands perform small, targeted maintenance on installed apps. None of them open a GUI window.

---

## `clear-cache <bundleId>`

Clear the caches of an installed app.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Output: `Clearing caches for <bundleId>...` then `Caches cleared`.
- Exit `3` if the app is not found.

```bash
PlayCover.app/Contents/MacOS/PlayCover clear-cache com.example.app
```

## `clear-play-chain <bundleId>`

Clear PlayChain data for an app (PlayCover's per-app state bridge).

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Output: `PlayChain cleared for <bundleId>`.
- Exit `3` if the app is not found.

## `show-in-finder <bundleId>`

Reveal the installed app bundle in Finder.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- **No stdout output** — this command opens a Finder window (or activates one) revealing the app.
- Exit `3` if the app is not found.

> Note: this does interact with the GUI (Finder), but it is invoked headlessly — PlayCover itself never shows a window.

## `open-container <bundleId>`

Open the app's container directory in Finder.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- **No stdout output** — opens Finder at the container path.
- Exit `3` if the app or its container is not found.

## `prune`

Remove orphaned files left behind by uninstalled apps (stale keymaps, settings, entitlements, containers, PlayChain data whose owning app no longer exists).

| Arg/Flag | Type | Description |
|----------|------|-------------|
| — | — | No arguments. |

- Output: `Pruned orphaned files` (and a summary of what was removed).
- Safe to run periodically as part of a cleanup script.

```bash
# Weekly cleanup via launchd / cron
PlayCover.app/Contents/MacOS/PlayCover prune
```
