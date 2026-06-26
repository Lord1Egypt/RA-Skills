# Idempotency Policy

## HTTP layer
Redis key: `idempotency:{request_id}`
- TTL: 24 hours
- stored fields: status, http_code, body, created_at

## Business layer
MySQL table: `bridge_processed_operations`
- unique key: `operation_key`
- retention: 30 days
- purpose: protect handlers under at-least-once delivery

## Expected behavior
- Redis `processing` => `202`
- Redis `completed` => `200`
- Redis `failed` => `409`
- Redis unavailable but MySQL operation key exists => rely on stored business result

## Handler pattern
1. start SQL transaction
2. insert business key uniquely
3. if duplicate: rollback or no-op and ack
4. if new: perform business write, commit, ack
