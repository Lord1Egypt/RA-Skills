---
name: lockpicker
description: Guide a user through capturing and analyzing a HAR file from their own logged-in browser session, extracting the minimum auth material needed, mapping the exact request chain behind a website action, and turning that known-good browser workflow into a reusable local script. Use when a user wants to reverse-engineer a legitimate action they are already authorized to perform on a website, such as upload, publish, schedule, or queue operations, especially when browser automation is flaky and a direct authenticated web-request workflow is preferred.
---

# Lockpicker

Guide the work from a user-owned browser session outward. Do not start by guessing endpoints.

## Core rules

- Use this only for services the user is authorized to access and operate.
- Use the user's own authenticated browser session.
- Reproduce a workflow the user can already perform manually.
- Prefer captured evidence over speculation.
- Do not brute-force hidden endpoints, fuzz auth, or expand scope beyond the requested action.
- If cookies, csrf, or auth headers are stale, refresh them cleanly from the browser session instead of trying bypasses.
- Warn the user that replaying private web calls may violate site terms, can break without notice, and may lock or rate-limit the account.
- Minimize sensitive retention: store only the auth material actually needed, keep it local, and avoid copying it into chat unless the user explicitly chooses that.

## Workflow

1. Confirm the target action.
2. Capture a clean HAR of one successful manual run.
3. Extract auth material from the same browser session.
4. Isolate the exact request chain.
5. Identify reusable constants vs dynamic fields.
6. Rebuild the workflow as a local script.
7. Test one item first.
8. Only then add queueing, scheduling, or batching.

## Step 1: confirm the target action

Write down the exact user goal in one sentence.

Examples:
- schedule a post with one image
- publish a drafted gallery item
- upload a file and submit metadata
- create a queued post for later release

Also record the success condition:
- returned id
- visible scheduled item
- published permalink
- draft created

## Step 2: capture a clean HAR

Read `references/har-capture-checklist.md` before capture.

Capture one clean successful run with as little extra noise as possible.

Prefer this sequence:
- open a fresh tab
- open DevTools Network
- Preserve log on
- Disable cache on
- clear old requests
- perform only the target action once
- export HAR immediately after success

If a site uses chunked upload or several chained calls, make sure the HAR includes the full sequence.

## Step 3: extract auth material

Read `references/auth-materials.md`.

Collect only what is actually needed for replay, typically:
- Cookie header
- csrf token
- Authorization header if present
- key client headers if the request depends on them

Save them as local runtime files in `workspace/tmp/` unless the user requests another location.

## Step 4: isolate the request chain

Read `references/request-analysis-patterns.md`.

Separate the workflow into stages such as:
- init
- append/upload
- finalize
- status/poll
- mutation/create
- confirm/readback

For each stage, identify:
- method
- url
- query params
- required headers
- body shape
- values copied from previous responses

Ignore decorative noise like analytics, passive feed refreshes, and unrelated GraphQL calls.

## Step 5: identify reusable vs dynamic fields

Mark each field as one of:
- constant across runs
- auth/session-derived
- generated per request
- user-supplied content
- returned from prior step

Examples:
- query id may be reusable until the site changes it
- csrf comes from session
- media id comes from upload init/finalize
- scheduled timestamp is user-supplied
- permalink may be derived from returned rest id

## Step 6: rebuild as a local script

Keep the first script narrow.

Preferred first-pass shape:
- one script that executes one known-good workflow end to end
- plain text auth files
- one media file
- one text payload
- one schedule timestamp if relevant
- JSON output file preserving step results

Use the bundled helpers when useful:
- `scripts/extract_har_requests.py` to summarize and filter HAR requests
- `scripts/extract_cookie_headers.py` to pull cookie / csrf / authorization material from a matching HAR request
- `scripts/diff_request_shapes.py` to compare two request JSON shapes and spot dynamic fields
- `scripts/scaffold_direct_client.py` to generate a first-pass replay script from one captured request JSON

## Step 7: test one item first

Do not batch first.

Validate:
- upload succeeds
- returned ids look real
- final mutation succeeds
- user-visible result exists

If the first test fails, compare the failing request with the HAR rather than guessing.

## Step 8: add queueing or scheduling

Only after a single-item success.

Use a queue manifest when the user wants repeated runs. Include fields like:
- scheduled_at
- text
- media_file
- status
- result ids
- permalink
- notes

Prefer small batches and pauses between groups when operating against production sites.

## Helper scripts

### Summarize matching HAR requests

```powershell
python scripts/extract_har_requests.py capture.har --contains graphql --contains upload --out requests.json
```

### Extract auth materials from a matching request

```powershell
python scripts/extract_cookie_headers.py capture.har --contains x.com/i/api/graphql --out-dir runtime-auth
```

### Compare two request shapes

```powershell
python scripts/diff_request_shapes.py request-a.json request-b.json
```

### Scaffold a first direct client

```powershell
python scripts/scaffold_direct_client.py request.json --out first_client.py
```

## When to read references

- Read `references/har-capture-checklist.md` before capture.
- Read `references/auth-materials.md` when extracting cookies, csrf, and auth headers.
- Read `references/request-analysis-patterns.md` when tracing the chain from HAR.
- Read `references/common-web-flows.md` when the workflow involves uploads, polling, GraphQL mutations, or delayed scheduling.
- Read `references/safety-boundaries.md` when the task touches terms-of-service, account-risk, or scope concerns.
