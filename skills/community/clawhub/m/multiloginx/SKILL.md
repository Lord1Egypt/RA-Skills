---                                                                                                            
name: multilogin                                                                                               
description: Use when you need to manage Multilogin through `xcli`, including Android cloud phones, browser profiles, workspaces, proxies, scripts, tags, files, apps, ADB access, and account settings.
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["xcli", "mlx-launcher"] } } }                   
---                                                                                                            
                                                                                                               
# Multilogin

Multilogin is a cloud phone platform for social media marketers. This skill connects OpenClaw with the Multilogin CLI (`xcli`), allowing people and AI agents to manage social profiles using AI prompts.

Use Android cloud phones for mobile app workflows and browser profiles for web workflows. The skill supports creating, listing, starting, stopping, and organizing profiles, as well as managing apps, files, proxies, scripts, tags, workspaces, ADB access, and account settings.

## CRITICAL: Launcher must run FIRST

The `mlx-launcher` process MUST be running before ANY `xcli` command (except `login`) will work.
If you skip this, you WILL get "connection refused" or "launcher not active" errors.

---

## Installation

### Version resolution

Both binaries have a `/latest` endpoint that returns the current version string:

https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest       → e.g. "0.0.72"
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest   → e.g. "1.75.0"

Download URLs follow the pattern:

https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/{VERSION}/xcli_{PLATFORM}
https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/{VERSION}/launcher-{PLATFORM}

**Platform suffixes:**

| Platform | xcli | mlx-launcher |
|----------|------|--------------|
| Linux x64 | `xcli_linux_amd64` | `launcher-linux_amd64.bin` |
| macOS x64 | `xcli_darwin_amd64` | `launcher-darwin_amd64.bin` |
| macOS ARM | `xcli_darwin_arm64` | `launcher-darwin_arm64.bin` |
| Windows | `xcli_windows_amd64.exe` | `launcher-windows_amd64.exe` |

### Install on Linux (VPS / Docker)

