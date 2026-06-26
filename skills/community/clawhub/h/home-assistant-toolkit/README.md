# Home Assistant Toolkit for OpenClaw v2.0.0

A comprehensive OpenClaw skill for managing and monitoring Home Assistant via SSH and REST API.

This skill allows OpenClaw to:
- Control devices and entities (turn on/off, toggle, set brightness, temperature)
- Create, edit, enable/disable and validate YAML automations with automatic backup and rollback
- Back up and restore Home Assistant configurations
- Monitor system health, detect offline devices and low batteries
- Check for updates across Core, OS, Add-ons and HACS in one command
- Manage HACS custom components and repositories
- Generate and manage dashboard views
- Scan installed integrations and generate personalized documentation
- Fetch version-aware release notes with breaking change detection

## What's Included

| Script | Purpose |
|--------|---------|
| `scripts/ha.sh` | Device control, queries, system commands, update checks |
| `scripts/ha-automations.sh` | Create, show, enable/disable, validate automations |
| `scripts/ha-monitor.sh` | Health status, offline devices, battery, stale sensors |
| `scripts/ha-backup.sh` | Full and partial backups, restore, download |
| `scripts/ha-hacs.sh` | HACS components, versions, updates, repositories |
| `scripts/ha-dashboard.sh` | List, show, generate views, apply dashboard configs |
| `scripts/scan_integrations.py` | Scan HA instance for installed integrations |
| `scripts/generate_integration_docs.py` | Generate personalized integration docs with breaking changes |
| `scripts/fetch_release_notes.py` | Fetch version-aware release notes from GitHub |
| `scripts/check-setup.sh` | Verify skill configuration before use |

## Installation and Configuration

### Step 1: Configure SSH Access

To allow OpenClaw to connect to your Home Assistant instance, configure SSH using a public key.

#### Option A: Home Assistant OS (HAOS) / Supervised
*Choose this if your Home Assistant has an "Add-ons" menu.*
1. In Home Assistant, go to **Settings > Add-ons > Add-on Store** and install **Terminal & SSH**.
2. Open the add-on, go to the **Configuration** tab.
3. Paste the OpenClaw machine's public SSH key into `authorized_keys`:
   ```yaml
   authorized_keys:
     - ssh-ed25519 AAAAC3NzaC1... user@machine
   ```
   Do NOT wrap the key in quotes — paste it as-is.
   Find your key: `cat ~/.ssh/id_ed25519.pub` (or generate: `ssh-keygen -t ed25519`)
4. The `password` field can be left as-is — key-based auth works regardless of password settings.
5. Under **Network**, set a port (usually `22` or `22222`).
6. **Save** and **Start** the add-on.

#### Option B: Container (TrueNAS / CasaOS / Docker)
*Choose this if your Home Assistant runs as a container without Add-ons.*
1. Add the OpenClaw public SSH key to the host's `~/.ssh/authorized_keys` file.
2. Note the absolute path where your HA config directory is mapped (e.g., `/mnt/pool/apps/homeassistant/config`).
3. Features relying on the `ha` Supervisor CLI won't work, but automation management, config reading, and integration scanning work via REST API.

### Finding Your HA IP Address

Go to **Settings > System > Network > Local network** in Home Assistant to see the IP address and port. Alternatively, check your router's DHCP table.

### Step 2: Configure OpenClaw

Set connection parameters in `~/.openclaw/openclaw.json` under `skills.entries`, or as environment variables. `HA_URL` is the primary connection method (REST API); `HA_HOST` enables SSH for file operations.

```json5
{
  "skills": {
    "entries": {
      "home-assistant-toolkit": {
        "enabled": true,
        "env": {
          "HA_URL": "http://192.168.1.100:8123",
          "HA_TOKEN": "eyJhbGciOiJIUzI1...",
          "HA_HOST": "192.168.1.100",
          "HA_SSH_PORT": "22",
          "HA_SSH_USER": "root",
          "HA_CONFIG_PATH": "/config"
        }
      }
    }
  }
}
```

## Usage

Once configured, mention Home Assistant in your queries to OpenClaw. Examples:

**Device control:**
- "Turn off the kitchen lights."
- "Set the thermostat to 22 degrees."
- "Toggle the bedroom fan."

**Monitoring:**
- "Check my Home Assistant connection."
- "Show me devices with low battery."
- "Are any devices offline?"
- "Check for updates."

**Automations:**
- "List my automations."
- "Show the kitchen light automation."
- "Create an automation that turns on lights at sunset."

**Backups & maintenance:**
- "Create a backup before I update."
- "Scan my Home Assistant integrations."
- "What's new in Home Assistant?"

**Dashboards:**
- "Generate a dashboard view for the kitchen."
- "Show my current dashboard config."
