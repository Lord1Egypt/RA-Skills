# `dylib` — manage user dylibs

Manage user-supplied dynamic libraries (`.dylib`) attached to an installed app — for tweaks, runtime patches, or third-party iOS frameworks loaded at launch. The `dylib` command is a **group** with three subcommands. `<bundleId>` identifies the app; `<name>` is the dylib's stored name.

---

## `dylib list <bundleId>`

List dylibs attached to an app.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Prints one dylib name per line.
- Exit `3` if the app is not installed.

## `dylib add <bundleId> <dylibPath>`

Attach a `.dylib` file to an app (copied into the app's install).

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `dylibPath` (positional) | `String` | Path to the `.dylib` file. `~` is expanded. |

- Output: `Added dylib <name> to <bundleId>`.
- The dylib is stored under a name derived from the file; use `dylib list` to see it.
- Exit `2` if the file does not exist.
- Exit `3` if the app is not installed.

## `dylib remove <bundleId> <name>`

Remove an attached dylib by its stored name.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Name of the dylib (from `dylib list`). |

- Output: `Removed dylib <name>`.
- Exit `2` if no dylib with that name is attached.

---

## Workflow

```bash
BIN="PlayCover.app/Contents/MacOS/PlayCover"

# Attach a tweak dylib
$BIN dylib add com.example.app ~/tweaks/MyTweak.dylib
$BIN dylib list com.example.app

# Launch to test
$BIN launch com.example.app

# Remove if not needed
$BIN dylib remove com.example.app MyTweak
```
