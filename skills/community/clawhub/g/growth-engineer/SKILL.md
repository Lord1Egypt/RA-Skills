---
name: growth-engineer
description: Growth Engineer for mobile apps and agent runtimes including OpenClaw and Hermes. Correlate analytics, crashes, billing, feedback, store signals, and repo context into proposal drafts that can flow into agent chat, GitHub issues, or draft pull requests.
license: MIT
homepage: https://github.com/Wotaso/growth-engineer-skill
metadata: {"author":"wotaso","version":"1.0.207","analyticscli-target":"@analyticscli/cli","analyticscli-supported-range":">=0.1.3 <0.2.0","openclaw":{"emoji":"🚀","homepage":"https://github.com/Wotaso/growth-engineer-skill","requires":{"bins":["node","analyticscli"]},"install":[{"id":"analyticscli-cli","kind":"node","package":"@analyticscli/cli","bins":["analyticscli"],"label":"Install/update AnalyticsCLI CLI (npm package @analyticscli/cli)"}]},"hermes":{"tags":["Growth","Analytics","Mobile","Product","OpenClaw","Hermes"],"homepage":"https://github.com/Wotaso/growth-engineer-skill","requires":{"bins":["node","analyticscli"]},"install":[{"id":"growth-engineer","kind":"skill","package":"Wotaso/growth-engineer-skill","label":"Install the shared Growth Engineer for Hermes"}]}}
---

# Growth Engineer

## Canonical Skill Identity

`growth-engineer` is the single canonical Growth Engineer for agent-driven product and growth work.
The old `ai-product-manager` / `product-manager-skill` package is deprecated and should be used only as a migration alias for existing installs.
Do not recommend installing or loading both skills.

Use this same skill for OpenClaw and Hermes. Do not create a duplicate Hermes-specific copy of the instructions, scripts, references, or runtime artifacts. If an agent-specific compatibility note is needed, add a small section here and keep the deterministic runtime shared.

## Agent Compatibility

- OpenClaw: install through ClawHub with `clawhub install growth-engineer` or `npx clawhub install growth-engineer`.
- Hermes: install the same public skill repository with `hermes skills install Wotaso/growth-engineer-skill`.
- Generic SKILL.md clients: install or mount the same `skills/openclaw-growth-engineer` folder.
- All agents should use the same bundled `scripts/`, `references/`, and `data/` files.
- macOS hosts, including Mac mini machines, are supported as normal local hosts. Use the same terminal wizard from the app workspace. For recurring unattended runs on macOS, use OpenClaw heartbeats, `openclaw run --loop`, or a host scheduler such as `launchd`; keep secrets in the host terminal/env/secret file, not in chat.

## Local AnalyticsCLI Operator Notes

These notes apply when this skill is used from the local `Wotaso/analyticscli-monorepo` workspace.

- Coolify resources, projects, or deployments named `prodinfos` are AnalyticsCLI production infrastructure, not a separate customer app. Treat failed `prodinfos` deployments as AnalyticsCLI production deployment-health signals.
- For this workspace, Coolify monitoring is configured through `openclaw.config.json` with `https://coolify.wotaso.com`; read access requires `COOLIFY_API_TOKEN` in the local host environment or Growth Engineer secret store.
- Do not send OpenClaw/Hermes GitHub PR or branch links for these deployment failures. Tell them to update from ClawHub/npm after a published fix, or handle local production remediation directly from the repo and Coolify logs.

## Post-Install Reply Contract

After installing this skill from ClawHub, OpenClaw or Hermes must not stop at "installed and ready" when setup is not complete. The next reply should be short and should immediately route the user to connector setup.

Use this minimal reply shape:

1. Say the skill is installed.
2. Say one short sentence: "Next, run the local wizard so you can choose connectors, intervals, output type, and paste secrets only in the host terminal."
3. Provide exactly one copy/paste command block for the VPS, Mac mini, or host shell.
4. Do not ask for API keys, private keys, or tokens in chat. Do not list provider docs unless the user asks.

Use this command block for OpenClaw, Hermes, VPS, Linux, and macOS hosts:

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

Run this from the OpenClaw/Hermes workspace. Connector setup should route through the npm wizard so hosts get the latest wizard fixes without manual bootstrap commands.

## Post-Setup Reply Contract

After the VPS/host wizard finishes successfully, OpenClaw or Hermes should not answer with a generic agent-status paragraph. Reply in this minimal shape:

1. Say that Growth Engineer setup completed.
2. List only the configured connector groups and output destinations.
3. Say that recurring health checks run every 6 hours by default and growth runs follow the configured daily/weekly/monthly cadence.
4. Provide exactly one next command for a manual verification run:

```bash
npx -y @analyticscli/growth-engineer run --config ~/data/openclaw-growth-engineer/config.json
```

Do not ask for project/repo scoping after successful setup. Do not claim a connector is broken unless `growth-engineer status --config ...` or the wizard result says it is blocked/partial.

## Hermes Startup Override

Hermes must treat user messages such as "ja los", "starte den Growth Engineer", "Connectoren einrichten", "setup", "installieren und starten", or close variants as a wizard setup/start request.

Do not satisfy those messages by only installing `analyticscli`, running `analyticscli login`, or telling the user to run `analyticscli login` manually. The Growth Engineer setup path is the bundled local terminal wizard because it handles connector selection, secret storage, project/app discovery, cadence, and smoke tests.

When Hermes is running from chat/Discord or any non-interactive agent terminal, do not start the interactive wizard process yourself. Reply with one complete copy/paste command and tell the user to run it in the VPS or host shell where Hermes/OpenClaw should be configured. Secrets must be pasted into that shell only, not into chat.

Use this exact command block in the reply after skill installation:

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

Then add exactly one short instruction sentence: "Run this in your VPS/host shell and paste secrets only there."

If AnalyticsCLI auth is missing or invalid, the next action is still the wizard command above. The wizard should ask for the readonly token in the local terminal and persist it as `ANALYTICSCLI_ACCESS_TOKEN`; chat should not ask the user to paste tokens or detour into a separate `analyticscli login` flow.

## Use This Skill When

- you want an agent to turn product signals into execution-ready backlog work
- you need one workflow across AnalyticsCLI product analytics/feedback, RevenueCat or Paddle monetization, SEO/GSC/Bing Webmaster/DataForSEO acquisition, Sentry-compatible crash monitoring including GlitchTip, ASC/App Store Connect, app reviews, and repo context
- you want the deterministic work to live in a standalone CLI and the host agent to stay the AI/chat layer
- you want proposal delivery to be configurable between agent chat handoff, GitHub issues, and draft pull requests

## Product Focus

- Primary focus: mobile apps
- Works well with: React Native, Expo, native iOS/Android, mobile growth loops, paywalls, store reviews, crashes, release readiness
- Still valid for SaaS/web products when your connectors export the same summary JSON shape

## Private Repo / Minimal Input Rule

Treat this as a private-repo-first skill. The setup and connector wizards should ask the user for as little information as possible.

