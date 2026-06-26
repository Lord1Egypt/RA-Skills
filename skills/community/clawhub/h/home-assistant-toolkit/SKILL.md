---
name: home-assistant-toolkit
description: >
  Home Assistant full management skill — control devices, create automations, monitor health,
  manage backups, update HACS, generate dashboards, all via SSH.
  Use this skill whenever the user mentions Home Assistant, HA, HASS, smart home, automations,
  YAML config, Jinja2 templates, ESPHome, IR control, Matter, integrations, dashboards,
  device control, turn on/off lights, scenes, scripts, backups, HACS updates, or device monitoring.
  Connects to HA via SSH for full access: config files, ha CLI, REST API, logs.
  Dynamically scans integrations and fetches release notes — never goes stale.
version: "2.0.0"
metadata:
  clawdbot:
    emoji: "🏠"
    homepage: https://github.com/motionbeard/home-assistant-openclaw
    always: false
    files:
      - "scripts/*"
    requires:
      bins:
        - ssh
        - jq
        - curl
        - python3
      anyBins:
        - sshpass
      env:
        - HA_URL
        - HA_TOKEN
        - HA_HOST
        - HA_SSH_PORT
        - HA_SSH_USER
        - HA_SSH_PASS
        - HA_CONFIG_PATH
    primaryEnv: HA_TOKEN
---

# Home Assistant Expert Skill

You are a Home Assistant expert. You help users configure, automate, and troubleshoot their Home Assistant installations. Your knowledge stays current through dynamic release note fetching and instance scanning.

> **IMPORTANT — Absolute paths only:** All script calls MUST use the absolute path to this skill directory.
> Relative paths like `scripts/check-setup.sh` will fail if the working directory differs from the skill root.
> Determine the skill directory first (the directory containing this SKILL.md), then prefix all script paths with it.
> Example: `bash /path/to/skill/scripts/check-setup.sh`, `python3 /path/to/skill/scripts/scan_integrations.py`

> **IMPORTANT — First run check:** Before executing ANY other command, run:
> ```bash
> bash /path/to/skill/scripts/check-setup.sh
> ```
> - Output `NOT_CONFIGURED` → skill is not set up yet. Jump to **"First-Time Setup (Onboarding)"** and start Quick Setup. Do NOT attempt to run other scripts.
> - Output `CONFIGURED` + `Connected` → ready to use.
> - Output `CONFIGURED` + `connection failed` → env vars are set but connection is broken. Help the user debug (wrong IP, token expired, SSH key not added, etc.).

> **Note for the agent:** The `references/` directory ships with empty template files (`ha_version: null`, placeholder text). These are NOT leftover data from a previous user — they are blank templates that get populated on first setup. Do not warn the user about them or suggest cleaning them up.

## Connection Setup

This skill connects to Home Assistant via **SSH**, giving full access to config files, logs, CLI, and device control.

### Requirements

- **Terminal & SSH** add-on installed in Home Assistant (Settings → Add-ons → Terminal & SSH)
- SSH access enabled with password or SSH key
- SSH port configured (default: 22)

### Step 1: Configure SSH on Home Assistant

1. Go to **Settings → Add-ons → Add-on Store** and install **Terminal & SSH**
2. Go to the **Configuration** tab of the add-on
3. Paste your public SSH key into the `authorized_keys` list:
   ```yaml
   authorized_keys:
     - ssh-ed25519 AAAAC3NzaC1... user@machine
   ```
   Do NOT wrap the key in quotes — paste it as-is.
4. The `password` field can be left as-is — key-based auth works regardless of password settings
5. Under **Network**, set the port (usually `22` or `22222`)
6. Save and restart the add-on

### Step 2: Configure Connection in OpenClaw

In `~/.openclaw/openclaw.json`:
```json5
{
  "skills": {
    "entries": {
      "home-assistant-toolkit": {
        "enabled": true,
        "env": {
          "HA_URL": "http://homeassistant.local:8123",
          "HA_TOKEN": "eyJhbGciOiJIUzI1...",
          "HA_HOST": "homeassistant.local",
          "HA_SSH_PORT": "22",
          "HA_SSH_USER": "root",
          "HA_CONFIG_PATH": "/config"
        }
      }
    }
  }
}
```

Or via shell environment variables (take precedence over openclaw.json):
```bash
export HA_URL="http://192.168.1.100:8123" # REST API Address
export HA_TOKEN="eyJhbGciOiJI..."         # Long-Lived Access Token
export HA_HOST="192.168.1.100"            # or homeassistant.local
export HA_SSH_PORT="22"                   # SSH add-on port
export HA_SSH_USER="root"                 # usually root for HA OS
export HA_CONFIG_PATH="/config"           # default config path
```

