---
name: lg-thinq-universal
description: Universal LG ThinQ device manager. Discovers appliances (AC, Refrigerator, Washer, etc.) and generates secure, device-specific OpenClaw skills. Use when the user wants to: (1) Integrate LG ThinQ devices, (2) Know how to get an LG PAT token, (3) Discover new LG appliances, (4) Create specialized control skills for their home automation.
version: 1.1.0
requires:
  env:
    - LG_PAT
    - LG_COUNTRY
  vars:
    - LG_DEVICE_ID
  install: ./setup.sh
metadata:
  openclaw:
    emoji: "🔐"
---

# LG ThinQ Universal Manager

## 🎯 Goal
Provide a secure, automated gateway for LG ThinQ device integration. This skill acts as a **discovery engine** and **skill generator**, allowing users to control their appliances via OpenClaw without duplicating sensitive credentials across multiple files.

## 📦 Supply Chain & Dependencies
For transparency and security, this skill performs the following automated installation steps:
1.  **Python Virtual Environment**: Created locally within the skill directory to ensure isolation.
2.  **External Packages (via PyPI)**:
    - `requests`: Used for secure communication with the LG ThinQ API.
    - `python-dotenv`: Used for local management of the `LG_DEVICE_ID`.
3.  **Network Access**: The installation script connects to `pypi.org` to download these libraries.

## 🔑 Obtaining Credentials
If the user asks how to get their tokens, provide these instructions:

1.  **Visit the Portal**: [https://connect-pat.lgthinq.com](https://connect-pat.lgthinq.com)
2.  **Log In**: Use your official LG ThinQ account.
3.  **Create Token**: Click "ADD NEW TOKEN", give it a name (e.g., "OpenClaw"), and select the required features.
4.  **Copy PAT**: Copy the generated Personal Access Token (PAT) immediately.
5.  **Identify Country**: Use your 2-letter ISO country code (e.g., `US`, `IN`, `GB`).

## 🛠️ Prerequisites
The agent **MUST** ensure the following are set before proceeding:
1.  **`LG_PAT`**: Stored in shell environment or root `.env`.
2.  **`LG_COUNTRY`**: Stored in shell environment or root `.env`.

## 🔄 Agent Workflow (Mandatory)

Follow these steps in order when a user requests setup:

### Step 1: Discovery
Run the automated discovery script. It validates configuration and prepares the device database. 

**Mandatory Safety Flow**: 
1.  **Generate Manifest**: Run `./setup.sh` (without flags).
2.  **Brief User**: Present the Manifest and explain exactly what actions will be performed.
3.  **Ask for Permission**: Use `ask_user` to obtain explicit consent.
4.  **Execute**: Only after approval, run: `./setup.sh --confirm`.

### Step 2: Assemble Workspace
Review the output from Step 1. Present the discovered devices to the user. Once an ID is selected, move **immediately** to assembly:
1.  **Generate Manifest**: Run `python3 scripts/assemble_device_workspace.py --id <DEVICE_ID>` (without flags).
2.  **Ask for Permission**: Use `ask_user` to obtain consent for the file/directory operations.
3.  **Execute**: Run: `python3 scripts/assemble_device_workspace.py --id <DEVICE_ID> --confirm`.

### Step 3: Document and Persist
After the assembly script completes, you **MUST** immediately:
1.  **Analyze**: Review the `[AVAILABLE COMMANDS]` and `[ENGINE CODE]` printed by the script.
2.  **Consult Reference**: Read `references/api-reference.md` for technical headers and control logic.
3.  **Generate SKILL.md**: Create the documentation in the new directory using `references/device-skill-template.md` as your guide.
4.  **Persistence**: Save the trigger phrase, skill path, and command summary into your global `MEMORY.md`.

## ⌨️ Universal Management Commands

Use these commands for maintenance and discovery:

| Command | Description | Use Case |
|---------|-------------|----------|
| `python scripts/lg_api_tool.py list-devices` | List all linked appliances | Verify connectivity |
| `python scripts/lg_api_tool.py save-route` | Discover regional server | Fix "Route not found" errors |
| `python scripts/lg_api_tool.py get-state <id>` | Get raw device state | Deep debugging |
| `python scripts/lg_api_tool.py --help` | Show all API tool options | Explore advanced features |

## 🛡️ Security Mandates
1.  **Zero-Leak Policy**: NEVER ask the user to paste their `LG_PAT` into the chat.
2.  **Credential Isolation**: NEVER copy `LG_PAT` into generated device skill directories. Only `LG_DEVICE_ID` is permitted in those locations.
3.  **Local-Only**: All API communication must remain local.

## 📚 References

| Document | Purpose |
|----------|---------|
| `references/skill-creation.md` | Detailed post-setup workflow for creating device skills |
| `references/skill-generation-guide.md` | Instructions for building device-specific SKILL.md files |
| `references/manual-setup.md` | Manual installation steps (without setup scripts) |
| `references/api-reference.md` | Technical details on API headers and control logic |
| `references/device-example.md` | Complete example of a generated device skill |
| `references/public_api_constants.json` | Public API keys and constants used by the scripts |

## 🚨 Error Handling

| Symptom | Resolution |
|---------|------------|
| `401 Unauthorized` | Token expired. Guide user to [https://connect-pat.lgthinq.com](https://connect-pat.lgthinq.com). |
| `No devices found` | Verify device is added to the official **LG ThinQ App** on mobile first. |
| `Permission denied` | The script should already be executable. If not, inform the developer. |