- Do not require `project.githubRepo` during connector setup. Defer repo selection until GitHub delivery or code mapping actually needs it.
- When the agent has permission to list repos, projects, apps, or Sentry/GlitchTip projects, discover them automatically and persist the best available mapping.
- Sentry/GlitchTip project lists are not required input. If org + token are configured, the exporter should discover visible projects at runtime and let the agent choose the relevant project from app/release context.
- If there are multiple plausible targets, use app/release/config context first; ask the user only when the choice is genuinely ambiguous.
- Keep GitHub issue/PR creation disabled unless explicitly requested or clearly configured. Missing repo context should be a deferred state, not a setup blocker.

## Preferred Runtime

Prefer the standalone `growth-engineer` CLI as the user-facing runtime surface when it is available. The old OpenClaw workspace CLI package is retired; do not direct users or automation to it.

- Wizard path: `growth-engineer wizard --connectors`
- Setup path: `growth-engineer setup --config openclaw.config.json`
- Primary path: `growth-engineer start --config openclaw.config.json`
- Local monorepo path: `pnpm --filter @analyticscli/growth-engineer dev start --repo-root <repo-root>`
- Copied-runtime scripts under `scripts/openclaw-growth-*.mjs` remain the compatibility path for agents that install this as a plain `SKILL.md` folder

The CLI is intentionally non-AI. The host agent should stay the only conversational/implementation layer.
Use the CLI to gather signals, generate proposals, schedule checks, and send deliveries.
If the user later asks the agent to implement a proposal, the agent should inspect the generated drafts and then use its own AI/runtime to do the work.

## OpenClaw And Hermes Cron / Recurring Run Contract

OpenClaw Gateway cron is the preferred wake-up mechanism for reliable VPS installs. The Growth Engineer schedule in `config.json` only decides what is due after the runner is invoked; it does not wake the agent by itself unless OpenClaw cron, `openclaw run --loop`, or a host scheduler is running.
Hermes Gateway cron is the matching wake-up mechanism for Hermes installs. Hermes jobs must use `hermes cron create ... --skill growth-engineer --deliver local --workdir <absolute-workspace>` so the scheduled run loads this skill and the app workspace context.

- Bootstrap/start must create or repair a non-empty workspace `HEARTBEAT.md` with an `openclaw-growth-engineer-run` fallback task.
- Wizard/start must also configure or print an OpenClaw Gateway cron job (`openclaw cron add ... --session main --system-event ... --wake now`) when `automation.openclawCron.enabled` is true.
- Wizard/start must also configure or print a Hermes cron job (`hermes cron create ... --skill growth-engineer --deliver local --workdir <absolute-workspace>`) when `automation.hermesCron.enabled` is true and Hermes is installed.
- The cron/system-event prompt must invoke `node scripts/openclaw-growth-runner.mjs --config <active-config> --state <active-config-dir>/state.json`. Do not let cron read config from one directory while the runner writes state/proof under the workspace default. The runner remains the source of truth for `schedule.intervalMinutes`, daily/weekly/monthly/quarterly/six-month/yearly cadences, connector health intervals, data-change skipping, and notification delivery.
- If a user asks whether automatic checks are enabled, inspect the matching agent scheduler first (`openclaw cron list`, `openclaw cron runs --id <job-id>`, `openclaw tasks list`, or `hermes cron list` / `hermes cron status <job-id>`), then inspect runner proof (`<state-dir>/runtime/scheduler-proof.jsonl`) and state (`<state-dir>/state.json`). Do not use Discord as the default coordination path.
- Keep `HEARTBEAT.md` tiny and secret-free. It is a fallback/awareness checklist and should say to reply `HEARTBEAT_OK` when no connector alert, production crash, generated issue, or actionable growth finding exists.

Implementation PR rule:

- If the user asks for a GitHub issue plus a pull request, or says "create a PR", "make the PR", "implement this", "fix the app", or close variants after a product/growth analysis, the agent must create an implementation PR with production app code changes in the target repository.
- Do not satisfy that request with a proposal-only markdown PR. The CLI's proposal PR mode is only for explicit requests such as "make a proposal PR", "planning PR", "draft proposal", or scheduled proposal delivery.
- A PR that only adds `.openclaw/proposals/*.md`, docs, or markdown planning files is not a valid implementation PR unless the user explicitly requested a proposal-only artifact.
- For implementation PRs, the agent must inspect the app repo, create or reuse a branch, edit the relevant app files, run targeted checks where feasible, then open/update the PR. Use GitHub issue creation for tracking, but keep the PR focused on real app behavior.
- If the implementation cannot be completed because repo write access, branch access, or local checkout is unavailable, say that directly and do not create a placeholder markdown PR.

`openclaw setup` should reuse the existing `analyticscli setup` flow instead of redefining skill installation locally. That means shared skills such as `analyticscli-cli` and `analyticscli-ts-sdk` come from the canonical AnalyticsCLI installer.

## Customization Boundary

Treat this installed skill as vendor-managed and replaceable.
Agents should almost never edit this skill in-place for user- or project-specific customization, because future skill updates may overwrite local changes.
When the user wants custom behavior, create a separate companion skill or project-local customization skill instead, for example `openclaw-growth-custom`, and have that skill reference or layer on top of this one.
Only modify this skill directly when the change is intended as an upstream reusable fix for the canonical skill repository.

## Setup DX Rules

Setup should feel guided for a developer, not like a silent preflight dump.

- Root-cause policy: when connector setup fails for a user, do not hand out VPS-specific workaround commands as the final answer. Fix the reusable Growth Engineer/CLI/wizard so every future installer gets the corrected flow, then publish/sync the skill and ask the running agent instance to refetch it.
- Prefer auto-detection and direct fixes over asking the user to run generic commands.
- In chat, explain only what the user needs for the next step. Put provider details, scopes, and secret prompts in the wizard unless the user asks.
- Ask for the minimum missing value only; do not request issue/PR permissions unless artifact creation is enabled.
- For blockers, return one short next action first. Add detailed status, permissions, or URLs only when the user asks or the wizard needs that value.
- After each setup phase, summarize only the result and the next concrete action.
- Keep secrets out of prompts, repo files, logs, and command arguments; prefer host-agent secret storage or environment injection.
- Never ask the user to paste API keys, GitHub tokens, or App Store Connect `.p8` private-key contents into Discord, OpenClaw chat, Hermes chat, GitHub issues, PRs, or any shared transcript. Chat is not an appropriate secret transport.
- For secrets, give a secure host-terminal path: set env vars in the runtime shell, an agent secret store, a password manager injection flow, or the wizard-managed `~/.config/openclaw-growth/secrets.env` with `chmod 600`. Growth commands must load that env file automatically. For ASC `.p8`, prefer asking for the local file path to Apple's original downloaded file name `AuthKey_<KEY_ID>.p8`; do not rename the file because the wizard derives the key id from that name. Pasted `.p8` content is only a fallback. Store only `ASC_PRIVATE_KEY_PATH` and never echo the private key back.
- When SDK instrumentation is missing or weak, guide the developer through the `analyticscli-ts-sdk` setup path so analytics events become useful for later growth analysis.
- If AnalyticsCLI has no default project and multiple projects are visible, do not report that as a hard error. List the available projects, ask the user which one to use, persist the choice with `openclaw start --config openclaw.config.json --project <project_id>` or `analyticscli projects select <project_id>`, and then retry the setup/run.

