# Encryption

Last reviewed: March 17, 2026.

Primary authority pointers:

- HIPAA Security Rule addressable encryption specifications
- HHS Security Rule guidance

## Why this domain matters

Encryption is necessary but not sufficient. In PRS, encryption supports stage progression only when it is part of a broader control set.

## Review questions

- Is encryption in transit enforced on relevant paths?
- Is at-rest encryption enabled or clearly inherited where appropriate?
- How are encryption keys managed?
- Are secrets separated from code and runtime logs?

## Minimum expectations by stage

- PRS-1: encryption and secrets management are materially implemented
- PRS-2: encryption scope and exceptions are documented
- PRS-3: approved scope accounts for real PHI data paths and stores
- PRS-4: live operations maintain key and secret control evidence where applicable

## Strong evidence

- KMS configuration
- encrypted storage configuration
- secrets manager usage
- key-access controls

## Common blockers

- plaintext secrets in repo or CI
- unclear key ownership
- unencrypted staging or backup path

## Recommended next actions

- centralize secret storage and rotation
- document encrypted stores and exceptions
- verify backup and replica paths follow the same protection model
