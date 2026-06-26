# Release Notes

## v1.0.3 - Mainstream Platform Push List

`v1.0.3` ships the completed mainstream marketplace push list as the canonical distribution package.

What changed:

- made `platforms/PUBLISHING-STATUS.md` the single operating table for OpenClaw / ClawHub, Claude Skills, OpenAI GPT Store, MCP registries, Hermes / agentskills.io, Dify, Copilot, Microsoft, Poe, and Gemini
- added registry-specific submission material for MCP Registry, Smithery, Glama, and PulseMCP
- added agentskills.io listing copy and Microsoft Commercial Marketplace notes
- updated validation so missing mainstream-platform files fail release checks
- corrected the GitHub Copilot route to avoid the retired GitHub App Copilot Extension path
- recorded OpenAI GPT Actions privacy-policy and Microsoft Partner Center / Agents Toolkit requirements

The release does not change the core operating cockpit runtime. It makes the published package match the platform push plan.

## v1.0.2 - Multi-Platform Adapter Pack

`v1.0.2` adds a distribution layer for publishing One Person Company OS beyond OpenClaw.

What changed:

- added `platforms/` with ready-to-submit adapters for Claude Skills, Hermes Agent, OpenAI GPT Store, Dify, Poe, Gemini Gems, GitHub Copilot Extensions, and Microsoft Copilot Studio
- added a stdio MCP server so MCP-compatible clients can call the canonical scripts directly
- documented account, approval, and backend requirements for each market
- recorded publishing status and experience notes so future releases do not confuse prepared packages with completed publication
- added platform validation to the release validation pipeline

The canonical package remains the repository root. Platform adapters are thin wrappers around the same operating cockpit contract.

## v1.0.1 - New-User Release Polish

`v1.0.1` tightens the package for first-time founders and marketplace review.

What improved:

- README and README.zh-CN now lead with the founder's first-run questions, workspace outputs, and operating cockpit value
- ClawHub listing and release materials now use the same business-loop story
- GUIDE files and bundled playbooks now describe current goal, current bottleneck, primary arena, and shortest action
- sample outputs point directly to the HTML cockpit and visual assets
- publishing docs now include the exact bash line-continuation rule and a single-line ClawHub command
- validation now checks public docs and standalone role brief output for stale visible workflow language

## v1.0.0 - Visual Operating Cockpit

`v1.0.0` is a breaking architecture release.

One Person Company OS is now a visual operating cockpit instead of a stage/round operating shell. The visible loop stays:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

What changed:

- v1.0 state no longer writes legacy `stage_id` or `current_round`
- the first HTML page after download is `阅读版/00-经营驾驶舱.html` or `reading/00-operating-cockpit.html`
- workspaces include deterministic SVGs for the business loop and revenue pipeline
- workspaces include optional AI image prompts for launch and promotional visuals
- old round/stage scripts now return deprecation guidance
- generated role briefs, flow notes, reminders, and DOCX starter templates now use v1.0 operating-loop language rather than the old stage/round surface

Normal use still does not require API keys, system package installation, or writes outside the approved workspace.

## v0.6.7 - Download-Friendly Reading Layer

`v0.6.7` upgrades the generated workspace from a markdown-heavy working folder into a better download artifact.

The new output model is:

- markdown for continued editing and agent updates
- localized HTML for direct reading after download
- DOCX for formal external deliverables

What changed:

- every generated workspace now includes `阅读版/00-先看这里.html` or `reading/00-start-here.html`
- the core dashboard, offer, pipeline, product, delivery, cash, asset, and deliverable-overview pages now export as localized HTML reading files
- release validation and public docs now describe the reading layer explicitly instead of presenting the package as markdown-only

## v0.6.6 - Marketplace Safety Boundary Hardening

`v0.6.5` fixed the founder-visible workspace surface.

`v0.6.6` fixes the next marketplace trust mismatch: the package behavior was coherent, but the public runtime contract still left too much ambiguity around host-environment changes and write scope.

This release adds and updates:

