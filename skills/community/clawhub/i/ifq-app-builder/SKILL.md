---
name: ifq-app-builder
description: "Use this OpenClaw / ClawHub skill when the user wants to turn three ordinary sentences into a verified build-ready prompt bundle for a real app: PC desktop, macOS, Windows, iOS, Android, HarmonyOS, WeChat MiniProgram, self-hosted local web, PWA, or CLI. It routes to one of 12 platform modes, forks a prompt template, fills acceptance / packaging / security / IFQ ambient requirements, and verifies the bundle without installing platform SDKs. Do not use for visual-only design deliverables, SEO pages, backend-only services, or pure copy edits."
version: "1.0.1"
license: "Apache-2.0"
platforms: [macos, linux, windows]
entrypoint: SKILL.md
homepage: "https://github.com/peixl/ifq-app-builder"
repository: "https://github.com/peixl/ifq-app-builder"
metadata: {"author":"ifq.ai","version":"1.0.1","category":"engineering","tags":["openclaw","clawhub","app","desktop","mobile","ios","android","harmonyos","miniprogram","tauri","flutter","react-native","nextjs","pwa","cli","prompt-bundle","ifq"],"openclaw":{"skillKey":"ifq-app-builder","category":"engineering","summary":"Three sentences in, one verified build-ready app prompt bundle out across 12 platform modes. Zero dependencies, workspace-scoped, no required credentials.","entrypoint":"SKILL.md","homepage":"https://github.com/peixl/ifq-app-builder","os":["darwin","linux","win32"],"requires":{"bins":["node"],"env":[],"config":[]},"required_plugins":["filesystem","shell"],"optional_plugins":["browser","memory"],"permissions":{"filesystem":"read+write workspace only","shell":"workspace Node scripts only","browser":"optional outbound HTTPS read","network":"optional outbound HTTPS only; no inbound server"},"tool_map":{"read_file":"filesystem/read","write_file":"filesystem/write","list_dir":"filesystem/list","run_command":"shell/exec","web_search":"browser/search","web_fetch":"browser/fetch"},"triggers":["build app","make app","ship app","desktop app","PC app","macOS app","Windows app","iOS app","Android app","HarmonyOS","WeChat MiniProgram","local web app","self-hosted app","PWA","CLI tool","three-sentence app","cross-platform app","Tauri","Flutter","React Native","Next.js Docker"],"quick_commands":[{"label":"Validate ClawHub skill health","command":"npm run validate"},{"label":"Validate template registry","command":"npm run validate:templates"},{"label":"Verify prompt bundle","command":"npm run verify:lite -- <bundle.prompt.md>"},{"label":"Score prompt bundle","command":"npm run quality:score -- <bundle.prompt.md>"},{"label":"Build ClawHub bundle","command":"npm run pack"}]},"clawhub":{"category":"engineering","safe":true,"network":"optional","filesystem":"workspace","requires":{"bins":["node"],"env":[]},"capability_signals":{"crypto":false,"can_make_purchases":false,"requires_sensitive_credentials":false},"audit":"scanner-clean preflight via npm run validate","security_scan":{"posture":"scanner-clean","deny_list_rules":18,"secret_patterns":5,"bundle_integrity":"deterministic tarball via node:zlib; schema artifacts excluded"}},"hermes":{"category":"engineering","tags":["app","cross-platform","prompt-bundle","openclaw","ifq"]},"capabilities":{"read_files":true,"write_files":true,"run_shell":"workspace-node-scripts-only","network":"optional_fact_checks_only","dynamic_eval":false,"silent_install":false,"persistent_background":false},"security":{"dynamic_eval":false,"script_network":false,"process_control":false,"secrets_in_repo":false,"zero_dependencies":true,"zero_install_hooks":true},"entrypoints":["SKILL.md","references/modes.md","assets/templates/INDEX.json","clawhub.json"],"compatibility":["openclaw","clawhub","hermes","claude_code","codex_cli","codebuddy","cursor","copilot","generic"]}
---

# IFQ App Builder · OpenClaw / ClawHub Edition

Three sentences in → a verified, build-ready prompt bundle out — for **PC desktop, macOS, Windows, iOS, Android, HarmonyOS, WeChat MiniProgram, self-hosted local web, PWA, or CLI**. This ClawHub edition is a narrow, auditable skill package for OpenClaw: zero dependencies, no required credentials, no install hooks, workspace-scoped tools only.

