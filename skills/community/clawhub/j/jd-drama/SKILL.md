---
name: jd-drama
description: Install and use the public beta jd-drama CLI to operate JianDan short-drama projects, scripts, uploaded imports, assets, storyboards, videos, brands, material libraries, and task diagnostics from Codex, Code, OpenClaw, or other agents.
metadata:
  openclaw:
    requires:
      bins:
        - jd-drama
---

# JianDan Short-Drama CLI

## Install And Start

1. Check `command -v jd-drama` and `jd-drama --version`.
2. If missing or older than `1.0.0-beta.6`, install or update with `npm install -g @flyengine/jd-drama-cli@beta`.
3. Run `jd-drama --json doctor`. The public beta defaults to `https://jiandan.flyengine.cn/api`, the JianDan production environment.
4. Run `jd-drama auth login` only when `auth.browserAuthorization.needsLogin` is true, and let the user approve it in the JianDan browser page. On older CLIs without this field, check `auth status`: log in when `authMode` is `none` or the server explicitly rejects the refresh authorization. `authorized: false` alone can mean the agent cannot read the macOS Keychain, not that a new login is needed.
5. Run `jd-drama --json release-check` before live work and proceed only when `data.ok` is true.

Never ask for a JianDan password or Token. The CLI supports browser authorization only. Use `--json` for agent calls. Do not override the production API unless the user explicitly requests a local or test environment.

Codex, WorkBuddy and other local agents normally share `~/.jd-drama/config.json` and one browser authorization. Reuse it; do not log in again just because a different tool is starting a task. `auth logout` revokes this shared authorization for all tools, so never use logout/login as an automatic repair. For `credential_unavailable` or `refresh_unavailable`, inspect the diagnostic, obtain the agent's normal filesystem/Keychain permissions or resolve the network error, then retry the original command. Do not copy tokens or disable sandbox protections. After a server-confirmed revocation, coordinate a single reauthorization, then resume both tools. Missing brand/material scopes require one new browser approval, not a preceding logout.

```bash
npm install -g @flyengine/jd-drama-cli@beta
jd-drama --version
jd-drama --json skill doctor --target codex
jd-drama auth login
jd-drama --json release-check
```

## Discover And Read

```bash
jd-drama --json projects list --limit 10
jd-drama --json projects get <projectId>
jd-drama --json brands list --keyword "品牌名"
jd-drama --json materials folders
jd-drama --json materials list --limit 20
jd-drama --json assets summary <projectId>
jd-drama --json storyboard episodes <projectId>
jd-drama --json storyboard generation-config-options <projectId>
jd-drama --json tasks recovery-plan <projectId>
```

Use named commands first. `raw get` is only for missing read wrappers under `/user/ai-drama`, `/user/brands`, or `/user/material`; full URLs are forbidden.

## Create

Preview every write with `--dry-run`. Execute only after the user approves the exact action, using the same command with `--confirm`.

```bash
jd-drama --json ai-script create --idea "品牌短剧创意" --episode-count 10 --name "项目名" --generate --dry-run
jd-drama --json imports create-from-file ./script.md --name "项目名" --parse-assets --dry-run
```

`--parse-assets` follows the Web two-stage flow: wait for the outline, run free parent asset extraction, wait for success, then start charged deep asset parsing. For staged execution, use `assets extract`, `assets extraction-progress`, `assets parse`, and `assets parse-progress` in that order. This system parsing flow is required for uploaded, AI-generated, and secondary-created projects alike.

To associate a brand, resolve its ID and pass `--brand-id` plus `--brand-placement-depth auto|light|medium|heavy` during initial project creation. Do not change an existing project's brand.

## Assets, Brands, And Materials

Roles, scenes, props, role appearances, and scene views must come from system asset extraction/parsing. Do not invent asset records, manually create them, or use direct API calls or episode materials to substitute for required parsed assets. The CLI and MCP do not expose manual creation. The matching backend update also rejects these requests for older CLI clients once deployed; do not rely on that server restriction during a staged rollout.

After the script and outline are ready, preview and confirm extraction, wait for successful extraction, then preview and confirm deep parsing. Deep parsing may consume credits and requires the usual user approval. Wait for parsing to succeed before editing parsed assets or generating their images. Do not treat an accepted task or existing parent records as proof that parsing is complete.

