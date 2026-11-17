## Description:

Prospeo (prospeo.io). Use this skill for ANY Prospeo request — searching and reading data. Whenever a task involves Prospeo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operators use this skill to search Prospeo people and companies, enrich person or company records, inspect account information, and retrieve search suggestions through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may run downloaded code whose exact remote contents are unverified.

Mitigation: Install and verify oo separately, and require approval before running either setup installer.

Risk: The CLI may have additional skill-installation behavior.

Mitigation: Review that behavior before using the CLI, and send only identifiers needed for the requested action through OOMOL to Prospeo.

## Reference(s):

- [Prospeo](https://prospeo.io)
- [Prospeo API documentation](https://prospeo.io/api-docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance, shell commands, and structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the connected Prospeo account; results are returned as structured data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
