---
name: openclaw-token-optimizer
description: "Find potential token waste in OpenClaw or Hermes Agent. Use when asked to reduce AI costs, review model choices, check large instructions or audit recurring tasks. Explain what matters and suggest safe next steps without changing settings."
version: 4.1.1
author: Asif2BD
homepage: https://missiondeck.ai
source: https://github.com/Asif2BD/OpenClaw-Token-Optimizer
license: MIT
openclaw: ">=2026.9.4"
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["python3"]}}}
---

# Make your AI agent leaner—not less capable

Ask your agent:

> “Check where I might be wasting tokens and tell me what to improve.”

Or try:

- “Review my scheduled tasks for unnecessary AI usage.”
- “Which instruction files are making my context heavy?”
- “Help me choose a suitable model for routine work.”

Works with **OpenClaw and Hermes Agent**. Your agent handles the technical steps below;
you do not need to copy Python commands or prepare exports when the required evidence
is already available in its environment.

## What you get

A short, prioritized explanation of what was checked, what deserves attention and what
to do next. Nothing silently changes your models, instructions or schedules. Potential
savings are opportunities to test—not a promise or a measured reduction in your bill.

Built by [MissionDeck.ai](https://missiondeck.ai).

## Instructions for the agent

### 1. Start with what you already know

When the user requests an audit, proceed with relevant read-only checks; do not ask them
to restate the runtime, agent ID or active profile if trusted session context already
provides it. Say briefly that you will inspect and recommend, without changing settings.

Use this decision order:

- An explicit user-selected runtime/profile takes priority.
- Otherwise use the hosting session's known runtime and active agent/profile.
- Installed binaries alone are not proof of which profile is active. If the host is unknown
  or multiple profiles are plausible, ask one focused question rather than auditing the
  wrong system. Continue any independent checks whose scope is already clear.

Resolve bundled script paths relative to this SKILL.md directory. Use an available Python
3.10+ interpreter. No automatic installs, recursive home-directory searches or credential
searches. Never print raw configuration or environment values.

### 2. Run the matching read-only audit

**In OpenClaw:** use the current agent ID from trusted runtime context, not the example
name or the CLI's default. Follow `references/QUICKSTART.md` for the command. Include
`--config` only when the active config path is already established and the audit needs it.
If the CLI is unavailable, use exports already supplied; otherwise report the missing
capability instead of asking the user to run a long list of commands.

**In Hermes:** use the active profile path already supplied by the host/user. A known
HERMES_HOME path is profile evidence; do not dump the environment or load `.env`. Do not
assume the default profile just because a default directory exists. The audit reads only
config.yaml and cron/jobs.json. Prefer the existing Hermes Python environment for YAML
support. If no cron file exists, report automation coverage as unavailable; audit the
available config separately rather than claiming zero jobs. See references/QUICKSTART.md.

Do not ask for catalog/status exports for an ordinary Hermes profile audit: those are
only needed for the separate model-routing function. Do not start Hermes or any job.

### 3. Match extra checks to the question

- Context: inspect only known, relevant instruction files. Character/4 estimates are not
  actual injected tokens; use native context diagnostics if available. Never delete instructions.
- Model choice: use the user's policy and known catalog/status evidence. Missing capability
  metadata means unverified, not unsupported. No automatic switching or paid canary.
- Spending: without complete usage evidence, say actual spending/savings are unknown.
  Native usage ingestion and automatic budget alerts are not implemented.

Read only the reference needed: QUICKSTART.md for commands, HERMES.md for profile/model
precedence, PROVIDERS.md for routing/cache advice. Do not load every reference by default.

### 4. Explain the result, not the machinery

Lead with a plain-language verdict and at most three prioritized next steps. For each,
explain the evidence, why it matters, and the uncertainty. Separate confirmed problems
from review candidates; do not count every informational finding as a fault. End with
what was not checked and confirmation that no settings were changed.

Do not paste raw JSON unless requested. Offer technical details only when useful. If
nothing actionable is found, say so. Never claim a fixed savings percentage, cheapest
model, successful authentication or measured dollars without evidence.

## Boundaries

All bundled commands are diagnostic. No config edits, installs, restarts, messages, new
jobs or credential reads. OpenClaw native reads may contact configured services and update
native caches. Hermes support is file-based, not native catalog/authentication discovery;
profile overlays and runtime overrides remain unverified. See SECURITY.md.

Python 3.10+; optional PyYAML for YAML input. OpenClaw adapter tested on 2026.9.4; Hermes
file compatibility is pinned in references/HERMES.md. The CLI still requires explicit
runtime selection for Hermes; the agent chooses it from trusted context, not autodetection.
