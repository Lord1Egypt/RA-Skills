# Setup — NodeJS

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Node fails quietly: the process is alive, the logs are clean, and the request is stuck behind a 40 ms sync call. Be specific about which layer is broken, name the check that proves it, and prefer a measurement over an opinion.

## How To Load Preferences

1. Read `~/Clawic/data/nodejs/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `package_manager: npm`, `module_system: esm`, `node_target: 24`, `test_runner: node`, `deploy_target: container`, `ts_runner: none`.
3. When the repository contradicts a default, the repository wins for that project: a `pnpm-lock.yaml`, a `"type": "commonjs"`, or an `engines.node` field is a stated fact about this codebase, not a preference to record globally.
4. Read `~/Clawic/data/nodejs/memory.md` for prior context (stack, recurring failures, depth of explanation). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about their setup, priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a package manager, module format, Node version, test runner, deploy target, or TypeScript execution model → update the matching key in `~/Clawic/data/nodejs/config.yaml`.
- User expresses a stance (crash-vs-catch posture, concurrency caps, log format, upgrade cadence, banned dependencies) → record it under the relevant preference area (tooling, conventions, platform, thresholds, risk posture, output format, work order, integrations, constraints, cadence) in `~/Clawic/data/nodejs/memory.md`.
- User corrects earlier guidance → update the stored value so the same correction is not needed twice.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their stack (framework, database client, hosting), the failures that keep recurring, and how much explanation they want — but only from what they actually reveal.
