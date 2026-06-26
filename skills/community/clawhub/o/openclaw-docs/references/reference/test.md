# Tests

Source: https://docs.openclaw.ai/reference/test

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationRelease notesTestsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
CLI ReferenceagentagentsapprovalsbrowserchannelsconfigurecrondashboarddirectorydnsdocsdoctorgatewayhealthhookslogsmemorymessagemodelsnodesonboardpairingpluginsresetSandbox CLIsecuritysessionssetupskillsstatussystemtuiuninstallupdatevoicecall
RPC and API
RPC AdaptersDevice Model Database
Templates
Default AGENTS.mdAGENTS.md TemplateBOOT.md TemplateBOOTSTRAP.md TemplateHEARTBEAT.md TemplateIDENTITYSOUL.md TemplateTOOLS.md TemplateUSER
Technical reference
Wizard ReferenceToken Use and CostsgrammY
Concept internals
TypeBoxMarkdown FormattingTyping IndicatorsUsage TrackingTimezones
Project
Credits
Release notes
Release ChecklistTests
Experiments
Onboarding and Config ProtocolCron Add HardeningTelegram Allowlist HardeningWorkspace Memory ResearchModel Config Exploration
On this page
- [Tests](#tests)
- [Model latency bench (local keys)](#model-latency-bench-local-keys)
- [Onboarding E2E (Docker)](#onboarding-e2e-docker)
- [QR import smoke (Docker)](#qr-import-smoke-docker)

​Tests

Full testing kit (suites, live, Docker): [Testing](/help/testing)

`pnpm test:force`: Kills any lingering gateway process holding the default control port, then runs the full Vitest suite with an isolated gateway port so server tests don’t collide with a running instance. Use this when a prior gateway run left port 18789 occupied.

`pnpm test:coverage`: Runs the unit suite with V8 coverage (via `vitest.unit.config.ts`). Global thresholds are 70% lines/branches/functions/statements. Coverage excludes integration-heavy entrypoints (CLI wiring, gateway/telegram bridges, webchat static server) to keep the target focused on unit-testable logic.

`pnpm test` on Node 24+: OpenClaw auto-disables Vitest `vmForks` and uses `forks` to avoid `ERR_VM_MODULE_LINK_FAILURE` / `module is already linked`. You can force behavior with `OPENCLAW_TEST_VM_FORKS=0|1`.

`pnpm test:e2e`: Runs gateway end-to-end smoke tests (multi-instance WS/HTTP/node pairing). Defaults to `vmForks` + adaptive workers in `vitest.e2e.config.ts`; tune with `OPENCLAW_E2E_WORKERS=<n>` and set `OPENCLAW_E2E_VERBOSE=1` for verbose logs.

`pnpm test:live`: Runs provider live tests (minimax/zai). Requires API keys and `LIVE=1` (or provider-specific `*_LIVE_TEST=1`) to unskip.

​Model latency bench (local keys)
Script: [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts)
Usage:

- `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`

- Optional env: `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`

- Default prompt: “Reply with a single word: ok. No punctuation or extra text.”

Last run (2025-12-31, 20 runs):

- minimax median 1279ms (min 1114, max 2431)

- opus median 2454ms (min 1224, max 3170)

​Onboarding E2E (Docker)
Docker is optional; this is only needed for containerized onboarding smoke tests.
Full cold-start flow in a clean Linux container:
Copy```
scripts/e2e/onboard-docker.sh

```

This script drives the interactive wizard via a pseudo-tty, verifies config/workspace/session files, then starts the gateway and runs `openclaw health`.
​QR import smoke (Docker)
Ensures `qrcode-terminal` loads under Node 22+ in Docker:
Copy```
pnpm test:docker:qr

```

Release ChecklistOnboarding and Config Protocol⌘I