## Description:

Search and read MoonClerk customers, payment forms, and payments through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and finance users can use this skill to retrieve MoonClerk customer, payment form, and payment records through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup offers remote installers whose code was not verified in the security review.

Mitigation: Use a separately approved, verified CLI installation and check whether it automatically installs agent skills before running setup.

Risk: The connected account can expose sensitive MoonClerk customer and payment records to the skill's agent workflow.

Mitigation: Use an approved OOMOL connection with only the access needed, and request only the records relevant to the task.

## Reference(s):

- [MoonClerk](https://moonclerk.com)
- [MoonClerk API documentation](https://github.com/moonclerk/developer)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON responses and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only customer, payment form, and payment data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
