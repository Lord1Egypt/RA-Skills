---
name: midea-cloud-control
description: Connect and control Midea devices through the Midea cloud with a local cached account/device config. Use when a user wants to connect a Midea account, list discovered Midea devices, or power on/off a named Midea air conditioner through cloud APIs. Triggers include requests like “连接美的设备”, “配置美的账号”, “列出我的美的设备”, “打开儿童房空调”, and “关闭主卧空调”.
---

# Midea Cloud Control

This is a **pure-text publishable skill** for ClawHub.

The uploaded skill folder contains only Markdown/text files. When the skill is first used, OpenClaw should write local helper scripts from the code blocks stored in `references/generated-config-store.md` and `references/generated-midea-skill-cli.md`, then execute those local scripts.

Use this skill only for the **minimum verified workflow**:
- connect a user's Midea cloud account
- read and cache device information locally
- power a named device on or off

Do **not** promise features that are not yet verified, including:
- temperature control
- real-time state reads
- indoor temperature reads
- mode switching

## Bootstrap step (first use only)

Before handling connect/list/toggle requests, ensure the following two local files exist in a local working directory, for example `skills_runtime/midea-cloud-control/` under the workspace:

- `config_store.py`
- `midea_skill_cli.py`

If they do not exist:
1. Read `references/generated-config-store.md`
2. Extract the Python code block and write it locally as `config_store.py`
3. Read `references/generated-midea-skill-cli.md`
4. Extract the Python code block and write it locally as `midea_skill_cli.py`
5. Then run commands against the local generated `midea_skill_cli.py`

Suggested local runtime directory:

```text
skills_runtime/midea-cloud-control/
```

## Conversation workflow

### Intent A: connect Midea account
When the user says things like:
- 我想连接美的设备
- 帮我配置美的账号
- 连接我的美的空调

Do this:
1. Tell the user credentials will be saved locally at `~/.openclaw/midea-cloud-control/config.json`.
2. Ask for account and password if they have not provided them yet.
3. Ensure the bootstrap step above has been completed.
4. Run:

```powershell
uv run python skills_runtime/midea-cloud-control/midea_skill_cli.py connect --account "<ACCOUNT>" --password "<PASSWORD>"
```

5. If success, summarize devices as:
   - device name
   - device id
   - model
   - home
6. If failure, show the returned failure reason clearly.

### Intent B: list connected devices
When the user asks to list devices:
1. Ensure the bootstrap step above has been completed.
2. Run:

```powershell
uv run python skills_runtime/midea-cloud-control/midea_skill_cli.py list
```

If config is missing, tell the user to connect account first.

### Intent C: power on/off by device name
When the user says things like:
- 打开儿童房空调
- 关闭主卧空调
- 打开“客厅空调”

Do this:
1. Ensure the bootstrap step above has been completed.
2. Run one of:

```powershell
uv run python skills_runtime/midea-cloud-control/midea_skill_cli.py toggle --device-name "儿童房空调" --power on
uv run python skills_runtime/midea-cloud-control/midea_skill_cli.py toggle --device-name "儿童房空调" --power off
```

Then:
1. Report that the cloud command was sent.
2. Do **not** claim physical success unless the user confirms the device reacted.
3. If the device name is missing from cache, tell the user to reconnect or list devices first.

## Safety and privacy
- Always warn before first-time credential storage.
- Do not echo passwords back in normal chat responses.
- Keep the response focused on success/failure and device summary.

## Resources

### references/
- `references/api-notes.md` — validated scope and limitations
- `references/generated-config-store.md` — source code to generate local `config_store.py`
- `references/generated-midea-skill-cli.md` — source code to generate local `midea_skill_cli.py`
