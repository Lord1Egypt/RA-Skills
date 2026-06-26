# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.14.x  | :white_check_mark: |
| < 0.14  | :x:                |

## Reporting a Vulnerability

**Do not open a public issue.** Instead, email:

📧 **security@firmade.ai**

PGP key available at: https://firmade.ai/security/pgp-key.asc

### What to expect

| Step | Timeline |
|------|----------|
| Acknowledgment | Within 2 business days |
| Initial assessment | Within 5 business days |
| Fix preparation | Within 30 days |
| Coordinated disclosure | Mutually agreed date (max 90 days) |

### Scope

NexLink is an OpenClaw skill that integrates Exchange, Nextcloud, and YouTube transcript extraction.

Issues in scope include:
- Missing or broken confirmation prompts on destructive operations
- Credential leaks or unsafe handling of env vars / tokens
- Path traversal in Nextcloud WebDAV operations
- HTML injection in generated email digests
- Unauthorized data access through Exchange EWS delegate escalation
- LCM memory poisoning or cross-user context leakage

Out of scope:
- Issues in third-party services (Exchange server, Nextcloud instance, YouTube API)
- Social engineering that requires physical access
- Denial of service without data exposure

## Security Design

NexLink's security model, described in [references/security-best-practices.md](references/security-best-practices.md):
- All destructive commands require explicit confirmation (interactive or per-command `--yes` flag)
- `move_to_trash()` is used for task deletion instead of permanent `delete()`
- Branding can be suppressed via `--no-branding` / `NEXLINK_NO_BRANDING=1`
- Dedicated least-privilege service accounts strongly recommended

## Acknowledgments

We appreciate responsible disclosure and will publicly thank researchers who follow this policy (unless they prefer anonymity).
