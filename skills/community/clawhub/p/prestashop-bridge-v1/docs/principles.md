# Principles

## 1. Security before convenience
Every protected request must use OAuth2 and HMAC. Security requirements are not optional.

## 2. Stable contract over native volatility
The Bridge exposes a stable contract even if native PrestaShop APIs evolve.

## 3. Reads are synchronous, writes are asynchronous
Business writes must be handled as jobs to avoid timeouts and partial failures.

## 4. Idempotency is mandatory
The transport is at-least-once. Business handlers must therefore be idempotent.

## 5. MySQL is the source of truth for job history
Redis is temporary. MySQL stores the authoritative job state.

## 6. Strict schemas only
All request and response payloads must follow strict JSON schemas with `additionalProperties: false`.

## 7. Agents must never overreach
No direct database access, no direct file access, no hidden side-channel behavior.

## 8. 202 is not business success
A `202 Accepted` means only that a job was accepted for processing. Agents must always poll job status before reporting business completion.
