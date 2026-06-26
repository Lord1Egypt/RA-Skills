---
name: ifq-design-skills
description: "Use this skill when the user asks for an HTML-first visual design deliverable: interactive prototype, slide deck, motion demo, infographic, dashboard, landing page, whitepaper, changelog, business card, social cover, brand system, design critique, multi-variant exploration, or export planning for MP4, GIF, PPTX, PDF, or SVG. Do not use for production web apps, SEO sites, backend systems, pure copy edits, or isolated CSS bug fixes."
version: 2.4.3
license: "MIT"
platforms: [macos, linux, windows]
entrypoint: SKILL.md
homepage: "https://github.com/peixl/ifq-design-skills"
repository: "https://github.com/peixl/ifq-design-skills"
metadata: {"author":"ifq.ai","version":"2.4.3","category":"creative","tags":["design","html","prototype","slides","motion","infographic","dashboard","brand","pptx","pdf","svg","mp4","gif","ifq"],"openclaw":{"skillKey":"ifq-design-skills","category":"creative","summary":"HTML-first design engine for prototypes, decks, dashboards, motion, and brand systems. Fork a template, weave the IFQ ambient layer, verify the artifact.","entrypoint":"SKILL.md","homepage":"https://github.com/peixl/ifq-design-skills","os":["darwin","linux","win32"],"requires":{"bins":["node"],"env":[],"config":[]},"required_plugins":["filesystem","shell"],"optional_plugins":["browser","memory"],"permissions":{"filesystem":"read+write workspace only","shell":"workspace Node scripts only","browser":"optional outbound HTTPS read","network":"optional outbound HTTPS only; no inbound server"},"tool_map":{"read_file":"filesystem/read","write_file":"filesystem/write","list_dir":"filesystem/list","run_command":"shell/exec","web_search":"browser/search","web_fetch":"browser/fetch","screenshot":"browser/screenshot-or-host-tool"},"triggers":["prototype","interactive prototype","hi-fi mockup","slide deck","ppt","pptx","dashboard","landing page","whitepaper","infographic","business card","social cover","brand system","design critique","design variants","motion demo","mp4 export plan","gif export plan","原型","幻灯片","信息图","名片","小红书","品牌诊断","3 方向","portfolio","onboarding","brand-diagnosis","changelog"],"quick_commands":[{"label":"Validate skill health","command":"npm run validate"},{"label":"Validate eval suite","command":"npm run evals:validate"},{"label":"Static HTML check","command":"npm run verify:lite -- <file.html>"},{"label":"Build ClawHub bundle","command":"npm run pack"},{"label":"Anti-slop preflight","command":"npm run anti-slop -- <file.html>"}]},"clawhub":{"category":"creative","safe":true,"network":"optional","filesystem":"workspace","requires":{"bins":["node"],"env":[]},"capability_signals":{"crypto":false,"can_make_purchases":false,"requires_sensitive_credentials":false},"audit":"scanner-clean preflight via npm run validate","security_scan":{"posture":"scanner-clean","deny_list_rules":18,"secret_patterns":5,"bundle_integrity":"deterministic tarball via node:zlib"}},"hermes":{"category":"creative","tags":["design","html","prototype","slides","motion","infographic","dashboard","brand","ifq"]},"capabilities":{"read_files":true,"write_files":true,"run_shell":"workspace-node-scripts-only","network":"optional_fact_checks_and_assets_only","dynamic_eval":false,"silent_install":false,"persistent_background":false},"security":{"dynamic_eval":false,"script_network":false,"child_process":false,"secrets_in_repo":false,"zero_dependencies":true,"zero_install_hooks":true,"deny_list_rules":18,"secret_patterns":5},"entrypoints":["SKILL.md","references/modes.md","assets/templates/INDEX.json"],"compatibility":["openclaw","clawhub","hermes","claude_code","codex_cli","codebuddy","cursor","generic"]}
---

# IFQ Design Skills

One prompt in, a shippable HTML-first visual artifact out. This skill exists to make AI higher leverage: humans speak in goals, agents get a deterministic route, and the final artifact carries proof instead of decoration. This ClawHub-safe root file is intentionally short: it routes the task, states the security contract, and points the agent to deeper references only when needed.

## 30-Second Load Path

