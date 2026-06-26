---
name: ocmemog-installer
description: Install and configure ocmemog, the OpenClaw durable memory plugin and sidecar. Use when a user asks to install ocmemog, set up durable memory, improve OpenClaw memory, enable transcript-backed continuity, configure the ocmemog sidecar, reinstall/update ocmemog, or troubleshoot its install. Prefer the public package install path first; fall back to the GitHub repo installer path when package install is unavailable or source checkout is explicitly desired.
---

# ocmemog Installer

Install `ocmemog` from the canonical public package/repo and configure OpenClaw to use it as the memory plugin.

## Public install paths

- npm package: `@openclaw/memory-ocmemog`
- GitHub repo: `https://github.com/simbimbo/ocmemog.git`
- GitHub release: `https://github.com/simbimbo/ocmemog/releases/tag/v0.1.2`
- Plugin id: `memory-ocmemog`
- Default sidecar endpoint: `http://127.0.0.1:17890`
- Default timeout: `30000`
- Bundled repo installer: `scripts/install-ocmemog.sh`

## Preferred workflow

1. If OpenClaw package install is available, prefer:
   - `openclaw plugins install @openclaw/memory-ocmemog`
   - `openclaw plugins enable memory-ocmemog`
2. If package install is unavailable, or the user wants a source checkout, use the repo installer flow:
   - clone/update `https://github.com/simbimbo/ocmemog.git`
   - run `scripts/install-ocmemog.sh`
   - this path creates `.venv`, installs Python requirements, attempts plugin install/enable, loads LaunchAgents, and pulls local Ollama models when Ollama is available
   - on macOS/Homebrew systems, `OCMEMOG_INSTALL_PREREQS=true` can also auto-install missing `ollama` and `ffmpeg`
3. Patch OpenClaw config so the `memory` slot points at `memory-ocmemog` and the plugin entry uses `http://127.0.0.1:17890` with `timeoutMs: 30000`.
4. Validate `/healthz` and a memory search/get smoke test.

## Agent behavior

- Prefer the package install path when available because it is the cleanest public distribution path.
- Fall back to the repo installer path when package install is unavailable, when the user needs a source checkout, or when debugging/pinning commits.
- If config patch tooling is available, patch config automatically instead of asking the user to hand-edit files.
- After install, verify the sidecar and plugin state before claiming success.
- If the environment blocks automatic config changes, provide the exact config snippet and the shortest possible manual next step.

## Config patching

Target config shape:

```yaml
plugins:
  load:
    paths:
      - /path/to/ocmemog
  slots:
    memory: memory-ocmemog
  entries:
    memory-ocmemog:
      enabled: true
      config:
        endpoint: http://127.0.0.1:17890
        timeoutMs: 30000
```

Rules:
- If installed from package tooling, use the normal plugin install location chosen by OpenClaw.
- If installed from the repo installer flow, use the actual checkout path chosen by the script.
- Preserve existing unrelated plugin configuration.
- If config patch tooling is unavailable, provide the exact patch/snippet the user should apply.

## Validation checklist

- Sidecar responds on `/healthz`
- `openclaw plugins` shows `memory-ocmemog` installed/enabled when CLI access exists
- Memory search/get calls return data instead of connection errors
- If packaging/publish questions arise, remember this skill is a ClawHub wrapper for the public plugin package/repo, not the plugin package itself

## Troubleshooting

- If package install fails, fall back to the GitHub repo installer path.
- If ClawHub users expect a direct plugin package, explain that this skill installs/configures the real plugin package/repo.
- If macOS LaunchAgents fail, rerun the installer and inspect `launchctl print gui/$UID/com.openclaw.ocmemog.sidecar`.
- If the sidecar health check fails, inspect repo logs / terminal output before changing config.
- Keep the sidecar bound to `127.0.0.1` unless explicit auth/network hardening is added.

## Notes

- Prefer public package install over source checkout when both are viable.
- Use this skill as the ClawHub-distributed installer/config guide for the public ocmemog package/repo.
