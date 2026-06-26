# Changelog

## v1.0.3 - 2026-05-06

- completed the mainstream marketplace push list with one canonical status table covering OpenClaw / ClawHub, Claude Skills, OpenAI GPT Store, MCP Registry, Smithery, Glama, PulseMCP, Hermes Agent / agentskills.io, Dify Marketplace, GitHub Copilot Extensions, Microsoft Copilot Studio / Commercial Marketplace, Poe Bots, and Gemini Gems
- added registry-specific submission notes for MCP Registry, Smithery, Glama, and PulseMCP
- added agentskills.io listing copy and Microsoft Commercial Marketplace publication notes
- corrected the GitHub Copilot adapter to avoid the retired GitHub App Copilot Extension path and describe the supported Copilot integration route as backend-needed
- added OpenAI GPT Actions privacy-policy and Microsoft Partner Center / Microsoft 365 Agents Toolkit marketplace requirements to the publishing plan
- expanded platform validation so missing mainstream platform materials fail release checks

## v1.0.2 - 2026-04-28

- added multi-platform adapter packages under `platforms/` for Claude Skills, Hermes Agent, MCP, OpenAI GPT Store, Dify, Poe, Gemini Gems, GitHub Copilot Extensions, and Microsoft Copilot Studio
- added a local stdio MCP server exposing `preflight_check`, `init_business`, `update_focus`, `generate_artifact_document`, and `validate_release`
- added platform publishing status, requirements, experience log, and publish-all checklist
- added `scripts/validate_platforms.py` and wired it into release validation

## v1.0.1 - 2026-04-28

- rewrote the English and Chinese README openings around first-time founder value instead of upgrade comparison
- refreshed ClawHub listing, release README files, sample outputs, announcement copy, and social copy to match the operating cockpit positioning
- replaced stale public guides and playbooks with current goal, bottleneck, primary arena, shortest-action language
- added a v1.0.1 release note and publishing guidance with a safe one-line `clawhub publish` command
- strengthened release validation for public docs and standalone role brief output

## v1.0.0 - 2026-04-24

- rebuilt the product as a visual operating cockpit for AI-native one-person companies
- changed the state contract to `version: 1.0` and removed legacy `stage_id` / `current_round` state fields
- upgraded the reading layer entry to `阅读版/00-经营驾驶舱.html` or `reading/00-operating-cockpit.html`
- added deterministic SVG visual assets under `视觉素材/` or `visual-kit/`
- added optional AI-image prompt assets for promotion while keeping image generation out of the required runtime path
- changed old stage/round commands into explicit v1.0 deprecation guidance
- aligned generated role briefs, flow notes, reminders, and DOCX starter templates with the v1.0 operating-loop language

## v0.6.7 - 2026-04-09

- added a localized HTML reading layer so every generated workspace now includes `阅读版/00-先看这里.html` or `reading/00-start-here.html` for direct viewing after download
- kept markdown as the editable workspace source while preserving numbered DOCX files for formal deliverables
- updated validation, README, SKILL, release collateral, and sample outputs so the public contract matches the new three-layer output model

## v0.6.6 - 2026-04-09

- disabled automatic host-package installation in the marketplace-facing Python compatibility helper so `scripts/ensure_python_runtime.py` now stays in compatibility-guidance mode unless it is only rerunning a target script with an already-trusted interpreter
- tightened persisted output boundaries by constraining generated artifact output and persisted role briefs to stay inside the approved company workspace
- disabled implicit invocation in `agents/openai.yaml` and rewrote README, SKILL, security docs, listing copy, publishing notes, and release collateral so the public safety boundary matches the real runtime behavior

## v0.6.5 - 2026-04-07

- localized the entire founder-visible workspace surface so Chinese founders now get Chinese file and directory names while English founders get English-visible equivalents
- moved machine state to the hidden internal path `.opcos/state/current-state.json` and removed the old visible state-file leak from founder workspaces
- added path-layout helpers, migration-safe workspace harmonization, localized artifact names, and stricter release validation for Chinese and English workspace separation

## v0.6.4 - 2026-04-07

- removed the hard-coded leaked vertical case from generated founder-facing surfaces such as landing copy, interview board, trial intake, feedback capture, and demo HTML
- enforced a direction-first bootstrap contract in `scripts/init_company.py` so workspace creation now requires confirmed founder inputs instead of placeholder defaults
- updated validation, README, release collateral, prompt metadata, and first-run docs so the public surface matches the real runtime behavior

## v0.6.3 - 2026-04-04

- removed leftover state lock artifacts from founder workspaces so merge-safe persistence no longer leaves `当前状态.json.lock` behind after script runs
- kept the merged-save and file-lock protection from `v0.6.2` while cleaning the user-visible workspace surface back to final deliverables only

## v0.6.2 - 2026-04-04

