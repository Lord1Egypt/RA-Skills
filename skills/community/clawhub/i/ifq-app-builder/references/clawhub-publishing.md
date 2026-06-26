# Publishing IFQ App Builder to ClawHub

This folder is the ClawHub-safe OpenClaw package. It should pass local checks before upload and should be uploaded as the generated tarball, not as a raw Git checkout.

## TL;DR

```bash
npm run validate
npm run pack
```

The pack command writes `../ifq-app-builder-clawhub-YYYY-MM-DD.tar.gz` by default. Archive mtimes default to `0` for reproducible output; set `SOURCE_DATE_EPOCH=<unix seconds>` only when a release process needs a specific timestamp.

## Why a dedicated bundle

ClawHub validators inspect the published artifact, not your intent. A raw repository can contain `.git/`, editor state, logs, local OpenClaw config, package locks, generated archives, or binary files that are harmless locally but noisy or disallowed in a marketplace scanner. This subpackage keeps the review surface narrow:

- `SKILL.md` with single-line JSON metadata
- `clawhub.json` with explicit OpenClaw triggers, permissions, plugins, tool map, first-run prompts, and evidence packet
- 12 prompt templates plus `INDEX.json`
- references needed by the skill loop
- zero-dependency validation and packing scripts
- demo prompt bundles and eval scenarios
- no `*.schema.json` artifacts in the published bundle; registry and eval checks run from local policy code

## Safety posture

- zero dependencies
- zero install hooks
- no required environment variables
- no script-side network calls
- no process spawning in skill scripts
- no dynamic execution
- no binary assets in the ClawHub bundle
- no JSON schema artifacts in the ClawHub bundle
- workspace-only filesystem permission
- shell usage limited to bundled Node scripts

## Pre-upload checklist

1. `npm run validate` exits `0`.
2. `npm run validate:templates` exits `0`.
3. `npm run evals:validate` exits `0`.
4. `npm run pack` exits `0` and prints archive path + entry count.
5. `tar -tzf ../ifq-app-builder-clawhub-*.tar.gz | head` shows `ifq-app-builder/` entries, not `.git/`.
6. Listing copy includes: install command, first-run prompt, evidence packet, no-credentials posture, and Tier 0/Tier 1 boundary.

## OpenClaw install test

After upload or local pack:

```bash
openclaw skills install ../ifq-app-builder-clawhub-YYYY-MM-DD.tar.gz
openclaw skills info ifq-app-builder
openclaw skills check ifq-app-builder
```

Expected readiness:

- required plugins: `filesystem`, `shell`
- optional plugins: `browser`, `memory`
- required bins: `node`
- required env: empty
- required config: empty
- filesystem: workspace
- shell: workspace Node scripts only

## First-run review script

Ask OpenClaw:

```text
Use ifq-app-builder to create a Mac + Windows desktop tool that turns PDF invoices into an Excel ledger and runs locally with no network.
```

The answer should produce a local `*.prompt.md` bundle, route `A-01`, template `T-pc-tauri`, labeled assumptions, `verify:lite` evidence, and caveats. It should not ask to install Rust/Tauri during Tier 0.

## Common rejection causes this package avoids

| Rejection cause | Prevented by |
|---|---|
| VCS metadata in upload | `clawhub.ignore.txt` + pack verifier |
| install-time execution | package safety check rejects lifecycle hooks |
| schema-file false positives | `*.schema.json` files are excluded by ignore and pack verifier |
| hidden credentials requirement | manifest and frontmatter require empty env arrays |
| broad filesystem access | workspace-only permission in manifest + SKILL |
| script network primitives | script safety rules |
| process spawning | script safety rules and no `node:child_process` imports |
| unclear first-run value | README + clawhub first_run block + demos |

— shaped with ifq.ai/app-builder · OpenClaw · ClawHub