1. Confirm the request is a visual deliverable built from HTML. If not, exit this skill.
2. Pick the mode from [references/modes.md](references/modes.md), then read `modeRoutes` and `templates` in [assets/templates/INDEX.json](assets/templates/INDEX.json).
3. Fork the routed template into the user's workspace. Never start from a blank HTML file when a listed template can be adapted.
4. If information is missing but a reversible draft is possible, write labeled assumptions/placeholders and continue. Ask only for facts, assets, permissions, or format decisions that would materially change the output.
5. Inline [assets/ifq-brand/ifq-tokens.css](assets/ifq-brand/ifq-tokens.css) and weave at least 3 IFQ ambient marks from [references/ifq-brand-spec.md](references/ifq-brand-spec.md).
6. Verify with the host browser/screenshot tools when available. After editing this skill package, run `npm run validate`.

## Quick Decision Tree

Route in under 3 seconds. Match the user prompt to the nearest trigger:

```
User prompt contains:
├─ "prototype" / "app" / "onboarding" / "flow" → M-06 (T-onboarding)
├─ "dashboard" / "KPI" / "monitor" / "command center" → M-04 (T-dashboard)
├─ "slides" / "deck" / "keynote" / "PPT" → M-08 (T-slide-title)
├─ "portfolio" / "personal site" / "about me" → M-02 (T-portfolio)
├─ "changelog" / "release notes" / "版本记录" → M-07 (T-changelog)
├─ "whitepaper" / "report" / "PDF" / "年报" → M-03 (T-infographic-vertical)
├─ "compare" / "vs" / "benchmark" / "横评" → M-05 (T-compare-vs)
├─ "social" / "小红书" / "cover" / "社媒" → M-09 (T-social-multi)
├─ "card" / "名片" / "invite" / "VIP" → M-10 (T-business-card)
├─ "brand audit" / "diagnosis" / "体检" / "升级" → M-11 (T-diagnosis)
├─ "brand from scratch" / "全栈品牌" / "新品牌" → M-12 (T-hero-landing)
├─ "launch" / "animation" / "motion" / "film" → M-01 (T-hero-landing)
└─ vague / multiple matches / "做设计" → propose 3 directions first
```

When in doubt, pick the narrowest route. If the prompt spans two modes, choose the primary deliverable and mention the secondary in caveats.

## Human + Agent Contract

| Audience | Promise |
|---|---|
| Human user | Say the goal in ordinary language; receive a concrete HTML-first artifact, the assumptions that shaped it, and the verification evidence. |
| AI agent | Follow a narrow route: classify mode, fork template, fill with real context, run anti-slop checks, verify, then report caveats without self-congratulation. |
| Maintainer | Keep the ClawHub bundle zero-install, auditable, and small; keep heavy export automation opt-in in the full GitHub repo. |

## First-Run Success Path

After install, make the first interaction produce a visible artifact in one turn:

1. Accept a natural-language prompt such as "Make a command center dashboard for our internal AI operations."
2. Route it to one mode and one template; name both in the final evidence.
3. Write the HTML file into the user's workspace with a short assumptions comment for unresolved facts.
4. Run `npm run verify:lite -- <file.html>` when shell is available, and preview or screenshot with the host browser when available.
5. Report the file path, route, template, assumptions, verification result, and only the caveats that affect use.

Do not turn first run into setup work. No account login, global install, export dependency, or broad environment change belongs in the ClawHub-safe path.

## AI Leverage Loop

This skill should make both sides more effective: humans should not learn prompt engineering before receiving a useful artifact, and agents should not improvise a design system from a blank page.

1. **Human gives intent** — ordinary language, partial facts, or a rough visual preference is enough to begin.
2. **Agent chooses the narrowest route** — one mode, one primary template, required references only.
3. **Artifact appears early** — a local HTML source is more valuable than an extended planning conversation.
4. **Assumptions stay visible** — unresolved facts, missing assets, and export limits are labeled in the output and final evidence.
5. **Proof closes the loop** — the final answer includes the file, mode, template, verification, and caveats, so the next iteration starts from real work.

## Output Boundary

