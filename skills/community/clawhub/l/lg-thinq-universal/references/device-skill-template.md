# LG ThinQ {Device Name} Skill Template

This is a template for the `SKILL.md` of a generated LG device skill.

---
name: lg-{type}-{location}
description: Control LG {Device Name} ({Type}). Use for: (1) Power on/off, (2) Adjust {features}, (3) Check status.
requires:
  vars:
    - LG_DEVICE_ID
metadata:
  openclaw:
    emoji: "❄️" # Change based on device type
---

# {Device Name} Control

## 📍 Configuration
The unique identifier for this device is stored in the local `.env` file within this directory.
- **File**: `~/.openclaw/workspace/skills/lg-{type}-{location}/.env`
- **Variable**: `LG_DEVICE_ID`

**Note**: Your `LG_PAT` and `LG_COUNTRY` must be available in your shell environment when this skill runs.

## ⌨️ Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `python lg_control.py on` | Turn device on | - |
| `python lg_control.py off` | Turn device off | - |
| `python lg_control.py status` | Get current state | - |
| `python lg_control.py {property} <val>` | Set a property | See help for values |

## 🤖 Agent Workflow

1. **Check Status**: Always check `status` before making changes.
2. **Explain Action**: Before running a command, tell the user what you are doing.
3. **Verify**: Run `status` again after a change to confirm it was successful.

## 🚨 Troubleshooting
- **401 Error**: Your account token (LG_PAT) has expired. Refresh it at the portal.
- **404 Error**: The `LG_DEVICE_ID` in the local `.env` is incorrect or the device is offline.
- **Permission Denied**: Run `chmod +x lg_control.py`.