During setup chat, keep the first answer short. The agent should not dump provider docs, permissions, status history, or troubleshooting unless the user asks for details.

Connector status questions:

- If the user asks whether connectors are connected, which connectors have access, or whether a specific app such as "Flashes" has all connectors, do not infer from memory, skill text, MCP config, or whether helper binaries exist.
- Run the deterministic status command from the active agent workspace:
  ```bash
  node scripts/openclaw-growth-status.mjs --config data/openclaw-growth-engineer/config.json --json
  ```
- The status command loads `~/.config/openclaw-growth/secrets.env`, runs live connector checks, and treats GitHub code access separately from GitHub issue/PR delivery.
- Do not require a single global GitHub repo for connector setup. GitHub is connected when auth/token is valid; choose or infer the repository per app/task later.
- Answer from that command only. If it cannot be run, say "I have not run a connector status check yet" and give the wizard command; do not say credentials are missing just because they are not visible in chat.
- Keep the answer short: say "Ja" only if every connector status is `connected`; otherwise list only the non-connected connector names and the status command's next action.
- The interval runner performs a connector health check at least every 6 hours by default (`schedule.connectorHealthCheckIntervalMinutes`, default `360`). If a configured connector is `partial`, `blocked`, or `unknown`, it writes a connector-health alert and sends it through the configured notification channel(s): agent chat outbox, Slack, generic webhook, or a custom command channel. Alert once per unhealthy incident/fingerprint, then suppress repeats until the connector recovers or the unhealthy fingerprint changes. Discord is only one possible command/webhook channel, not the default assumption.

Retention reliability:

- Treat D1/D3/D7 retention as an identity-quality-sensitive metric, not as an unconditional product fact.
- Before making strong retention claims, inspect the `analyticscli retention` response `quality.reliability`, stable identity share, and warnings.
- `analyticscli retention` defaults to `--identity-quality stable`. This excludes ephemeral/unknown SDK identities so consent-gated users without persistent identity do not create misleading multi-day retention noise.
- Use `--identity-quality all` only as an explicit diagnostic comparison. Do not treat all-identity D1/D3/D7 as product truth when stable identity share is low.
- If retention reliability is `low` or `unknown`, say the metric may be undercounted because some SDK sessions/users do not have persistent identity. Recommend verifying SDK identity persistence before prioritizing major retention work from D1/D7 alone.
- Do not filter silently. If using stable-only retention, disclose that ephemeral/unknown identities were excluded and compare the remaining cohort size.
- Product recommendations can still mention weak retention, but phrase it as "appears low" when reliability is weak and pair it with an instrumentation/persistence action.

AnalyticsCLI product feedback:

- Use Sentry/GlitchTip for production exceptions, crashes, hangs, and backend stack traces.
- Use `analyticscli feedback submit` for feedback to the AnalyticsCLI SaaS owner about AnalyticsCLI itself: missing features, broken CLI/API/dashboard behavior, confusing errors, poor docs, or workflow friction.
- Do not confuse this with tenant-owned end-user feedback collected by the AnalyticsCLI feedback feature. Tenant feedback is a product signal for the tenant's app; `analyticscli feedback submit` is operator feedback about AnalyticsCLI/OpenClaw tooling.
- When an AnalyticsCLI/OpenClaw/SDK command, endpoint, or documented workflow fails, first try to refetch or update the relevant current version before declaring the behavior broken:
  - Growth Engineer: `npx -y clawhub --no-input --dir skills update growth-engineer --force` or reinstall from the canonical skill source, then rerun the workflow.
  - AnalyticsCLI CLI: update `@analyticscli/cli`, verify `analyticscli --help`, then rerun the exact failing command.
  - AnalyticsCLI SDK: upgrade `@analyticscli/sdk` within the supported range and rerun the minimal host-app or test repro.
- If no newer version is available, the update cannot be applied, or the newest version still fails, submit a bounded `analyticscli feedback submit` report if feedback service credentials are configured. Include installed versions checked, command/endpoint, project id when safe, sanitized payload shape, status code, error body, request id if present, expected behavior, workaround used, and whether an update was attempted.
- Example:
  ```bash
  analyticscli feedback submit --category bug --message "Retention query returns HTTP 500 for minimal payload" --context "endpoint=/v1/query/retention project=<project_id> anchorEvent=onboarding:start days=[1] last=7d identityQuality=all updateAttempt=cli@preview+skill@latest workaround=funnel+RevenueCat requestId=<request_id_if_present>"
  ```

Growth operating plan:

- Goal: increase durable product value and business output by reducing churn, increasing MRR/LTV, improving acquisition quality, optimizing funnels/paywalls/onboarding/activation, and creating, changing, or deleting features only when the data supports it.
- Data-first rule: gather all connected sources before recommendations whenever feasible: AnalyticsCLI events/funnels/retention, RevenueCat subscriptions/churn/revenue, Paddle billing metrics, SEO/GSC/Bing Webmaster/DataForSEO acquisition signals, Sentry crashes/performance, App Store Connect store/reviews/builds, GitHub code/release context, feedback, and any configured social/marketing sources.
- Long analysis rule: prefer a longer cross-source investigation over fast generic advice. Look for correlations across connectors, for example Sentry regressions after a release, RevenueCat churn after a paywall change, App Store review themes matching funnel drop-offs, or marketing traffic that brings low-retention users.
- Usage-choice rule: setup must ask how the user wants to use the tool before scheduling it. At minimum offer production autopilot, advisory-only summaries, and manual reports. Then ask whether the default cadence plan is acceptable; if not, collect/edit what should happen daily, weekly, monthly, every 3 months, every 6 months, and yearly.
- GitHub production-version rule: always determine which code version is production before mapping data to files. Check repo default branch, release branches/tags, app version/build metadata, deployment workflows, App Store Connect build/version, Sentry release tags, and AnalyticsCLI appVersion. If they disagree, state the uncertainty and avoid overconfident file blame.
- Action rule: every recommendation should include a concrete user/operator plan: what to do, where to do it, what data supports it, how to verify it, and which KPI should move. For implementation requests, create real code changes, not proposal-only docs.
- Cadence for the user:
  - Daily default: analyze every configured project for critical production or business-health issues: Sentry/GlitchTip crashes/errors, ASC crash totals, failed releases, onboarding or purchase drop-offs, zero-conversion days, missing buyers, very low active users, or other severe analytics anomalies. Always do root-cause analysis with exact evidence, recent code/release changes, and a concrete fix/debugging step. Prefer a GitHub issue or draft PR when write access is configured; otherwise hand off via OpenClaw chat. Do not generate generic growth ideas on a daily-only run.
  - Weekly default: create an executive product and growth summary across all configured projects, connectors, recent releases, code changes, revenue, activation, retention, reviews, and stability. Pick one to three high-confidence improvements with KPI target and verification plan.
  - Monthly default: compare all configured projects month-over-month: MRR, trial conversion, churn, acquisition quality, store/listing conversion, retention, review themes, feature usage, crash totals, and codebase changes. Decide what to build, change, delete, or instrument next.
  - Every 3 months default: revisit positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, and major funnel bets. Look for structural constraints and durable opportunities.
  - Every 6 months default: audit connector coverage, SDK instrumentation, event taxonomy, data reliability, memory, growth loops, and whether product/marketing strategy still matches the best users.
  - Yearly default: reset strategy from all evidence: market/channel fit, monetization model, retention ceiling, product scope, and whether to double down, reposition, rebuild, or sunset major surfaces/features.