- a marketplace-safe `scripts/ensure_python_runtime.py` path that stays in compatibility-guidance mode instead of auto-installing system packages
- tighter write-boundary checks so persisted artifact output and saved role briefs stay inside the approved company workspace
- an explicit no-implicit-invocation policy in `agents/openai.yaml`
- synchronized README, SKILL, security docs, listing copy, publishing notes, and release material so the public package surface matches the runtime safety boundary

The result is a package that is easier to audit, easier to trust, and less likely to trigger marketplace review concerns while keeping the founder workflow intact.

## v0.6.5 - Fully Localized Workspace Surface

`v0.6.4` fixed the direction-first contract and neutralized leaked default cases.

`v0.6.5` fixes the next serious product mismatch: the runtime could already speak Chinese or English, but the generated workspace still mixed Chinese and English paths and exposed the machine state file in the founder-visible surface.

This release adds and updates:

- fully localized Chinese-visible and English-visible workspace files and directories
- a hidden stable machine-state path at `.opcos/state/current-state.json`
- localized default artifact names, role brief filenames, support work surfaces, and flow files
- stronger layout harmonization for migrated workspaces
- release validation that explicitly checks Chinese and English workspace separation

The result is a cleaner and more trustworthy product surface: founders now get a workspace that actually matches their language, while automation still has one hidden stable state path.

## v0.6.4 - Direction-First Bootstrap And Vertical-Neutral Defaults

`v0.6.3` cleaned the lock-file artifact left by safer persistence.

`v0.6.4` fixes the deeper founder-trust problem exposed in the next audit: the package still looked direction-first in documentation, but the generated default surfaces were effectively bound to one leaked vertical case.

This release adds and updates:

- vertical-neutral landing-copy, interview-board, trial-intake, feedback, and demo templates
- a confirmed-input gate in `scripts/init_company.py` so workspace creation requires real founder direction instead of placeholder defaults
- updated README, release docs, ClawHub prompt copy, and validation so the public contract matches the actual runtime behavior

The result is a cleaner product boundary: the system now asks for direction first, waits for confirmation, and only then writes a reusable one-person-company workspace.

## v0.6.3 - Lock-Artifact Cleanup

`v0.6.2` added merge-safe locked persistence for overlapping founder actions.

`v0.6.3` closes the remaining surface issue: the lock file itself should not remain in the founder workspace after a successful run.

This release adds and updates:

- automatic cleanup of the temporary state lock file after each save
- the same safer merged persistence behavior from `v0.6.2`, but without polluting the workspace with `.lock` artifacts

The result is a cleaner founder workspace surface: the concurrency protection stays, but the user only sees final working files.

## v0.6.2 - Founder Conversion Surfaces And Safer Parallel Persistence

`v0.6.1` fixed stage drift and shallow support work surfaces.

`v0.6.2` fixes the next founder-run gap: the system still did not create enough outward-facing conversion assets by default, and parallel business scripts could still overwrite unrelated state changes.

This release adds and updates:

- a generated landing-copy file for founder outreach
- a generated interview sprint board for the first 10 target conversations
- a generated trial intake questionnaire and a trial feedback capture sheet
- a generated static HTML demo page with scope boundary, pricing, CTA flow, and visible intake fields
- direct links from the dashboard and product-status views into those new sell-side and trial-side surfaces
- baseline-aware merged state saves plus file locking so concurrent business scripts preserve unrelated sections instead of clobbering them

The result is a system that is more useful in a real founder run: it now pushes closer to actual outreach and trial execution, and it is safer to keep advancing multiple business surfaces in the same session.

## v0.6.1 - Support-Surface Upgrade And Stage-Inference Fix

`v0.6.0` rebuilt the product around a business loop.

`v0.6.1` fixes two practical issues that appeared during a real founder-style run:

- stage inference could drift when cash updates changed focus metadata
- supporting work surfaces under `product/`, `sales/`, and `ops/` were still too shallow and duplicated the root docs

This release adds and updates:

- a safer `stage_from_product_and_focus()` rule so build-stage products stay in build unless real launch or live signals exist
- a fix in `update_cash.py` so cash updates stop hijacking the main arena by default
- actionable generated checklists for MVP, revenue actions, and launch readiness
- stronger release validation that explicitly generates and verifies deployment and production DOCX artifacts

The result is a system that behaves more coherently during real execution, especially when a founder is moving between product, sales, delivery, and cash views inside one ongoing company loop.

