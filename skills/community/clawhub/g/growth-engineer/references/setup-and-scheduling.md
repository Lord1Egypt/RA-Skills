# Setup And Scheduling

This is the recommended OpenClaw-first baseline.

## 1) Install Runtime

```bash
npx -y clawhub install openclaw-growth-engineer
bash skills/openclaw-growth-engineer/scripts/bootstrap-openclaw-workspace.sh
```

The runtime must also ensure the AnalyticsCLI npm package is present. The package name is
`@analyticscli/cli`; the binary name is `analyticscli`.

```bash
npm install -g @analyticscli/cli
```

If global npm installs fail on a VPS, use:

```bash
bash skills/openclaw-growth-engineer/scripts/install-analyticscli-cli.sh
```

`openclaw setup`, `openclaw start`, and the copied preflight/start runtime should run this
install/update automatically before using `analyticscli`.

## 2) Generate Config

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

The config is non-secret and commit-safe:

- `data/openclaw-growth-engineer/config.json`

The setup flow should be developer-friendly:

- auto-detect repo root, package manager, git remote, and available AnalyticsCLI auth when possible
- explain why each requested connection is needed before asking for it
- ask for the minimum missing secret or permission, not a broad token
- show a status checklist after setup: configured, optional, blocked, and next command
- hand off weak or missing app instrumentation to the `analyticscli-ts-sdk` skill with concrete SDK setup steps
- ask exactly which optional connections the user wants to set up before requesting credentials: AnalyticsCLI baseline with feedback summaries, GitHub code access, ASC / App Store Connect CLI, RevenueCat, Paddle, SEO/GSC/DataForSEO, Sentry-compatible crash monitoring including Sentry Cloud and GlitchTip accounts, or skip
- ask how the tool should be used before enabling scheduling: production autopilot, advisory-only summaries, or manual reports
- ask whether to keep the default cadence plan; if not, collect what should happen daily, weekly, monthly, every 3 months, every 6 months, and yearly

For GitHub, RevenueCat, Paddle, SEO/GSC/DataForSEO, Sentry, and App Store Connect connector setup, use the connector wizard instead of asking the user to compose setup commands manually:

```bash
npx -y @analyticscli/growth-engineer wizard --connectors github,revenuecat,paddle,seo,sentry,asc
```

The connector wizard asks only for the selected connectors, explains each provider step in the terminal, writes local secrets to `~/.config/openclaw-growth/secrets.env`, and runs helper setup for the selected connectors.

## 3) Choose GitHub Code Access And Delivery Mode

Connect GitHub with readable repo/code access whenever possible.
This is very important for turning analytics signals into concrete file/module hypotheses.
Issue and pull-request write permissions are optional; request them only when the selected delivery mode should create GitHub artifacts.

Prefer GitHub CLI:

```bash
gh auth status
gh auth login
gh repo view --json nameWithOwner,defaultBranchRef
```

For analysis-only token fallback, ask for a fine-grained read-only token with `Contents: Read` and `Metadata: Read`.
Ask for all repositories only when the user wants cross-repo code analysis.

Set in config:

- `actions.mode = "issue"`
- or `actions.mode = "pull_request"`

PR mode creates proposal branches and draft PRs with `.openclaw/proposals/...md` files.

## 4) Configure Connectors

Built-in source keys:

- `analytics`
- `revenuecat`
- `paddle`
- `seo`
- `sentry`
- `coolify`
- `feedback`

Treat `feedback` as an AnalyticsCLI/custom feedback source key, not as a separate primary connector in high-level setup answers.

Extra sources:

- add entries to `sources.extra[]`
- use `mode=file` for the most stable setup
- use `mode=command` only when the command deterministically returns JSON

Recommended mobile extras:

- `app-store-reviews`
- `play-console`

Do not configure GlitchTip as a separate extra connector when it exposes the Sentry-compatible API. Put Sentry Cloud and GlitchTip instances under `sources.sentry.accounts[]` so crash monitoring remains one Sentry-compatible connector. ASC is a first-class App Store Connect connector, not an extra analytics alias.

Paddle setup:

- Ask whether to connect Paddle for web billing, MRR, revenue, refunds, chargebacks, checkout conversion, and active subscriber metrics.
- Do not ask for or store a single Paddle product/project selection in the wizard. Keep account-level metrics access so the Growth Engineer can compare all Paddle revenue context available to the API key.
- Tell the user to open `https://vendors.paddle.com/authentication-v2`, go to Developer Tools > Authentication > API keys, create a live API key, and grant `metrics.read`.
- Store the key as `PADDLE_API_KEY` in the local secrets file.
- Treat sandbox Paddle metrics as setup-only evidence, not production revenue evidence.