- Memory and change-correlation rule: inspect persisted OpenClaw state, prior summaries, release/build metadata, Git history/recent commits where available, and previously created issues/PRs before assigning causality. Prefer explanations that connect "what changed" to "what moved" across data sources.
- Marketing/social rule: if social or marketing automation exists, treat it as a growth source when data is available. Ask for or configure account analytics case-by-case (TikTok, Instagram, ads, creator automation, landing pages, UTM/source data), then connect those signals back to acquisition quality, activation, retention, churn, and revenue instead of optimizing impressions alone.
- Social summary rule: whenever the Growth Engineer completes a meaningful run, creates a finding, or detects connector/production-health attention, send a short summary through configured social/chat channels (OpenClaw chat, Slack, Discord command channel, generic webhook, or equivalent). Do not include secrets. Respect `notifications.growthRun.enabled=false`, `notifications.connectorHealth.enabled=false`, or a direct user request to stop social summaries.
- Chart rule: when a result has meaningful numeric evidence, try to render a simple chart using the bundled Matplotlib script (`scripts/openclaw-growth-charts.py`). Prefer a bar/column chart for current-vs-baseline metrics and use other chart types only when they genuinely make the signal easier to understand. Attach generated PNGs to GitHub issues/PRs when GitHub artifact delivery is active. For chat/social/webhook delivery, include the chart manifest and local PNG attachment metadata so OpenClaw/Hermes can attach the images when the target channel supports file uploads.

Production crash and ASC growth monitoring:

- Run the production health loop every day for every public, analytics-accessible app. Apps that are not public yet, not eligible for ASC API-key analytics reports, or returning ASC analytics-report 403s should be marked `not_public_or_not_analytics_ready` and skipped without calling them broken.
- Daily crash check: prefer total production crashes from ASC App Usage breakdowns and Sentry production issue/event counts. Use ASC `crashRate` only as a supporting ratio, never as the only stability signal. TestFlight crashes are out of scope unless the user explicitly asks.
- Any non-zero production crash count should trigger a short user notification through the configured agent chat/social delivery channel. The notification should name the app, date range, total crash count, affected app version when available, Sentry issue count/users when connected, and the recommended next action.
- If GitHub issue/PR write access is configured through the agent's GitHub API connection, automatically create the tracking GitHub issue or implementation PR for production crashes and high-confidence growth findings. Only skip GitHub artifact creation when `actions.disableAutoCreateGitHubArtifacts = true`, GitHub write access is unavailable, or the finding is too low-confidence to be useful.
- Correlate ASC total crashes with Sentry production data before recommending growth pushes: app version/build, release date, top Sentry issue, affected users/events, funnel step, paywall/purchase path, and recent code changes. If ASC and Sentry disagree, report both and say which connector is more complete for the app.
- Sentry-compatible crash monitoring is multi-account. Do not assume one global Sentry org/project. Support `sources.sentry.accounts[]` with separate `baseUrl`, `tokenEnv`, `org`, `projects[]`, and `environment` entries, for example Sentry Cloud plus a self-hosted GlitchTip instance with different projects.
- Daily ASC acquisition check: refresh and parse API-key ASC batch reports in the background when ASC is configured: App Analytics report instances, Sales and Trends reports when `ASC_VENDOR_NUMBER` is available, plus ratings/reviews/build/TestFlight/status surfaces. Collect all available metrics, including but not limited to `units`, `redownloads`, `conversionRate`, `crashRate`, source page views, app usage, updates, app opens, subscription state, and total crashes. Treat ASC source data as source-level product page views, not source-level download units unless the CLI exposes a true source-download measure.
- Do not require ASC web auth for setup, health checks, or normal scheduled runs. Experimental `asc web analytics ...` may be used only as an exception when a specific needed metric cannot be retrieved through documented API-key reports. In that case, ask the user before prompting for `ASC_WEB_APPLE_ID`, explain that the Apple Account web session can expire quickly on a VPS, and continue using API-key ASC reports if the user declines or the session expires.
- Weekly growth review: compare units/downloads, redownloads, conversion rate, source mix, AnalyticsCLI activation/funnels/retention, Sentry stability, RevenueCat monetization, reviews, and recent releases. Turn the strongest cross-source pattern into one implementation-ready Handlungsempfehlung.
- Monthly growth review: compare month-over-month units, conversion, source quality, reviews, retention, churn, crash totals, and production versions. Decide which acquisition channel, store listing element, onboarding step, paywall, or feature should be built, changed, or deleted next.
- Handlungsempfehlungen must be source-aware: Search means ASO/keywords/screenshots; Web Referrer means landing pages, UTMs, creator/SEO traffic, and deep links; Browse means category positioning and visual conversion; App Referrer means cross-promotion and in-app referral paths. Always verify the recommendation against units/conversion and downstream activation, not traffic volume alone.
- For financial data, keep it secondary unless the user asks. Prioritize production crashes, downloads/units, redownloads, conversion, source traffic, activation, retention, and qualitative store/user feedback.

Hard override for Growth Engineer connector questions:

If the user says any of these or close variants, apply this override before any generic OpenClaw, AnalyticsCLI, MCP, messaging-channel, or env-var connector knowledge:

- "Growth Engineer connectors"
- "analyticscli connectors"
- "AI Product Manager connectors"
- "I want to setup connectors" in the context of this skill
- "which connectors can I set up" in the context of this skill
- "how do I set them up" after asking about this skill's connectors

Answer only with this shape:

```text
Growth Engineer connectors:
- AnalyticsCLI baseline: product analytics plus built-in feedback summaries
- GitHub code access: repo context and issue/PR delivery
- RevenueCat monetization: subscriptions, trials, revenue, and churn
- Sentry-compatible crash monitoring: Sentry Cloud and/or self-hosted GlitchTip via multi-account Sentry config
- Coolify deployment monitoring: failed deploys, unhealthy resources, servers, and production health-check gaps
- ASC / App Store Connect CLI: store analytics, reviews/ratings, builds/TestFlight/release context, downloads/units, conversion, source traffic, app usage, subscriptions, purchases, and crash totals when configured

Run the wizard from the active agent workspace:
```

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

Then add only: "Select the connectors in the wizard. Secrets stay in the terminal."

