# Setup Guide

Use this guide when the goal is "make OpenClaw use GitHub Copilot with the least friction."

## Who this is for

This skill is useful when:

- OpenClaw is already installed
- the user wants GitHub Copilot as the default coding model
- the user wants the shortest reliable path, not a deep dive into provider internals

## 1. Confirm OpenClaw is installed

```bash
openclaw --version
```

If that command fails, install OpenClaw first. The skill itself does not replace the CLI.

## 2. Check whether Copilot is already available

From the skill directory:

```bash
bash scripts/copilot-status.sh
```

Expected outcomes:

- if the model exists and is already default, you are done
- if the model exists but is not default, switch it
- if the model does not exist or probe fails, continue to login

## 3. Run the official GitHub Copilot login flow

Use the built-in OpenClaw command:

```bash
openclaw models auth login-github-copilot
```

Notes:

- run this in a real terminal
- expect a device-code or browser confirmation step
- do not try to automate around it unless you control the entire TTY workflow

## 4. Re-check with a live probe

```bash
bash scripts/copilot-status.sh --probe
```

This is the easiest way to catch expired auth or a half-finished login.

## 5. Make Copilot the default model

Simplest path:

```bash
bash scripts/copilot-activate.sh
```

Manual equivalent:

```bash
openclaw models set copilot-auto
```

If `copilot-auto` does not exist:

```bash
openclaw models set copilot-bridge/github-copilot
```

## 6. Optional: create the short alias

If the model exists but the alias is missing, you can add it:

```bash
openclaw models aliases add copilot-auto copilot-bridge/github-copilot
```

This is optional but makes later instructions much nicer.

## 7. One-command guided flow

If you want one command that diagnoses, optionally logs in, optionally repairs the alias, and switches the default model:

```bash
bash scripts/copilot-quickstart.sh --probe --login --ensure-alias --activate
```

Recommended usage:

- use `--probe` for a stronger auth check
- add `--login` only in an interactive TTY
- add `--ensure-alias` only if you want the short alias normalized
- add `--activate` when the user explicitly wants Copilot selected

## 8. Verify the result

```bash
openclaw models status --plain
```

If behavior in an existing conversation still seems stale, start a fresh session. Model defaults are configuration state; sessions may still carry prior context.

## 9. Minimal command set to remember

```bash
openclaw models list --plain
openclaw models aliases list
openclaw models status --plain
openclaw models auth login-github-copilot
openclaw models set copilot-auto
```

## 10. Suggested wording for end users

Use short, direct language:

```text
先跑 `bash scripts/copilot-status.sh --probe` 看 Copilot 模型和鉴权状态。
如果缺登录，就执行 `openclaw models auth login-github-copilot`。
确认正常后，跑 `bash scripts/copilot-activate.sh` 把默认模型切过去。
```