```bash
# Resolve latest versions
CLI_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest")
LAUNCHER_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest")
echo "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
curl -L -o /usr/local/bin/xcli
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_linux_amd64"
curl -L -o /usr/local/bin/mlx-launcher
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-linux_amd64.bin"

# Make executable
chmod +x /usr/local/bin/xcli /usr/local/bin/mlx-launcher

# Verify
xcli --help
mlx-launcher --help

Install on macOS

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
  SUFFIX="darwin_arm64"
else
  SUFFIX="darwin_amd64"
fi

# Resolve latest versions
CLI_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest")
LAUNCHER_VER=$(curl -sL "https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest")
echo "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
curl -L -o /usr/local/bin/xcli
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_${SUFFIX}"
curl -L -o /usr/local/bin/mlx-launcher
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-${SUFFIX}.bin"

# Make executable
chmod +x /usr/local/bin/xcli /usr/local/bin/mlx-launcher

# macOS may quarantine downloaded binaries — remove the flag
xattr -d com.apple.quarantine /usr/local/bin/xcli 2>/dev/null
xattr -d com.apple.quarantine /usr/local/bin/mlx-launcher 2>/dev/null

# Verify
xcli --help
mlx-launcher --help

Install on Windows

# Resolve latest versions
$CLI_VER = (Invoke-WebRequest -Uri
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/latest").Content.Trim()
$LAUNCHER_VER = (Invoke-WebRequest -Uri
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/latest").Content.Trim()
Write-Host "Installing xcli $CLI_VER, launcher $LAUNCHER_VER"

# Download binaries
Invoke-WebRequest -Uri
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/cli-mlx/${CLI_VER}/xcli_windows_amd64.exe" -OutFile
"$env:USERPROFILE\xcli.exe"
Invoke-WebRequest -Uri
"https://ml000x-dev-dists.s3.eu-north-1.amazonaws.com/launcher-mlx/${LAUNCHER_VER}/launcher-windows_amd64.exe"
-OutFile "$env:USERPROFILE\mlx-launcher.exe"

# Add to PATH (current session)
$env:PATH += ";$env:USERPROFILE"

---
Environment Detection

Detect your environment before running commands:

# Am I in Docker?
if [ -f /.dockerenv ]; then
  echo "DOCKER"
else
  echo "BARE METAL"
fi

Both environments use the same xcli and mlx-launcher binaries — they must be in PATH.

---
Headless (VPS / Docker) — Step by Step

This is the primary mode. No display, no GUI. Profiles run headless.

Step 1: Start the launcher

mlx-launcher -port 45000 &
sleep 5

Verify:

xcli launcher-info

You MUST see a version number before proceeding. If error — wait and retry.

Step 2: Login

xcli login --username 'USER@EMAIL' --password 'PASSWORD'

Ask the user for credentials if not provided. Tokens last ~24h, stored in ~/.config/xcli/.

Step 3: Launch quick profiles

Quick profiles are disposable — deleted automatically when stopped.

xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless

Launch 2 quick profiles:

xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless
xcli profile-quick --browser-type mimic --os-type linux --automation puppeteer --headless

Each returns a profile ID and a port for Puppeteer/Selenium automation.

Headless constraints

- Always use --headless — no display server available.
- Always use --os-type linux — must match the host OS.
- Always use --browser-type mimic — stealthfox is NOT available on Linux.
- Do NOT use profile-create for disposable sessions — use profile-quick.
- Do NOT run xcli commands in background with & (only mlx-launcher).

---
Desktop (macOS / Windows / Linux with GUI)

When running on a machine with a display (e.g. a Mac node), profiles can open visible browser windows.

Step 1: Start the launcher

mlx-launcher -port 45000 &
sleep 5
xcli launcher-info

Step 2: Login

xcli login --username 'USER@EMAIL' --password 'PASSWORD'

Step 3: Launch profiles (with GUI)

On macOS:

xcli profile-quick --browser-type mimic --os-type macos --automation puppeteer
xcli profile-quick --browser-type stealthfox --os-type macos --automation puppeteer

On Windows:

xcli profile-quick --browser-type mimic --os-type windows --automation puppeteer
xcli profile-quick --browser-type stealthfox --os-type windows --automation puppeteer

Note: No --headless flag — browser windows will be visible.

Desktop constraints

- --os-type must match the actual OS (macos, windows, or linux).
- Both mimic (Chromium) and stealthfox (Firefox) are available on macOS and Windows.
- On Linux with GUI, only mimic is available.

---
GUI via OpenClaw Node (VPS + Mac hybrid)

The most elegant setup: VPS runs 24/7 headless, Mac node handles GUI tasks on demand.

Architecture

VPS (OpenClaw main agent, 24/7, headless)
  ↕ paired via gateway
Mac (OpenClaw Node, paired device)
  → runs Multilogin with visible browser windows
  → VPS delegates GUI tasks here

When to use the Node

Use the VPS for:
- Headless quick profiles (automation, scraping, batch tasks)
- All non-GUI work

Delegate to the Mac node when:
- User wants to SEE the browser (visual inspection, manual interaction)
- A task requires a real display (CAPTCHAs, visual verification)
- stealthfox is needed (not available on Linux)
- Debugging a profile visually

How to delegate to the Node

From the VPS main agent, use sessions_spawn to send a task to the Mac node:

{
  "tool": "sessions_spawn",
  "agentId": "node-mac",
  "message": "Start the Multilogin launcher and launch 2 quick profiles with GUI. Use: mlx-launcher -port 45000
 & sleep 5 && xcli login --username 'USER' --password 'PASS' && xcli profile-quick --browser-type mimic
--os-type macos --automation puppeteer && xcli profile-quick --browser-type stealthfox --os-type macos
--automation puppeteer"
}

The node will:
1. Start the launcher locally on the Mac
2. Login with the provided credentials
3. Launch profiles with visible browser windows
4. Report back the profile IDs and ports

Setup requirements for the Node

The Mac node needs:
- xcli and mlx-launcher binaries for macOS in PATH (see Install on macOS above)
- Network access to Multilogin API (signin.multilogin.com)
- OpenClaw Node running and paired to the VPS gateway

---
## Cloud Phones (Mobile Profiles)

Multilogin **cloud phones** are Android mobile profiles, driven with the
`mobile-profiles-*` / `mobile-phone-*` command family. They use the same
authenticated `xcli` session as browser profiles — the launcher must be running
and you must be logged in. A cloud phone runs **server-side**, so starting one
**spends mobile-minutes** (metered for as long as it runs, even headless).

> **Billing:** always check remaining minutes with `mobile-profiles-limit`
> before starting, and always `mobile-profiles-phone-stop` when finished.
> Disabling ADB is **not** the same as stopping the phone.

### Prerequisites

- Launcher running and logged in — exactly as for browser profiles
  (`mlx-launcher -port 45000 &`, then `xcli login …`).
- For ADB control: `adb` installed and in `PATH` (`adb version`).
- A mobile profile — create one below, or list existing ones with
  `mobile-profiles-phone-list`.

### Plan limits (preflight)

```bash
xcli mobile-profiles-limit      # total plan limit, current usage, remaining minutes
```

Do not start phones when the remaining minutes is 0.

### Create a cloud phone

Look up device / location options, then create. **A proxy is required.**

```bash
xcli mobile-profiles-phone-brand-list --android-version 14   # brands/models for an Android version
xcli mobile-profiles-states --country "USA"                  # region options
xcli mobile-profiles-cities --state "California"

