# ImageForge Installation

ImageForge is the `image-forge` skill in this repository. It targets OpenClaw, Codex, Claude Code, and other agents that can read Agent Skills.

## Local clone with npx

From a local clone of this multi-skill repository:

```bash
npx skills add . --list --full-depth
```

Local discovery has been verified with this command: `npx skills add . --list --full-depth` lists `image-forge` in this multi-skill repo.

To install only ImageForge from the local clone:

```bash
npx skills add . --skill image-forge --full-depth
```

For a private multi-skill repo, the safest verified path is:

```bash
git clone <private repo URL>
cd product-skills
npx skills add . --list --full-depth
npx skills add . --skill image-forge --full-depth
```

## GitHub package/source caveats

`npx skills add <package>` supports GitHub package/source input according to CLI help. Private remote install still depends on the target machine's Git, network, and authentication setup.

For private repositories, prefer cloning first and installing from the local directory. This avoids ambiguity around private remote access and multi-skill repo selection.

## OpenClaw note

ImageForge is designed for OpenClaw as an Agent Skill. Use the OpenClaw skill installation path supported by the target OpenClaw version, or install from a local clone with `npx skills add` when that is the verified path for the machine.

If the target agent scans skills only at startup, restart or reload the agent after installing `image-forge`.

## First-use configuration

After installing the skill, normal users do not need to run setup commands manually. The agent must resolve the installed helper and run `ensure-ready` before every ImageForge operation:

```bash
WORKSPACE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
IMAGE_FORGE_SCRIPT=""
for candidate in \
  "$WORKSPACE_ROOT/.agents/skills/image-forge/scripts/image_forge.py" \
  "$PWD/.agents/skills/image-forge/scripts/image_forge.py" \
  "$HOME/.agents/skills/image-forge/scripts/image_forge.py"; do
  if [ -f "$candidate" ]; then IMAGE_FORGE_SCRIPT="$candidate"; break; fi
done
if [ -z "$IMAGE_FORGE_SCRIPT" ]; then echo "ImageForge helper not found"; exit 2; fi
python3 "$IMAGE_FORGE_SCRIPT" ensure-ready
```

If configuration is missing, `ensure-ready` stops the current flow and starts the local setup page. The setup server listens only on `127.0.0.1`, prints a one-time local URL, and tries to open the browser. The user registers/logs in at `https://www.nextai-code.com`, gets an API Key, then fills API key and default model in that page. The default model is `gpt-image-2`; keep it unless NextAI Code requires another model. The API URL is fixed to `https://www.nextai-code.com/v1` and cannot be changed. The service must implement:

- `/v1/images/generations`
- `/v1/images/edits`

After saving, the setup server persists configuration and shuts down automatically. Secrets are written to the user secret file, never to the skill folder, Git, logs, or agent replies.

Generated and edited images are saved by default directly in the project root. ImageForge writes `.png` image files only; it does not create `ImageForge/outputs/YYYY-MM-DD/` or output sidecar `.json` files.

Before any ImageForge task, run:

```bash
python3 "$IMAGE_FORGE_SCRIPT" ensure-ready
```

If readiness fails, stop. Do not continue with local layout, local drawing, screenshots, or any non-ImageForge fallback. Configure API key and model first; the API URL is fixed to NextAI Code.

## Basic commands

Check readiness:

```bash
python3 "$IMAGE_FORGE_SCRIPT" ensure-ready
```

Check current configuration without starting setup:

```bash
python3 "$IMAGE_FORGE_SCRIPT" preflight
```

Generate after the Image Brief Gate is approved:

```bash
python3 "$IMAGE_FORGE_SCRIPT" generate --brief '<approved brief>' --prompt '<prompt>'
```

Edit after the Image Brief Gate is approved:

```bash
python3 "$IMAGE_FORGE_SCRIPT" edit --brief '<approved brief>' --image '<path>' --prompt '<instruction>'
```

Diagnose local configuration:

```bash
python3 "$IMAGE_FORGE_SCRIPT" doctor
```

## Update check

Run:

```bash
python3 "$IMAGE_FORGE_SCRIPT" check-version
```

Version checks degrade safely and never block generation or editing. If an update is available, the output includes:

```bash
npx skills update image-forge
```