Do not list Discord, Telegram, WhatsApp, Slack, Matrix, OpenAI service connectors, MCP servers, browser connectors, feedback endpoints, raw environment variables, token scopes, verification commands, or provider URLs in the initial answer. Do not list GlitchTip as a separate connector; it is a Sentry-compatible account under Sentry. Do not list Feedback as a separate primary connector; feedback is part of AnalyticsCLI when available or a custom extra source when explicitly configured. Do not present ASC as optional/partial after it is connected; when configured, use every available read-only App Store Connect signal. Those details belong inside the wizard or in a direct follow-up answer.


If the user asks a broad question such as "how do I setup everything", answer with only:

```text
Available connectors:
- AnalyticsCLI baseline: product analytics plus built-in feedback summaries
- GitHub code access: repo context and issue/PR delivery
- RevenueCat monetization: subscriptions, trials, revenue, and churn
- Sentry-compatible crash monitoring: Sentry Cloud and/or self-hosted GlitchTip via multi-account Sentry config
- Coolify deployment monitoring: failed deploys, unhealthy resources, servers, and production health-check gaps
- ASC / App Store Connect CLI: store analytics, reviews/ratings, builds/TestFlight/release context, downloads/units, conversion, source traffic, app usage, subscriptions, purchases, and crash totals when configured

Run the wizard from the active agent workspace:
```

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

Then add one sentence: "The wizard will ask for the selected connectors and any secrets in the local terminal only."

If the user asks which connectors exist, list only the connector names and one short purpose each. Treat Sentry Cloud and GlitchTip as Sentry-compatible accounts under one Sentry connector. Treat AnalyticsCLI feedback as part of AnalyticsCLI unless the user asks for custom extra sources. Do not include setup URLs, permissions, token scopes, status history, or validation output in that initial answer.

If the user already names specific connectors, still prefer the checkbox wizard unless they explicitly ask for a non-interactive command. For explicit connector setup, use one copy-paste command from the active agent workspace:

```bash
npx -y @analyticscli/growth-engineer wizard --connectors analytics,github,revenuecat,paddle,seo,sentry,coolify,asc
```

Use only the connectors the user accepted. The wizard owns provider-specific instructions, local-terminal secret prompts, helper setup, and smoke tests. Chat should only summarize results after the wizard finishes or when the user asks.

Do not ask for `ASC_APP_ID` during initial setup. ASC summaries default to all accessible App Store Connect apps. A single app ID is only an optional explicit filter later.

Growth Engineer connectors are local CLI/secrets-backed sources, not chat/MCP tools. ASC/App Store Connect is not expected to appear as a loaded chat tool. If the user asks whether ASC/App Store Connect analytics access is available, never inspect loaded tools and never answer "no" because no App Store Connect tool is callable. Check Growth Engineer status from the active workspace with `node scripts/openclaw-growth-status.mjs --config <config> --json --only-connectors asc` or run `node scripts/openclaw-growth-runner.mjs --config <config> --state <state>`. If ASC status/setup reports pass, connected, healthy, or the wizard just finished ASC connector setup successfully, answer exactly: "Yes. ASC analytics is connected through Growth Engineer local asc CLI/API-key setup."

Connection setup requests are not satisfied by a successful product-manager run. If the user asks to set up `asc`, App Store Connect, RevenueCat, Paddle, SEO/GSC/Bing Webmaster/DataForSEO, Sentry, Coolify, GitHub, or codebase access, point them to the wizard command above and keep any extra explanation out of chat unless requested.

For Paddle setup, the wizard must explain the account-level metrics model: do not ask for or hard-code one Paddle product/project. The user should create a live API key at `https://vendors.paddle.com/authentication-v2` with `metrics.read` permission.

For SEO setup, the wizard must not hard-code one Search Console property by default. Leave `GSC_SITE_URL` empty to query all verified properties visible to the account; set it only when the user explicitly wants to restrict analysis. Bing Webmaster is optional supplemental indexing/sitemap evidence; store `BING_WEBMASTER_API_KEY` and `BING_WEBMASTER_SITE_URL` only in the host terminal/secret file. Explain Search Console (`https://search.google.com/search-console`), service-account setup (`https://console.cloud.google.com/iam-admin/serviceaccounts`), Bing Webmaster API (`https://www.bing.com/webmasters/`), and optional paid DataForSEO (`https://app.dataforseo.com/api-dashboard`) step by step.

Reference URLs for the wizard or for explicit follow-up questions:

- RevenueCat dashboard/API keys: https://app.revenuecat.com/
- RevenueCat API key docs: https://www.revenuecat.com/docs/projects/authentication
- RevenueCat MCP setup docs: https://www.revenuecat.com/docs/tools/mcp/setup
- App Store Connect API keys: https://appstoreconnect.apple.com/access/integrations/api
- Coolify API tokens: open the hosted Coolify base URL and go to `/security/api-tokens`, for example `https://coolify.wotaso.com/security/api-tokens`
- App Store Connect users/access: https://appstoreconnect.apple.com/access/users
- App Store Connect individual API key profile: https://appstoreconnect.apple.com/account
- GitHub token creation: https://github.com/settings/tokens/new
- GitHub CLI auth docs: https://cli.github.com/manual/gh_auth_login
- GitHub CLI install docs: https://github.com/cli/cli#installation
- GitHub repo settings/apps, for repository-level access checks: https://github.com/settings/installations

Safe secret handoff rules:

- Do not ask the user to send secrets through Discord/OpenClaw chat. It is not safe enough for API keys, GitHub tokens, or `.p8` private keys because messages can be retained, logged, indexed, screenshotted, or visible to other bots/users.
- Ask the user to set secrets directly on the host where OpenClaw runs, then reply only with "done" or the non-sensitive file path/variable name.
- Good terminal pattern for env secrets:
  ```bash
  install -d -m 700 ~/.config/openclaw-growth
  umask 077
  $EDITOR ~/.config/openclaw-growth/secrets.env
  # add lines like:
  # REVENUECAT_API_KEY=...
  # ASC_KEY_ID=...
  # ASC_ISSUER_ID=...
  # ASC_PRIVATE_KEY_PATH=/home/lo/.config/openclaw-growth/AuthKey_XXXX.p8
  chmod 600 ~/.config/openclaw-growth/secrets.env
  ```
- Good `.p8` pattern: keep Apple's original downloaded file name `AuthKey_<KEY_ID>.p8`, then paste only that local file path into the terminal wizard. Do not rename the file; the wizard derives `ASC_KEY_ID` / `ASC_BOOTSTRAP_KEY_ID` from the file name. Pasting the full `.p8` content is only a fallback when the file is not available on the host.
- OpenClaw Growth commands load the wizard-managed env file automatically; never put secrets in command-line args.

## Mandatory Baseline

Before autopilot runs, these are non-negotiable:

- `analyticscli` CLI available
- target repo checkout readable via `project.repoRoot`
- a writable `openclaw.config.json`
- `sources.analytics` enabled

GitHub connection is strongly recommended for serious analysis, even when GitHub delivery is disabled.
Treat readable GitHub repo access as very important because analytics signals become much more actionable when OpenClaw can map funnels, events, crashes, revenue signals, and feedback back to actual code areas.
Without repo context, findings stay generic and file/module hypotheses are lower confidence.