SEO / Search Console / DataForSEO setup:

- Ask whether to connect SEO acquisition data from Google Search Console and optional DataForSEO.
- Do not hard-code one Search Console property by default. Leave `GSC_SITE_URL` empty so the exporter lists and queries all verified properties visible to the account.
- Only set `GSC_SITE_URL` when the user intentionally wants to restrict analysis to one domain/property.
- Tell the user to open `https://search.google.com/search-console` and verify the properties they want included.
- For OAuth token mode, use a read-only Search Console token with `webmasters.readonly` scope and store it as `GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN`.
- For service-account mode, tell the user to open `https://console.cloud.google.com/iam-admin/serviceaccounts`, create or choose a service account, add its email as a Search Console user on the relevant properties, then set `GOOGLE_APPLICATION_CREDENTIALS` or `GSC_SERVICE_ACCOUNT_JSON` outside chat.
- DataForSEO is optional and paid. Tell the user to open `https://app.dataforseo.com/api-dashboard`; store `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` only when requested. Commands must include `--confirm-paid` and a bounded `--max-paid-requests`.

For Apple-platform apps, ask whether to connect the `asc` CLI plus the App Store Connect agent skill for read-only App Store Connect reporting.
When configured, use every available read-only ASC surface: App Analytics, Sales and Trends, downloads/units, redownloads, conversion, source traffic, app usage, purchases, subscriptions, ratings/reviews, build/TestFlight/release context, and crash totals. Do not describe ASC as partial or analytics-only once it is connected.
ASC setup uses two API keys:

- Reports key: `Sales and Reports` for ongoing Growth Engineer downloads. `Finance` or `Admin` also works for report downloads, but prefer `Sales and Reports` after bootstrap.
- Setup key: temporary `Admin`, used once to create the initial App Analytics report request, then revoked in App Store Connect.

Optional extra roles on the Reports key: `Customer Support` for review text, `Developer` for builds/TestFlight context, and `App Manager` only when app metadata or release settings are explicitly needed.

ASC key locations:

- Team key: App Store Connect -> Users and Access -> Integrations -> App Store Connect API
- Individual key: profile menu -> Edit Profile -> Individual API Key
- Keep Apple's original `AuthKey_<KEY_ID>.p8` filenames. The wizard derives `ASC_KEY_ID` and `ASC_BOOTSTRAP_KEY_ID` from those names.

RevenueCat setup:

- Ask whether to connect RevenueCat for monetization/subscription data.
- For SDK instrumentation use only the public app-specific SDK key in app code.
- For server-side summaries use a secret API key from RevenueCat -> Project Settings -> API Keys -> + New secret API key.
- Prefer v2 read permissions for charts/metrics and required project configuration resources; store as `REVENUECAT_API_KEY`.

Sentry setup:

- Ask whether to connect Sentry-compatible crash monitoring for crash, error, release, and performance signals.
- Use the wizard to collect one or more accounts directly. For each account, collect label, `baseUrl`, `tokenEnv`, token, `org`, `environment`, and optional comma-separated `projects[]`.
- Do not ask for one global `SENTRY_PROJECT` in the setup wizard. Defer Sentry project selection to app/repo/release context, or set account-specific `sources.sentry.accounts[].projects[]` only when a product has a known fixed mapping.
- For multiple Sentry-compatible accounts, configure `sources.sentry.accounts[]` with separate `baseUrl`, `tokenEnv`, `org`, `projects[]`, and `environment` values for each account, for example Sentry Cloud plus self-hosted GlitchTip with different projects.
- Use read-only Sentry API scopes: `org:read`, `project:read`, and `event:read`.
- The direct source command is `node scripts/export-sentry-summary.mjs`; optional MCP config uses `@sentry/mcp-server@latest` when `npx` is available.
- Treat Sentry as connected only after auth and exporter smoke tests pass.
- Multiple Sentry-compatible accounts are supported. Put them under `sources.sentry.accounts[]` with a separate `baseUrl`, `tokenEnv`, `org`, `projects[]`, and `environment` for each account. Use this for setups such as Sentry Cloud plus self-hosted GlitchTip where the projects and tokens differ.
- For production crash monitoring, compare Sentry issue/event/user counts with ASC total crashes and app-version crash breakdowns. ASC `crashRate` is supporting context; total crashes and affected users are the daily alert trigger.

