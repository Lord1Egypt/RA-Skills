# Async Job Polling Example

Use this example when the API is asynchronous: submit a task first, then poll until a terminal state, then verify the result endpoint.

## Best Fit

- export/report generation
- async batch jobs
- delayed processing pipelines

## Required Variables

- `HOST`
- `AUTH_TOKEN`

Optional:

- `TASK_ID` (skip submit and reuse an existing task)
- `MAX_POLL_ATTEMPTS` (default `20`)
- `POLL_INTERVAL_SECONDS` (default `2`)

## Run

```bash
bash -n './async-job-polling.api-verify.sh'
bash -n './async-job-polling.prepare-and-verify.sh'

HOST='https://api.example.test' AUTH_TOKEN='token value' bash './async-job-polling.prepare-and-verify.sh'
```

## What To Check

- submit response contains a task id
- polling reaches a terminal success state instead of timing out
- final result endpoint returns expected fields (for example `downloadUrl`)