When the user says they want to connect GitHub or the codebase, do not ask them to manually send a repo path first.
Reference and use the dedicated ClawHub GitHub skill when available: `steipete/github` (`https://clawhub.ai/steipete/github`).
It is a `gh` CLI helper skill for issues, PRs, runs, and advanced `gh api` queries, so it should own GitHub command patterns while this skill owns product/growth analysis.
Install or verify it before deeper GitHub setup when OpenClaw can manage skills:

```bash
openclaw skills install steipete/github
# or
npx clawhub@latest install github
```

GitHub setup must go through the connector wizard's classic-token scope guide, not a raw `gh auth login` flow. The wizard should:

1. Detect repo root/remote when useful.
2. Show the classic token URL: `https://github.com/settings/tokens/new`.
3. Explain the relevant scopes briefly: `public_repo`, `repo`, and optional `workflow`.
4. Store `GITHUB_TOKEN` locally when the user pastes it into the terminal wizard.
5. Install `gh` locally only as a helper binary; do not use GitHub CLI OAuth as the default credential path because it can request broad repository/workflow permissions.
6. Tell the user they can rerun the wizard later to change GitHub permissions.

Use least privilege:

- public repo context only: `public_repo`
- private repo access or private issue/PR work: `repo` (classic tokens make this broad)
- workflow permission: add `workflow` only when the user explicitly wants OpenClaw to edit GitHub Actions workflow files
- avoid packages, admin/org, hooks, gist, user, delete_repo, enterprise, codespace, and copilot scopes unless explicitly needed

## Dependency Refresh Protocol

Run this protocol at the start of every setup/start/run request, and whenever the user asks to fetch, update, upgrade, or reinstall this skill.
Do not stop after saying the skill was fetched from ClawHub.
The job is not done until the npm binary and companion skills are updated and verified.
If the user reports `analyticscli: command not found` in their own terminal, treat that as unresolved even if `analyticscli` works inside OpenClaw's child process.
Child processes cannot mutate the PATH of an already-open parent terminal.

Host update boundary:

- OpenClaw and Hermes host instances must update the Growth Engineer runtime from the installed skill distribution only.
- Do not tell OpenClaw or Hermes hosts to `git fetch`, `git checkout`, `git pull`, or copy runtime files from private monorepo/app branches as an upgrade path.
- Never send OpenClaw or Hermes a GitHub PR/branch link as something to pull, test, or use for runtime upgrade. PR links are for human review only.
- When notifying OpenClaw or Hermes about an unreleased fix, say only that they should wait for the ClawHub/npm publication and then update automatically from that distribution.
- Private repo branches may be used to develop and validate a new Growth Engineer release, but the host-facing update instruction must be to publish/refresh the canonical skill distribution first, then update via ClawHub for OpenClaw or the shared Growth Engineer skill install path for Hermes.
- If a previous host instruction used a private repo branch or manual runtime copy, correct it by reverting that host-side override and refreshing from the canonical skill source.

1. Refresh this ClawHub skill:
   ```bash
   npx -y clawhub install growth-engineer
   ```
2. Refresh the AnalyticsCLI agent skill only when it can run non-interactively:
   ```bash
   npx -y skills add wotaso/analyticscli-skills --skill analyticscli-cli
   ```
   If this command asks an interactive agent-selection question, stop that command and continue with the npm package install instead of blocking.
   Do not describe an interactive `skills add` prompt as a successful refresh.
3. Install or update the npm package that provides the `analyticscli` binary:
   ```bash
   npm install -g @analyticscli/cli
   ```
4. If global npm install fails with a permissions error, use the bundled helper from the installed skill root:
   ```bash
   bash skills/openclaw-growth-engineer/scripts/install-analyticscli-cli.sh
   ```
5. Verify and report the exact binary path:
   ```bash
   command -v analyticscli
   analyticscli --help
   ```

If `analyticscli: command not found` still happens, do not claim setup is complete.
Find the user-local binary and fix PATH for future shells yourself; do not bounce this step back to the user:

```bash
export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"
command -v analyticscli || ls -l "$HOME/.local/bin/analyticscli" "$HOME/.local/analyticscli-npm/bin/analyticscli"
```

If the binary exists under `$HOME/.local/bin` or `$HOME/.local/analyticscli-npm/bin`, make future shells pick it up. Update all common shell startup files idempotently, then verify from a fresh shell:

```bash
for f in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.zprofile"; do
  touch "$f"
  grep -Fq 'export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"' "$f" ||
    printf '\n# AnalyticsCLI CLI user-local npm bin\nexport PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"\n' >> "$f"
done
bash -lc 'source "$HOME/.bashrc" 2>/dev/null || true; source "$HOME/.profile" 2>/dev/null || true; command -v analyticscli && analyticscli --help >/dev/null'
```

Child processes cannot mutate an already-open parent terminal. Say that only as residual context after you have already updated profile files and verified a fresh shell. Do not say "analyticscli is fixed" unless this exact command succeeds in the same command context you control:

```bash
command -v analyticscli && analyticscli --help >/dev/null
```

## AnalyticsCLI CLI Install Protocol

Before any setup, preflight, start, or run path tries to execute `analyticscli`, make sure the npm package is installed and current.
If the user reports `analyticscli: command not found`, run the Dependency Refresh Protocol before any other action.

The package name is `@analyticscli/cli`; the installed binary name is `analyticscli`.
Do not search npm for `analyticscli` or `analyticsscli`.

Use this exact install/update command:

```bash
npm install -g @analyticscli/cli
```

Then verify:

```bash
command -v analyticscli
analyticscli --help
```

If global npm installs are blocked on a VPS, use the bundled helper from the installed skill root:

```bash
bash skills/openclaw-growth-engineer/scripts/install-analyticscli-cli.sh
```

The helper falls back to a user-local npm prefix at `~/.local` when global install fails with permissions errors, prepends `~/.local/bin` for the current run, and prints a PATH hint if the shell needs it.
It must also update common shell profile files and verify that a fresh shell can resolve `analyticscli`.
Only ask the user for help if both direct npm install and the bundled helper fail with a concrete permission, missing `npm`, or network error.

## Delivery Modes

The CLI can write proposals to one or more targets:

- `deliveries.openclawChat.enabled = true`: write `.openclaw/chat/latest.md` and `.openclaw/chat/latest.json` as local outbox artifacts. This is not an external human notification by itself.
- Real user notifications require a successful external channel such as native OpenClaw cron delivery, `deliveries.command`, Slack webhook, or generic webhook. OpenClaw cron delivery defaults to `automation.openclawCron.delivery.channel = "last"` so it uses the chat/social channel already connected to that OpenClaw instance, whether that is Discord, Slack, Telegram, WhatsApp, or another supported channel. If only `openclawChat` is configured, connector-health alerts must report: `Alert written locally, but no external notification channel configured.`
- `deliveries.github.mode = "issue"` with `deliveries.github.autoCreate = true`: create implementation-ready GitHub issues
- `deliveries.github.mode = "pull_request"` with `deliveries.github.autoCreate = true`: create proposal-only draft PRs that add `.openclaw/proposals/...md` proposal files to the repo. Use this only for explicit proposal delivery, not when the user asks OpenClaw to implement changes.

