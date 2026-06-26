# Setup - Google Pay

Read this when `~/google-pay/` is missing or empty.
Keep setup practical and non-blocking.

## Operating Priorities

- Answer the immediate user request first.
- Confirm platform and payment architecture early.
- Avoid long onboarding before delivering value.

## First Activation Flow

1. Confirm what is being integrated now:
- Web checkout
- Android app checkout
- PSP handoff flow
- Recurring or subscription behavior

2. Confirm environment and merchant readiness:
- Test or production target
- Merchant profile and gateway status
- Origin or package configuration status
- Fallback payment method availability

3. Confirm business constraints:
- Single country or multi-country launch
- Authorization and capture flow requirements
- Refund and support expectations

4. If setup context is approved, initialize local workspace:
```bash
mkdir -p ~/google-pay
touch ~/google-pay/{memory.md,implementations.md,validation-log.md,incidents.md}
chmod 700 ~/google-pay
chmod 600 ~/google-pay/{memory.md,implementations.md,validation-log.md,incidents.md}
```

5. If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Start in test mode unless user explicitly requests production checks.
- Prefer one checkout path at a time per ticket.
- Require fallback behavior documentation before go-live recommendations.
- Require idempotency strategy before enabling retries.

## What to Save

- Active platform, path, and PSP scope
- Merchant and gateway validation status
- Validation outcomes and unresolved risks
- Incident signatures and mitigation status
- Launch readiness and rollback state

## Guardrails

- Never ask the user to expose private keys in chat.
- Never store raw Google Pay token payloads in local notes.
- Never claim production readiness without validation evidence.
