# Troubleshooting

## Table of contents

1. Missing model
2. Missing alias
3. Auth or token issues
4. Session behavior
5. Minimal command set

## 1. Missing model

If `copilot-bridge/github-copilot` does not appear in:

```bash
openclaw models list --plain
```

do not guess at config internals first.

Prefer this order:

1. run `openclaw models list`
2. run `openclaw models status`
3. check whether the environment already supports GitHub Copilot auth
4. if needed, run `openclaw models auth login-github-copilot`

If the model still does not appear after a successful login, treat it as an environment or provider configuration problem rather than a skill problem.

## 2. Missing alias

The shortest alias is usually:

```bash
copilot-auto
```

If it is absent, use the full model id instead:

```bash
openclaw models set copilot-bridge/github-copilot
```

Only add or edit aliases if the user explicitly wants that cleanup step:

```bash
openclaw models aliases add copilot-auto copilot-bridge/github-copilot
```

## 3. Auth or token issues

Prefer the official device-login flow:

```bash
openclaw models auth login-github-copilot
```

Important constraints:

- It needs a TTY.
- It may prompt the user to complete a browser/device-code step.
- Do not promise silent background auth.

For a stronger post-login verification, use:

```bash
openclaw models status --probe
```

## 4. Session behavior

Changing the default model with:

```bash
openclaw models set copilot-auto
```

updates the configured default model. Existing sessions may still have prior context or session-level state, so verify the active session if the user expects an immediate behavioral change.

When in doubt:

1. confirm the configured default with `openclaw models status --plain`
2. confirm the active session or create a fresh session if required by the user's workflow

## 5. Minimal command set

Use these commands and avoid inventing manual config edits unless necessary:

```bash
openclaw models list
openclaw models aliases list
openclaw models status --plain
openclaw models set copilot-auto
openclaw models auth login-github-copilot
```
