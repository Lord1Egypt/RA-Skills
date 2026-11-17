## Description:

Secure credential and secrets management for OpenClaw agents using Locker Secrets Manager, with read-only and read-write vault access, in-memory caching, vault references, and guidance to prevent credential leakage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moskoweb](https://clawhub.ai/user/moskoweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help OpenClaw agents retrieve, reference, cache, and manage sensitive credentials through Locker Secrets Manager instead of storing raw secrets in configs, logs, cron jobs, or agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged for review before installation because it documents unsafe installation and secret-handling patterns.

Mitigation: Review the skill before use and require a verified, pinned Locker CLI installation path.

Risk: Some examples write secrets to .env files, export all secrets, or place access keys in crontab.

Mitigation: Remove those patterns before deployment; use read-only Locker keys by default and store vault references instead of raw values.

Risk: Create and update flows pass secret values as command-line arguments.

Mitigation: Avoid write paths that expose secret values in process arguments unless the Locker CLI supports a safer stdin or file-descriptor mechanism.

## Reference(s):

- [Locker Vault skill page](https://clawhub.ai/moskoweb/skills/locker-vault)
- [Locker Secrets Manager CLI Reference](references/cli-reference.md)
- [Vault Patterns - Common Use Cases](references/vault-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize vault references and masked values rather than raw secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