Use issue mode when:

- you want backlog-first planning
- engineering should pick up and implement later

Use pull-request mode when:

- you want every proposal anchored in a branch and reviewable artifact
- you want the requested changes written down inside the repository immediately

## Connector Model

Built-in channels:

- `analytics`
- `revenuecat`
- `sentry`
- `feedback`
  default command path: `analyticscli feedback summary --format json`
  default cursor behavior: auto-bounded with `--last 30d` on first run, then `--since <lastCollectedAt>` on later runs unless the command already sets `--since`, `--until`, or `--last`

Additional connectors:

- configure `sources.extra[]`
- each extra connector can use `mode=file` or `mode=command`
- preferred output is shared `signals[]`
- crash-style tools may use `issues[]`
- feedback-style tools may use `items[]`

For iOS/macOS products, explicitly ask whether the user wants to connect the `asc` CLI and the related App Store Connect agent skill. ASC means App Store Connect, not analytics.
Never abbreviate this as just "analytics" in status messages, because it is easy to confuse with AnalyticsCLI.
Say "ASC / App Store Connect" when referring to `asc`, and "AnalyticsCLI baseline" when referring to the AnalyticsCLI project.
An AnalyticsCLI auth check, selected AnalyticsCLI project, or successful PM run does not prove that ASC is connected.
Only say ASC is connected after `asc` auth is configured, accessible App Store Connect apps are discovered or an explicit app filter is set, and a read-only ASC command/export has succeeded.
Frame ASC as an App Store Connect connector, not as a synonym for analytics. AnalyticsCLI remains the product analytics baseline; when ASC is configured, App Store Connect API-key batch reports are fully used for discovery, downloads/units, redownloads, conversion, source traffic, app usage, purchases, subscriptions, ratings, reviews, release, build, TestFlight, and crash-total context when those surfaces are available.
Do not request ASC permissions for release management, TestFlight management, pricing changes, user management, or other write/admin workflows when the user only selected read-only App Store Connect reporting.
Reference the ASC skill pack as the canonical companion skills for `asc`: `rorkai/app-store-connect-cli-skills` (`https://github.com/rorkai/app-store-connect-cli-skills`).
Use it for `asc` command syntax, auth, pagination, ID resolution, and App Store Connect workflows; for read-only App Store Connect reporting prefer the least invasive skills such as `asc-cli-usage` and `asc-id-resolver`, not release/submission/signing skills.
Install or refresh it when the user selects ASC:

```bash
npx skills add rorkai/app-store-connect-cli-skills
```

ASC setup guidance:

- Ask: "Soll ASC CLI fuer App Store Connect verbunden werden?"
- Send the user to exactly this page to create the key: https://appstoreconnect.apple.com/access/integrations/api.
- Say ASC setup uses two API keys: a Reports key with `Sales and Reports` for ongoing Growth Engineer downloads, plus a temporary Setup key with `Admin` used once to create the initial App Analytics report request. `Finance` or `Admin` also works for ongoing report downloads, but prefer `Sales and Reports` after bootstrap. Add `Customer Support` for App Store ratings/review text, `Developer` for builds/TestFlight/delivery status, and `App Manager` only when app metadata, pricing, or release settings are needed.
- Tell the user to copy `ASC_ISSUER_ID` from the API keys page, download both `.p8` files, keep Apple's original `AuthKey_<KEY_ID>.p8` file names, and paste the local file paths into the terminal wizard. Do not tell them to rename the `.p8`; the wizard derives `ASC_KEY_ID` and `ASC_BOOTSTRAP_KEY_ID` from the file names.
- Store only env vars/secrets: `ASC_KEY_ID`, `ASC_ISSUER_ID`, and `ASC_PRIVATE_KEY_PATH`; the wizard can still create the `.p8` file from validated pasted terminal content as a fallback. Never commit the `.p8` private key.
- The Setup Admin key is not saved to `secrets.env`. The wizard keeps the temporary secure `.p8` copy on the host and tells the user to revoke the Admin key in App Store Connect after setup.
- Do not ask for `ASC_APP_ID` upfront. After auth succeeds, ASC should use all accessible apps by default. Store an app filter only if the user explicitly asks to scope ASC to one app.
- After the key is present, run one read-only API-key `asc` smoke test before marking ASC connected. Do not check `asc web auth` and do not force a target app selection; default ASC analysis covers all accessible apps.
- Prefer `asc auth login` when the local `asc` CLI supports keychain storage; otherwise use runtime env injection.

RevenueCat setup guidance:

- Ask: "Soll RevenueCat fuer Monetization-/Subscription-Daten verbunden werden?"
- For SDK instrumentation, use the public app-specific SDK key only in the app.
- For server-side growth summaries, request a RevenueCat secret API key stored server-side only. Tell the user to generate a new secret API key named `analyticscli`, choose API version 2, and set Charts metrics, Customer information, and Project configuration permissions to read.
- Tell the user to open https://app.revenuecat.com/, select the app, then choose "Apps & providers" in the sidebar and click "API keys". Do not ask for a RevenueCat project id just to build a deep link.

Sentry setup guidance:

- Ask: "Soll Sentry fuer Crash-, Error- und Performance-Signale verbunden werden?"
- Use the direct Sentry API exporter as the canonical growth source: `node scripts/export-sentry-summary.mjs`.
- The wizard should configure one or more Sentry-compatible accounts directly. For each account, ask for label, `baseUrl`, `tokenEnv`, token, `org`, `environment`, and optional comma-separated `projects[]`. Do not ask for a single global `SENTRY_PROJECT`; defer project scope to app/repo/release context unless the user provides known fixed projects for that account. Use this for Sentry Cloud plus self-hosted GlitchTip with separate tokens and projects.
- For multiple crash accounts, configure `sources.sentry.accounts[]` instead of overwriting one global account. Each account can define its own `baseUrl`, `tokenEnv`, `org`, `projects[]`, and `environment`.
- Tell the user to create a Sentry auth token at https://sentry.io/settings/account/api/auth-tokens/ with read-only API scopes `org:read`, `project:read`, and `event:read`.
- Configure optional Sentry MCP through `@sentry/mcp-server@latest` when `npx` and `SENTRY_AUTH_TOKEN` are available, but do not ask for broader write scopes unless the user explicitly wants Sentry mutation workflows.
- Mark Sentry connected only after the auth check and exporter smoke test pass. Do not infer Sentry access from a token being present.
- When Sentry is connected, always correlate top crashes/errors across every configured Sentry-compatible account with AnalyticsCLI funnel steps, RevenueCat purchase/churn movement, ASC release/build metadata, and GitHub production code version before recommending growth experiments.

Coolify setup guidance:

