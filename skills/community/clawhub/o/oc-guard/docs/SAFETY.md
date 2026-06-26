# SAFETY

## Scope

This skill provides guarded OpenClaw config operations.

- `plan`: preview and validate
- `apply --confirm`: execute guarded changes

## Security Diagram

![oc-guard security principles infographic](docs.png)

## Security Principles

1. Never directly edit production config without guard validation.
2. Always create backup before apply.
3. Fail closed on unknown or unsupported paths.
4. Roll back automatically if restart/health check fails.
5. Never expose secrets in logs or receipts.
6. If `plan` or `apply` returns failed/blocked, never bypass `oc-guard` by directly editing config.
7. `Runtime: running` is not enough; apply must pass post-restart canary replies.

## Secret Handling

Do not commit or publish:

- API keys
- tokens
- app secrets
- user-specific config files
- runtime logs containing sensitive data

## Publishing Checklist

- No hardcoded secrets
- No personal runtime data
- No private logs/backups
- README clearly states security boundaries
- Example configs are sanitized

## Execution Integrity

Receipt output must include:

- executor
- operation
- request id
- status
- signature (12 chars)

If command is not executed, output must explicitly state non-execution.

If proposal generation fails, inspect `/tmp/oc-guard-last-opencode-output.txt` for diagnostics.

## ClawHub Packaging Consistency

Before trusting a published version, verify:

- `clawhub inspect oc-guard-skill --files` includes `scripts/oc-guard.py`
- `clawhub inspect oc-guard-skill --file SKILL.md` includes `metadata.openclaw.requires`
