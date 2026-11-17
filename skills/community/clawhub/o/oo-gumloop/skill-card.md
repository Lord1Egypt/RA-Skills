## Description:

Use this skill for Gumloop requests to read, create, update, or delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Gumloop flows and run them through a connected Gumloop account. Actions that start or stop flows require the skill's confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI may execute unverified code.

Mitigation: Review and approve the installation separately, preferably using a pinned, verified release.

Risk: The integration relies on OOMOL with access to the connected Gumloop account and task data, and CLI startup synchronization can make broader changes to agent skills.

Mitigation: Review the CLI's automatic skill installation and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Starting or stopping Gumloop flows can change state or stop running work.

Mitigation: Keep the skill's confirmation requirements for start and stop actions.

## Reference(s):

- [Gumloop API authentication documentation](https://docs.gumloop.com/api-reference/authentication)
- [Gumloop](https://www.gumloop.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON payloads and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gumloop action results are returned as JSON.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
