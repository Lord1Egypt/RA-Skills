# OpenClaw Growth Engineer

Shared AI Growth Engineer for mobile apps, centered around a standalone `openclaw` CLI runtime plus the host agent as the AI layer.

It pulls together analytics, monetization, crashes, feedback, store signals, and repo context and turns them into proposal drafts that can be handed to OpenClaw chat, GitHub issues, or draft PRs.

If you only want the normal setup path: run the local connector wizard once, then start the CLI.

## Shared Skill Distribution

This folder is the single canonical skill for OpenClaw, Hermes, and generic `SKILL.md` clients. Do not fork the instructions or runtime for Hermes. Keep shared behavior in this folder and use only small metadata/docs notes for agent-specific install paths.

OpenClaw install:

```bash
npx clawhub install openclaw-growth-engineer
```

Hermes install:

```bash
hermes skills install Wotaso/openclaw-growth-engineer-skill
```

## Quick Start

1. Paste this into the VPS, Mac mini, or host shell for the active app workspace:

```bash
npx -y @analyticscli/growth-engineer wizard --connectors
```

Secrets stay in the VPS/host shell wizard. Do not use chat or a standalone `analyticscli login` step for first setup.

2. Run setup:

```bash
growth-engineer setup --config openclaw.config.json
```

This should:

- initialize `openclaw.config.json`
- install/update `@analyticscli/cli` so the `analyticscli` binary exists
- reuse the existing AnalyticsCLI setup flow
- install/update the shared skills like `analyticscli-cli` and `analyticscli-ts-sdk`
- install the canonical OpenClaw skill path through the shared installer instead of redefining it locally

3. Run preflight:

```bash
growth-engineer preflight --config openclaw.config.json --test-connections
```

The preflight/start runtime also repairs a missing `analyticscli` binary by running:

```bash
npm install -g @analyticscli/cli
```

If global npm installs are blocked, it falls back to a user-local npm prefix at `~/.local`.
For manual repair from a copied skill runtime, run:

```bash
bash skills/openclaw-growth-engineer/scripts/install-analyticscli-cli.sh
```

4. Start the first pass:

```bash
openclaw start --config openclaw.config.json
```

For recurring OpenClaw checks, setup/start configures OpenClaw Gateway cron when available and keeps a non-empty workspace `HEARTBEAT.md` in place as fallback. For Hermes installs, the same wizard/start path configures Hermes cron when the `hermes` CLI is available. In both cases, the scheduler only wakes the agent; the Growth Engineer runner remains the source of truth for daily, weekly, monthly, quarterly, six-month, and yearly cadence decisions.

Setup should guide the developer through each missing piece. When something is blocked, the agent should explain what was detected, why the missing value matters, where to get it, and the minimum permission needed instead of returning a generic failure.
Before requesting optional credentials, ask which connections the user wants to set up: AnalyticsCLI baseline with feedback summaries, GitHub code access, ASC / App Store Connect CLI, RevenueCat, Sentry-compatible crash monitoring including Sentry Cloud and GlitchTip accounts, or skip.
The setup wizard also asks how the user wants the tool to operate and whether to keep or edit the default cadence plan:

- daily: critical production/business-health guardrail only, with root cause and exact fix/debug step
- weekly: conversion, traffic, activation, retention, RevenueCat, source quality, reviews, releases, and stability
- monthly: MoM revenue, conversion, churn, acquisition quality, store/listing conversion, retention, reviews, usage, and crash totals
- every 3 months: positioning, pricing/packaging, onboarding architecture, roadmap assumptions, tracking quality, and major funnel bets
- every 6 months: connector coverage, SDK instrumentation, event taxonomy, data reliability, memory, and growth loops
- yearly: evidence reset for market/channel fit, monetization model, retention ceiling, product scope, and major strategic direction

## What It Does

