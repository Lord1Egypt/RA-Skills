# Architecture Overview

## Runtime stack
- PrestaShop 9
- Symfony 6.4
- API Platform 3
- Redis single node
- MySQL

## Data flow

### Read path
1. Client gets OAuth token.
2. Client signs request with HMAC.
3. Bridge validates JWT, timestamp, signature, and rate limits.
4. Bridge returns synchronous resource data.

### Write path
1. Client gets OAuth token.
2. Client signs request with HMAC.
3. Bridge validates schema and idempotency cache.
4. Bridge persists a `bridge_job` row in MySQL.
5. Bridge dispatches message to Redis Messenger transport.
6. Worker processes message transactionally.
7. Worker persists final status in MySQL.
8. Client polls `GET /v1/jobs/{jobId}` from MySQL.

## Persistence roles
- Redis: transport and temporary HTTP idempotency cache only.
- MySQL: job state, business idempotency, failed jobs, audit references.