**Key-based auth** (recommended):
```bash
# Copy key once
ssh-copy-id -p 22 root@homeassistant.local
```

**Password auth** — set `HA_SSH_PASS` in env (less secure).

### Step 3: Verify Connection

```bash
scripts/ha.sh info
```
If successful, shows HA version, installation name, and add-on list.

Or ask the agent: **"Check Home Assistant connection"**

### What SSH Provides

- `ha` CLI — manage HA core, add-ons, backups, updates
- Direct access to `/config/` — read and edit YAML files
- Logs — `ha core logs`, `ha supervisor logs`
- Restart — `ha core restart`, `ha core check`
- Supervisor REST API also available inside: `curl http://supervisor/core/api/...` with the SUPERVISOR_TOKEN env var

### Security

- Use SSH keys instead of passwords
- Do not expose SSH port to the internet — local network or Tailscale VPN only
- For remote access: Nabu Casa cloud or VPN

### Security & Privacy

This skill runs **entirely locally** between your machine and your Home Assistant instance. No telemetry, analytics, or third-party services are involved in device control, monitoring, or configuration management.

**What stays on your machine / HA instance:**
- All SSH commands and REST API calls go directly to your HA instance
- Entity states, automation YAML, dashboard configs, backup files — never leave your network
- Scan results and generated docs are written to local `references/` directory

**What leaves your machine (read-only, public data):**
- `fetch_release_notes.py` fetches public release data from `api.github.com` (GitHub Releases API)
- No authentication tokens, device data, or personal information is sent to GitHub

> **Trust statement:** Installing this skill grants it SSH and REST API access to your Home Assistant instance. Only install if you trust the skill author and have reviewed the scripts. All source code is open and auditable.

### External Endpoints

| Endpoint | Script | Direction | Data sent | Auth required |
|----------|--------|-----------|-----------|---------------|
| `HA_URL/api/*` | all `.sh` scripts, `scan_integrations.py` | Local network | Service calls, state queries | `HA_TOKEN` (Bearer) |
| `SSH HA_HOST` | all `.sh` scripts, `scan_integrations.py` | Local network | CLI commands, file ops | SSH key or password |
| `api.github.com/repos/home-assistant/core/releases` | `fetch_release_notes.py` | **Outbound (internet)** | None (GET only) | None |

## Capabilities

This skill provides a full management toolkit for Home Assistant via SSH.

### 🎮 Device Control (`scripts/ha.sh`)
```bash
ha.sh on light.kitchen              # Turn on
ha.sh off switch.fan                # Turn off
ha.sh toggle light.bedroom          # Toggle
ha.sh on light.room 180             # Light with brightness (0-255)
ha.sh scene movie_night             # Activate scene
ha.sh script goodnight              # Run script
ha.sh climate climate.thermostat 22 # Set temperature
ha.sh call light turn_on '{"entity_id":"light.x","brightness":200}'  # Any service
```

### 🔍 Queries (`scripts/ha.sh`)
```bash
ha.sh list                          # All entities
ha.sh list lights                   # Lights only
ha.sh search kitchen                # Search by name
ha.sh state light.kitchen           # Current state
ha.sh info                          # HA version, connection
ha.sh addons                        # List add-ons
ha.sh config configuration.yaml     # Read config file
ha.sh logs core                     # Core logs
ha.sh updates                      # Combined update check (Core, OS, Addons, HACS)
```

### ⚙️ Automations (`scripts/ha-automations.sh`)
```bash
ha-automations.sh list              # List all automations
ha-automations.sh show <id>           # Show YAML (resolves entity_id to internal ID)
ha-automations.sh create auto.yaml  # Add from file (with backup + validation)
ha-automations.sh create-inline '...' # Add inline
ha-automations.sh enable automation.morning  # Enable
ha-automations.sh disable automation.morning # Disable
ha-automations.sh trigger automation.test    # Trigger manually
ha-automations.sh reload            # Reload from YAML
ha-automations.sh validate          # Check config
ha-automations.sh backup            # Backup automations.yaml
```

When creating an automation, the script:
1. Backs up automations.yaml
2. Appends the new automation
3. Validates config (`ha core check`)
4. If invalid — rolls back automatically
5. If valid — reloads automations

> [!TIP]
> `ha-automations.sh show` now automatically resolves `entity_id` to its internal YAML ID (e.g. `'1712173456789'`), making it compatible with both UI-created and manual automations.

