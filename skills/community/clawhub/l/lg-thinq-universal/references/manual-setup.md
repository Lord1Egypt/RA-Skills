# Manual Setup Guide

Use this guide when `setup.sh` is not available or for understanding the complete setup process.

## Security Protocol (Mandatory)

The agent **MUST** follow these hard mandates:

1. **Ask First**: Use `ask_user` before every:
   - Network discovery call to LG API
   - File creation or modification on disk
   - Memory persistence entry

2. **Zero-Leak**: Never ask user to paste `LG_PAT` into chat.

3. **Environment Precedence**: Scripts use `load_dotenv(override=False)`. Shell environment variables take precedence.

4. **Minimal Credentials**: Only `LG_DEVICE_ID` in skill's `.env`. Never write `LG_PAT` or `LG_COUNTRY` there.

---

## Phase 1: Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `python-dotenv>=1.0.0` - Environment variable loading
- `requests>=2.25.0` - HTTP client

### 2. Configure Environment

**Shell environment (recommended)**:
```bash
export LG_PAT="thinqpat_your_token_here"
export LG_COUNTRY="IN"
```

**Or .env file in project root** (where this skill is installed):
```bash
echo "LG_PAT=thinqpat_your_token_here" > .env
echo "LG_COUNTRY=IN" >> .env
```
> ⚠️ **SECURITY WARNING**: This `.env` file should ONLY exist in the universal manager root. NEVER copy your `LG_PAT` into generated per-device folders. Shell environment variables are always the safest option.

Shell env takes precedence. API server URL is cached in `.api_server_cache`.

### 3. Save API Route (One-time)

```bash
python scripts/lg_api_tool.py save-route
```

Discovers regional API server and caches to `.api_server_cache`.

### 4. Check Configuration

```bash
python scripts/lg_api_tool.py check-config
```

Expected output:
```
✅ LG_PAT: set (XX chars)
✅ LG_COUNTRY: IN
✅ LG_API_SERVER: https://api-kic.lgthinq.com
```

---

## Phase 2: Device Discovery

### 5. Obtain Consent

Before calling the API, use `ask_user`:

> "May I use your LG_PAT to discover devices on the LG ThinQ API? This will list all connected LG ThinQ devices."

### 6. List Devices

```bash
python scripts/lg_api_tool.py list-devices
```

This returns all connected LG ThinQ devices with their IDs, names, and types.

### 7. Present Device List

Present the device list to user and ask which device(s) to integrate. Example:

```json
{
  "response": {
    "deviceList": [
      {
        "deviceId": "abc123...",
        "deviceName": "Living Room AC",
        "deviceType": "RAC"
      }
    ]
  }
}
```

---

## Phase 3: Skill Creation (For Each Device)

For each selected device, follow these steps:

### 8. Fetch Device Profile

```bash
python scripts/lg_api_tool.py get-profile <device_id>
```

Save to file for script generation:
```bash
python scripts/lg_api_tool.py get-profile <device_id> > profile.json
```

The profile contains all device capabilities: controllable properties, modes, ranges, etc.

### 9. Generate Control Script

```bash
python scripts/generate_control_script.py profile.json > lg_control.py
chmod +x lg_control.py
```

The generated script includes:
- All controllable properties from the profile
- Power commands (`on`, `off`)
- Status command (`status`)
- Device-specific commands (temperature, mode, fan speed, etc.)

### 10. Test Control Script

```bash
python lg_control.py --help     # Show available commands
python lg_control.py status     # Get current state
```

### 11. Create Skill Directory

```bash
mkdir -p ~/.openclaw/workspace/skills/lg-{device-type}-{short-id}
```

Example: `~/.openclaw/workspace/skills/lg-ac-livingroom/`

### 12. Move Files to Skill Directory

```bash
mv lg_control.py ~/.openclaw/workspace/skills/lg-{device-type}-{short-id}/
cp scripts/lg_api_tool.py ~/.openclaw/workspace/skills/lg-{device-type}-{short-id}/
```

### 13. Create Local .env

In the skill directory, create `.env` with only `LG_DEVICE_ID`:

```bash
cd ~/.openclaw/workspace/skills/lg-{device-type}-{short-id}
echo "LG_DEVICE_ID=<device_id>" > .env
chmod 600 .env
```

**Security**: Never write `LG_PAT` or `LG_COUNTRY` into this file. Only `LG_DEVICE_ID`.

### 14. Create Skill SKILL.md

Create `SKILL.md` for the device following `references/skill-generation-guide.md`.

### 15. Verify Skill

```bash
cd ~/.openclaw/workspace/skills/lg-{device-type}-{short-id}
python lg_control.py status
```

### 16. Save to Memory (With Consent)

Use `ask_user`:

> "May I record this setup in your memory for future recall?"

If approved, save:
```
[LG ThinQ Device Setup]
Device: {Device Name}
Trigger: "OpenClaw, manage my {Device Name}"
```

### 17. Notify User

> "Your {Device Name} is integrated! Try saying: 'OpenClaw, check the status of my {Device Name}'."

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
Run: `pip install -r requirements.txt`

### "LG_PAT is missing"
Ensure `LG_PAT` is set in environment or `.env` file.

### "LG_COUNTRY is missing"
Set `LG_COUNTRY` to your 2-letter ISO country code.

### API returns 401 Unauthorized
Your `LG_PAT` may be expired. Regenerate it from the LG ThinQ app.

### Device not responding
The `x-conditional-control` header may have rejected the command due to a state change. Retry the command.
