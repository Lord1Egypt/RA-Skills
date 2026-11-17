# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /v1/translate` (40 sats) with `text` (6,000-character cap) and `target_language`.
- Removed formality control, cultural notes and the English default. The user names the target language.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
