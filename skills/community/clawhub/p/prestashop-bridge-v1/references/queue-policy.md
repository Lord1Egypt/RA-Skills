# Queue Policy

## Transport
Redis single node is used as the Messenger transport in MVP.

## Persistence
MySQL persists:
- `bridge_job`
- `bridge_failed_jobs`
- `bridge_processed_operations`

## Retry policy
- max attempts: 3
- backoff: `min(2^attempt * 1000 + random(0,1000), 60000)`

## Non-retryable cases
- `400 Bad Request`
- `422 Unprocessable Entity`

## Status authority
`GET /v1/jobs/{jobId}` always reads from MySQL.