## 5) Store Secrets

Prefer OpenClaw secret storage.
Inject env vars at runtime only.

Never store secrets in:

- repo files
- config JSON
- shell history
- issue/PR content

## 6) Validate

```bash
node scripts/openclaw-growth-preflight.mjs --config data/openclaw-growth-engineer/config.json --test-connections
```

Checks include:

- `analyticscli` package install/update and binary availability
- `analyticscli-cli` skill presence
- readable GitHub repo access when available for code-aware analysis
- connector file/command readiness
- required secrets for enabled sources and delivery modes
- live smoke tests where possible

## 7) Run

One pass:

```bash
node scripts/openclaw-growth-runner.mjs \
  --config data/openclaw-growth-engineer/config.json \
  --state data/openclaw-growth-engineer/state.json
```

Loop:

```bash
node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json --loop
```

OpenClaw Gateway cron:

For reliable VPS installs, prefer OpenClaw's built-in cron scheduler over Discord delivery or host-level cron. `openclaw-growth-wizard.mjs` and `openclaw-growth-start.mjs` should configure an OpenClaw cron job when `automation.openclawCron.enabled` is true. The job runs in the main session via a system event, wakes immediately, and asks OpenClaw to run:

```bash
node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json
```

Recommended cron job:

```bash
openclaw cron add \
  --name "OpenClaw Growth Engineer scheduler" \
  --cron "*/30 * * * *" \
  --tz "UTC" \
  --session main \
  --system-event "Run OpenClaw Growth Engineer for this workspace. Execute: node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json --state data/openclaw-growth-engineer/state.json. The runner is the source of truth for connector health, daily, weekly, monthly, quarterly, six-month, and yearly cadence decisions. After the command finishes, inspect data/openclaw-growth-engineer/state.json and data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl. If connector health is healthy, no production issue is found, and no actionable growth finding was generated, reply HEARTBEAT_OK." \
  --announce \
  --channel last \
  --wake now
```

`--channel last` is intentional: it lets OpenClaw use the chat/social route already connected to that instance instead of assuming Discord, Slack, Telegram, or any other specific provider. Set `automation.openclawCron.delivery.channel` and `to` only when an install needs a pinned target.

Verification on the VPS:

```bash
openclaw cron list
openclaw tasks list
openclaw tasks audit
tail -n 20 data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl
jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' data/openclaw-growth-engineer/state.json
```

Hermes cron:

For Hermes installs, prefer Hermes Gateway cron over Discord delivery or host-level cron. `openclaw-growth-wizard.mjs` and `openclaw-growth-start.mjs` should configure a Hermes cron job when `automation.hermesCron.enabled` is true and the `hermes` CLI is available. The job must attach the shared skill and workspace:

```bash
hermes cron create \
  "*/30 * * * *" \
  "Run Growth Engineer for this workspace. Execute: node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json --state data/openclaw-growth-engineer/state.json. The runner is the source of truth for connector health, daily, weekly, monthly, quarterly, six-month, and yearly cadence decisions. After the command finishes, inspect data/openclaw-growth-engineer/state.json and data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl. If connector health is healthy, no production issue is found, and no actionable growth finding was generated, reply HEARTBEAT_OK." \
  --name "Hermes Growth Engineer scheduler" \
  --skill growth-engineer \
  --deliver local \
  --workdir "$PWD"
```

Verification on the Hermes host:

```bash
hermes cron list
hermes gateway status
tail -n 20 data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl
jq '.connectorHealth, .cadences, .lastRunAt, .skippedReason' data/openclaw-growth-engineer/state.json
```

OpenClaw heartbeat:

The setup/bootstrap path must still leave a real workspace `HEARTBEAT.md` task in place as a fallback and awareness checklist. OpenClaw skips heartbeat runs when `HEARTBEAT.md` is empty or comment-only, so an enabled Growth Engineer schedule is not sufficient by itself.

Expected heartbeat task:

```yaml
tasks:

- name: openclaw-growth-engineer-run
  interval: 6h
  prompt: "Run `node scripts/openclaw-growth-runner.mjs --config data/openclaw-growth-engineer/config.json` from the workspace if the config and runtime files exist. The runner owns schedule.cadences, connectorHealthCheckIntervalMinutes, skipIfNoDataChange, and skipIfIssueSetUnchanged. If it reports connector-health alerts, production crashes, generated issues, or actionable growth findings, summarize only the action and evidence. If setup files are missing, tell the user to run `npx -y @analyticscli/growth-engineer wizard --connectors`. If there is no actionable output, reply HEARTBEAT_OK."
```

