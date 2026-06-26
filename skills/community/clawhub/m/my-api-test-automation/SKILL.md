---
name: api-test-automation
description: Generate complete automated API test cases from interface documentation such as OpenAPI, Swagger exports, Postman collections, Markdown API docs, or endpoint tables. Use when Codex needs to analyze interface docs, generate executable API test cases, add configurable pre-request scripts and post-response assertion scripts, adapt the suite to a user-provided runtime environment, execute the generated tests, and produce a complete test report with pass/fail details, diagnostics, and environment summary.
---

# API Test Automation

## Overview

Use this skill to turn API or interface documentation into an executable automated test suite. Always carry the work through end-to-end: understand the API spec, generate complete test cases, wire pre-request and post-assertion logic, execute the suite in the requested environment, and emit a complete report.

## Workflow

1. Identify the input artifacts.
2. Normalize the execution environment.
3. Generate the test workspace and test cases.
4. Add pre-request scripts and post-response assertion scripts.
5. Execute the suite in the requested environment.
6. Produce the report and call out gaps or assumptions.

## Step 1: Identify the Input Artifacts

Accept any of these as the source of truth:

- OpenAPI or Swagger JSON or YAML
- Postman collection or environment exports
- Markdown, Word, PDF, spreadsheet, or plain-text API documentation
- Tables that describe endpoints, methods, headers, parameters, request bodies, and expected responses

Before generating tests, extract at least:

- base URL or environment-specific host mapping
- authentication mechanism
- endpoint path and HTTP method
- request parameters, headers, and body schema
- expected status codes and business assertions
- setup or dependency relationships between endpoints

If the documentation is partial, continue by making explicit assumptions and record them in the final report.

## Step 2: Normalize the Execution Environment

Read [environment-contract.md](references/environment-contract.md) when the user provides runtime or environment details or asks to execute the generated suite.

Capture these items before execution:

- runner choice: `postman`, `newman`, `pytest`, or another user-mandated runner
- base URL and environment name
- auth secrets or auth injection method
- common headers and variables
- setup or teardown hooks
- report output path

Prefer these execution strategies:

- Use `newman` when the user environment already relies on Postman collections or JavaScript test scripts.
- Use `pytest` plus `requests` when the user wants Python-based suites or the environment clearly supports Python better.
- Follow the user-required runner if they specify one.

## Step 3: Generate the Test Workspace and Cases

Run `scripts/prepare_test_workspace.py` to create a stable workspace skeleton before filling in test logic.

Example:

```powershell
python scripts/prepare_test_workspace.py --output C:\work\api-test-output --runner postman --env-name sit
```

Then populate the generated workspace with:

- endpoint-by-endpoint happy-path cases
- validation and error cases for required fields, data types, bounds, and permissions
- dependency-chain cases for create, query, update, delete, or equivalent flows
- data-driven variants when the documentation exposes enumerations or boundary values

Always create or update `case-manifest.json` so the report stage can map results back to endpoints and coverage.

## Step 4: Add Pre-request and Post-assertion Logic

Use templates from `assets/templates/` when you need a quick starting point.

Pre-request logic should handle things like:

- auth token acquisition and refresh
- timestamp or signature generation
- shared headers or trace IDs
- setup requests and variable extraction

Post-response assertion logic should validate both transport and business semantics:

- HTTP status code
- response time or basic performance budget when required
- required fields and schema fragments
- business codes or messages
- cross-step state propagation

Keep environment-sensitive values in config or env files rather than hard-coding them into each case.

## Step 5: Execute the Suite

If the user asks to run the suite, execute it in the provided environment after confirming the runner and prerequisites from the available local context.

Execution checklist:

- verify required CLI or runtime exists (`newman`, `node`, `python`, `pytest`, and so on)
- inject environment variables or environment files
- run the generated suite from the generated workspace
- capture raw stdout or stderr and machine-readable result artifacts when possible
- do not silently skip failed setup steps; report them

If the environment is missing a dependency, report the exact blocker and, when appropriate, suggest the minimal install command.

## Step 6: Produce the Report

Run `scripts/build_test_report.py` after execution to generate a human-readable summary and machine-readable JSON report.

Example:

```powershell
python scripts/build_test_report.py --manifest C:\work\api-test-output\case-manifest.json --results-dir C:\work\api-test-output\reports --output-md C:\work\api-test-output\reports\test-report.md --output-json C:\work\api-test-output\reports\test-report.json
```

The final report should include:

- environment summary
- source artifacts used
- generated suite summary
- total, passed, failed, and skipped counts
- per-case failure details
- endpoint coverage or uncovered items
- assumptions, blockers, and follow-up recommendations

## Resources

### `scripts/prepare_test_workspace.py`

Create a reusable output skeleton with config, report, and script directories plus a starter `case-manifest.json`.

### `scripts/build_test_report.py`

Merge execution artifacts into a complete Markdown and JSON report.

### `references/environment-contract.md`

Read when runtime or environment details are provided or when deciding how to execute the generated tests.

### `references/report-contract.md`

Read when you need the expected report sections or result-file shape.

### `assets/templates/`

Use starter templates for environment config, pre-request script, post-assertion script, and test-plan notes. Copy and adapt them instead of re-creating boilerplate.