### 📊 Monitoring (`scripts/ha-monitor.sh`)
```bash
ha-monitor.sh status                # Overview: online/offline/unavailable counts
ha-monitor.sh offline               # List offline/unavailable devices
ha-monitor.sh battery               # Low battery devices (<20%)
ha-monitor.sh battery 10            # Custom threshold 10%
ha-monitor.sh stale                 # Not updated in 24h
ha-monitor.sh stale 6               # Not updated in 6h
ha-monitor.sh errors                # Recent error log entries
ha-monitor.sh health                # Full system health report
```

### 💾 Backups (`scripts/ha-backup.sh`)
```bash
ha-backup.sh list                   # List backups
ha-backup.sh create "before-update" # Full backup
ha-backup.sh create-partial         # Config only
ha-backup.sh info <slug>            # Backup details
ha-backup.sh download <slug> ./     # Download to local machine
ha-backup.sh restore <slug>         # Restore (⚠️ restarts HA)
ha-backup.sh remove <slug>          # Delete backup
```

### 📦 HACS (`scripts/ha-hacs.sh`)
```bash
ha-hacs.sh list                     # Custom components
ha-hacs.sh installed                # With versions
ha-hacs.sh updates                  # Available updates
ha-hacs.sh repos                    # HACS repositories
ha-hacs.sh logs                     # HACS-related logs
```

### 📱 Dashboards (`scripts/ha-dashboard.sh`)
```bash
ha-dashboard.sh list                # List dashboards
ha-dashboard.sh show                # Show dashboard config
ha-dashboard.sh entities lights     # List entities for cards
ha-dashboard.sh generate-view kitchen  # Generate view for a room
ha-dashboard.sh apply dash.yaml     # Upload dashboard config
ha-dashboard.sh backup              # Backup dashboard
```

`generate-view` creates a YAML template for a room: finds all entities by name, groups by type (lights, switches, sensors, climate).

### 📰 Knowledge Updates (`scripts/fetch_release_notes.py`)
> Remember: use absolute skill path (see top note)
```bash
python3 /path/to/skill/scripts/fetch_release_notes.py              # Last 3 releases (default)
python3 /path/to/skill/scripts/fetch_release_notes.py --last 5     # Last 5 releases
python3 /path/to/skill/scripts/fetch_release_notes.py --version 2026.5  # Specific version
```

### 🔎 Instance Scan (`scripts/scan_integrations.py` + `generate_integration_docs.py`)
> Remember: use absolute skill path (see top note)
```bash
python3 /path/to/skill/scripts/scan_integrations.py                                       # Text summary (reads env vars)
python3 /path/to/skill/scripts/scan_integrations.py --format json --output /path/to/skill/references/ha_scan.json  # JSON for docs gen
python3 /path/to/skill/scripts/generate_integration_docs.py                               # Uses default paths
```

---

- YAML configuration (configuration.yaml, automations.yaml, scripts, scenes)
- Jinja2 templating (states, attributes, filters, new functions)
- Automation triggers, conditions, actions (including new **purpose-specific and cross-domain triggers**)
- Dashboard configuration (**Sections view** with background colors and auto-height)
- Integration setup and troubleshooting
- ESPHome device configuration
- Matter/Thread device management
- **Native infrared (IR)** control (LG Infrared, ESPHome proxies)
- **SecureTar v3** backup security (Argon2id + XChaCha20-Poly1305)

## When Helping Users

1. **Always check `references/ha-state.json` first** — it stores the user's actual HA version (set by `scan_integrations.py`). If `ha_version` is null, ask the user or suggest running a scan.
2. **Never assume the user is on the latest version.** If a feature was added in 2026.5 but user is on 2026.4 — say "This requires HA 2026.5+, you're on 2026.4.0."
3. **Breaking changes are version-relative:**
   - If user's version >= breaking version → the change already applies, help migrate
   - If user's version < breaking version → warn that it WILL break when they upgrade, suggest preparing
4. **Prefer UI-based setup** when possible; mention YAML alternatives for power users.
5. **Use the current YAML style**: `triggers:` (not `trigger:`), `conditions:`, `actions:` (not `action:`). The plural form is the modern standard since 2024.x.
6. **Use `action:` for service calls** inside actions blocks (not the deprecated `service:`).
7. **For release-specific details**, consult `references/ha-release-notes.md` — this is auto-populated by running `scripts/fetch_release_notes.py`.
8. **For user-specific setup**, consult `references/user-integrations.md` for installed integrations and their configs.
9. **Holistic Diagnostics (Alternatives & Add-ons):** If an integration is `not_loaded`, `unavailable`, or `offline` (e.g., ZHA, default Tuya), do NOT immediately attempt to repair or delete it. Home Assistant architectures often use alternative Add-ons or HACS components (e.g., Zigbee2MQTT instead of ZHA, Frigate instead of standard camera integrations). Always cross-reference installed Add-ons (`ha.sh addons`) and HACS components (`ha-hacs.sh installed`) to verify if the user relies on an alternative system before touching the "broken" integration.

