# Changelog

## 0.1.2 - 2026-09-24

- Fixed strict YAML consumers rejecting the unquoted description containing `: `.

## 0.1.1 - 2026-09-24

- Added same-session reuse of a verified zero-Anlas billing profile when parameters remain unchanged.
- Added up to three sequential retries for transient failures while blocking billing, account, parameter, and ambiguous failures.

## 0.1.0 - 2026-09-06

- Initial zero-Anlas policy variant.
- Added strict account, estimator, and single-image gates.
- Blocked image editing, references, post-processing, batches, and paid fallbacks.
