# Complex Scenarios

Use this file after the basic template or an example already works. The goal is to extend coverage without turning the `.http` file into an unreadable workflow script.

## Runnable Pattern: Submit -> Poll -> Verify

For async APIs, use a two-layer setup:

1. A small pre-step script does submission and polling.
2. The reusable `.http` assertions focus on terminal-state checks.

Reference implementation:

- `examples/async-job-polling/async-job-polling.prepare-and-verify.sh`
- `examples/async-job-polling/async-job-polling.api-tests.http.txt`
- `examples/async-job-polling/async-job-polling.api-verify.sh`

Why this split works:

- polling logic stays explicit and readable in shell
- `.http` assertions remain stable and endpoint-focused
- failures can be classified as submit/poll/assertion instead of a single opaque failure

Recommended run order:

```bash
bash -n './async-job-polling.api-verify.sh'
bash -n './async-job-polling.prepare-and-verify.sh'
HOST='https://api.example.test' AUTH_TOKEN='token value' bash './async-job-polling.prepare-and-verify.sh'
```

## Multi-Step Flows

Typical case:

1. Create or log in.
2. Extract an identifier from the response.
3. Reuse it in a follow-up request.

Recommended pattern:

- Keep each HTTP call as its own `###` case.
- Promote reusable values into variables.
- If the second request depends on the first response, document the dependency in a nearby comment and keep the extraction logic in the verification script or a tiny pre-step instead of embedding too much logic in the `.http` file.

When to split:

- Split into multiple cases when each request is meaningful on its own.
- Keep a single validation flow only when the whole sequence forms one atomic business check.

## List and Pagination Checks

Recommended focus:

- Validate that a target element exists or does not exist.
- Validate only the fields that reflect business correctness.
- Treat one page as the unit of verification unless the user explicitly needs cross-page aggregation.

Example:

```http
# expect.status = 200
# expect.list_contains = data.items[].code:TARGET_CODE
# expect.list_not_contains = data.items[].code:REMOVED_CODE
# output.fields = code,message,data.pageInfo.total
```

Avoid asserting every list field unless the response shape is contractually stable.

## Async Polling

Typical case:

1. Submit a task.
2. Poll a status endpoint until success, failure, or timeout.

Recommended script behavior:

- cap retries with a fixed maximum
- sleep between retries
- distinguish timeout from assertion failure
- print the last observed state when the poll times out

Do not treat one immediate non-terminal response as a business failure unless the API contract says it should be terminal.

## Non-JSON Responses

Not every endpoint returns JSON. For HTML, plain text, or mixed payloads:

- prefer `expect.contains`
- use `expect.not_contains` to guard against common error pages or debug traces
- print content type in the report

If the endpoint sometimes returns JSON and sometimes returns HTML, let the assertions reflect that. Do not force every case into `expect.json_path`.

## When To Stop Expanding

A test definition is probably too complex when:

- one `.http` file tries to model an entire business workflow end to end
- a single case has many unrelated assertions
- the verification script starts carrying environment-specific business logic

When that happens, split the coverage into smaller endpoint-focused artifacts.