- ClawHub-safe core outputs verified local HTML, SVG/static companion files, and export-ready source structure.
- MP4/GIF/PDF/PPTX automation is not bundled in the ClawHub-safe package. For those requests, prepare the HTML source and export plan here, then use the full GitHub repo only when the user explicitly wants local automation.
- Never claim that an export file exists until the corresponding export command has actually run and the file has been inspected.

## Use When

- Interactive prototype, hi-fi mockup, clickable app flow, dashboard, landing page, whitepaper, report, infographic, slide deck, changelog, card, invitation, social cover, or brand system.
- Motion demo or launch animation, especially when the user also wants export planning for MP4/GIF.
- Design critique, brand diagnosis, or 3 differentiated style directions before implementation.
- PDF/PPTX/SVG export is requested from an HTML-first source; the ClawHub bundle prepares export-ready source, while heavy export helpers live in the full GitHub repo.

## Do Not Use When

- The real task is production frontend engineering, backend work, SEO-critical site implementation, or a CSS bug inside an existing app.
- The user only wants copy editing with no visual artifact.
- The deliverable must round-trip through Word, Google Docs, or a locked corporate template.

## OpenClaw And ClawHub Contract

- Install/publish through ClawHub: `openclaw skills install ifq-design-skills`; packed bundles are built with `npm run pack`.
- Discovery metadata is duplicated in this frontmatter and [clawhub.json](clawhub.json) so OpenClaw can read triggers, permissions, `requires`, `os`, and neutral-verb tool mapping without parsing the full manual.
- Minimum runtime: Node >= 18.17. `metadata.openclaw.requires.bins` declares `node`; required env/config gates are intentionally empty. The ClawHub bundle has zero dependencies, zero install hooks, and no script-side outbound network calls.
- Permissions are workspace-scoped: filesystem read/write inside the active workspace, shell only for bundled Node scripts, browser only for optional outbound HTTPS reads of facts, fonts, or legal image assets.
- If browser/network is unavailable, keep the artifact local-first: system fonts, honest placeholders, and no factual claims that require fresh web verification.

## Core Rule 0 · Facts Before Assumptions

For any concrete product, company, technology, release date, version, person, or spec, fact-check before designing or asserting. Search official or authoritative sources when network is available; if network is blocked, ask the user for sources and mark the fact unresolved. Then follow [references/asset-protocol.md](references/asset-protocol.md) for logo, product image, UI screenshot, color, and typography assets.

## Routing Contract

- Clear visual request: route through [references/modes.md](references/modes.md) and `modeRoutes` in [assets/templates/INDEX.json](assets/templates/INDEX.json).
- Vague request or no style/context: propose 3 directions using [references/design-styles.md](references/design-styles.md), [references/ifq-native-recipes.md](references/ifq-native-recipes.md), and [references/design-context.md](references/design-context.md).
- Real brand/product: run [references/asset-protocol.md](references/asset-protocol.md) before color, layout, or hero imagery decisions.
- App prototype: use [references/ios-prototype.md](references/ios-prototype.md) and the frame assets.
- Slides/decks: load [references/slide-decks.md](references/slide-decks.md) before writing; use [references/editable-pptx.md](references/editable-pptx.md) only when editable export is requested.
- Motion/video: load [references/animation-pitfalls.md](references/animation-pitfalls.md), [references/animation-best-practices.md](references/animation-best-practices.md), [references/animations.md](references/animations.md), and [references/video-export.md](references/video-export.md).

## IFQ Ambient Layer

- The user's brand is the subject. IFQ is the authored layer: layout rhythm, warm paper, rust ledger, mono field notes, signal spark, quiet URL, and editorial contrast.
- Every deliverable uses at least 3 IFQ marks. Do not paste a loud generic watermark unless the task is IFQ-owned or an animation export explicitly calls for a closing credit.
- Built-in templates use China-safe font loading; see [references/font-loading.md](references/font-loading.md).
- Avoid visible internal taxonomy labels such as `Signal Spark` or `Rust Ledger` in user-facing designs. Write real content instead.

## Safety Contract

- Root instructions stay scoped to HTML-first visual delivery. Do not ask for unrelated secrets, host config, persistent agents, or background services.
- Scripts are local-first: no dynamic eval, no child_process, no runtime network calls, no hidden installs, and no writes outside the user's workspace.
- Required environment variables are intentionally empty. Optional export automation is not bundled here; use the full GitHub repo only after explicit user intent.
- ClawHub/VirusTotal posture and package hygiene are tracked in [references/clawhub-publishing.md](references/clawhub-publishing.md) and [references/smoke-test.md](references/smoke-test.md).

