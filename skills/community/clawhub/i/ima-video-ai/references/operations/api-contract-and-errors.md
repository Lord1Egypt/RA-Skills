# API Contract And Errors

## Task Lifecycle

The shipped create/poll contract is:

1. `GET /open/v1/product/list`
2. `POST /open/v1/tasks/create`
3. `POST /open/v1/tasks/detail` until success, failure, delete, or timeout

`create_task()` raises immediately when the API returns a non-zero/non-200 code or no task ID.

## Polling Contract

`poll_task()` treats task media as the source of truth:

- `resource_status` null is treated as processing
- `resource_status=2` fails the task
- `resource_status=3` means deleted
- success requires every media entry to reach `resource_status=1`
- once all medias are done, the runtime inspects the first media and returns only after that first entry exposes a URL or watermark URL

The configured poll interval is 8 seconds for all current video task types, and the max wait is 40 minutes.

## Error Categories

- create-time API errors: bad auth, credit issues, attribute/rule mismatch, invalid params
- transport errors: request failures from `requests`
- poll-time task failures: explicit media error, delete state, backend-reported failure
- timeout: no terminal success before `VIDEO_MAX_WAIT_SECONDS`

## User-Facing Boundary

Execution-path CLI failures are translated through the shared error policy. The repo does not expose raw backend request bodies as the primary user explanation, and create-task runtime errors no longer embed serialized payloads.