# One Android 14 phone with a proxy
xcli mobile-profiles-create \
  --mobile-type "Android 14" \
  --profile-name "my-phone" \
  --proxy "socks5://user:pass@host:1080"

# Three phones in a folder, tagged, on Wi-Fi networking
xcli mobile-profiles-create --mobile-type "Android 14" --profile-name "bulk" \
  --proxy "socks5://user:pass@host:1080" --quantity 3 \
  --folder-id "<folder-uuid>" --tags "team-a,automation" --net-type 0
```

- `--proxy` is **required**; `--net-type` `0` = Wi-Fi, `1` = Mobile (default `1`).
- `--quantity` creates N phones, each with its own serial number and device identity.
- Validate a proxy first if unsure:
  `xcli mobile-profiles-proxy-check --proxy-type socks5 --server host --port 1080 [--username u --password p]`.

### List / inspect

```bash
xcli mobile-profiles-phone-list                                    # paginated (default 50/page)
xcli mobile-profiles-phone-list --ids "<id1>,<id2>"
xcli mobile-profiles-phone-list --folder-id "<uuid>" --serial-name "my" --page 1 --page-size 50
```

### Start / stop lifecycle

```bash
xcli mobile-profiles-phone-start --ids "<id>"     # start headless — SPENDS minutes
xcli mobile-profiles-statuses    --ids "<id>"     # poll until Started
xcli mobile-profiles-phone-stop  --ids "<id>"     # ALWAYS stop when done
```

**Status codes** (`mobile-profiles-statuses`): `0` Started · `1` Starting (wait,
re-poll) · `2` Shut down · `3` Expired.

> `mobile-phone-launch` / `mobile-phone-shutdown` are the launcher-backed
> start/stop variants. For headless automation prefer
> `mobile-profiles-phone-start` / `mobile-profiles-phone-stop`.

### Control a phone over ADB

Once a phone is **Started**, enable ADB, read the connection details, and attach
your local `adb`:

```bash
xcli mobile-profiles-adb-set  --ids "<id>" --enable    # enable ADB (up to 50 ids)
xcli mobile-profiles-adb-info --ids "<id>"             # -> per-profile {ip, port, pwd, status}
```

`mobile-profiles-adb-info` reports a per-profile `status`:

- `active` — `ip`/`port`/`pwd` populated, ready to connect
- `disabled` — phone stopped or ADB not enabled (start the phone / re-enable ADB)
- `error` — unsupported or unknown

Connect and drive. The `glogin` session **expires after ~30–60s** — re-`glogin`
immediately before each action rather than once at the start:

```bash
adb connect <ip>:<port>
adb -s <ip>:<port> shell glogin <pwd>                 # expect "glogin success"
adb -s <ip>:<port> shell screencap -p /sdcard/s.png   # capture
adb -s <ip>:<port> shell uiautomator dump             # inspect (tap by node bounds)
adb -s <ip>:<port> shell input tap <x> <y>            # act
adb -s <ip>:<port> shell input text "hello"
```

Disable ADB when finished (separate from stopping the phone):

```bash
xcli mobile-profiles-adb-set --ids "<id>" --disable
adb disconnect <ip>:<port>
```

- The `pwd` is a short-lived `glogin` code, **not** an API token — never log or persist it.
- Up to 50 ids per `adb-set` / `adb-info` call; non-running phones are skipped and reported.

### Install apps

```bash
xcli mobile-profiles-app-list --key "TikTok"           # find the app + version IDs
xcli mobile-profiles-group                             # workspace group ID (auto-created)
xcli mobile-profiles-app-install --id "<app-id>" --version_id "<version-id>" \
  [--install_group_ids "<group-id>"]                   # omit to use the workspace default group