## v0.6.0 - Business-Loop Operating System

`v0.5.8` fixed the file surface so deliverables looked like real documents instead of document specification.

`v0.6.0` fixes the deeper product mismatch: the system still behaved too much like a stage-and-round startup shell instead of a real one-person-company operating system.

This release rebuilds the product around a business loop:

- promise
- buyer
- product capability
- delivery
- cash
- learning
- asset

This release adds and updates:

- a new v3 state model centered on `founder / focus / offer / pipeline / product / delivery / cash / assets / risk`
- a new workspace surface led by `00-经营总盘.md`, `02-价值承诺与报价.md`, `03-机会与成交管道.md`, `04-产品与上线状态.md`, and `05-客户交付与回款.md`
- new business scripts such as `init_business.py`, `update_focus.py`, `advance_product.py`, `advance_pipeline.py`, `advance_delivery.py`, `update_cash.py`, and `record_asset.py`
- migration support for old workspaces and compatibility writes for old round/stage scripts
- updated release validation so the generated package must pass through the new business-loop workflow locally
- rewritten README, release README, listing copy, skill metadata, and publishing notes so the repository surface now matches the actual product

The result is a system that can support a founder starting from an idea, pushing an MVP toward something sellable, managing real buyers and delivery, and recovering cash while building reusable assets.

## v0.5.8 - Final-Named Deliverables And Real Document Surface

`v0.5.7` made the operating model lighter.

`v0.5.8` fixes the next serious problem: generated output still looked too much like document specification and placeholder management instead of real deliverable documents.

This release upgrades the artifact model around one rule:

- formal documents should use their final deliverable names from the start

This release adds and updates:

- final-named DOCX files without `[待生成]` or `[已生成]` in the file name
- a new `07-交付物地图.md` instead of `07-文档产物规范.md`
- a new `11-交付目录总览.md` instead of `11-交付状态总览.md`
- removal of the workspace-level deliverable-template starter directory from the default generated pack
- document-maturity tracking inside file content rather than in file names
- updated artifact generation, stage transition, workspace rendering, sample outputs, and release validation

The result is a project that now reads and behaves more like a real delivery system: fewer placeholder semantics, clearer file paths, and a stronger final-output feel across the workspace.

## v0.5.7 - AI-Era Fast Loop And Lightweight Stages

`v0.5.6` made the first-run and deliverable board clearer.

`v0.5.7` fixes the next real problem: the product still exposed too much stage and process weight to founders who should really be moving on a faster AI-era loop.

This release reframes the visible operating model around:

- narrow the user and pain
- validate demand quickly
- ship the smallest useful MVP
- launch narrowly
- collect feedback and production reality
- improve before scaling growth

This release adds and updates:

- a new `12-AI时代快循环.md` generated into every workspace
- founder-start guidance that explains the fast loop directly
- lighter stage descriptions that position stages as bottleneck labels rather than bureaucracy
- updated current-stage, execution, calibration, and deliverable templates
- aligned README, guide, agent metadata, ClawHub listing, and release copy
- stronger validation so the generated workspace must include the fast-loop guide

The result is a system that still keeps real control structures internally, but feels closer to how an AI-native solo company should actually run.

## v0.5.6 - Founder Intake And Placeholder Deliverable Control

`v0.5.5` improved the storefront hook.

`v0.5.6` improves the actual founder experience and artifact discipline during real use.

The gap was no longer positioning alone.
It was that first-run interaction still asked too much of the founder, and the workspace still did not make pending vs completed deliverables obvious enough.

This release adds:

- proactive founder intake from a one-line idea, with 3 to 4 suggested directions when the founder is still undecided
- a new `10-创始人启动卡.md` so the workspace itself teaches the founder how to reply with low effort
- a new `11-交付状态总览.md` so users can immediately see which DOCX files are pending and which are complete
- placeholder starter deliverables marked with `[待生成]` and automatic promotion to `[已生成]` when a formal artifact is generated
- review-path and improvement reminders in every runtime report
- stricter validation against legacy unnumbered artifact folders and outdated deliverable naming

The product now behaves more like a serious control board:

- lighter founder input at the start
- clearer output visibility during execution
- stronger formal-deliverable discipline throughout the workspace lifecycle

## v0.5.5 - Outcome-Driven Storefront Hook

This patch release makes the ClawHub storefront more compelling.

The previous summary was cleaner, but still mostly descriptive.
This version shifts the opening line to an outcome:

- start from one AI product idea
- end with a run-ready solo company

This release updates:

- the `SKILL.md` public summary
- the ClawHub listing short description

No runtime behavior changes are included in this patch.

## v0.5.4 - ClawHub Summary Compression

This patch release shortens the public storefront summary.

The product surface was already in the right order, with English first and Chinese second.
The remaining issue was card-level length: the English sentence still took too much room, so the Chinese half was cut off too early in ClawHub previews.

This release fixes that by:

- replacing the long storefront summary with a shorter English hook
- keeping the same Chinese value proposition in a more compact form
- aligning the ClawHub listing short description with the new compressed summary

## v0.5.3 - English-First Storefront Polish

This patch release improves the public-facing storefront for both GitHub and ClawHub.

The runtime and generated materials were already bilingual.
The remaining weak point was presentation:

- the English README still showed too many raw Chinese workspace paths without enough English framing
- the public `SKILL.md` still read like an internal Chinese-first spec instead of a storefront that English users could scan quickly
- ClawHub-facing copy still exposed Chinese before English in places where English readers were likely to bounce

This release closes that gap by:

- rewriting the GitHub English README sections that describe canonical workspace files
- turning `SKILL.md` into an English-first bilingual storefront while preserving the same operating rules
- reordering ClawHub listing copy and prompts so English users see an immediately understandable product surface

## v0.5.2 - Bilingual Listing Metadata Polish

This patch release fixes the remaining public-surface mismatch after the bilingual runtime upgrade.

The runtime, generated documents, GitHub README, and release materials were already bilingual.
The remaining weak point was the live ClawHub listing summary, which still rendered as Chinese-only metadata.

This release closes that gap by:

- updating `SKILL.md` frontmatter to use a concise Chinese-plus-English description
- making the latest ClawHub listing readable to both Chinese and English users before they even open the repository
- keeping the runtime and packaging behavior unchanged so the patch is safe to ship immediately

## v0.5.1 - Bilingual Runtime And Document Upgrade

This release upgrades `one-person-company-os` from “Chinese-friendly” to “actually bilingual in production use.”

The remaining gap was not core workflow design.
It was language continuity across the real product surface:

- English founders could read the README but still hit Chinese-only runtime output
- generated role briefs and formal deliverables did not fully follow English execution
- public release copy still leaned too hard on a Chinese-only framing

This release closes that gap by adding:

- language-aware runtime reports across the main workflow scripts
- English role localization and English generated workspace content
- English DOCX artifact content generation
- release validation that now checks the English path as well as the Chinese path
- updated GitHub, ClawHub, guide, and release materials for both Chinese and English founders

## v0.5.0 - Numbered DOCX Deliverables and Post-Launch Ops Pack

This release upgrades `one-person-company-os` from “deliverable-aware” to “actually deliverable under audit.”

The remaining gaps were practical:

- artifacts still produced too many markdown-like forms instead of one formal output
- software or non-software runs could look “busy” without leaving clear real deliverables
- launch-stage work could miss deployment or production materials because the default role/output set was too light

This release closes those gaps by adding:

- numbered `.docx` outputs only inside `产物/`
- a built-in DOCX writer so the workspace can generate formal deliverables without extra tooling
- starter deliverable packs for actual outputs, software/code evidence, and non-software deliverables
- automatic deployment, rollback, monitoring, and production materials for launch and later stages
- explicit stage-role and deliverable matrices so users can see which roles and outputs must exist at each stage
- default launch-stage activation of `运维保障` and `用户运营`
- updated validation so release checks now assert numbered DOCX artifacts and launch-stage ops materials

## v0.4.0 - Navigation UX and Deliverable Document System

This minor release upgrades the product from “state-aware skill” to “navigable and deliverable operating system.”

The main problem was no longer content quality.
It was that founders could still lose orientation inside a long run, and key artifacts still depended too much on ad hoc chat formatting.