```bash
jd-drama --json assets extract <projectId> --dry-run
jd-drama --json assets extraction-progress <projectId>
jd-drama --json assets parse <projectId> --dry-run
jd-drama --json assets parse-progress <projectId>
jd-drama --json assets summary <projectId>
```

If extraction or parsing fails or misses an entity, inspect `tasks errors` and the saved script. Report the issue, correct the script when permitted, or retry the supported system stage with approval. Never fall back to manual asset creation. Edits to existing assets and their `regenerate-*` commands remain supported; do not fabricate asset IDs.

Brand profile and material-library CRUD are supported with the same preview/approval boundary. Brand create/update requires a JSON product array containing at least `name` and `thumbnailUrl` per product.

```bash
jd-drama --json brands create --name "品牌名" --products-file ./products.json --dry-run
jd-drama --json materials create-folder --name "产品资料" --dry-run
jd-drama --json materials upload ./product.pdf --dry-run
jd-drama --json materials create-text --title "产品卖点" --content-file ./selling-points.md --dry-run
```

## Edit Script Episodes

This works for generated scripts, parsed uploads, and secondary-created scripts. Read the current official episode first. Preview a complete replacement, then execute only after explicit approval.

```bash
jd-drama --json script episode <projectId> --episode-no 1
jd-drama --json script update-episode <projectId> --episode-no 1 --title "第1集：新的开始" --content-file ./episode-1.md --dry-run
jd-drama --json script verify-episode <projectId> --episode-no 1 --title "第1集：新的开始" --content-file ./episode-1.md --dry-run
jd-drama --json script versions <projectId> --episode-no 1
jd-drama --json script restore-version <projectId> --episode-no 1 --version-id <versionId> --dry-run
```

`update-episode` replaces the full official title and content and creates a version snapshot. `verify-episode` stages the same full edit and runs the Agent's `manual_verify` flow without directly saving it. These commands are available while the project remains in the script-outline stage. Prefer `--content-file` for long scripts. Restoring a version also creates a new revision. None of these actions automatically regenerates outline, assets, storyboards, or videos; inspect downstream content before continuing.

## Storyboard And Video

```bash
jd-drama --json storyboard generation-config-options <projectId>
jd-drama --json storyboard generate <projectId> --episode-ids <episodeIdA>,<episodeIdB> --dry-run
jd-drama --json storyboard generate <projectId> --episode-ids <episodeIdA>,<episodeIdB> --use-seedance-25 --max-segment-duration-seconds 30 --dry-run
jd-drama --json storyboard regenerate-episode <projectId> --episode-id <episodeId> --use-seedance-25 --max-segment-duration-seconds 30 --dry-run
jd-drama --json storyboard unlock-video-model <projectId> --episode-id <episodeId> --dry-run
jd-drama --json storyboard optimize-segment <projectId> --episode-id <episodeId> --segment-id <segmentId> --dry-run
jd-drama --json storyboard update-segment <projectId> --episode-id <episodeId> --segment-id <segmentId> --duration-seconds 8 --text "完整分镜" --dry-run
jd-drama --json video generate <projectId> --episode-id <episodeId> --segment-ids <segmentId> --model-code <modelCode> --resolution 720p --dry-run
jd-drama --json video attach <projectId> --episode-id <episodeId> --segment-id <segmentId> --file ./segment.mp4 --dry-run
```

Storyboard generation defaults to Seedance 2.0 and always sends the required model switch. Before selecting Seedance 2.5, read `generation-config-options` and use one of its returned durations with both `--use-seedance-25` and `--max-segment-duration-seconds`.

`unlock-video-model` records that the user has confirmed switching one episode away from the Seedance 2.5 recommendation. It does not enable model access or spend generation quota.

Segment optimization returns a candidate but does not save it. Review the candidate, then preview and confirm `storyboard update-segment` separately.

## Boundaries

- Treat the current npm package as a public beta connected to production user data and real quotas.
- Do not expose credentials or config file contents.
- Do not bypass `--dry-run` and `--confirm` with direct API calls.
- Do not run task retry, generic asset generation, or raw non-GET requests as live writes.
- Diagnose failures with `tasks errors` or `tasks recovery-plan` before retrying work.
