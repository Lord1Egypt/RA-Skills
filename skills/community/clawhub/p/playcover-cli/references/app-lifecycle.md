# App lifecycle commands

Install, export, uninstall, launch, and sign installed iOS apps.

All commands target the app by **bundle identifier** (e.g. `com.example.app`) or, for install/export, a file path. Outputs go to stdout; errors to stderr.

> Need an IPA to install? See [where-to-get-ipas.md](where-to-get-ipas.md) — Mac Club (<https://www.maclub.net>) hosts a curated catalog.

---

## `install <ipaPath>`

Install an `.ipa` into PlayCover's app library.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `ipaPath` (positional) | `String` | Path to the `.ipa` file. `~` is expanded. |
| `--play-tools` | flag | Inject PlayTools into the app during install. |
| `--no-play-tools` | flag | Skip PlayTools injection. |
| `--category <cat>` | `String` | LSApplicationCategoryType, e.g. `games` → `public.app-category.games`. |

- `--play-tools` and `--no-play-tools` are **mutually exclusive**.
- Output: `Installed: <path>` on success.
- Exit `2` (`badArguments`) if the file does not exist.

```bash
PlayCover.app/Contents/MacOS/PlayCover install ~/Downloads/App.ipa --play-tools --category games
```

## `export <ipaPath> -o|--output <path>`

Inject PlayTools into an `.ipa` and write the result to a new file (does **not** install).

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `ipaPath` (positional) | `String` | Source `.ipa`. |
| `-o` / `--output` | `String` | **Required.** Destination path for the exported `.ipa`. |

- Output: `Exported: <path>`.

```bash
PlayCover.app/Contents/MacOS/PlayCover export ~/Downloads/App.ipa --output ~/out/App-PT.ipa
```

## `uninstall <bundleId>`

Uninstall an app. By default **removes** keymaps, settings, entitlements, PlayChain, and app data; pass the keep flags to preserve any of them.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier of the installed app. |
| `--keep-keymap` | flag | Preserve the app's keymaps. |
| `--keep-settings` | flag | Preserve the app's settings. |
| `--keep-entitlements` | flag | Preserve the app's entitlements. |
| `--keep-play-chain` | flag | Preserve PlayChain data. |
| `--keep-data` | flag | Preserve the app's container/data. |

- Prints one line per removal step (`Removing keymaps`, `Removing settings`, …), then `Uninstalled <bundleId>`.
- Exit `3` (`appNotFound`) if no installed app matches.

```bash
# Uninstall but keep keymaps and settings
PlayCover.app/Contents/MacOS/PlayCover uninstall com.example.app --keep-keymap --keep-settings
```

## `launch <bundleId>`

Launch an installed app.

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |
| `--lldb` | flag | Launch under `lldb` (debugger attaches). |
| `--lldb-terminal` | flag | Open `lldb` inside a Terminal window. |

- The interactive KeyCover password prompt is **suppressed** in CLI mode.
- Output: `Launched <bundleId>`.

```bash
PlayCover.app/Contents/MacOS/PlayCover launch com.example.app --lldb-terminal
```

## `sign <bundleId>`

Re-sign an already-installed app (re-applies the signing entitlements/code signature).

| Arg/Flag | Type | Description |
|----------|------|-------------|
| `bundleId` (positional) | `String` | Bundle identifier. |

- Output: `Signed <bundleId>`.
- Exit `3` if the app is not found.