## Anti-Slop Preflight (Hard Gate)

Before delivery, run the 7-point checklist from [references/anti-ai-slop.md](references/anti-ai-slop.md). Every item is a hard gate — skip one and the output looks like default AI:

1. No side border-left > 1px as card emphasis. Use full borders, background blocks, or icon leads.
2. No gradient text (`background-clip: text`). Use solid color + weight/size for hierarchy.
3. No default glassmorphism. Use only when real spatial depth exists.
4. No hero-metric template (big number + small label + gradient row). SaaS cliché since 2018.
5. No same-size icon card grid. Vary rhythm — irregular sizes, mixed layouts.
6. No purple gradient on white. AI "premium" cliché.
7. Display font is not Inter/Roboto/Arial/system default. Use Newsreader, Noto Serif SC, or the user's brand font.

Run `npm run anti-slop -- <file.html>` when shell is available, or scan manually. Fix violations before delivery.

## Verification Before Delivery

1. Open or preview the generated HTML with the host agent's browser tooling when available.
2. For app prototypes, click at least one primary path, one tab/screen switch, and one detail or annotation action.
3. For decks, verify slide count, aspect ratio, and format requirements before any PDF/PPTX handoff; in ClawHub-safe mode, report the export plan rather than pretending the helper ran.
4. For motion exports, verify timing, audio policy, promotion mark, and final file presence only when the full GitHub repo helper has actually produced the file.
5. After editing this skill package, run `npm run validate`; before publishing, also run `npm run pack`.

## Reference Map

| Need | Load |
|---|---|
| OpenClaw, ClawHub, agent install, tool mapping | [references/agent-compatibility.md](references/agent-compatibility.md), [references/clawhub-publishing.md](references/clawhub-publishing.md), [references/smoke-test.md](references/smoke-test.md) |
| Marketplace lessons and quality bar | [references/skill-ecosystem-quality.md](references/skill-ecosystem-quality.md) |
| Mode routing and execution workflow | [references/modes.md](references/modes.md), [references/workflow.md](references/workflow.md), [references/verification.md](references/verification.md) |
| Facts, brand assets, design context, critique | [references/asset-protocol.md](references/asset-protocol.md), [references/design-context.md](references/design-context.md), [references/critique-guide.md](references/critique-guide.md) |
| Style direction and anti-slop | [references/design-styles.md](references/design-styles.md), [references/ifq-native-recipes.md](references/ifq-native-recipes.md), [references/content-guidelines.md](references/content-guidelines.md), [references/anti-ai-slop.md](references/anti-ai-slop.md) |
| React/Babel single-file output and fonts | [references/react-setup.md](references/react-setup.md), [references/font-loading.md](references/font-loading.md) |
| IFQ identity assets | [references/ifq-brand-spec.md](references/ifq-brand-spec.md), [assets/ifq-brand/BRAND-DNA.md](assets/ifq-brand/BRAND-DNA.md) |
| App prototypes | [references/ios-prototype.md](references/ios-prototype.md) |
| Slides and editable PPTX | [references/slide-decks.md](references/slide-decks.md), [references/editable-pptx.md](references/editable-pptx.md) |
| Motion, video, and audio | [references/animations.md](references/animations.md), [references/animation-best-practices.md](references/animation-best-practices.md), [references/animation-pitfalls.md](references/animation-pitfalls.md), [references/video-export.md](references/video-export.md), [references/audio-design-rules.md](references/audio-design-rules.md), [references/sfx-library.md](references/sfx-library.md) |
| Scenes, live tweaking, and showcase patterns | [references/scene-templates.md](references/scene-templates.md), [references/tweaks-system.md](references/tweaks-system.md), [references/apple-gallery-showcase.md](references/apple-gallery-showcase.md), [references/hero-animation-case-study.md](references/hero-animation-case-study.md), [references/revolution-gap.md](references/revolution-gap.md) |

## Completion Rule

Deliver the smallest verified artifact that satisfies the request. Report the output file, verification performed, and any caveats. Do not claim export, screenshots, or marketplace safety unless the relevant check actually passed.
