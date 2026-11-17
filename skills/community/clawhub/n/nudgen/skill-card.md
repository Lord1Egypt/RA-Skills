## Description:

Nudgen equips agents to support AI-powered email retention, automation, marketing strategy, API workflows, CLI usage, and email-sending best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toannhu96](https://clawhub.ai/user/toannhu96)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketing operators, and automation engineers use this skill to integrate Nudgen APIs, operate the Nudgen CLI, and review email retention programs for deliverability, consent, and lifecycle strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install examples reference mutable remote code, including latest/default-branch and curl-to-bash style commands.

Mitigation: Review install commands before use, prefer pinned versions and project-scoped installs, and verify checksums or signatures in sensitive environments.

Risk: Nudgen API workflows use Personal Access Tokens.

Mitigation: Treat PATs as secrets, keep them server-side, avoid printing them, and store them in secure secret storage or the system keychain.

Risk: Team-scoped commands and API writes can affect the wrong team if context is stale.

Mitigation: Confirm active team context before delete or write operations and validate changes with a read or identity check.

Risk: Some CLI commands are documented as placeholder behavior.

Mitigation: Use command-specific help and prefer API or dashboard workflows when documented CLI behavior is incomplete.

Risk: Email automation can create deliverability, consent, or suppression failures if launched without operational checks.

Mitigation: Validate consent source, suppression states, tracking, unsubscribe behavior, stop rules, and sending metrics before broad sends.

## Reference(s):

- [Nudgen Skill Package](https://clawhub.ai/toannhu96/skills/nudgen)
- [Nudgen HTTP API Reference](skills/api/references/http-api.md)
- [Nudgen CLI Reference](skills/cli/references/cli.md)
- [Audience And Consent](skills/email-sending-best-practices/references/audience-and-consent.md)
- [Content And Design](skills/email-sending-best-practices/references/content-and-design.md)
- [Deliverability](skills/email-sending-best-practices/references/deliverability.md)
- [Email Types And Program Strategy](skills/email-sending-best-practices/references/email-types-and-program-strategy.md)
- [Nudgen Operational Caveats](skills/email-sending-best-practices/references/nudgen-operational-caveats.md)
- [Nudgen API Documentation](https://docs.nudgen.net/en/api-references)
- [Nudgen CLI README](https://github.com/Nudgen-Marketing/nudgen-cli/README.md)
- [Nudgen CLI Commands](https://github.com/Nudgen-Marketing/nudgen-cli/cmd)
- [Nudgen CLI API Client](https://github.com/Nudgen-Marketing/nudgen-cli/internal/api/client.go)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, API request examples, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI guidance, endpoint examples, validation steps, and operational caveats.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