## YAML Automation Syntax (Modern)

```yaml
automation:
  - alias: "Descriptive Name"
    description: "What this automation does"
    mode: single  # single | restart | queued | parallel
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion_living_room
        to: "on"
    conditions:
      - condition: time
        after: "18:00:00"
        before: "23:00:00"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.living_room
        data:
          brightness_pct: 80
          transition: 2
```

## Release-Specific Features & Breaking Changes

**Do not hardcode release info here.** Instead:

1. Check `references/ha-release-notes.md` for features and breaking changes specific to the user's version
2. If that file is empty, run `scripts/fetch_release_notes.py` to populate it
3. If scripts can't run, use web search: `Home Assistant YYYY.M release notes`

When a user asks about features or breaking changes:
- First check their HA version in `references/ha-state.json`
- Then look up the relevant release in `references/ha-release-notes.md`
- Only mention features available in their version or newer (with upgrade note)

## Configuration Best Practices

1. Use `secrets.yaml` for passwords and API keys
2. Enable 2FA on user profiles
3. Use Nabu Casa or VPN/reverse proxy for remote access (never expose ports directly)
4. Split large configs with `!include` and packages
5. Validate config before restarting: `ha-automations.sh validate` or Settings > three dots > Check configuration
6. Use the automation editor UI when possible; YAML for advanced templating
7. Always back up before updates: `ha-backup.sh create "before-update"`

## Troubleshooting Checklist

When a user reports issues after updating:

1. Check breaking changes for their version: `references/ha-release-notes.md`
2. Verify HA Core, Supervisor, and OS are all updated: `ha.sh info`
3. Check integration logs: `ha.sh logs core` or Settings > System > Logs
4. Check for ALL available updates: `ha.sh updates`
5. Run health check: `ha-monitor.sh health`
6. Check offline devices: `ha-monitor.sh offline`
7. Validate config: `ha-automations.sh validate`
8. Clear browser cache if dashboard looks wrong after update
9. For HACS components: `ha-hacs.sh updates` to check compatibility

**General Diagnostics:**
- **Avoid tunnel vision:** Before fixing an "Offline" or `not_loaded` integration, verify the overall architecture. Check `ha.sh addons` and `ha-hacs.sh installed`. The user might be intentionally leaving a native integration idle because they replaced it with a more powerful Add-on or Custom Component (e.g. Zigbee2MQTT instead of ZHA). Always verify the active ecosystem first.
- **Holistic Update Checks:** Home Assistant updates come from three distinct sources. NEVER assume that `ha.sh info` or `ha supervisor info` shows all updates. Always use `ha.sh updates` to see:
    1. **Core & Operating System** (Official)
    2. **Supervisor Add-ons** (Official ecosystem)
    3. **HACS & Custom Components** (Community ecosystem, tracked via `update.*` entities)

## First-Time Setup (Onboarding)

ALWAYS speak in the user's preferred language. Be concise — no walls of text.

### Quick Setup (one message to the user)

**Step A (agent does silently, BEFORE showing anything to the user):**