When `schedule.intervalMinutes` or `schedule.connectorHealthCheckIntervalMinutes` is customized, `openclaw-growth-start.mjs` should rewrite this task interval to the smaller cadence. Heartbeat is not the primary scheduler on VPS installs; OpenClaw cron should wake the agent, and the runner decides whether daily, weekly, monthly, quarterly, six-month, or yearly growth work is due.

## 7a) Production Health And Growth Cadence

The default growth loop interval is one day (`schedule.intervalMinutes = 1440`), while connector health runs every 6 hours by default (`schedule.connectorHealthCheckIntervalMinutes = 360`). Daily growth runs should cover every configured public production app.
If ASC analytics reports return a 403 for an app that is not public yet or not analytics-ready, record it as skipped/not-public rather than a failure.

Daily:

- Only investigate critical production or business-health issues: Sentry/GlitchTip production errors, crashes, onboarding or purchase drop-offs, zero-conversion days, missing buyers, very low users, conversion, purchases, or other urgent drops.
- Check ASC total production crashes by app version and Sentry production issues/events/users.
- Notify the OpenClaw user through configured chat/social delivery when total production crashes are non-zero.
- Refresh and parse API-key ASC batch reports in the background, especially App Analytics report instances and Sales and Trends reports when `ASC_VENDOR_NUMBER` is available. Check every available ASC metric, especially units/downloads, redownloads, conversion rate, app usage, updates, app opens, subscription state, source traffic, and unique product page views by source, but only alert on severe anomalies during daily-only runs.
- Do not require `asc web auth` during normal scheduled runs. Use experimental ASC web analytics only after asking the user, and only when a specific needed metric is unavailable through documented API-key reports.
- Compare crash movement with release/build data before recommending more acquisition traffic.
- Inspect memory/state and recent releases/code changes before assigning root cause.
- Automatically create GitHub issues or implementation PRs when OpenClaw has configured GitHub API write access. Skip only when write access is missing, the finding is too low-confidence, or `actions.disableAutoCreateGitHubArtifacts = true`.

Weekly:

- Compare units, conversion, source mix, AnalyticsCLI activation/funnels/retention, Sentry stability, RevenueCat monetization when enabled, reviews, and releases.
- Produce one executive summary plus one to three Handlungsempfehlungen with evidence, expected KPI movement, and likely code/store surfaces.

Monthly:

- Compare month-over-month units/downloads, redownloads, conversion, source quality, crash totals, review themes, retention, and churn.
- Decide which acquisition channel, listing element, onboarding step, paywall, feature, or instrumentation surface should be built, changed, deleted, or repaired from codebase evidence.

Every 3 months:

- Revisit positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, and major funnel bets.
- Look for structural constraints and durable opportunities, not only tactical UI changes.

Every 6 months:

- Audit connector coverage, SDK instrumentation, event taxonomy, data reliability, memory/state quality, and whether growth loops still match the best users.
- Prioritize measurement and system fixes that make future recommendations more trustworthy.

Yearly:

- Reset strategy from all available evidence: market/channel fit, monetization model, retention ceiling, product scope, and major surfaces/features.
- Decide whether to double down, reposition, rebuild, or sunset major directions.

Social summaries:

- By default, a meaningful growth run sends a short summary through configured OpenClaw chat, Slack, Discord command, webhook, or equivalent channels.
- Disable with `notifications.growthRun.enabled=false` or by removing all growth-run notification channels.
- Never include secrets in social summaries.

ASC source reporting caveat:

- ASC source reports describe product page views by source. Do not call this downloads by source unless ASC exposes a true source-level download/unit measure.
- Use source page views together with units and conversion rate to infer traffic quality.

## 8) Feedback Collection

Optional local feedback API:

```bash
FEEDBACK_API_TOKEN=<token> node scripts/openclaw-feedback-api.mjs --port 4310
```

Expected payload fields now support:

- `feedback`
- `location` / `locationId`
- `appSurface`
- `metadata`

The generated summary aggregates recurring themes and top feedback locations.

## 9) Mobile Feedback Best Practice

- Use tenant-owned backend/proxy endpoints for app-side feedback submission
- Keep `locationId` stable and code-oriented
- Example ids:
  - `onboarding/paywall`
  - `settings/restore`
  - `profile/delete_account`
