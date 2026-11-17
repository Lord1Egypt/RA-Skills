## Description:

Use Omise to review account balances, charges, and customers, and to manage customer records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support or operations teams use this skill to inspect Omise account data and manage customer records through guided actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute installer downloads whose contents have not been verified.

Mitigation: Review the installer and use a pinned CLI release before installation.

Risk: Setup may make broader changes to skills installed across agents.

Mitigation: Explicitly control which bundled skills are deployed to agents.

Risk: Customer updates or deletions can change or remove Omise records.

Mitigation: Confirm the exact target and effect before customer writes or deletions.

## Reference(s):

- [Omise API documentation](https://docs.omise.co)
- [Omise homepage](https://www.omise.co)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes action guidance and JSON-formatted connector responses.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