- added founder-facing growth assets to the workspace renderer: `sales/04-对外落地页文案.md`, `sales/05-访谈冲刺看板.md`, `sales/06-试用申请问卷.md`, `delivery/04-试用反馈回收表.md`, and `product/demo/index.html`
- upgraded `00-经营总盘.md` and `04-产品与上线状态.md` so they link directly to demo, landing, intake, and feedback surfaces instead of stopping at abstract status summaries
- turned the generated demo into a real static HTML page with pricing, product boundary, trial path, and a visible intake form block
- hardened state persistence in `scripts/common.py` with baseline-aware merge saves plus file locking so parallel script runs no longer clobber unrelated state sections
- revalidated the package with `python3 scripts/validate_release.py`, `git diff --check`, and a concurrent founder-run regression on a temporary workspace

## v0.6.1 - 2026-04-04

- fixed stage inference so updating cash no longer incorrectly promotes a build-stage company into operate or grow
- stopped `update_cash.py` from forcibly overwriting the founder's primary arena
- upgraded generated support work surfaces so `product/01-MVP与上线清单.md`, `sales/01-成交动作清单.md`, and `ops/01-上线检查清单.md` are now actionable checklists instead of duplicated root docs
- tightened release validation to generate and verify deployment and production DOCX artifacts explicitly instead of relying on stage side effects
- validated the improved workflow against a realistic narrow-founder scenario without binding the package to any leaked or hard-coded vertical case

## v0.6.0 - 2026-04-04

- rebuilt the product around a business-loop state model instead of a stage/round-first surface
- added v3 state handling with shared objects for founder, focus, offer, pipeline, product, delivery, cash, assets, and risk while keeping legacy compatibility fields
- changed the generated workspace to a new operating dashboard surface with direct files for offer, pipeline, product, delivery, cash, assets, risks, weekly focus, and daily action
- added business-first scripts for focus, offer, pipeline, product, delivery, cash, asset, migration, and system validation
- kept legacy round and stage scripts runnable by mapping them onto the new state model
- updated validation, README, release docs, skill metadata, and agent metadata to present the project as a true one-person-company operating system instead of a round-driven document system

## v0.5.8 - 2026-04-04

- removed status markers such as `[待生成]` and `[已生成]` from generated DOCX file names so artifacts now use their final deliverable names from the start
- replaced `07-文档产物规范.md` and `11-交付状态总览.md` with `07-交付物地图.md` and `11-交付目录总览.md` to make the workspace read like real output instead of output specification
- dropped the workspace-level deliverable-template directory and shifted the generated artifact pack toward actual formal documents
- upgraded artifact templates, workspace rendering, stage transition logic, and release validation to track document maturity inside content rather than in file names
- refreshed README, guides, release collateral, and publishing notes so the project surface matches the new final-document model end to end

## v0.5.7 - 2026-04-04

- repositioned the visible workflow around an AI-era fast loop: validate demand, ship the smallest useful MVP, launch narrowly, capture feedback, improve, then scale
- kept the internal stage engine but reframed stages as lightweight bottleneck labels instead of heavyweight process phases
- added `12-AI时代快循环.md` to generated workspaces so founders can read the operating model directly on disk
- updated founder start guidance, stage/output templates, release copy, and agent metadata to match the new fast-loop positioning
- expanded release validation to check the new fast-loop guide in generated workspaces

## v0.5.6 - 2026-04-04

- upgraded the first-run contract so the system now actively asks for a one-line founder idea or offers 3 to 4 startup directions instead of front-loading heavy input
- added `10-创始人启动卡.md` and `11-交付状态总览.md` so founders can immediately see how to start and which formal deliverables are still pending vs completed
- changed starter artifact generation from plain fixed DOCX files to status-marked placeholder files such as `[待生成]` and automatic promotion to `[已生成]`
- added review-path and improvement reminders to every runtime report so users always know where to inspect the latest output and how to request changes
- tightened validation to check the new placeholder naming, status overview, removal of legacy unnumbered artifact folders, and placeholder-to-completed promotion flow

## v0.5.5 - 2026-04-03

- upgraded the ClawHub storefront summary from descriptive to outcome-driven so the first line feels more compelling to new users
- aligned the listing short description with the new stronger hook

## v0.5.4 - 2026-04-03

- shortened the public ClawHub summary so the English hook is tighter and more of the Chinese summary fits on the listing card
- aligned the ClawHub listing short description with the new concise storefront summary

## v0.5.3 - 2026-04-03

- polished the GitHub English README so canonical Chinese workspace paths are explained with English-first labels instead of looking like untranslated product copy
- rewrote `SKILL.md` into an English-first bilingual storefront so ClawHub readers can understand the product, entry points, runtime model, and trust boundaries immediately
- reordered ClawHub-facing copy so English-facing summaries and prompts lead, while still keeping Chinese support visible

## v0.5.2 - 2026-04-03

- updated `SKILL.md` metadata so the public ClawHub summary is readable for both Chinese and English users
- aligned the latest release notes and publishing references with the metadata polish release

## v0.5.1 - 2026-04-03

