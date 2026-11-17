## Description:

Use Assured Platform through an OOMOL-connected account to search and read platform data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to inspect their Assured Platform account, retrieve task details, and list tasks through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installation code without a clear approval step and may add other agent skills.

Mitigation: Review setup before installing, install a verified CLI release yourself, and disable automatic skill synchronization unless you want it to add other skills. Connect only the Assured Platform access you intend OOMOL to use.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Assured Platform](https://www.withassured.com)
- [Assured Platform API documentation](https://developers.withassured.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured platform data summarized in natural language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account and task data; requires the oo CLI and an active Assured Platform connection.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
