## Description:

Use Simplesat to read, create, and update customer and survey data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and customer support teams use this skill to review Simplesat customers, surveys, questions, and responses, and to create or update customers or schedule survey emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified remote code, and startup skill synchronization may add skills without a clear approval step.

Mitigation: Review and approve CLI installation separately using a verified release; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI.

Risk: The connected account may expose customer information, and write actions can update customer records or schedule survey emails.

Mitigation: Connect only the intended Simplesat account, review customer updates and survey emails, and confirm the exact write action before execution.

## Reference(s):

- [Simplesat API documentation](https://developer.simplesat.io/api)
- [Simplesat](https://www.simplesat.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands]

**Output Format:** [JSON connector requests and responses, with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read customer and survey data, update customers, or schedule survey emails; write actions require confirmation according to the skill guidance.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