- Reads analytics by default and can add RevenueCat, Sentry-compatible crash monitoring, AnalyticsCLI feedback summaries, store/release connectors, Slack, and generic webhooks.
- For iOS/macOS apps, setup should ask whether to connect the `asc` CLI and App Store Connect skill for all available read-only App Store Connect signals: units/downloads, redownloads, conversion, source page views, app usage, purchases, subscriptions, reviews/ratings, builds/releases, and crash totals.
- Runs a daily production health pass when scheduled: non-zero production crash totals should notify the OpenClaw user through configured chat/social delivery, then create a GitHub issue or implementation PR automatically when GitHub API write access is configured.
- Sends short growth-run summaries through configured social/chat channels. OpenClaw cron defaults to the instance's connected channel route (`channel=last`), and Discord is only one possible command/webhook channel when explicitly configured.
- Uses API-key ASC batch reports only and does not require browser or web-session login for setup or health checks.
- Uses `analyticscli feedback summary --format json` as the built-in feedback source instead of a separate duplicate feedback definition.
- Correlates product signals with repo context; connect GitHub with readable code access whenever possible because it makes analytics findings much more actionable.
- Generates local issue drafts by default.
- Writes an OpenClaw chat outbox by default, and creates GitHub issues or draft pull requests only when GitHub artifact creation is explicitly enabled in config.
- Leaves all conversational analysis and implementation work to the host agent.

## What The Wizard Writes

The CLI writes only the commit-safe config:

- `openclaw.config.json`

You do not need to hand-edit `openclaw.config.json` for the basic setup.

One useful knob in the config is:

- `strategy.proposalMode = "mandatory" | "balanced" | "creative"`
- `deliveries.openclawChat.enabled = true | false`
- `deliveries.github.mode = "issue" | "pull_request"`
- `deliveries.github.autoCreate = true | false`
- `sources.feedback.cursorMode = "auto_since_last_fetch" | "manual"`
- `sources.feedback.initialLookback = "30d"`

Use it to control how conservative the generated requests should be.
Use the delivery flags to choose whether proposals should show up in OpenClaw chat, become GitHub issues, or land as draft PRs on a new branch.
The feedback cursor settings make old feedback history opt-in instead of accidental: first run uses `--last 30d`, later runs use the stored `lastCollectedAt` unless the command already sets its own time range.

Secrets should stay out of repo files. The normal path is to let OpenClaw manage the runtime environment or secret store and keep the config non-secret.

## Main Commands

Preflight only:

```bash
openclaw preflight --config openclaw.config.json --test-connections
```

One run:

```bash
openclaw run --config openclaw.config.json
```

Loop mode:

```bash
openclaw run --config openclaw.config.json --loop
```

## Maintainer Notes

In this monorepo, `packages/growth-engineer` is the canonical runtime surface. The checked-in `skills/openclaw-growth-engineer/src` and `scripts/openclaw-*` files remain compatibility paths for plain skill-folder installs.

The CLI is deliberately deterministic. It should not carry its own AI configuration.
The host agent should call the CLI for data collection and proposal generation, then use its own AI/runtime when the user wants interpretation or implementation.

Run this after editing runtime scripts:

```bash
pnpm openclaw-skill:quality
```

In the standalone skill repository, run:

```bash
npm run quality
```

The checked-in `.mjs` files are the zero-install runtime artifact for OpenClaw workspaces. Edit `.mts` files under `src/`, then run the quality command to rebuild and verify the runtime.

## Advanced Topics

Keep the README short and use the references below only when you need more control:

- [Advanced Setup](references/advanced-setup.md)
- [Setup And Scheduling](references/setup-and-scheduling.md)
- [Required Secrets](references/required-secrets.md)
- [Input Schema](references/input-schema.md)

## Workspace Files

The bootstrap step creates the runtime files below:

- `scripts/openclaw-growth-*.mjs`
- `scripts/openclaw-feedback-api.mjs`
- `data/openclaw-growth-engineer/*.example.json`
- `data/openclaw-growth-engineer/config.example.json`
