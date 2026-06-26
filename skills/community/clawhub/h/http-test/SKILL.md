---
name: http-api-test-runner
description: Build reusable HTTP API test artifacts from user-provided endpoints, authentication, request data, expected results, and validation rules. Use this skill when the user wants to create .http files, run HTTP/REST API checks, replay browser or curl requests, validate JSON fields or response markers, compare expected vs actual responses, or generate formatted PASS/FAIL API test reports.
---

# HTTP API Test Runner

Use this skill to turn one-off HTTP checks into reusable `.http` cases and a runnable verification script.

Generate two artifacts by default:

- `<feature>.api-tests.http`
- `<feature>.api-verify.sh`

The `.http` file is the source of truth. The shell script executes the cases, prints readable `PASS/FAIL/SKIP` output, and exits non-zero when any non-skipped case fails.

## Quick Start

1. Collect only the missing inputs: host, method, auth, request data, cases, and expected results.
2. Choose a starting point:
   - Use `templates/` for a new endpoint.
   - Use `examples/` when the endpoint looks similar to an existing example.
   - Use `references/complex-scenarios.md` for multi-step or advanced validation.
3. Generate or update:
   - `<feature>.api-tests.http`
   - `<feature>.api-verify.sh`
4. Validate the generated script:

```bash
bash -n './<feature>.api-verify.sh'
bash './<feature>.api-verify.sh'
COOKIE='full Cookie header' AUTH_TOKEN='token value' bash './<feature>.api-verify.sh'
```

5. If cases fail, classify the problem before editing assertions:
   - auth mismatch
   - request shape mismatch
   - environment or fixture mismatch
   - business assertion mismatch

See `references/debugging-cookbook.md` for the failure checklist.

## What To Collect

Ask only for fields the user did not already provide.

| Input | Needed for |
| --- | --- |
| Base URL / host | Resolving request targets |
| HTTP method | Building the request |
| Authentication | Cookie, bearer, custom headers, or none |
| Request data | Path params, query params, JSON body, form body |
| Cases | Positive, negative, auth failure, boundary checks |
| Expected results | Status, JSON path, marker text, list membership, error behavior |
| Output preference | Brief summary, key fields, raw response save path |

For cookie-based tests, tell the user to copy the full `Cookie:` request header from a successful browser Network request. Do not reconstruct cookies from the storage panel.

Generated comments and final usage notes should follow the user's language.

## Choose Your Starting Point

- `templates/basic.api-tests.http.txt`
  - Fastest path for a new endpoint.
  - Includes a small set of common variables and assertions.
- `templates/basic.api-verify.sh`
  - Runnable shell script with timeout handling, env-based secrets, and formatted output.
- `examples/resource-detail/`
  - Resource detail lookup with cookie auth and JSON field assertions.
- `examples/auth-login-required/`
  - Unauthenticated and invalid-auth cases.
- `examples/list-assertions/`
  - List projection, membership, and absence checks.
- `examples/async-job-polling/`
  - Submit -> poll -> verify pattern with a runnable pre-step script for async workflows.

Note: publishable skill assets use `.http.txt` to satisfy upload restrictions, while generated runtime artifacts should still use `.api-tests.http`.

## Artifact Contract

The generated `.http` file should:

- declare variables such as `@host`, `@cookie`, `@token`, `@resourceId`
- use `###` titles for each case
- keep one request per case
- add explicit `expect.*` comments
- keep real secrets out of the file by default

The generated shell script should:

- read the `.http` file
- resolve `{{variable}}` placeholders
- accept secrets from environment variables
- print `PASS/FAIL/SKIP` output for each case
- print a summary line
- exit non-zero if any non-skipped case fails

## Safety Rules

- Do not commit real cookies, tokens, passwords, or internal credentials.
- Use placeholders such as `@cookie = <set via COOKIE>` and `@token = <set via AUTH_TOKEN>`.
- When secrets are missing, authenticated cases should `SKIP` with a clear reason instead of crashing the parser.
- Before publishing or committing generated artifacts, run a lightweight secret scan:

```bash
rg -n "password|secret|session_id|auth_token|access_token|refresh_token" <artifact-dir>
rg -n "Authorization: Bearer [A-Za-z0-9._-]+|C[o]okie: [A-Za-z0-9_%-]+=" <artifact-dir>
```

## Reference Map

- Assertion reference: `references/assertion-cheatsheet.md`
- Complex flows and advanced validation: `references/complex-scenarios.md`
- Failure diagnosis and triage: `references/debugging-cookbook.md`
- Lightweight publishable example: `references/http_test_artifact_example.md`

## Default Running Checks

After generating artifacts, run:

```bash
bash -n './<feature>.api-verify.sh'
bash './<feature>.api-verify.sh'
COOKIE='full Cookie header' AUTH_TOKEN='token value' bash './<feature>.api-verify.sh'
```

Interpretation:

- `bash -n` catches shell syntax errors.
- Running without secrets should verify parsing and expected `SKIP` behavior.
- Running with secrets should verify actual API behavior and assertions.
