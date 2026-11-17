## Description:

Passlane helps agents retrieve credentials, payment cards, secure notes, and just-in-time TOTP codes from a Keepass-backed passlane vault for login automation and local credential audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[passlane](https://clawhub.ai/user/passlane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Passlane to automate authenticated workflows by retrieving exact vault entries, current 2FA codes, or structured credential data from a local passlane vault. It is suited to login scripting and local credential audits where the user has already unlocked the relevant vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant agents broad access to highly sensitive vault data.

Mitigation: Install it only for specific login or audit tasks, keep vaults locked when not needed, and use exact anchored selectors.

Risk: Credentials and TOTP codes can be exposed through logs, files, command history, or process arguments.

Mitigation: Pipe secrets directly to consumers, capture them only in local variables when necessary, avoid broad list or export operations, and do not print or commit secret output.

Risk: TOTP codes expire quickly and cached codes may fail or be reused inappropriately.

Mitigation: Fetch TOTP codes just before each use and re-fetch on retries instead of caching them.

Risk: Locked or ambiguous vault lookups can block unattended automation or produce unusable output.

Mitigation: Require the user to unlock the relevant vault first, use anchored regex selectors, and stop on passlane exit code 1.

## Reference(s):

- [Automation Examples](references/automation-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/passlane/skills/passlane)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and automation patterns.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secrets are intended for direct local consumption and should not be logged, cached, committed, or passed through exposed process arguments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
