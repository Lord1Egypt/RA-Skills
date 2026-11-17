## Description:

TwitterAPI.io (twitterapi.io). Use this skill for ANY TwitterAPI.io request — reading, creating, updating, and deleting data. Whenever a task involves TwitterAPI.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search and retrieve X data and manage TwitterAPI.io monitoring or filter settings through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing oo CLI dependency may trigger installation of unverified remote code without clear user approval.

Mitigation: Install and verify the CLI separately, prevent automatic installer execution, and review its effects before running it.

Risk: Monitoring and filter changes can modify or delete TwitterAPI.io settings.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for destructive actions.

## Reference(s):

- [TwitterAPI.io documentation](https://docs.twitterapi.io/)
- [TwitterAPI.io](https://twitterapi.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Usage guidance]

**Output Format:** [JSON API responses and shell commands, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return provider data; state-changing actions require review and approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
