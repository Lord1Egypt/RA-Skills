# CI Pipeline

Source: https://docs.openclaw.ai/ci

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationContributingCI PipelineGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpHelp
HelpTroubleshootingFAQ
Community
OpenClaw Lore
Environment and debugging
Environment VariablesDebuggingTestingScripts
Node runtime
Node.js
Compaction internals
Session Management Deep Dive
Developer setup
Setup
Contributing
CI Pipeline
Docs meta
Docs HubsDocs directory
On this page
- [CI Pipeline](#ci-pipeline)
- [Job Overview](#job-overview)
- [Fail-Fast Order](#fail-fast-order)
- [Runners](#runners)
- [Local Equivalents](#local-equivalents)

​CI Pipeline
The CI runs on every push to `main` and every pull request. It uses smart scoping to skip expensive jobs when only docs or native code changed.
​Job Overview
JobPurposeWhen it runs`docs-scope`Detect docs-only changesAlways`changed-scope`Detect which areas changed (node/macos/android)Non-docs PRs`check`TypeScript types, lint, formatNon-docs changes`check-docs`Markdown lint + broken link checkDocs changed`code-analysis`LOC threshold check (1000 lines)PRs only`secrets`Detect leaked secretsAlways`build-artifacts`Build dist once, share with other jobsNon-docs, node changes`release-check`Validate npm pack contentsAfter build`checks`Node/Bun tests + protocol checkNon-docs, node changes`checks-windows`Windows-specific testsNon-docs, node changes`macos`Swift lint/build/test + TS testsPRs with macos changes`android`Gradle build + testsNon-docs, android changes
​Fail-Fast Order
Jobs are ordered so cheap checks fail before expensive ones run:

- `docs-scope` + `code-analysis` + `check` (parallel, ~1-2 min)

- `build-artifacts` (blocked on above)

- `checks`, `checks-windows`, `macos`, `android` (blocked on build)

​Runners
RunnerJobs`blacksmith-4vcpu-ubuntu-2404`Most Linux jobs`blacksmith-4vcpu-windows-2025``checks-windows``macos-latest``macos`, `ios``ubuntu-latest`Scope detection (lightweight)
​Local Equivalents
Copy```
pnpm check          # types + lint + format
pnpm test           # vitest tests
pnpm check:docs     # docs format + lint + broken links
pnpm release:check  # validate npm pack

```

SetupDocs Hubs⌘I