---
name: openclaw-voice-control
description: Local macOS voice-control integration for OpenClaw. Use when setting up, deploying, troubleshooting, or operating wakeword-triggered voice access to a local OpenClaw agent with ASR, TTS, overlay UI, and launchd background support.
homepage: https://github.com/CarrotYuan/openclaw-voice-control
metadata: {"openclaw":{"os":["darwin"],"homepage":"https://github.com/CarrotYuan/openclaw-voice-control","requires":{"bins":["python3","git","launchctl"],"env":["OPENCLAW_BASE_URL","OPENCLAW_TOKEN","SENSEVOICE_MODEL_PATH","SENSEVOICE_VAD_MODEL_PATH"]},"primaryEnv":"OPENCLAW_TOKEN"}}
---

# OpenClaw Voice Control

OpenClaw Voice Control is a local macOS voice-control integration for OpenClaw.

Repository source:

- GitHub: [CarrotYuan/openclaw-voice-control](https://github.com/CarrotYuan/openclaw-voice-control)

It provides:

- wakeword activation
- local microphone capture
- local ASR with FunASR / SenseVoice
- forwarding recognized text to a local OpenClaw agent
- macOS TTS playback
- optional overlay UI
- launchd-based background resident behavior
- auto-start after user login

## Platform

- macOS only

## Safety Warning

This skill adds a voice entrypoint, and that entrypoint is not identity-bound.

That means:

- anyone near the microphone may be able to trigger it
- any capability exposed through the connected OpenClaw agent may become reachable by voice

Recommended safety practice:

- add explicit safety constraints to the connected agent prompt
- require confirmation for high-risk actions
- avoid broad autonomous permissions for the voice-facing agent
- use least privilege for tools and connected systems

## Main Path

Treat this as a local deployment skill, not as a prompt-only helper.

When this skill is installed into OpenClaw:

- work inside the current installed skill directory for the current conversation agent
- use the declared GitHub repository as the source of truth
- do not silently switch to another local clone or an already-prepared environment
- do not continue until the workspace contains the real repository files, not just `SKILL.md`

The main installation guide is the repository `README.md`.
`README.zh-CN.md` is the Chinese companion guide.

Use this as the standard install path:

1. sync the full repository into the current installed skill workspace
2. create and activate `.venv`
3. run `pip install -e .`
4. download or populate the SenseVoice model directory
5. download or populate the VAD model directory
6. copy `.env.example` to `.env`
7. fill the required values in `.env`
8. use the default openWakeWord route
9. run direct-run validation with both the voice service and overlay process
10. ask whether the user wants background resident behavior and auto-start
11. if yes, run `./scripts/deploy_macos.sh`
12. if no, stop after direct-run validation

Before running any system-changing step in that path, explicitly tell the user
what you are about to do and get confirmation for:

- fetching and checking out the repository into the skill workspace
- running `pip install -e .` from the repository
- downloading large local models or wakeword assets
- enabling background resident behavior or launchd auto-start

Minimum command path:

```bash
# from the current conversation agent's installed skill directory
git init
git remote add origin https://github.com/CarrotYuan/openclaw-voice-control.git
git fetch --depth 1 origin main
git checkout -B main FETCH_HEAD
# do not continue until the workspace contains scripts/, src/, config/,
# launchagents/, and README.md
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
./.venv/bin/modelscope download --model iic/SenseVoiceSmall --local_dir models/SenseVoiceSmall
./.venv/bin/python - <<'PY'
from funasr import AutoModel
AutoModel(model='fsmn-vad', disable_update=True)
PY
cp .env.example .env
# terminal 1, from the current installed skill workspace
python -m openclaw_voice_control --config config/default.yaml --env-file .env
# terminal 2, from the same workspace
python -m openclaw_voice_control.overlay_app --config config/default.yaml --env-file .env
```

Direct-run validation is not complete unless both commands above are running at
the same time from the same installed skill workspace.

Before any next step after direct-run validation, stop that test
first.

This includes:

- background resident deployment
- auto-start validation
- starting another direct-run test

If an old direct-run service and overlay are left running, two active voice
runtimes can respond to the same wakeword and produce duplicate replies.

## What Must Exist Before Setup

Before setup begins, make sure these prerequisites exist or can be provided:

- Python 3.11 or newer
- a running local OpenClaw service
- `OPENCLAW_TOKEN`
- macOS microphone permission
- a way to download the local SenseVoice and VAD model directories

For the default route, the remaining setup can usually be handled by the AI or
operator:

- copy `.env.example` to `.env`
- download the SenseVoice model directory
- download or populate the VAD model directory
- let openWakeWord download the selected pretrained wakeword model on first run

## Recommended Defaults

The default public route is:

- `WAKEWORD_PROVIDER=openwakeword`
- `OPENWAKEWORD_MODEL_NAME=hey jarvis`
- `OPENCLAW_AGENT_ID=main`
- `OPENCLAW_MODEL=openclaw:main`
- `OPENCLAW_USER=openclaw-voice-control`

Prefer that route unless the user explicitly asks for something else.

## Default Route Variables

These are the main values for the default route:

- required in `.env`
  - `OPENCLAW_BASE_URL`
  - `OPENCLAW_TOKEN`
  - `SENSEVOICE_MODEL_PATH`
  - `SENSEVOICE_VAD_MODEL_PATH`
- usually left at their documented defaults unless the user wants customization
  - `WAKEWORD_PROVIDER=openwakeword`
  - `OPENWAKEWORD_MODEL_NAME=hey jarvis`
  - `OPENCLAW_AGENT_ID=main`
  - `OPENCLAW_MODEL=openclaw:main`
  - `OPENCLAW_USER=openclaw-voice-control`

If the user changes the macOS TTS voice, first make sure that voice has been
downloaded in:

- System Settings
- Accessibility
- Spoken Content
- the `i` button next to System Voice
- Language
- Voice

## Optional Porcupine Route

Picovoice / Porcupine is an optional fallback route, not the default path.

Only switch to it when the user explicitly wants to use a local `.ppn` wakeword
model.

If that route is chosen, set:

- `WAKEWORD_PROVIDER=porcupine`
- `PICOVOICE_ACCESS_KEY`
- `WAKEWORD_FILE`

Only ask for those Porcupine-specific values when the user explicitly chooses
that route.

## Switching openWakeWord Models

To switch the default openWakeWord wakeword, change:

- `OPENWAKEWORD_MODEL_NAME`

Common official pretrained examples include:

- `hey jarvis`
- `hey mycroft`
- `hey rhasspy`
- `alexa`

Those pretrained wakeword models are downloaded automatically on first use.

The code path already supports changing `OPENWAKEWORD_MODEL_NAME`, but only the
default `hey jarvis` route has been smoke-tested in this repository so far.

## Execution Rules

When using this skill, follow these rules:

1. Use the declared GitHub repository first.
   - Start from `https://github.com/CarrotYuan/openclaw-voice-control.git`
   - Do not substitute another repository just because it looks similar.

2. Keep deployment work in the current installed skill workspace.
   - Do not silently switch to another local clone.
   - If GitHub access fails and a local clone exists, ask before using it.

3. Do not silently reuse an old environment.
   - Do not assume an existing `.venv`, local model cache, previous `.env`, or private runtime should be reused.
   - If reusing cached assets might save time, explain that and ask first.

4. Do not invent missing values.
   - When writing `.env`, use the exact variable names required by the project, especially `OPENCLAW_TOKEN`.
   - If required values or local assets are missing, stop and point to the documented source of truth.

5. Handle secrets conservatively.
   - Do not print real tokens or keys back into the conversation unless the user explicitly asks to see them.
   - For this project, use the OpenClaw token from `~/.openclaw/openclaw.json`, specifically the `gateway` configuration.
   - Do not use `~/.openclaw/identity/device-auth.json` as the token source for this project.

6. Ask before any system-changing action.
   - Do not assume you should fetch the repository, run `pip install -e .`, download models, or enable launchd behavior without user approval.
   - Explain the action first, then continue only after the user confirms.

7. Ask before enabling background resident behavior.
   - Foreground validation comes first.
   - Direct-run validation means starting both `python -m openclaw_voice_control --config config/default.yaml --env-file .env` and `python -m openclaw_voice_control.overlay_app --config config/default.yaml --env-file .env` from the same installed skill workspace.
   - Only run `./scripts/deploy_macos.sh` when the user explicitly wants background resident behavior or auto-start.

## Daily Maintenance

Primary scripts:

- deploy background runtime: `./scripts/deploy_macos.sh`
- restart installed background services: `./scripts/restart_service.sh`
- uninstall installed background services: `./scripts/uninstall_macos.sh`
- inspect local installation and environment issues: `./scripts/doctor.sh`

Double-click `.command` wrappers are also available in `scripts/` for macOS users who prefer Finder-based execution.

## Shutdown Intents

Treat shutdown requests as one of these two user intents:

- temporarily disable voice functionality
  - stop the running direct-run process, or stop the deployed background runtime
  - do not delete the skill folder
- delete the skill completely
  - remove the skill folder itself
  - only do this when the user explicitly asks for full removal

If the user says something ambiguous like "turn it off" or "stop voice", ask one short clarification question before acting.

## Background Architecture

The canonical background startup path is:

- `launchd -> host app -> shell script -> python`

`./scripts/deploy_macos.sh` builds the required host apps automatically.

## Configuration Surface

Default-route required values:

- `OPENCLAW_BASE_URL`
- `OPENCLAW_TOKEN`
- `SENSEVOICE_MODEL_PATH`
- `SENSEVOICE_VAD_MODEL_PATH`

Default-route configurable values:

- `OPENCLAW_AGENT_ID`
- `OPENCLAW_MODEL`
- `OPENCLAW_USER`
- `WAKEWORD_PROVIDER`
- `OPENWAKEWORD_MODEL_NAME`
- `OPENWAKEWORD_MODEL_PATH`

If the user explicitly switches to the optional Porcupine route, also configure:

- `PICOVOICE_ACCESS_KEY`
- `WAKEWORD_FILE`

Interpreter override variables still exist:

- `VOICE_CONTROL_PYTHON_BIN`
- `VOICE_CONTROL_OVERLAY_PYTHON_BIN`

They are troubleshooting knobs only, not the main deployment model.

`OPENWAKEWORD_THRESHOLD` still exists as a tuning variable, but it is a
troubleshooting adjustment rather than a first-run requirement.

As a rule, machine-specific secrets and paths belong in `.env`, while wakeword
timing and threshold tuning should normally be adjusted in `config/default.yaml`.

## Where To Get Missing Requirements

After syncing the repository into the current installed skill workspace, read these sections in `README.md`:

- `What Must Exist Before Setup`
- `Required Variables`
- `Where To Get Each Requirement`

Practical source notes:

- `OPENCLAW_BASE_URL`: use the full OpenClaw chat completions endpoint, not only the host and port root. For the default local setup, use `http://127.0.0.1:18789/v1/chat/completions`
- `OPENCLAW_TOKEN`: obtain it from the local OpenClaw gateway configuration in `~/.openclaw/openclaw.json`, under `gateway`
- default wakeword route: use openWakeWord with the built-in English `hey jarvis` model
- optional Porcupine route: obtain `PICOVOICE_ACCESS_KEY` and the local `.ppn` file from [Picovoice](https://picovoice.ai/)
- if GitHub clone fails, report that first rather than switching to an unrelated local directory

## Related Files

- `README.md` in the cloned repository
- `README.zh-CN.md` in the cloned repository
- `docs/macos-install.md` in the cloned repository