```

### Files (shared mobile drive)

```bash
xcli mobile-profiles-files-upload --file "/path/to/app.apk"     # jpg/png/gif/mp4/apk/xapk/xml…
xcli mobile-profiles-files-list --page 1 --page-size 20 [--file-type 1]   # 1=image, 2=video/app
xcli mobile-profiles-files-delete --ids "<file-id>"
xcli mobile-profiles-files-tag-assign   --material-id "<file-id>" --tags "<tag-id>"
xcli mobile-profiles-files-tag-unassign --material-id "<file-id>" --tags "<tag-id>"
```

### Tags

```bash
xcli mobile-profiles-tag-assign   --profile-id "<id>" --tags "<tag-id-1>,<tag-id-2>"   # max 10
xcli mobile-profiles-tag-unassign --profile-id "<id>" --tags "<tag-id-1>"
```

Tag IDs come from `tag-list`; the tags must already exist in the workspace.

### Manage (update / delete / transfer / import-export)

```bash
xcli mobile-profiles-update --id "<id>" --name "new-name" [--folder-id <uuid>] [--remark "…"] \
  [--proxy-server host --proxy-port 1080 --proxy-protocol 1] [--tags "a,b"]
xcli mobile-profiles-delete   --ids "<id1>,<id2>"                 # PERMANENT — no trash recovery
xcli mobile-profiles-transfer --ids "<id>" --target-email "colleague@example.com"

