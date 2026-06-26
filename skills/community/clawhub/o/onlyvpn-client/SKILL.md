---
name: onlyvpn-cli
description: >-
  Operates the OnlyVPN desktop client via vpn-cli.exe on Windows (default
  C:\Program Files\onlynet) or vpn-cli on macOS, after the GUI/main process is
  running (onlynet.exe on Windows; Onlynet.app/Contents/MacOS/OnlyNet on
  macOS)—JSON output for status, subscriptions, connect/disconnect, and
  help/version. Use when the user needs VPN automation, subscription
  management, node selection, or scripting against OnlyVPN; when they mention
  vpn-cli, vpn-cli.exe, OnlyVPN, or this client’s command-line interface.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - vpn-cli
        - vpn-cli.exe
    homepage: https://onlyvpn.net
    emoji: "🔐"
---

# OnlyVPN CLI

## Platform invocation

| Platform | Main app (start this first) | CLI |
| --- | --- | --- |
| Windows | **`onlynet.exe`** in install dir (default `C:\Program Files\onlynet\`) | **`vpn-cli.exe`** (same folder by default) |
| macOS | **`Onlynet.app/Contents/MacOS/OnlyNet`** (see install layout below) | **`vpn-cli`** (often on `PATH` after copy to `/usr/local/bin/`) |

**Prerequisite:** The **main client process must be running** before `vpn-cli` / `vpn-cli.exe` will work. Start **`onlynet.exe`** (Windows) or launch **`OnlyNet`** inside **`Onlynet.app`** (macOS) first; then use the CLI.

All documented subcommands and flags are passed **after** the CLI name (e.g. Windows: `vpn-cli.exe status`; macOS: `vpn-cli status`).

## When to use this skill

Apply when automating or documenting the **OnlyVPN** VPN client through **`vpn-cli.exe` (Windows)** or **`vpn-cli` (macOS)**—**only after** the main app (`onlynet.exe` / `OnlyNet`) is running. Output is **JSON** for scripting; parse `code`, `message`, and `data` / `error` fields.

## Install and startup order (before using the CLI)

### Windows

1. Download: `https://onlyvpn.net/download/client/onlynet_win.exe`
2. Run the installer. By default the application installs under **`C:\Program Files\onlynet`**.
3. **Start the main client first:** run **`onlynet.exe`** from that directory, for example:

   `"C:\Program Files\onlynet\onlynet.exe"`

   Keep this process running; the CLI talks to it.
4. Then run the CLI with **`vpn-cli.exe`** plus arguments, for example:

   `"C:\Program Files\onlynet\vpn-cli.exe" --version`

   If the installer adds that directory to `PATH`, you can run `onlynet.exe` and `vpn-cli.exe` without full paths.

### macOS

1. Download: `https://onlyvpn.net/download/client/onlynet_mac.zip`
2. Unzip the archive. Locate **`Onlynet.app`** in the extracted folder (exact path depends on zip layout). Optionally install the included **`.dmg`** and copy **`Onlynet.app`** to **Applications**—either way you need the bundle on disk.
3. **Start the main client first** (required before `vpn-cli` works). Standard macOS bundle layout uses **`Contents/MacOS/`** (not a single `ContentsMacOS` folder):

   ```bash
   open path/to/Onlynet.app
   ```

   or run the binary directly:

   ```bash
   path/to/Onlynet.app/Contents/MacOS/OnlyNet
   ```

   If the app lives under **Applications**, use e.g. `/Applications/Onlynet.app/Contents/MacOS/OnlyNet` or `open -a Onlynet`. Leave this process running.
4. Use the **`vpn-cli`** binary from the zip (no `.exe`) with arguments. If it is not on `PATH`, copy it into a directory on `PATH`, for example:

   ```bash
   sudo cp path/to/vpn-cli /usr/local/bin/
   sudo chmod +x /usr/local/bin/vpn-cli
   ```

5. Confirm (with **`OnlyNet`** already running): `vpn-cli --version`

## Response shape (success)

Successful commands return JSON with `code`, `message`, and usually `data`. Example shapes are in [reference.md](reference.md).

**Note:** Product docs may state success as `code: 0`; examples below often use `code: 200`. Treat success per your installed build (either `0` or `200` as documented) and treat other values as failure; always read `message` and optional `error`.

## Response shape (failure)

On failure, responses include `code` (not success), `message`, and an `error` object with `type`, `details`, optional `hint`, plus optional `request_id` and `ts` (UTC ISO8601). See [reference.md](reference.md) for common error codes.

## Commands (quick reference)

Replace **`vpn-cli`** below with **`vpn-cli.exe`** on Windows (and quote the full path if needed, e.g. `"C:\Program Files\onlynet\vpn-cli.exe"`).

| Area | Command |
| --- | --- |
| Status | `vpn-cli status` |
| Add subscription | `vpn-cli sub add "<url>"` |
| Update all subs | `vpn-cli sub update` |
| List subscriptions | `vpn-cli sub list` |
| Remove subscription | `vpn-cli sub remove "<name>"` |
| Nodes under a sub | `vpn-cli sub nodelist "<name>"` |
| Connect (named sub + node) | `vpn-cli connect sub "<name>" node "<node>"` |
| Connect best latency | `vpn-cli connect --best` |
| Disconnect | `vpn-cli disconnect` |
| Help | `vpn-cli --help` |
| Version | `vpn-cli --version` |

### Connect behavior (defaults)

- With **`connect sub ... node ...`**: optional `--best` may apply where supported.
- Without `sub`: uses last used or first subscription.
- Without `node` or if the name is missing: uses first node in scope.
- Without both: connects to the first node.

## Agent guidance

- **Start the main client before any CLI:** on **Windows** run **`onlynet.exe`** from the install directory (default `C:\Program Files\onlynet\`); on **macOS** launch **`Onlynet.app`** or run **`Onlynet.app/Contents/MacOS/OnlyNet`** from the unzip (or installed) location.
- Then run the real CLI: **Windows** — **`vpn-cli.exe`**; **macOS** — **`vpn-cli`**. Do not invent a separate HTTP API.
- If CLI commands fail or hang, verify **`onlynet.exe` / `OnlyNet`** is still running.
- Parse **JSON stdout**; handle both example success codes (`200` vs `0`) if users report differences between builds.
- For full response examples and error catalog, read [reference.md](reference.md).
