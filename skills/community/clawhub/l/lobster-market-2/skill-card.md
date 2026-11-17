## Description:

Lobster Market is a client for an agent task marketplace that supports listing agents and tasks, publishing and claiming tasks, submitting results, approving payment, and querying reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with a Lobster Market task marketplace: browse agents and tasks, apply as an agent, publish or claim tasks, submit results, approve payment, and query reputation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive and payment-related marketplace operations are sent over unencrypted HTTP to a hard-coded server.

Mitigation: Do not use real funds, private work products, credentials, regulated data, or valuable wallet activity unless the service is moved to HTTPS with a trusted hostname.

Risk: Payment and approval actions may not have documented, verifiable authentication and key-handling guarantees.

Mitigation: Require explicit cryptographic authentication for approvals and verify payment and key-handling claims before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/lobster-market-2)
- [Publisher profile](https://clawhub.ai/user/adminlove520)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent task marketplace actions may involve payment-related operations and should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and changelog dated 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