# Bulk import: download template -> fill -> validate (returns validation_id) -> confirm
xcli mobile-profiles-phone-import-template -o template.xlsx
xcli mobile-profiles-phone-import-validate --file profiles.xlsx
xcli mobile-profiles-phone-export --ids "<id1>,<id2>" -o export.xlsx
```

### Constraints

- Starting a phone spends mobile-minutes — always `mobile-profiles-phone-stop`
  when done. Disabling ADB does **not** stop the phone or its billing.
- `--proxy` is required at create time.
- `mobile-profiles-delete` is permanent; deleted phones cannot be restored.
- The ADB `pwd` is a transient `glogin` code — re-`glogin` before every action;
  a stale session fails silently mid-run.

### Troubleshooting (cloud phones)

| Problem | Cause | Fix |
|---------|-------|-----|
| `mobile-profiles-adb-info` returns `status: disabled` | Phone not started, or ADB not enabled | Start the phone (`mobile-profiles-phone-start`), then `mobile-profiles-adb-set … --enable`; poll info until `active` |
| `adb connect` works but shell commands are unauthorized / do nothing | `glogin` session expired (~30–60s) | Re-run `adb -s <ip>:<port> shell glogin <pwd>` right before the action |
| `glogin` does not print `glogin success` | Wrong/expired `pwd`, or ADB disabled | Re-fetch with `mobile-profiles-adb-info` and reconnect |
| `mobile-profiles-create` rejected | Missing/invalid `--proxy`, or unknown `--mobile-type` | Provide a valid proxy string; check the Android version with `mobile-profiles-phone-brand-list` |
| Phone won't start / minutes not decreasing | Plan limit reached or phone expired (status `3`) | Check `mobile-profiles-limit`; recreate expired phones |

---

Full CLI Command Reference

General

┌───────────────┬────────────────────────────────────────────────────┐
│    Command    │                    Description                     │
├───────────────┼────────────────────────────────────────────────────┤
│ login         │ Log in to your account                             │
├───────────────┼────────────────────────────────────────────────────┤
│ launcher-info │ Get info about the running launcher (app or agent) │
├───────────────┼────────────────────────────────────────────────────┤
│ help          │ Help for all commands                              │
└───────────────┴────────────────────────────────────────────────────┘

Folders

┌───────────────┬────────────────────────────────────────┐
│    Command    │              Description               │
├───────────────┼────────────────────────────────────────┤
│ create-folder │ Create a folder with a given name      │
├───────────────┼────────────────────────────────────────┤
│ list-folder   │ View all available folders             │
├───────────────┼────────────────────────────────────────┤
│ remove-folder │ Remove a folder by ID (or list of IDs) │
├───────────────┼────────────────────────────────────────┤
│ update-folder │ Update folder details using its ID     │
└───────────────┴────────────────────────────────────────┘

Workspaces

┌──────────────────┬─────────────────────────────────┐
│     Command      │           Description           │
├──────────────────┼─────────────────────────────────┤
│ list-workspace   │ Display available workspaces    │
├──────────────────┼─────────────────────────────────┤
│ switch-workspace │ Switch to a different workspace │
└──────────────────┴─────────────────────────────────┘

Proxies

┌─────────────────┬───────────────────────────────────────────┐
│     Command     │                Description                │
├─────────────────┼───────────────────────────────────────────┤
│ proxy-countries │ List available countries in proxy service │
├─────────────────┼───────────────────────────────────────────┤
│ proxy-regions   │ Get regions by country code               │
├─────────────────┼───────────────────────────────────────────┤
│ proxy-cities    │ Get cities by region code                 │
├─────────────────┼───────────────────────────────────────────┤
│ proxy-get       │ Get a proxy URL based on parameters       │
└─────────────────┴───────────────────────────────────────────┘

Profiles

┌───────────────────────┬──────────────────────────────────────────────┐
│        Command        │                 Description                  │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-quick         │ Launch a disposable quick profile (v4 API)   │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-create        │ Create a new persistent profile              │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-template      │ Create a new template for a browser profile  │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-start         │ Start a profile by ID                        │
├───────────────────────┼────────────────────────────────���─────────────┤
│ profile-stop          │ Stop a profile by ID                         │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-list          │ List profiles in a given folder              │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-stat          │ Statistics about currently launched profiles │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-status        │ Status of given profile(s)                   │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-update        │ Update an existing profile                   │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-clone         │ Duplicate a profile                          │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-move          │ Move profile to a different folder           │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-remove        │ Remove profiles by IDs                       │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-restore       │ Restore a deleted profile from trash         │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-export        │ Export a profile into a file                 │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-export-status │ Show profile export status                   │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-import        │ Import a profile from a file                 │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-import-status │ Show profile import status                   │
├───────────────────────┼─────────���────────────────────────────────────┤
│ profile-cookie-import │ Import cookies to a profile                  │
├───────────────────────┼──────────────────────────────────────────────┤
│ profile-cookie-export │ Export cookies from a profile                │
└───────────────────────┴──────────────────────────────────────────────┘

Mobile profiles (cloud phones)

┌───────────────────────────────────────┬──────────────────────────────────────────────────┐
│ Command                               │ Description                                      │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-limit                 │ Plan limit, current usage, and remaining minutes │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-group                 │ Get/create the workspace mobile profile group    │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-states                │ List states/regions by country code              │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-cities                │ List cities by state                             │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-proxy-check           │ Test a proxy and return geo details              │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-brand-list      │ List phone brands/models by Android version      │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-list            │ List cloud phones (paginated, filterable)        │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-create                │ Create cloud phone(s)                            │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-update                │ Update a cloud phone                             │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-delete                │ Permanently delete cloud phones by ID            │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-statuses              │ Runtime status of cloud phones (0/1/2/3)         │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-start           │ Start cloud phone(s) headless (spends minutes)   │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-stop            │ Stop cloud phone(s)                              │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-phone-launch                   │ Start cloud phone(s) via launcher                │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-phone-shutdown                 │ Stop cloud phone(s) via launcher                 │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-adb-set               │ Enable/disable ADB (--enable/--disable, max 50)  │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-adb-info              │ Get ADB connection info (ip/port/pwd/status)     │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-app-list              │ List installable apps (system + uploaded)        │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-app-install           │ Batch-install an app version to a group          │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-tag-assign            │ Assign tags to a cloud phone (max 10)            │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-tag-unassign          │ Remove tags from a cloud phone                   │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-files-list            │ List files on the shared mobile drive            │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-files-upload          │ Upload a file to the mobile drive                │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-files-delete          │ Delete files from the mobile drive               │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-files-tag-assign      │ Assign tags to a mobile-drive file               │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-files-tag-unassign    │ Remove tags from a mobile-drive file             │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-transfer              │ Transfer phone ownership to another user         │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-import-template │ Download the bulk-import Excel template          │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-import-validate │ Validate a bulk-import Excel file                │
├───────────────────────────────────────┼──────────────────────────────────────────────────┤
│ mobile-profiles-phone-export          │ Export cloud phones to Excel                     │
└───────────────────────────────────────┴──────────────────────────────────────────────────┘

Scripts

┌──────────────┬────────────────────────────────────────────────┐
│   Command    │                  Description                   │
├──────────────┼────────────────────────────────────────────────┤
│ script-list  │ List available scripts in Script Runner folder │
├──────────────┼────────────────────────────────────────────────┤
│ script-start │ Run a script in a Multilogin profile           │
├──────────────┼────────────────────────────────────────────────┤
│ script-stop  │ Stop a running script                          │
├──────────────┼────────────────────────────────────────────────┤
│ cookie-robot │ Start Cookie Robot on profile(s)               │
└──────────────┴────────────────────────────────────────────────┘

Objects (extensions, files, etc.)

┌─────────────────────────┬───────────────────────────────────────────┐
│         Command         │                Description                │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-types            │ List object types                         │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-list             │ List objects                              │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-meta             │ Fetch object metadata                     │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-create           │ Create an object (requires running agent) │
├───────────────────���─────┼───────────────────────────────────────────┤
│ object-download         │ Download object to local storage          │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-delete           │ Delete an object                          │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-restore          │ Restore object from trash                 │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-stats            │ Display object usage statistics           │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-convert          │ Convert storage type (local ↔ cloud)      │
├─────────────────────────┼───────────────────────────────────────────┤
│ enable-object           │ Enable object for profiles                │
├─────────────────────────┼───────────────────────────────────────────┤
│ disable-object          │ Disable object for profiles               │
├─────────────────────────┼───────────────────────────────────────────┤
│ object-extension-create │ Create an extension object from a URL     │
└─────────────────────────┴───────────────────────────────────────────┘

Tags

┌──────────────┬─────────────────────────────────────────┐
│   Command    │               Description               │
├──────────────┼─────────────────────────────────────────┤
│ create-tag   │ Create one or more tags                 │
├──────────────┼─────────────────────────────────────────┤
│ tag-list     │ List tags (with optional search filter) │
├──────────────┼─────────────────────────────────────────┤
│ tag-remove   │ Remove tags by IDs                      │
├──────────────┼─────────────────────────────────────────┤
│ tag-assign   │ Assign tags to a profile                │
├──────────────���─────────────────────────────────────────┤
│ tag-unassign │ Unassign tags from a profile            │
└──────────────┴─────────────────────────────────────────┘

2FA

┌───────────────────────────┬──────────────────────────────────┐
│          Command          │           Description            │
├───────────────────────────┼──────────────────────────────────┤
│ enable-2fa                │ Enable two-factor authentication │
├───────────────────────────┼──────────────────────────────────┤
│ view-backup-codes         │ View backup codes                │
├───────────────────────────┼──────────────────────────────────┤
│ disable-2fa-for-user      │ Disable 2FA for user             │
├───────────────────────────┼──────────────────────────────────┤
│ disable-2fa-for-workspace │ Disable 2FA for workspace        │
├───────────────────────────┼──────────────────────────────────┤
│ enable-2fa-for-workspace  │ Enable 2FA for workspace         │
└───────────────────────────┴──────────────────────────────────┘

Billing

┌───────────────┬─────────────────────────┐
│    Command    │       Description       │
├───────────────┼─────────────────────────┤
│ referral-code │ Get referral code       │
├───────────────┼─────────────────────────┤
│ multipoints   │ Get multipoints balance │
└───────────────┴─────────────────────────┘

---
Quick reference flags

┌────────────────┬────────────────────────────────┬──────────────────────────────┐
│      Flag      │             Values             │            Notes             │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --browser-type │ mimic, stealthfox              │ Linux: only mimic            │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --os-type      │ linux, macos, windows, android │ Must match host              │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --automation   │ puppeteer, selenium            │                              │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --headless     │ (no value)                     │ Required on headless servers │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --proxy-string │ "host:port:user:pass"          │ Optional proxy               │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --proxy-type   │ http, https, socks5            │ Required if using proxy      │
├────────────────┼────────────────────────────────┼──────────────────────────────┤
│ --core-version │ e.g. 144.4                     │ Specific browser version     │
└────────────────┴────────────────────────────────┴──────────────────────────────┘

---
Troubleshooting

Problem: connection refused / launcher not active
Cause: Launcher not running
Fix: mlx-launcher -port 45000 & then sleep 5
────────────────────────────────────────
Problem: browser version not found
Cause: Wrong os-type/browser-type combo
Fix: Use --browser-type mimic --os-type linux on Linux
────────────────────────────────────────
Problem: context deadline exceeded
Cause: Launcher downloading cores (first run)
Fix: Wait 30-60s, retry. Cores are cached after first download
────────────────────────────────────────
Problem: token contains invalid segments
Cause: Not logged in
Fix: xcli login
────────────────────────────────────────
Problem: UNAUTHORIZED_REQUEST
Cause: Token expired (>24h)
Fix: xcli login again
─────────────────────────────────────���──
Problem: Need GUI but on VPS
Cause: No display server
Fix: Delegate to Mac node via sessions_spawn
────────────────────────────────────────
Problem: macOS: "unidentified developer"
Cause: Gatekeeper quarantine
Fix: Run xattr -d com.apple.quarantine <binary>
────────────────────────────────────────
Problem: ```
Cause:
Fix: