# `keymap` — manage keymaps

Per-app keyboard mapping management. A "keymap" is a `.playmap` (or legacy `.plist`) file mapping keyboard keys to touch coordinates and actions for an iOS app running under PlayCover.

The `keymap` command is a **group** with eight subcommands. `<bundleId>` identifies the app; `<name>` is the keymap's local name within that app.

---

## `keymap list <bundleId>`

List all keymaps for an app.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Prints one keymap name per line. The default keymap (if any) is marked.
- Exit `3` if the app is not installed.

## `keymap create <bundleId> <name>`

Create a new empty keymap named `<name>` for the app.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Name for the new keymap. |

- Output: `Created keymap <name> for <bundleId>`.
- Exit `2` if a keymap with that name already exists.

## `keymap delete <bundleId> <name>`

Delete a keymap.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Name of the keymap to delete. |

- Output: `Deleted keymap <name>`.
- Exit `2` if the keymap does not exist.

## `keymap rename <bundleId> <oldName> <newName>`

Rename a keymap.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `oldName` (positional) | `String` | Current name. |
| `newName` (positional) | `String` | New name. |

- Exit `2` if `oldName` does not exist or `newName` already exists.

## `keymap set-default <bundleId> <name>`

Mark a keymap as the default for the app (the one used at launch).

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Keymap name to make default. |

- Output: `Default keymap set to <name>`.

## `keymap reset <bundleId> <name>`

Reset a keymap to the default rules from `Rules/default.yaml` (clears custom bindings).

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Keymap name to reset. |

## `keymap import <bundleId> <name> <filePath> [--force]`

Import a keymap from a `.playmap` or `.plist` file (legacy keymap files are also accepted).

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Name to store the keymap under. |
| `filePath` (positional) | `String` | Source `.playmap`/`.plist` file. |
| `--force` | flag | Allow importing even if the file's embedded bundle ID does not match `<bundleId>`. |

- Without `--force`, a mismatch between the file's embedded bundle ID and `<bundleId>` causes exit `4` (`verificationFailed`).
- Exit `2` if the source file does not exist or is not a supported format.

## `keymap export <bundleId> <name> -o|--output <path>`

Export a keymap to a `.playmap` file.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `name` (positional) | `String` | Keymap name to export. |
| `-o` / `--output` | `String` | **Required.** Destination file path. |

- Output: `Exported <name> to <path>`.

---

## Snapshot + restore pattern

```bash
BIN="PlayCover.app/Contents/MacOS/PlayCover"

# Back up the default keymap
$BIN keymap export com.example.app default -o /tmp/example-default.playmap

# Reset to try new bindings
$BIN keymap reset com.example.app default

# Restore if needed
$BIN keymap import com.example.app default /tmp/example-default.playmap --force
```
