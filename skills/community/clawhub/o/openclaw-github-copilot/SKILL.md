---
name: openclaw-github-copilot
description: Use GitHub Copilot as your OpenClaw coding agent via the built-in copilot-bridge. Use when setting up Copilot for the first time, switching the default model, diagnosing auth or alias issues, or giving someone the shortest working path to `copilot-bridge/github-copilot`.
homepage: https://docs.openclaw.ai/cli/models
metadata: {"openclaw":{"emoji":"🐙","homepage":"https://docs.openclaw.ai/cli/models","requires":{"bins":["openclaw"]},"install":[{"id":"node","kind":"node","package":"openclaw","bins":["openclaw"],"label":"Install OpenClaw CLI"}]}}
---

# OpenClaw GitHub Copilot

Use this skill to make GitHub Copilot the simplest possible OpenClaw default.

This skill is for four jobs:

1. first-time GitHub Copilot setup in OpenClaw
2. switching the default model to Copilot
3. fixing common `copilot-bridge/github-copilot` auth or alias issues
4. giving the user one short command path instead of a pile of manual steps

## What this skill assumes

- `openclaw` is installed
- the user has GitHub Copilot access on the GitHub account they will log in with
- the agent prefers OpenClaw CLI commands over hand-editing config files

## Fast path

Start with the single diagnostic command:

```bash
bash {baseDir}/scripts/copilot-quickstart.sh --probe
```

If the user wants Copilot to become the default model and auth is already valid:

```bash
bash {baseDir}/scripts/copilot-quickstart.sh --probe --activate
```

If auth is missing or expired and you are in an interactive TTY:

```bash
bash {baseDir}/scripts/copilot-quickstart.sh --probe --login --activate
```

That wrapper is the preferred entrypoint because it:

- checks whether the Copilot model exists
- checks whether the short alias exists
- optionally creates the alias when asked
- optionally runs the official GitHub Copilot device login
- optionally switches the default model to Copilot

## Canonical identifiers

- Full model id: `copilot-bridge/github-copilot`
- Preferred alias: `copilot-auto`

Always verify what OpenClaw already knows before claiming anything:

```bash
openclaw models list --plain
openclaw models aliases list
openclaw models status --plain
```

If the alias exists, prefer it in human-facing instructions because it is shorter:

```bash
openclaw models set copilot-auto
```

If the alias is missing, use the full model id:

```bash
openclaw models set copilot-bridge/github-copilot
```

## Recommended workflow

### 1. Diagnose first

Run:

```bash
bash {baseDir}/scripts/copilot-status.sh
```

Use the stronger live probe when auth freshness matters:

```bash
bash {baseDir}/scripts/copilot-status.sh --probe
```

The script reports:

- whether the Copilot model is registered
- whether `copilot-auto` points at that model
- what the current default model is
- whether GitHub Copilot is already the active default

### 2. Authenticate only with the official flow

If the model exists but auth is missing or stale, use:

```bash
openclaw models auth login-github-copilot
```

Important:

- this requires an interactive TTY
- it may require a browser/device-code step
- do not pretend it can be completed silently in the background

### 3. Switch the default model

If the user explicitly wants Copilot as the default model:

```bash
bash {baseDir}/scripts/copilot-activate.sh
```

Or use the wrapper:

```bash
bash {baseDir}/scripts/copilot-quickstart.sh --activate
```

### 4. Confirm result

Verify with:

```bash
openclaw models status --plain
```

The configured default should resolve to `copilot-bridge/github-copilot`.

If the current session still behaves like the old model, start a fresh OpenClaw session. Skill and default-model changes are most reliable in a new session.

## Good trigger phrases

Use this skill for requests like:

- "让 OpenClaw 用 GitHub Copilot"
- "把默认 agent 切到 Copilot"
- "检查 Copilot bridge 配好了没有"
- "GitHub Copilot 在 OpenClaw 里怎么登录"
- "给我一个最简单的 Copilot 配置流程"
- "copilot-auto 不生效"

## Practical response pattern

When helping a user, keep the answer operational:

1. say whether the model exists
2. say whether it is already the default
3. give the next exact command
4. only mention manual alias cleanup or config editing if the CLI flow is insufficient

Example:

```text
GitHub Copilot 这个模型已经在 OpenClaw 里了，但当前默认模型不是它。
直接执行 `bash {baseDir}/scripts/copilot-quickstart.sh --probe --activate`。
如果后面提示鉴权失效，再跑 `openclaw models auth login-github-copilot`。
```

## References

- `references/setup-guide.md` - full first-time setup walkthrough
- `references/troubleshooting.md` - missing model, alias, auth, and session behavior
- `references/publish-checklist.md` - release checklist for publishing to ClawHub
