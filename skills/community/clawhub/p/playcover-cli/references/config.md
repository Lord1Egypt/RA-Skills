# `config` — global preferences

View and modify PlayCover's **global** preferences (stored in `UserDefaults`, shared across all apps). The `config` command is a **group** with three subcommands. For **per-app** settings, use [`settings`](app-settings.md) instead.

---

## `config list [--json]`

List all configurable global preferences.

| Flag | Type | Description |
|------|------|-------------|
| `--json` | flag | Emit JSON instead of text. |

- Text: one `key = value` line per preference.
- JSON: object of `{ key: value }`, pretty-printed with keys sorted.

## `config get <key>`

Read a single global preference.

| Arg | Type | Description |
|-----|------|-------------|
| `key` (positional) | `String` | Preference key (must be in the allowed set). |

- Prints the value to stdout (no key prefix).
- Exit `2` if `key` is not in the allowed set.

## `config set <key> <value>`

Write a single global preference.

| Arg | Type | Description |
|-----|------|-------------|
| `key` (positional) | `String` | Preference key (must be in the allowed set). |
| `value` (positional) | `String` | New value (type is preserved — see below). |

### Type preservation

The value is coerced to match the **existing value's type** in `UserDefaults`:

| Existing type | Accepted `value` |
|---------------|------------------|
| `Bool` | `true` / `false` |
| `Int` | integer |
| `Double` | floating-point number |

- Exit `2` if `key` is not in the allowed set or the value cannot be coerced.

---

## Allowed keys

Only the following keys are accepted by `config get`/`config set`. Any other key exits `2`.

### Install behavior

| Key | Type | Meaning |
|-----|------|---------|
| `AlwaysInstallPlayTools` | Bool | Inject PlayTools on every install by default. |
| `DefaultAppType` | (Int/String) | Default app category for new installs. |
| `ShowInstallPopup` | Bool | Show the GUI install confirmation dialog. |
| `ShowAppStorePopup` | Bool | Show the App Store redirect dialog. |
| `ShowUninstallPopup` | Bool | Show the GUI uninstall confirmation dialog. |

### Uninstall cleanup

| Key | Type | Meaning |
|-----|------|---------|
| `ClearAppDataUninstall` | Bool | Clear app data on uninstall. |
| `RemoveAppKeymapUninstall` | Bool | Remove keymaps on uninstall. |
| `RemoveAppSettingUninstall` | Bool | Remove settings on uninstall. |
| `RemoveAppEntitlementsUninstall` | Bool | Remove entitlements on uninstall. |
| `RemovePlayChainUninstall` | Bool | Remove PlayChain on uninstall. |

### Updates & security

| Key | Type | Meaning |
|-----|------|---------|
| `SUEnableAutomaticChecks` | Bool | Sparkle automatic update checks. |
| `keyCoverEnabled` | Bool | Enable KeyCover (encryption-at-rest for app keys). |
| `promptForKeyCoverPasswordAtLaunch` | Bool | Prompt for the KeyCover password at launch (vs. on-demand). |

---

## Examples

```bash
BIN="PlayCover.app/Contents/MacOS/PlayCover"

# Always inject PlayTools, suppress the install popup
$BIN config set AlwaysInstallPlayTools true
$BIN config set ShowInstallPopup false

# Snapshot current config
$BIN config list --json > /tmp/playcover-config.json

# Inspect one value
$BIN config get SUEnableAutomaticChecks
```
