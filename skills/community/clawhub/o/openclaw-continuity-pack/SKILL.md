---
name: openclaw-continuity-pack
description: "用于给 OpenClaw 安装可复用的 continuity 模板与统一安装入口，支持 workspace-only、continuity-only 和 full continuity 三条路线；可选对匹配源码树应用 runtime patch，实现前台同一对话、后台自动续接、静默 continuity 准备的工作流。"
license: MIT
---

# OpenClaw全自动新对话续接

## ClawHub quick install

If you found this on ClawHub and want to install it into OpenClaw immediately, use either of these:

```bash
openclaw skills install openclaw-continuity-pack
```

or:

```bash
clawhub install openclaw-continuity-pack
```

Then start a **new OpenClaw session** so the newly installed skill is eligible.

## 30-second route chooser

After install, choose one path:

1. **Workspace-only install**
   - Reuse the prompts, templates, and continuity workflow without changing OpenClaw source.
   - Fastest command:
     - `python3 {baseDir}/scripts/install_continuity_pack.py --route workspace`
2. **Continuity-only install**
   - Install only the `memory / plans / status / handoff` workflow files.
   - Fastest command:
     - `python3 {baseDir}/scripts/install_continuity_pack.py --route continuity`
3. **Full continuity install**
   - Scaffold the workspace layer, then apply the runtime patch to a **matching OpenClaw source tree**, rebuild, and redeploy.
   - Fastest command:
     - `python3 {baseDir}/scripts/install_continuity_pack.py --route full --source-root <OPENCLAW_SOURCE_ROOT> --apply-runtime-patch --rebuild`

The installer auto-detects the workspace from the current OpenClaw workspace when possible, and otherwise falls back to `~/.openclaw/workspace`.

Once installed, treat the skill root as `{baseDir}` when following the bundled commands and file references.

Use this skill when the goal is to give another OpenClaw project the **maximum reusable subset** of a verified continuity stack without shipping a live machine snapshot.

The current runtime patch targets **silent continuity preparation**: ordinary chat pages no longer render continuity/context hint messages, while same-thread rollover and hidden handoff remain in place.

This skill is for three situations:

1. **Install workspace continuity only**
   - scaffold reproducible prompts, continuity templates, and workspace conventions
2. **Install full continuity**
   - scaffold the workspace layer, apply the runtime patch to a matching source tree, rebuild, and verify
3. **Package / audit / publish**
   - review this skill for distribution without leaking secrets, logs, machine paths, or live state

## Fast path

### Workspace-only install
- Read `references/install.md`
- Preferred one-shot command:
  - `scripts/install_continuity_pack.py --route workspace`
- Lower-level equivalent:
  - `scripts/bootstrap_workspace.py --workspace auto`
- If the user wants only continuity files and not the broader operating layer, use:
  - `scripts/install_continuity_pack.py --route continuity`

### Full continuity install
- Preferred one-shot command:
  - `scripts/install_continuity_pack.py --route full --source-root <OPENCLAW_SOURCE_ROOT> --apply-runtime-patch --rebuild`
- Lower-level equivalent:
  - `scripts/bootstrap_workspace.py --workspace auto`
  - `scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT> --apply --rebuild`
- Then follow:
  - `references/deploy-notes.md`
  - `references/verify.md`
  - `references/rollback.md`

## Bundled resources

### scripts/
- `scripts/install_continuity_pack.py`
- `scripts/bootstrap_workspace.py`
- `scripts/apply_runtime_patch.py`
- `scripts/continuity_doctor.py`

### assets/
- `assets/workspace/` for the reusable operating layer and continuity templates
- `assets/config/openclaw.example.json` for a sanitized continuity-oriented config example
- `assets/patch/thread-continuity.patch` for the formal runtime/UI patch

### references/
- `references/overview.md`
- `references/install.md`
- `references/usage.md`
- `references/capability-layers.md`
- `references/files-to-replace.md`
- `references/deploy-notes.md`
- `references/verify.md`
- `references/rollback.md`
- `references/release-notes.md`
- `references/changelog.md`
- `references/distribution.md`
- `references/source-audit.md`
- `references/upgrade-maintenance.md`

## Working rules for this skill

When using this skill:

1. Reuse the bundled scripts instead of hand-copying files when the scripts already fit.
2. Keep the request split cleanly:
   - workspace continuity only
   - workspace + runtime patch
   - publishing/auditing the pack itself
3. Do not claim this reproduces a whole live assistant.
4. Do not ship real user memory, logs, secrets, API keys, channel config, hidden prompts, deploy backups, or temporary validation artifacts.

## Boundaries

- This is **not** an infinite-context solution.
- This is **not** a full `~/.openclaw` snapshot.
- The workspace layer reproduces public operating style and continuity discipline, but **not** the base model, permission policy, plugin inventory, or runtime state by itself.
- Full same-thread continuity still requires a matching OpenClaw source tree plus:
  - `pnpm build`
  - `pnpm ui:build`

## Read only what you need

1. `README.md`
2. `references/overview.md`
3. `references/install.md`
4. `references/usage.md`
5. `references/capability-layers.md`
6. `references/verify.md`
7. `references/rollback.md`
8. `references/upgrade-maintenance.md`
9. `references/distribution.md`
10. `references/source-audit.md`
