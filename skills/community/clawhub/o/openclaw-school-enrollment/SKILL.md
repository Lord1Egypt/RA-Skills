---
name: openclaw-school-enrollment
description: Connect OpenClaw to the claw-school training flow with an enrollment code, use default training URLs unless overridden, ensure clawhub is available, install the mapped ClawHub skills for that package, and report each training step back to the claw-school server.
---

# OpenClaw School Enrollment

## Overview

Use this skill to complete a real claw-school enrollment from OpenClaw.

This skill requires:

- an `enrollment token`

This skill can optionally accept:

- a custom `base URL`
- a custom `clawhub registry URL`

If you do not provide overrides, the skill will automatically use:

- `base URL`: `https://openclaw-school.space`
- `clawhub registry URL`: `https://cn.clawhub-mirror.com`

The bundled script supports stepwise orchestration so you can keep the user informed after every completed phase while still reporting the real training progress to the web app.

## Workflow

1. Gather:
   - `--enrollment-token`
   - optional `--base-url`
   - optional `--clawhub-registry-url`
   - optional `--skill-version`
2. If the enrollment token is missing, ask only for that value.
3. Start the run with structured output:

```bash
node "{baseDir}/scripts/enroll-and-train.mjs" start --json --enrollment-token "<token>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
```

4. After `start` succeeds:
   - keep `orderId`, `runId`, `reportToken`, `directionName`, `baseUrl` only for internal chaining
   - do not proactively expose those raw fields to the user
   - send exactly one short Chinese progress sentence to the user:
     - `已完成入学报到，正在开始入学测试。`
5. Run the following phases in order, always with `--json`, always reusing the returned `runId` and `reportToken`:

```bash
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase baseline_testing --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase course_resolving --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase package_fetching --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase supplies_procuring --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase package_installing --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase capability_activating --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase graduation_testing --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
node "{baseDir}/scripts/enroll-and-train.mjs" phase --json --phase graduation_ready --run-id "<runId>" --report-token "<reportToken>" [--base-url "<url>"] [--clawhub-registry-url "<url>"]
```

   - Never skip, reorder, or combine phases.
   - If a phase is rejected because the order is wrong, immediately run the missing required phase, then retry the blocked phase, and only then continue forward.

6. After each successful phase:
   - read `userFacingMessage` from the JSON output
   - send that one sentence to the user in concise Chinese
   - do not add raw `skillSlugs`, `orderId`, `runId`, `clawhub` command lines, or registry details unless the user explicitly asks
7. Testing phases must always produce a start event and a completion event:
   - `baseline_testing`: before running the phase, tell the user `已开始入学测试。`; then wait 10 seconds only when no baseline score exists yet; after the command returns, send its completion message and explicitly mention reuse when applicable
   - `graduation_testing`: before running the phase, tell the user `已开始毕业测试。`; then always wait 10 seconds; after the command returns, send its completion message with the new score
8. After the final phase:
   - tell the user that training progress has been reported to the web app
   - remind the user to open a new OpenClaw session before using the newly acquired abilities
   - keep the close-out short and product-facing

## Output Rules

- Prefer product language such as `课程`, `训练资源`, `学习物资`, `能力装配`, `职业能力`.
- Avoid implementation language such as `skill slug`, `clawhub command`, `runId`, `orderId`, `registry URL` unless needed for debugging.
- If the user asks for technical details, you may reveal the structured fields returned by the script.
- Do not use the `run-all` mode for normal user-facing conversations. It is only for manual verification or debugging.

## Troubleshooting

- If the enrollment token is expired or already used, stop and surface the server error directly.
- If the course API returns an empty or invalid install plan, stop and surface the server error directly.
- If `npm install -g clawhub` fails, surface the failure directly and do not continue silently.
- If a `clawhub install --force` command fails, surface the failing slug and do not continue silently.
- Do not invent install plans or skill slugs. The server is the source of truth.
