# info.toml Reference

The `info.toml` file specifies metadata for an Openplanet plugin. Format: [TOML](https://toml.io/en/latest).

## [meta] table (Required)

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `name` | String | Recommended | Display name of the plugin |
| `author` | String | Recommended | Plugin author |
| `version` | String | Yes | Version string, required for website submission |
| `category` | String | Recommended | Grouping category (e.g. "Utility", "Galaxy", "GUI") |
| `siteid` | Integer | No | Auto-added during plugin review |
| `blocks` | String[] | No | Plugin identifiers to block (e.g., block old versions) |
| `perms` | String | Deprecated | Use Permissions API instead (`free`, `paid`, `full`) |

## [game] table (Optional)

| Key | Type | Description |
|-----|------|-------------|
| `min_version` | String | Minimum game build date: `"2022-02-03"` or `"2022-02-03 18:03"` |
| `max_version` | String | Maximum game build date (same format) |

## [script] table (Optional)

| Key | Type | Description |
|-----|------|-------------|
| `timeout` | Integer | Callback execution timeout in ms. `0` = disabled (no infinite-loop protection) |
| `imports` | String[] | Script files from `Openplanet/Scripts/` to include (e.g., `["Dialogs.as"]`) |
| `exports` | String[] | Files to export to dependent plugins (compiled into dependents, not self) |
| `shared_exports` | String[] | Like exports, but also compiled into this plugin |
| `dependencies` | String[] | Required plugin UIDs (e.g., `["VehicleState"]`). Plugin won't load if missing |
| `export_dependencies` | String[] | Dependencies to also export to any plugin depending on this one |
| `optional_dependencies` | String[] | Optional plugin UIDs — plugin loads without them, no compile error |
| `defines` | String[] | Preprocessor defines (e.g., `["DEBUG"]`) |
| `module` | String | Force a specific module name (defaults to plugin identifier) |

## Minimal Example

```toml
[meta]
name = "Minimal Plugin"
author = "tomekdot"
version = "1.0.0"
category = "Utility"
```

## Full Example

```toml
[meta]
name = "Calendar & Events"
author = "tomekdot"
version = "1.0.0"
category = "Utility"

[game]
min_version = "2023-01-01"

[script]
timeout = 5000
defines = ["BETA"]
```

### Reference: launch-commands

# Openplanet Plugin Dev — launch & verify commands

Copy-paste recipes for the MP4 dev loop. Paths are Windows; run the terminal
commands from the Hermes bash shell (POSIX paths work).

## Launch the game (via cua-driver, hidden — no focus steal)

MCP tool:
```
mcp__cua_driver__launch_app(path="C:\\Program Files (x86)\\ManiaPlanet\\ManiaPlanet.exe")
```
This opens ManiaPlanet in the background. First boot goes through Ubisoft
Connect login + shader cache and takes ~20–40s. The window lands at z_index 0
(behind other windows) — bring it forward with `Alt-Tab`, or raise it via
cua-driver if you need to drive it.

## Kill the game (releases any .op lock, forces a clean reload)

```
taskkill /F /IM ManiaPlanet.exe
```
Always kill before copying a fresh `.op` zip, otherwise the file is locked.
Folder plugins don't need this for dev edits (they read source live).

## Reload plugins in-game (MP4 quirk)

1. Click the game window (give it focus).
2. Press **F3** → opens the Openplanet overlay.
3. THEN press **Ctrl+Shift+R** → reloads plugins.
   (`Ctrl+Shift+R` alone does nothing on MP4 until F3 is open.)
A full restart (kill + relaunch) is the most reliable reload.

## Verify the plugin compiled & loaded (read the log, don't fight focus)

```
# clear log first for a clean run
> "C:\Users\tomekdot\Openplanet4\Openplanet.log"
# then after launch, check for compile errors
grep "ERR :" "C:\Users\tomekdot\Openplanet4\Openplanet.log" | grep -oP "Plugins/[^/]+/"
# should be EMPTY for your plugin
# confirm it loaded + debug log fired
grep -iE "TMNews|maniacalendar" "C:\Users\tomekdot\Openplanet4\Openplanet.log"
# lag check (should be EMPTY)
grep "laggy" "C:\Users\tomekdot\Openplanet4\Openplanet.log"
```

## Sanity-check a plugin before launching (brace/paren balance)

```bash
python -c "s=open(r'C:\Users\tomekdot\Openplanet4\Plugins\<name>\Main.as',encoding='utf-8').read();print('braces',s.count('{'),s.count('}'));print('parens',s.count('('),s.count(')'));print('brackets',s.count('['),s.count(']'))"
```
All three pairs must be balanced. (`python` exists; `python3` does NOT.)

## Poll whether the game process is still alive

```
tasklist 2>/dev/null | grep -i maniaplanet
```

## Open the plugin UI in-game

- **F3** → Openplanet overlay → Plugins list (toggle checkboxes / Settings).
- For YouTube/news plugins: enable **Show Debug** in Settings, open the plugin
  tab, confirm the channel log / video count is populated.

### Reference: mp4-api-mismatches

