# Validation Checklist - Google Pay

Use this checklist before recommending release.

## Merchant and Environment

- Merchant profile configured for the correct environment.
- Gateway and Google Pay configuration are aligned.
- Test and production credentials are separated.
- Web origin or Android package configuration is correct.

## Functional Paths

- Happy path payment succeeds.
- User cancellation path is handled without checkout lock.
- Declined payment path returns actionable messaging.
- Retry path works without duplicate authorization.
- Fallback card or alternative payment path is available.

## Platform Matrix

- Real Android device tests executed for supported versions.
- Web tests executed on Chrome and Android browsers in scope.
- Unsupported browser behavior is explicit and safe.

## Data and Consistency

- Server totals always match displayed totals.
- Idempotency behavior validated with repeated requests.
- Webhook or callback reconciliation confirms final state.

## Observability and Safety

- Payment events include request id and outcome.
- Logs avoid raw token payloads and private data.
- Alerts exist for elevated failures or timeouts.
- Rollback plan is documented and tested.

## Release Gate

Do not recommend production rollout until all checklist sections pass.