This release closes that gap by adding:

- a three-layer navigation bar with `阶段 / 回合 / 本次 Step`
- dual-labeled steps with natural-language intent plus system step names
- a split output contract with `用户导航版` and `审计版`
- explicit `本次会做 / 不会做`, `本次变化`, and `回合仪表盘` sections
- user-readable save explanations and runtime explanations instead of terse raw fields alone
- a new `scripts/generate_artifact_document.py` entry point for artifact generation
- three standard artifact forms:
  - `内部工作稿`
  - `标准规范稿`
  - `可转 DOCX 稿`
- built-in workspace templates and a document-output guide so deliverables can be persisted in a standard format
- updated README, release listing copy, and sample outputs to match the upgraded interaction model

## v0.3.3 - README Professionalization and Architecture Clarity

This patch release sharpens the public product surface.

The goal is simple: a founder should be able to open the README and understand in under a minute:

- what this system is
- what architecture it uses
- why it is more professional than a generic startup prompt
- how to install it in one line
- how to start it in one line

This release includes:

- a full rewrite of the main README information architecture
- a clearer architecture section for the system layers
- a stronger, more professional product definition
- one-line install and one-line start sections
- aligned release README, ClawHub listing, and agent metadata

## v0.3.2 - State Transparency and Runtime Recovery

This patch release makes the skill behave more like a real company operating system and less like an endless advisory prompt.

This release includes:

- fixed `Step 1/5 -> Step 5/5` execution reporting across preflight, workspace creation, round start, round update, calibration, checkpoint save, and stage transition
- explicit save reporting that states whether content was saved, where it was saved, which files were written, and why content remained chat-only
- a new `scripts/preflight_check.py` entry point for environment checks and mode selection
- a new `scripts/checkpoint_save.py` entry point for saving recoverable company checkpoints
- a new `scripts/ensure_python_runtime.py` entry point for Python runtime discovery, install planning, and interpreter switching
- updated runtime reporting that distinguishes `installed`, `runnable`, `python_supported`, `workspace_created`, and `persisted`
- a homepage rewrite and release-copy rewrite that target founders actively building AI-native solo companies

## v0.3.0 - Round-Based Solo Company OS

This release is a full V2 rewrite of the skill.

The product is no longer organized around weekly review and heavy startup documentation. It is now organized around:

- create the company
- start a round
- advance the round
- calibrate only when triggered
- transition stages when the bottleneck changes

This release includes:

- a rewritten `SKILL.md` centered on five clear user intents
- a Chinese-first workspace with Chinese file names and operating language by default
- a new `总控台` role and a smaller default starter role set
- new scripts for round start, round update, calibration, and stage transition
- rewritten references, templates, sample outputs, and release materials
- removal of the old weekly review flow, the legacy role/workflow references, and the previous bilingual SaaS example pack

## v0.2.1 - Release Validation and Publishing Cleanup

This patch release tightens the publishing surface without changing the core positioning of the skill.

This release includes:

- a single-command `scripts/validate_release.py` check for workspace setup, weekly review generation, role-agent brief generation, and release SVG parsing
- a GitHub Actions workflow that reuses the same release validator locally and in CI
- README, publishing, and release-checklist updates so the validation step is part of the default release flow
- `.gitignore` updates for local Codex metadata and tmp-validation output

## v0.2.0 - First Public Release

One Person Company OS is an AI-native operating system for solo founders, with solo SaaS founders as the primary use case.

This release includes:

- a publishable `SKILL.md` with quick-start prompts and explicit language behavior
- role references across founder, product, engineering, QA, DevOps, growth, support, finance, legal, data, content, and community
- workflow references for validation, build, launch, operating rhythm, and feedback loops
- reusable templates for company charter, ICP, offer sheet, PRD, launch brief, dashboard outline, and weekly review
- helper scripts for company setup and recurring weekly reviews
- example outputs for a bilingual global SaaS scenario
- GitHub, ClawHub, and social launch materials

Key behavior:

- strong first-run bias toward artifact creation
- draft-first trust boundary for high-risk actions
- Chinese prompt in -> Chinese output by default
- English prompt in -> English output by default
- bilingual output only when requested
