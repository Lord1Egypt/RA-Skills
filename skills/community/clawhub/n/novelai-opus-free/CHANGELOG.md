# Changelog

## 0.2.3 - 2026-09-24

- Fixed strict YAML consumers rejecting the unquoted description containing `: `.

## 0.2.2 - 2026-09-24

- Added up to three sequential retries after the initial attempt for transient failures.
- Kept exact parameters on retries and blocked retries for billing, account, parameter, or ambiguous processing failures.

## 0.2.1 - 2026-09-23

- Added same-session verification reuse when billing-affecting parameters remain unchanged.
- Removed arbitrary time and reuse-count expiry; invalidate only on restart, errors, account/billing signals, or parameter changes.
- Clarified that missing billing fields in a successful reused operation are not themselves an error.

## 0.2.0 - 2026-09-06

- Added Opus-only account and Usage Limit gates.
- Allowed zero-estimate img2img and inpainting under normal-size, single-image conditions.
- Allowed pre-encoded Vibe generation, annotation, and the tested free Director subset.
- Kept Vibe encoding, background removal, references, post-processing, batches, and paid fallbacks blocked.