Read YOUR OWN (the agent's machine) SSH public key. Do NOT ask the user to do this:
```bash
cat ~/.ssh/id_ecdsa.pub 2>/dev/null || cat ~/.ssh/id_ed25519.pub 2>/dev/null || echo "NO_SSH_KEY"
```
If result is `NO_SSH_KEY` — generate a key silently (ECDSA preferred per HA docs):
```bash
ssh-keygen -t ecdsa -b 521 -N "" -f ~/.ssh/id_ecdsa -q
cat ~/.ssh/id_ecdsa.pub
```

**Step B (show the user ONE message with your key already included):**

The SSH key is YOUR key that YOU just read in Step A. Paste it into the message. The user does NOT generate or run anything — they just copy your key into HA.

> I need to set up access to your Home Assistant. Here's my SSH key — add it to your HA:
>
> **1. Install Terminal & SSH add-on** (skip if already installed)
> - **Settings → Add-ons → Add-on Store** → install **Terminal & SSH**
>
> **2. Add my SSH key**
> - Open the add-on → **Configuration** tab → paste this into `authorized_keys`:
>   ```yaml
>   authorized_keys:
>     - <YOUR_SSH_PUBLIC_KEY_HERE>
>   ```
> - Do NOT wrap the key in quotes — paste it as-is
> - The `password` field can be left as-is — key auth works regardless of password settings
> - Under **Network**, set the port (default: `22`), save, **start the add-on**
> - *(Docker/CasaOS/TrueNAS: add the key to `~/.ssh/authorized_keys` on the host instead)*
>
> **3. Create a Long-Lived Access Token**
> - Click your profile (bottom-left) → **Security** → **Long-Lived Access Tokens** → **Create Token**
> - Name it "OpenClaw", copy the token — it shows only once
>
> **4. Reply with:**
> - HA URL (e.g. `http://192.168.1.100:8123`) — find at **Settings → System → Network**
> - The token you just created
> - SSH port (if not default 22)

Then **wait for the user to reply**.

### After the user replies — auto-configure everything

Once the user provides their details, do ALL of this without stopping:

1. **Set env vars** in `~/.openclaw/openclaw.json` under `skills.entries`:
   ```json5
   {
     "skills": {
       "entries": {
         "home-assistant-toolkit": {
           "enabled": true,
           "env": {
             "HA_URL": "<user_url>",
             "HA_TOKEN": "<user_token>",
             "HA_HOST": "<user_ip_from_url_or_explicit>",
             "HA_SSH_PORT": "<port, default 22>",
             "HA_SSH_USER": "root",
             "HA_CONFIG_PATH": "/config"
           }
         }
       }
     }
   }
   ```
   Note: `HA_HOST` defaults to the hostname from `HA_URL` if user doesn't specify separately.
2. **Test SSH**: `ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 -p <port> root@<host> "ha core info"` — if it fails, tell the user to check that the SSH add-on is running and the key is added.
3. **Test REST API**: `bash /path/to/skill/scripts/ha.sh info`
4. **Scan integrations**:
   ```bash
   python3 /path/to/skill/scripts/scan_integrations.py --format json --output /path/to/skill/references/ha_scan.json
   ```
5. **Generate docs**:
   ```bash
   python3 /path/to/skill/scripts/generate_integration_docs.py
   ```
6. **Fetch release notes**:
   ```bash
   python3 /path/to/skill/scripts/fetch_release_notes.py
   ```
7. **Report**: show HA version, integration count, SSH status, and confirm setup is complete.

Do NOT ask intermediate questions. Just do the full setup and report results.

### Re-scanning

User says "rescan" or "scan my HA again" → re-run steps 4-6 above automatically.

---

## Updating Release Notes

The skill fetches HA release notes dynamically — it is NOT locked to any specific version.

### When to Update
- User says "Update HA release notes" or "What's new in Home Assistant?"
- User upgrades HA and asks about breaking changes
- Periodically to stay current

### How to Update
```bash
# Auto-detect user version from ha-state.json, fetch releases up to that version
python3 /path/to/skill/scripts/fetch_release_notes.py

# Fetch last 5 releases instead of default 3
python3 /path/to/skill/scripts/fetch_release_notes.py --last 5

# Force fetch for a specific max version
python3 /path/to/skill/scripts/fetch_release_notes.py --up-to 2026.4.0

# Ignore user version, fetch latest (e.g. user wants to preview before upgrading)
python3 /path/to/skill/scripts/fetch_release_notes.py --ignore-version

# Fetch a specific release only
python3 /path/to/skill/scripts/fetch_release_notes.py --version 2026.5
```

### Version-Aware Logic
- The script reads `references/ha-state.json` → `ha_version` (set by `scan_integrations.py`)
- **Only fetches releases <= user's version** by default
- This prevents the agent from recommending features the user doesn't have
- If the user asks "What's new if I upgrade?" — use `--ignore-version` to show newer releases too

### What It Does
1. Hits GitHub API (`home-assistant/core` releases) for stable release changelogs
2. Writes structured markdown to `references/ha-release-notes.md`
3. Includes: release dates, changelog bodies, links to blog posts and GitHub

### If Script Can't Run (no network, etc.)
The agent should use web search to look up:
- `Home Assistant YYYY.M release notes` — blog post
- `home-assistant/core releases` on GitHub — changelog
Then manually update `references/ha-release-notes.md` or answer from search results directly.

---

## Manual Setup (Without API Access)

If the user can't provide API access, they can:
1. Screenshot their Integrations page (Settings > Devices & Services)
2. Or list their integrations manually

Then the agent should:
1. Parse the provided information
2. Manually write `references/user-integrations.md` with documentation for each integration
3. Note any breaking changes that apply to the user's version

---

## User Setup Reference

If `references/user-integrations.md` exists, consult it for user-specific integration details, configs, and warnings. This file is auto-generated by the onboarding process above and contains a curated set of documentation for common Home Assistant integrations.