- Use the direct Coolify API exporter through the standalone CLI as the canonical deployment/hosting source: `npx -y @analyticscli/growth-engineer exporters coolify-summary`.
- Ask for the Coolify base URL and token only in the local terminal wizard. For Wotaso-hosted Coolify, the token page is `https://coolify.wotaso.com/security/api-tokens`.
- Tell the user to open the Coolify dashboard, choose `Keys & Tokens` in the sidebar, open `API tokens`, and create an API key/token with read-only permissions.
- Persist non-secret config in `sources.coolify` with `enabled=true`, `mode=command`, `command=npx -y @analyticscli/growth-engineer exporters coolify-summary --config <config>`, `baseUrl`, and `tokenEnv`.
- Persist the secret only as `COOLIFY_API_TOKEN`; keep `COOLIFY_BASE_URL` non-secret but allow it in the local secrets file for convenience.
- The daily guardrail must read Coolify when configured and correlate failed deploys, unhealthy resources, disabled/missing health checks, and server/resource anomalies with Sentry errors, AnalyticsCLI traffic/conversion drops, and recent code changes.
- Mark Coolify connected only after the auth check and exporter smoke test pass. Do not infer Coolify access from a token being present.

Mobile-focused extra source examples:

- `firebase-crashlytics`
- `app-store-reviews`
- `play-console`
- `stripe`
- `adapty`
- `superwall`

Do not list GlitchTip or ASC CLI as mobile extras in setup answers. GlitchTip belongs under the Sentry-compatible connector when it exposes the Sentry API; ASC CLI is the App Store Connect connector.

## Feedback Rules

- Prefer tenant-owned backend/proxy submission for mobile apps
- Do not put privileged feedback secrets directly into shipped app binaries unless they are intentionally public and app-scoped
- Always include a stable `locationId` for feedback collection points
- Always include a human-readable `originName` for where the feedback originated in the product
- Use human-meaningful, code-stable location ids such as `onboarding/paywall`, `settings/restore`, `profile/delete_account`
- The SDK should track lightweight feedback submission events without sending raw feedback text into analytics events

## Feedback Source Memory

- The CLI should persist per-source cursor state, especially for the built-in `feedback` source.
- Default behavior must avoid accidental historical re-fetches.
- If `sources.feedback.cursorMode = "auto_since_last_fetch"` and the command has no explicit time flags, the CLI should:
  first run: append `--last <initialLookback>` (default `30d`)
  later runs: append `--since <lastCollectedAt>`
- If the user intentionally wants older history again, that must be a conscious action:
  either set explicit `--last` / `--since` / `--until` in the command
  or reset the stored cursor state

## Startup Protocol

When the user says "start", "run", or "kick off" the skill:

1. Run the Dependency Refresh Protocol first. It must update this skill, the `analyticscli-cli` skill when available, and the `@analyticscli/cli` npm package, then verify `command -v analyticscli`.
2. If setup is incomplete, connectors are not selected, AnalyticsCLI auth is missing/invalid, or the host is Hermes, route the user to the bundled wizard before any preflight/start run.
   - In Hermes chat/Discord/non-interactive terminals, do not run the wizard yourself. Show the full command below and tell the user to paste it into the VPS/host shell.
   - Only run this command yourself when you are already operating inside an interactive user terminal that can safely receive secret input outside chat.
   ```bash
   npx -y @analyticscli/growth-engineer wizard --connectors
   ```
   Do not tell the user to run `analyticscli login` as the next step; the wizard owns AnalyticsCLI token collection and retesting.
3. Prefer the CLI entrypoint after the wizard/config exists:
   - `growth-engineer setup --config openclaw.config.json`
   - this should initialize config and install the shared AnalyticsCLI skills via the canonical AnalyticsCLI setup flow
4. Then run:
   - `growth-engineer start --config openclaw.config.json`
5. In this monorepo, use the workspace dev entrypoint when `openclaw` is not installed globally:
   - `pnpm --filter @analyticscli/growth-engineer dev start --repo-root <repo-root>`
6. Run portable checks first when setup is incomplete:
   - `command -v analyticscli`
   - `analyticscli projects list`
   - detect `project.githubRepo` from git remote when possible
   - verify readable GitHub repo access when available so analytics findings can be mapped to code
   - verify GitHub issue/PR write scopes only if GitHub delivery is enabled
   - if the user already pasted an AnalyticsCLI token candidate, use it immediately for the check/start attempt instead of asking a follow-up token question first
7. If preflight fails, return only a concrete blocker checklist, and for AnalyticsCLI auth blockers point back to the wizard command, not `analyticscli login`
8. If preflight passes, continue with `openclaw run --config openclaw.config.json`

When the user asks for analysis only:
- run the CLI
- summarize the generated drafts/signals in natural language

When the user asks OpenClaw to implement:
- run the CLI if fresh signals/proposals are needed
- inspect the generated issue drafts
- then implement with OpenClaw itself, not by delegating implementation to the CLI

## Proposal Strategy

The CLI config should expose `strategy.proposalMode`:

- `mandatory`: only strongest, clearly evidenced fixes and must-have requests
- `balanced`: default mix of necessary fixes and moderate product ideas
- `creative`: still evidence-led, but more willing to suggest bolder experiments or feature ideas

Use the legacy bootstrap-and-copy runtime only when the standalone CLI is unavailable in the target workspace.

## Output Rules

- max 3-5 proposals per pass
- each proposal must include measurable impact and file/module hypotheses
- each proposal must say what should change
- low-confidence findings must be marked explicitly
- when GitHub delivery is disabled, proposals should still be fully usable via the OpenClaw chat outbox

## Required Secrets

- `GITHUB_TOKEN`
  - strongly recommended with readable repo/code access for code-aware analysis
  - required with write scopes only when GitHub issue or pull-request delivery is enabled
  - use the classic token page at `https://github.com/settings/tokens/new`; use `public_repo` for public repos, `repo` for private repo access, and `workflow` only for GitHub Actions workflow edits
  - issue mode: add `Issues: Read/Write` only when issue creation is enabled
  - pull-request mode: add `Pull requests: Read/Write` and `Contents: Read/Write` only when draft PR creation is enabled
- `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY_PATH`
  - optional; ask before setup
  - App Store Connect analytics first, plus optional reviews, builds, TestFlight, and store context
  - ongoing Reports key: prefer Sales and Reports; Finance or Admin also works for report downloads
  - one-time Setup key: Admin, only to create the initial App Analytics report request; revoke after setup
  - add Customer Support for reviews, Developer for builds/TestFlight, and App Manager only for app metadata/pricing/release settings
- `ANALYTICSCLI_ACCESS_TOKEN`
  - recommended for CLI/agent auth when no local CLI login exists
  - do not ask for `ANALYTICSCLI_READONLY_TOKEN`; the readonly token is collected by the connector wizard and stored as `ANALYTICSCLI_ACCESS_TOKEN`
- `REVENUECAT_API_KEY`
  - optional; ask before setup
  - use a server-side secret API key for RevenueCat command/API mode
  - prefer v2 read permissions for charts/metrics and required project configuration resources
- `SENTRY_AUTH_TOKEN`
  - recommended for Sentry command/API mode
- optional connector-specific `secretEnv` per `sources.extra[]`

## References

- [README](README.md)
- [Setup And Scheduling](references/setup-and-scheduling.md)
- [Required Secrets](references/required-secrets.md)
- [Input Schema](references/input-schema.md)
- [Issue Template](references/issue-template.md)
