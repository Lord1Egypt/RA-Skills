# `settings` — per-app settings

View and modify per-app PlayCover settings (the same values exposed in the GUI's per-app settings sheet). The `settings` command is a **group** with four subcommands. `<bundleId>` identifies the app; `<key>` is a settings field name.

---

## `settings list <bundleId> [--json]`

List all settings for an app.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `--json` | flag | Emit JSON instead of text. |

- Text: one `key = value` line per setting.
- JSON: an object of `{ key: value }`, pretty-printed with keys sorted.
- Exit `3` if the app is not installed.

## `settings get <bundleId> <key>`

Read a single setting.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `key` (positional) | `String` | Setting key. |

- Prints the value to stdout (no key prefix).
- Exit `2` if the key does not exist on the app's settings.

## `settings set <bundleId> <key> <value>`

Write a single setting.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `key` (positional) | `String` | Setting key. |
| `value` (positional) | `String` | New value (type is inferred — see below). |

### Type inference

The value's type is inferred from the **existing field's type** via reflection (`Mirror`):

| Existing field type | Accepted `value` |
|---------------------|------------------|
| `Bool` | `true` / `false` |
| `Int` | integer |
| `Float` / `Double` | floating-point number |
| `String` | any text |

- **`metalHUD` is special**: setting it also applies the side effect via `Shell.setMetalHUD`, so the change takes effect system-wide for Metal HUD visibility.
- **`bundleIdentifier` is read-only**: attempting to set it exits `2`.
- Exit `2` if the key does not exist or the value cannot be coerced to the field's type.

```bash
# Disable vsync for an app
PlayCover.app/Contents/MacOS/PlayCover settings set com.example.app gfxApi metal
PlayCover.app/Contents/MacOS/PlayCover settings set com.example.app metalHUD true
```

## `settings reset <bundleId>`

Reset all settings for an app to their defaults.

| Arg | Type | Description |
|-----|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Output: `Settings reset for <bundleId>`.

---

## Common settings keys

The exact set of keys depends on `AppSettings`, but typical fields include:

- `gfxApi` (String) — graphics backend (`metal`, etc.).
- `graphics` (Float/Int) — rendering quality.
- `vsync` (Bool) — vertical sync.
- `metalHUD` (Bool) — Metal performance HUD (also applies a system side effect).
- `disableTimeout` (Bool) — disable app suspension on focus loss.
- `keymap` (String) — currently active keymap name.
- `bundleIdentifier` (String, **read-only**) — the app's bundle ID.

To see the full list for your version, run `settings list <bundleId>`.
