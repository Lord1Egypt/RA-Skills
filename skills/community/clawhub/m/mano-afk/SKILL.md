---
name: mano-afk
description: Autonomous full-cycle app builder — PRD, architecture, code, deployment, testing, and bug fixing from a natural language description. Remembers user preferences and development pitfalls to self-evolve across projects. Use when the user explicitly requests a fully autonomous end-to-end app build.
homepage: https://github.com/Mininglamp-AI/mano-afk
metadata: {"openclaw": {"emoji": "⚙️", "install": [{"id": "brew", "kind": "brew", "formula":"Mininglamp-AI/tap/mano-afk", "bins":["mano-afk"],"label": "Install mano-afk (brew)"}]}}
---

# mano-afk

Fully automated pipeline that builds, deploys, and tests applications from a natural language description. The user is AFK for the entire duration. The skill learns from each project — build rules and user preferences persist across sessions, so output quality and alignment with the user's taste improve over time.

**Claude Code users:** Use the Claude Code-specific SKILL.md at [`claude/SKILL.md`](https://github.com/Mininglamp-AI/mano-afk/tree/master/claude).

## Architecture

Three roles collaborate to deliver the application:

- **Main Agent** (you): orchestration, test execution, fix coordination, user communication
- **Build Sub-agent**: requirements → architecture → code → deploy → bug fixes (when given specific errors)
- **Adversary Sub-agent**: independent test case design (does not execute tests)

The main agent delegates code generation to a sub-agent (the longest phase) and stays free during that time. The main agent runs all tests directly for full visibility into results.

## Orchestration

**AFK rule:** Step 0 is the only user interaction window. From Step 1 onward, make all decisions autonomously — never ask the user. Ambiguous decisions (8bit vs float, React vs Vue, port selection) use the most reasonable default and document in PRD.md. Only stop if completely infeasible (missing hardware, no permissions, 10 fix iterations exhausted).

### Step 0: User Setup (interactive)

This is the only step where the agent may ask the user questions.

**Requirements triage:** If the request is too vague to determine core functionality (e.g., "build me an app"), or contains ambiguous requirements that could lead to fundamentally different products, ask the user to clarify — keep it to 1-2 focused questions, not a long interview. Non-critical gaps (visual design, validation rules, tech stack, layout) are filled autonomously by the build sub-agent.

**E2E test setup:** Check `mano-afk config --get e2e-mode`.

- **`local` or `cloud`** — already configured, proceed.
- **Not set** — recommend E2E testing to the user: "E2E testing lets mano-afk verify your app through the actual UI — clicking buttons, filling forms, checking visual results. Want to set it up?" Then run `mano-afk check` and follow its printed guidance to complete configuration. If the user declines, skip E2E — the skill works without it.

When Step 0 completes, tell the user: **"Hold the beer. AFK from now on."**

### Step 1: Prepare (autonomous — no user interaction)

Derive a short, kebab-case project name from the request (e.g., "make me a todo app" → `todo-app`).

**Project directory:** Read the configured project root via `mano-afk config --get projects-dir` (default: `~/Projects/`). Project directory: `{projects-dir}/{project-name}/`.

Read `references/report-template.md` — you will use it in Step 4 to write `report.md`. Note the absolute path to the `references/` directory — it will be passed to sub-agents for the remaining reference files.

### Step 2: Build (sub-agent)

Spawn a build sub-agent via `sessions_spawn` with `runtime="subagent"`. Construct the prompt with:

1. The absolute path to `build-pipeline.md` — instruct the sub-agent to read and follow it
2. The absolute path to this skill's `references/` directory — the sub-agent reads rules.md, preferences.md, and templates as needed
3. The user's original request, verbatim
4. The project directory path

Respond to the user immediately with what is being built and the project directory. The build sub-agent follows 4 phases internally: **Phase 1** generates `PRD.md` (product requirements with acceptance criteria), **Phase 2** designs architecture and generates `README.md` (with test cases derived from PRD), **Phase 3** writes code, **Phase 4** deploys. Wait for `progress.md` to show `status: ready_for_testing`.

**Timeout:** Build tasks (dependency installation, compilation, deployment) can take a long time. Set a generous timeout when spawning the sub-agent — at least 30 minutes, or no timeout if the platform supports it.

### Step 3: Verify Deployment

Before testing, confirm the app is accessible:
1. Check that `deploy/start.sh` exists in the project
2. Run it if servers are not already running
3. Verify with `curl` or port check
4. If deployment fails (start.sh missing, server crashes, port unreachable), read `deploy/backend.log` and `deploy/frontend.log`, then go to Step 5 (Fix Loop) with the deployment error as the failure description

### Step 4: Test

Execute every test case defined in the README across all categories. No test case may be skipped or deferred.

Before starting each category, count the total test cases from the README. Print a progress counter for each test: `[3/18] api_3 PASS` or `[5/18] api_5 FAIL`. This makes skipped tests visible — if the counter jumps from 3 to 7, tests 4-6 were skipped.

Record results in `report.md` (use the report template). On failure, include full error output (response body, stderr, logs).

#### 4.1 Lint

Run the linter configured by the build sub-agent. Auto-fix what's possible (`--fix`), then report remaining errors.

#### 4.2 API Tests

Run every API test case defined in the README. Use `curl -s -w "\nHTTP_STATUS:%{http_code}\n"` to capture response body and status code. Print full response body on failure.

#### 4.3 E2E Tests (optional)

E2E tests use `mano-afk run` to open the app in a browser, interact with the UI via a vision-language model, and verify visual outcomes.

**Prerequisites — skip this section entirely if any check fails:**
1. `mano-afk` is on PATH (installed via the skill's brew metadata during skill installation — do NOT install packages autonomously)
2. `mano-afk config --get e2e-mode` returns `local` or `cloud` (if not set, skip and record reason in `report.md`)

**Database reset:** Before running the first E2E test, clear all application tables (e.g., `DELETE FROM` each app table, or delete and re-initialize the SQLite file). This removes residual data from API tests. Do NOT reset between individual E2E tests — they run sequentially and may depend on state created by prior tests.

Run every E2E test case defined in the README:

```bash
mano-afk run "{steps}" --url "{url}" --expect "{expected}"
```

`--url` opens the target page in the default browser before the agent starts. The agent sees the page already loaded — do NOT include "Open localhost:..." in the task steps.

All execution parameters (`--local`/`--cloud`, `--max-steps`, `--minimize`) are read from `mano-afk config`. CLI flags override config when specified. Use `mano-afk config --list` to see current values.

Execution rules:
- Run each test sequentially
- Each `mano-afk` task can take up to 30 minutes. Set `exec` timeout to at least 1800s, or use `background: true` with `yieldMs: 1800000`. Never use a short timeout
- Do not use mouse/keyboard while a test is running
- Use `mano-afk stop` to: resolve 409 session conflicts, clean up after a killed process, or abort a running task

#### 4.4 Adversary Review

After all previous tests pass, spawn an adversary sub-agent via `sessions_spawn` with `runtime="subagent"`. Construct the prompt with:
1. Role: "You are an independent QA reviewer. Your job is to identify potential problems the builder likely missed."
2. The full content of the project's `PRD.md` (requirements and acceptance criteria) and `README.md` (architecture and test cases)
3. The project directory path (the adversary reads source code for code-level findings)

The adversary does NOT interact with the running app — it reviews requirements and code only.

The adversary sub-agent **identifies potential problems only** — it does NOT execute anything. It returns findings in two layers, each as a table with columns: ID, Finding, Severity, Suggested Verification.

- **Layer 1 — User perspective**: usability gaps, cross-feature consistency, confusing flows, poor UX
- **Layer 2 — Code perspective**: data integrity, missing validation, error handling, state consistency

Constraints: cover both layers, do NOT repeat issues already in README test cases, do NOT flag security vulnerabilities (XSS, SQL injection, CSRF).

**Triage each finding yourself** using the appropriate method: code inspection (schema/config issues), API test (backend behavior via curl), or E2E test (UI rendering, user flows, visual state). At least 2-3 findings must be verified via E2E test. **Reset the database before running adversary E2E verifications** to avoid pollution from prior tests. Record each verdict in report.md: confirmed (→ fix loop) or dismissed (with reason).

### Completion Checklist (before proceeding to Step 5 or 6)

Before moving forward, verify each item. If any is "no", go back and complete it.

- [ ] Every API test case in README executed and recorded
- [ ] Every E2E test case in README executed and recorded (or all skipped with reason if prerequisites not met)
- [ ] Adversary review completed with findings from both layers
- [ ] At least 2-3 adversary findings verified via E2E test (if E2E is available)
- [ ] All confirmed adversary findings entered into fix loop

### Step 5: Fix Loop

If any test fails:

1. Collect all failures with full error output (response body, stderr, logs, mano-afk output)
2. Spawn a **new** build sub-agent in fix mode via `sessions_spawn` with `runtime="subagent"` — provide:
   - The absolute path to `build-pipeline.md` (fix mode does not need other reference files)
   - Project directory path
   - Detailed failure descriptions: test ID, command run, expected result, actual result, full error output
3. Wait for the sub-agent to fix and re-deploy (`progress.md` shows `status: ready_for_testing`)
4. Re-run failed tests with the same tool and method used in the original test. A test verified via E2E test must be re-verified via E2E test.
5. Repeat until all pass (max 10 iterations)

**E2E false positives:** If an E2E test fails but you inspect the code and confirm the implementation is correct (the failure is a vision model misinterpretation), dismiss it as a false positive in `report.md` with your reasoning. Do not enter the fix loop for false positives — fixing correct code wastes iterations.

**Step back on repeated failures:** If the same test fails 2+ times, include a note in the fix prompt: "This test has failed N times. Previous fix attempts: [descriptions]. Consider a structural fix rather than a patch."

**Exhausted iterations:** If 10 iterations are reached and failures remain, proceed to Step 6 with current results. Finalize `report.md` with all remaining failures, iteration history, and a summary of what was attempted.

### Step 6: Completion

- Summarize to the user: total tests, pass/fail, project directory
- **Update rules:** Review the fix loop history. If any error pattern would prevent the same class of bug in a future project, add a general rule to `references/rules.md` (max 100, remove least valuable if full). Also merge any `new-rules.md` the build sub-agent wrote in the project root.
- **Update preferences:** If the user gives follow-up feedback (styling, features), update `references/preferences.md`

## Reference Directory

The `references/` directory is **local to this skill** and contains files that evolve across projects. It does not modify any global CLI configuration, system settings, or files outside this skill's directory.

**Scope:** These files are only read by mano-afk's build and adversary sub-agents. They have no effect on other skills, other CLI tools, or the host system.

**What is stored:**

| File | Purpose | Updated When | Max entries |
|---|---|---|---|
| `build-pipeline.md` | Build sub-agent instructions (phases 1-4 + fix mode) | Manual only | — |
| `rules.md` | General build rules, lessons learned from past fix loops | After fix loop completes (Step 6) | 100 |
| `preferences.md` | User styling/UX preferences | After user gives feedback (Step 6) | 50 |
| `prd-template.md` | PRD generation template (5 chapters) | Manual only | — |
| `project-structure.md` | Standard directory layout template | Manual only | — |
| `readme-template.md` | README.md generation template | Manual only | — |
| `report-template.md` | report.md generation template | Manual only | — |

Only `rules.md` and `preferences.md` are modified during execution. All other files are read-only templates. Rules and preferences persist across projects so the skill can improve over time.

## Data & Privacy

- **Local by default:** Code generation, linting, API tests, and deployment run entirely on your machine.
- **Cloud data transmission:** E2E tests (4.3) in cloud mode use `mano-afk run`, which sends screenshots and task descriptions to cloud VLA model providers. This only happens when `e2e-mode` is explicitly set to `cloud` via `mano-afk config`. Local mode and skipping E2E tests involve no cloud calls.
- **Opt-in only:** E2E tests require explicit configuration (`mano-afk config --set e2e-mode local|cloud`). Without this, they are skipped.
- **No other external calls:** The skill does not phone home, collect telemetry, or send project data to any service beyond the above opt-in test execution.