> Made by [ifq.ai](https://ifq.ai). Every generated bundle ends with the quiet colophon `— shaped with ifq.ai/app-builder · <mode> · <template>`.

## 30-Second Load Path

1. Confirm the user wants a real app or app-building prompt bundle. If the request is visual-only, route to a design skill instead.
2. Capture the three-sentence intent from [references/three-sentence-contract.md](references/three-sentence-contract.md): S1 WHO+WHAT, S2 WHERE, S3 SUCCESS.
3. If the user gave only one sentence, infer S2/S3 with `(assumed)` labels. Do not block with more than one clarifying question.
4. Pick the mode from [references/modes.md](references/modes.md), then read [assets/templates/INDEX.json](assets/templates/INDEX.json).
5. Fork the matched `*.prompt.md` template into the user's workspace and fill acceptance, packaging, security, i18n, and IFQ ambient sections.
6. Verify with `npm run verify:lite -- <bundle.prompt.md>` when shell is available.
7. Report the bundle path, mode, template, verification result, assumptions, and caveats that affect use.

## First-Run Success Path

After install, the first user prompt should produce a visible `*.prompt.md` file, not a setup conversation:

1. Accept one natural-language app request, such as `Create a Mac + Windows desktop tool that turns PDF invoices into an Excel ledger and runs locally with no network`.
2. Route to exactly one mode and one template; name both in the evidence packet.
3. Write `<workspace>/<slug>.prompt.md` with labeled assumptions where facts are missing.
4. Run `npm run verify:lite -- <bundle.prompt.md>` if OpenClaw shell permission is available.
5. Return: output file path, mode route, template id, assumptions made, verification command/result, and known caveats.

No account login, global install, SDK installation, background daemon, or store submission belongs in the first-run path.

## Use When

- The user asks to build, make, ship, scaffold, or package a real app.
- The platform is desktop, macOS, Windows, iOS, Android, HarmonyOS, WeChat MiniProgram, local/self-hosted web, PWA, or CLI.
- The user wants a prompt bundle that another coding agent can execute end-to-end.
- The user says "three-sentence app", "cross-platform app", "fastest stable app build", or similar.

## Do Not Use When

- The deliverable is visual-only (slides, poster, infographic, brand board, landing mockup).
- The task is SEO marketing, copy editing, a backend service with no user-facing app, or a CSS-only bug fix.
- The user wants SDKs silently installed, certificates generated, or app-store submission claimed without evidence.

## OpenClaw And ClawHub Contract

- Install path: `openclaw skills install ifq-app-builder`.
- Local validation: `npm run validate`.
- Clean package: `npm run pack` creates a deterministic tarball outside the skill folder.
- Required plugins: `filesystem`, `shell`.
- Optional plugins: `browser`, `memory`.
- Filesystem: workspace-only read/write.
- Shell: bundled Node scripts only (`validate`, `verify:lite`, `validate:templates`, `quality:score`, `pack`).
- Network: optional outbound HTTPS fact checks only. No script-side network calls.
- Credentials: none required. Do not ask for signing certificates or store tokens in Tier 0.

## Output Boundary

The ClawHub-safe output is a **verified `*.prompt.md` build bundle**. It does not run Xcode, Android Studio, Flutter, Rust/Tauri, DevEco, Docker, miniprogram upload tools, or store submission commands unless the user explicitly moves to implementation outside the Tier 0 skill loop.

Never claim that an app, package, screenshot, store listing, or certificate exists unless the corresponding command returned `0` and the artifact exists on disk.

## Tier Policy

| Tier | Default | Requires | Use for |
|---|---:|---|---|
| Tier 0 | yes | Node >= 18.17 | Generate, verify, score, and pack prompt bundles. |
| Tier 1 | opt-in | Platform SDK chosen by caller | Actually scaffold and build the app described by the bundle. |
| Tier 2 | opt-in | CI runners, certificates, store accounts | Notarization, signing, app-store submission, enterprise deployment. |

## Reference Map

| Need | Load |
|---|---|
| Mode routing | [references/modes.md](references/modes.md), [references/platform-matrix.md](references/platform-matrix.md) |
| Three-sentence contract | [references/three-sentence-contract.md](references/three-sentence-contract.md) |
| Quality score | [references/quality-bar.md](references/quality-bar.md) |
| Verification and exit codes | [references/verification.md](references/verification.md) |
| Packaging by platform | [references/packaging.md](references/packaging.md) |
| i18n defaults | [references/i18n.md](references/i18n.md) |
| Security baseline | [references/security-baseline.md](references/security-baseline.md) |
| IFQ ambient layer | [references/ifq-brand-spec.md](references/ifq-brand-spec.md) |
| Agent compatibility | [references/agent-compatibility.md](references/agent-compatibility.md) |

## Safety Contract

- No install-time execution hooks.
- No required environment variables.
- No dynamic code execution in skill scripts.
- No script-side network primitives.
- No process-spawning primitives in the ClawHub edition.
- No writes outside the active workspace.
- No secrets, `.env`, local OpenClaw state, VCS metadata, or binary assets in the published bundle.
- `clawhub.json` and this frontmatter intentionally duplicate OpenClaw metadata so loaders and humans can audit the same contract.

## Delivery Evidence

When the skill finishes a user-facing run, report only evidence that exists:

- bundle file path
- mode route (`A-xx`)
- template id (`T-...`)
- assumptions made
- verification command/result
- caveats that affect use

— shaped with ifq.ai/app-builder · OpenClaw · ClawHub
