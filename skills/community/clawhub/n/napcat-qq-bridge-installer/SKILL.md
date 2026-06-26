---
name: napcat-qq-bridge-installer
description: Install, start, repair, and smoke-test a Windows QQ + NapCat + OpenClaw bridge. Use this when the user explicitly wants an end-to-end local QQ bot setup, needs NTQQ/NapCat downloaded from public sources, or needs an existing NapCat bridge fixed.
---

# NapCat QQ Bridge Installer

## Overview

Use this skill for Windows hosts that need a local QQ bot stack built around NTQQ, NapCat, and an OpenClaw agent running through WSL + Docker.

This skill is script-driven. Prefer the bundled Python entrypoint instead of rewriting the setup flow by hand:

- `scripts/manage.py`

The script can:

- install NTQQ with `winget` if QQ is missing
- download the latest public NapCat release from GitHub at runtime
- overlay a local `bridge.mjs`, `start-all.bat`, and `stop-all.bat`
- generate `config/bridge.json` and `config/onebot11_<qq>.json`
- bootstrap a basic OpenClaw Docker container if requested
- start, stop, repair, health-check, and smoke-test the bridge

## When To Use It

Use this skill when the user asks for any of the following:

- install a QQ bot on Windows
- wire NapCat to OpenClaw
- download NTQQ / NapCat automatically
- repair a broken QQ bridge
- start or stop an existing NapCat + OpenClaw runtime
- verify whether QQ replies are still flowing

Do not use this skill for official QQ APIs or cloud-hosted bot platforms. This is for local unofficial automation with NapCat.

## Host Prerequisites

Expect these host tools to exist or be installable on demand:

- Windows with Python 3 available as `python`
- `winget` for installing `Tencent.QQ.NT`
- `wsl.exe`
- Docker inside the selected WSL distro

Download sources used by the bundled script:

- `https://api.github.com/repos/NapNeko/NapCatQQ/releases/latest`
- `winget install --id Tencent.QQ.NT --exact`

## Workflow

### 1. Pick the runtime root

Default runtime root:

- `C:\Users\<user>\NapCat.OpenClaw`

If the user already has an extracted NapCat runtime, point `-Root` at that folder and prefer `repair` over `install`.

### 2. Run the bundled manager

Typical install:

```powershell
python .\scripts\manage.py `
  -Action install `
  -Root C:\Bots\NapCat.OpenClaw `
  -BotQq 123456789 `
  -AdminQq 987654321 `
  -GroupIds 123456,234567 `
  -BootstrapOpenClaw
```

Typical repair:

```powershell
python .\scripts\manage.py `
  -Action repair `
  -Root C:\Bots\NapCat.OpenClaw `
  -BotQq 123456789
```

Start / stop / health / smoke test:

```powershell
python .\scripts\manage.py -Action start -Root C:\Bots\NapCat.OpenClaw
python .\scripts\manage.py -Action stop -Root C:\Bots\NapCat.OpenClaw
python .\scripts\manage.py -Action health -Root C:\Bots\NapCat.OpenClaw
python .\scripts\manage.py -Action smoke-test -Root C:\Bots\NapCat.OpenClaw
```

### 3. Handle OpenClaw auth when needed

If the OpenClaw container is new or unauthenticated, the user still needs one browser login step for `openai-codex`.

Use:

```powershell
python .\scripts\manage.py -Action auth -Root C:\Bots\NapCat.OpenClaw
```

That action opens a terminal with the recommended onboarding command. Do not promise fully unattended OAuth login.

### 4. Validate the running bridge

After install or repair, always run:

- `health`
- `smoke-test`

If the user already has a live QQ session, prefer a private-message self-test to the configured admin QQ.

## Safety And Publishing Constraints

- This skill is public. Never hardcode a real QQ number, group ID, token, container auth blob, or local secret into the published files.
- Generate local tokens at install time inside `config/bridge.json` and `config/onebot11_<qq>.json`.
- Generate `config/.env` and `config/webui.json` values locally for NapCat quick-login fallback. Do not publish real runtime secrets.
- Download NTQQ and NapCat from public runtime sources at execution time. Do not bundle vendor binaries into the skill.
- If the OpenClaw container already exists, repair it in place instead of deleting user data.
- Do not assume quick login can bypass every QQ verification challenge. QQ may still require a fresh verification step.

## Bundled Resources

- `scripts/manage.py`: main entrypoint for install, auth, start, stop, repair, health, and smoke test
- `assets/runtime/bridge.mjs`: generic Windows-host bridge that talks to NapCat and calls OpenClaw through `wsl docker exec ... openclaw agent`
- `assets/runtime/start-all.bat.txt`: rendered into the runtime root
- `assets/runtime/stop-all.bat.txt`: rendered into the runtime root
