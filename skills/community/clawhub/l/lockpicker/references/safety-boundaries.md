# Safety boundaries

## Allowed framing
This skill is for reproducing a workflow the user is already authorized to perform from their own logged-in browser session.

## Do not do
- brute-force hidden endpoints
- expand scope beyond the requested workflow
- bypass login, MFA, paywalls, or rate limits
- reuse someone else's session material
- disguise unauthorized access as testing

## Always warn about
- terms-of-service risk
- account lock or challenge risk
- private endpoint instability
- auth expiry and silent breakage
- rate limits and anti-abuse systems

## Best practice
- test one item first
- keep batches small
- save raw evidence locally
- prefer deterministic scripts over repeated manual guessing
