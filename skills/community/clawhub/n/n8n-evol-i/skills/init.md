---
name: init
description: Scaffold a fresh n8n-evol-I workspace at ${PWD}/n8n-evol-I-workspace/.
user-invocable: false
---

# init

## When

First-time use of n8n-evol-I in a project, or to reset from a clean slate.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/init.py
```

Optional flags:

- `--workspace <path>`: override default `${PWD}/n8n-evol-I-workspace`
- `--force`: clobber existing workspace (DESTRUCTIVE — confirm with the user)

## Side effects

Creates the workspace tree:

- `n8n-config/` — env YAML + `.env.<env>` files (initially with `.env.example`)
- `n8n-workflows-template/` — `*.template.json` (canonical, version-controlled)
- `n8n-build/` — hydrated outputs (gitignored)
- `n8n-prompts/{prompts,datasets,evals}/`
- `n8n-functions/{js,py}/`, `n8n-functions-tests/`
- `n8n-assets/{email-templates,images,misc}/`
- `cloud-functions/{,functions/}`, `cloud-functions-tests/`
- `AGENTS.md` — workspace orientation (folder tree, skill router pointer, maintain-incentive instructions)
- `N8N-WORKSPACE-MEMORY.md` — rolling journal (agent reads and appends each session)
- `CLAUDE.md` at project root — alias pointing to `AGENTS.md` (written only when workspace is at default location)
- `.github/copilot-instructions.md` at project root — same alias (same condition)
- `.gitignore` (`n8n-build/`, `.env.*`)

## Idempotence

Refuses to clobber an existing workspace. Pass `--force` to recreate (DESTRUCTIVE).

## Next step

Run `bootstrap-env.md` to configure your first environment.

## Migrating from N8N-HARNESS-MEMORY.md

Existing workspaces created before this change have `N8N-HARNESS-MEMORY.md`. To
migrate manually:
1. Copy the Notes section contents to the new `N8N-WORKSPACE-MEMORY.md`.
2. Rename `N8N-HARNESS-MEMORY.md` to `AGENTS.md` and replace its content with the
   current template (visible at `helpers/init.py`'s `_AGENTS_MD` constant).
3. Add `CLAUDE.md` at your project root with content `@n8n-evol-I-workspace/AGENTS.md`
   plus the fallback note from `_ALIAS_TEMPLATE`.