- added language-aware runtime reports so Chinese prompts default to Chinese output and English prompts default to English output
- added English role localization, English workspace content generation, and English DOCX content generation without breaking the canonical workspace layout
- upgraded `scripts/validate_release.py` to verify the English runtime and document-generation path in addition to the existing Chinese path
- updated README, guides, ClawHub listing copy, release collateral, and publishing notes to present the project as bilingual rather than Chinese-only

## v0.5.0 - 2026-04-03

- replaced the old three-form artifact model with numbered `.docx` deliverables inside `产物/`
- added real DOCX generation in `scripts/common.py` and upgraded `scripts/generate_artifact_document.py` to emit numbered files only
- added workspace starter deliverables for actual output tracking, software/code evidence, non-software deliverables, and post-launch deployment/production materials
- added `08-阶段角色与交付矩阵.md` and `09-当前阶段交付要求.md` so role activation and required outputs are explicit
- promoted `devops-sre` and `customer-success` into the default launch-stage role set to ensure上线后资料不缺位
- upgraded release validation to assert numbered DOCX artifacts, launch-stage ops docs, and the expanded launch role pack

## v0.4.0 - 2026-04-03

- upgraded the interaction contract from plain step reporting to a two-view output system with `用户导航版` and `审计版`
- added a three-layer navigation bar across the workflow so every major operation now surfaces `阶段 / 回合 / 本次 Step`
- changed `Step 1/5 -> Step 5/5` from system-only labels to dual labels with natural-language intent plus system step names
- added explicit `本次会做 / 不会做`, `本次变化`, and `回合仪表盘` sections to the runtime report layer
- replaced terse save/runtime reporting with user-readable save explanations and runtime explanations
- added `scripts/generate_artifact_document.py` to generate standard artifact outputs
- added three standard artifact forms: `内部工作稿`, `标准规范稿`, and `可转 DOCX 稿`
- added workspace artifact templates and `07-文档产物规范.md` so document delivery is built into the workspace instead of left to ad hoc chat output
- updated README, release copy, sample outputs, and agent metadata to reflect the new navigation and document model

## v0.3.3 - 2026-04-02

- rewrote the repository README to explain the product as a professional, state-driven company operating system instead of a generic prompt
- added explicit architecture framing so users can immediately understand the system layers and operating model
- added one-line install and one-line start entry points for faster onboarding
- aligned release READMEs, ClawHub listing copy, and agent metadata with the sharper positioning

## v0.3.2 - 2026-04-02

- added fixed `Step 1/5 -> Step 5/5` progress reporting plus default `状态栏 / 保存状态 / 运行状态` output across the workflow
- made persistence explicit by reporting whether artifacts were saved, where they were saved, and why they were not saved
- introduced `scripts/preflight_check.py` for environment checks and clearer separation between `installed`, `runnable`, `workspace_created`, and `persisted`
- introduced `scripts/checkpoint_save.py` for explicit checkpoint persistence during live company operation
- introduced `scripts/ensure_python_runtime.py` to detect compatible runtimes, generate install plans, and let OpenClaw recover from Python incompatibility
- widened helper-script compatibility to older Python environments by removing newer union syntax from runtime-critical paths
- rewrote the main README and release-facing copy to target founders actively building AI-native solo companies instead of generic startup readers

## v0.3.0 - 2026-04-02

- rebuilt the skill around `创建公司 -> 启动回合 -> 推进回合 -> 校准 -> 切阶段`
- made Chinese-first workspace names, file names, role names, and operating language the default for Chinese users
- replaced week-based operating rhythm with round-based execution and trigger-based calibration
- introduced `总控台` as the central coordinating role and reduced the default starter role set
- rewrote the repository references, templates, examples, and release materials to match the V2 product shape
- added new scripts for starting rounds, updating rounds, calibrating rounds, and transitioning stages
- removed the old weekly review script, old role/workflow references, and the legacy bilingual SaaS example pack

## v0.2.1 - 2026-04-01

- added a single-command release validator that checks workspace scripts, agent-brief generation, and release SVG assets
- updated GitHub Actions to run the shared release validator instead of duplicated inline checks
- documented the validation step in the README, publishing guide, PR template, and release checklist
- ignored local Codex metadata and tmp-validation outputs from Git status

## v0.2.0 - 2026-04-01

- narrowed the primary positioning to solo SaaS founders while keeping broader one-person business support
- added quick-start prompts to the skill itself
- emphasized first-run artifact creation instead of theory-heavy responses
- strengthened trust-boundary and approval language
- aligned packaging copy across skill metadata, GitHub materials, and ClawHub listing
- added repository README for direct GitHub publishing
- added Chinese repository README and bilingual navigation
- added in-repo release materials for GitHub, ClawHub, and social launch
- added GitHub validation workflow and contribution templates

## v0.1.0 - 2026-04-01

- initial publishable skill package
- role references across company functions
- lifecycle and workflow references
- reusable templates
- company initialization and weekly review scripts
- global bilingual SaaS example pack
