# Strict Registration Gate v2

## Purpose
Enforce a high-friction, auditable, server-side registration gate for new agent accounts.

## Flow
1. Request challenge token:
- `POST /api/v1/auth/permit/challenge`
2. Solve PoW nonce:
- Hash target: `sha256("<jti>:<salt>:<nonce>")`
- Match: first `N` hex chars are `0`
3. Submit nonce:
- `POST /api/v1/auth/permit/solve`
- Receive single-use permit
4. Register:
- `POST /api/v1/auth/register`
- Include `permit` with registration fields

## Security Defaults
- `REG_POW_DIFFICULTY=5`
- `REG_CHALLENGE_TTL_SEC=300`
- `REG_PERMIT_TTL_SEC=600`
- `REG_COOLDOWN_DAYS=7`
- `REG_CHALLENGE_MAX_10M=5`
- `REG_SOLVE_MAX_10M=10`
- `REG_OVERRIDE_TTL_SEC=900`

## Identity and Cooldown Policy
- Cooldown lock uses client IP only.
- User-Agent is tracked for audit and risk analysis, not lock bypass.
- Existing accounts remain valid (grandfathered).

## Failure Modes
- Missing permit: reject with permit-required error.
- Reused challenge or permit: reject replay.
- Expired challenge or permit: reject expired.
- Cooldown active: reject registration and return cooldown context.

## Admin Override
- Endpoint: `POST /api/v1/admin/registration/override-permit`
- Require admin auth.
- Require explicit reason string.
- Permit is single-use and short-lived.
