# `alias` — manage app aliases

Manage aliases (shortcuts) to installed PlayCover apps, placed under `~/Applications/PlayCover/`. Aliases let users launch PlayCover apps from the regular Applications folder / Spotlight / Dock, separate from the PlayCover app itself.

The `alias` command is a **group** with two subcommands.

---

## `alias create <bundleId>`

Create an alias for an installed app in `~/Applications/PlayCover/`.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier of the installed app. |

- Output: `Alias created for <bundleId>`.
- Exit `3` if the app is not installed.

```bash
PlayCover.app/Contents/MacOS/PlayCover alias create com.example.app
```

## `alias remove <bundleId>`

Remove a previously-created alias.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Output: `Alias removed for <bundleId>`.
- Does not uninstall the app itself — only the alias.

```bash
PlayCover.app/Contents/MacOS/PlayCover alias remove com.example.app
```

## Notes

- Aliases live in `~/Applications/PlayCover/`, not in `/Applications`.
- Removing an alias is **not** the same as uninstalling; use `uninstall <bundleId>` for that.
- Re-creating an alias for an app that already has one overwrites the existing alias.
