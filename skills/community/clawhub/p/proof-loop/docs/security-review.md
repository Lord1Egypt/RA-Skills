# ClawHub review — 2026-11-07

## Fixed in 0.3.1

- Empty objects and incomplete AC coverage could pass the completion gate. The gate now matches all declared spec ACs exactly once and requires typed verify-phase metadata, evidence and an explicit empty problems file.
- Schema validation checked only top-level required fields. Nested fields, types, enums and timestamps now fail closed against the bundled schema subset. Unsupported schema keywords are rejected.

## Reviewed scanner false positives

The navigation-label checker is a demo fixture, not the skill implementation. Local initialization writes task artifacts by design; it does not self-modify the installed skill. Tests use argument-list subprocess calls, not shell interpolation. German/English strings are fixture expectations, not a language policy imposed on users. The workflow table grants no destructive-action authority.

## Trust boundary

Files remain editable by their owner. The checker does not authenticate agent identities, attest execution, or certify evidence truth. A fresh verifier must inspect evidence. Mechanical PASS is not a cryptographic CI attestation.

## Follow-up review

The 0.3.2 scanner still objects to self-reported verifier identity and editable local specifications. This is the documented file-based discipline trust boundary, not cryptographic attestation. The optional OpenCode template’s broader trigger was inconsistent with SKILL.md and is now aligned with explicit opt-in. No identity/signature enforcement or unrequested external trust service was added.
