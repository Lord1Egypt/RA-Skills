## Description:

Mails (mails.so). Use this skill for ANY Mails request — reading, creating, and updating data. Whenever a task involves Mails, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to validate a single email address or create and retrieve a batch email validation job through a connected Mails account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can change other agent skills, a behavior not clearly disclosed by this skill.

Mitigation: Review and install the CLI yourself; set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations to prevent skill changes.

Risk: Email addresses and connected credentials may be exposed to OOMOL, while remote installers and the hosted backend are outside the inspected bundle; batch payloads may also incur costs.

Mitigation: Consider OOMOL's access to submitted addresses and connected credentials, and review batch payloads and costs before approval.

## Reference(s):

- [Mails homepage](https://mails.so)
- [Mails API authentication documentation](https://docs.mails.so/authentication/)
- [oo CLI controls documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-mails-so)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a connected Mails account; batch validation creates a job.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
