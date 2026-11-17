## Description:

Mailjet (mailjet.com). Use this skill for ANY Mailjet request — reading, creating, and updating data. Whenever a task involves Mailjet, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Mailjet contacts and create or update contact records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute an unverified online installer.

Mitigation: Review and approve CLI installation separately; prefer a verified release and check its effects on other installed agent skills.

Risk: Mailjet contact creation and updates change account data.

Mitigation: Confirm the connected account and the exact payload and effect of each proposed write.

## Reference(s):

- [Mailjet API authentication documentation](https://dev.mailjet.com/email/reference/overview/authentication/)
- [Mailjet](https://www.mailjet.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector payloads and results, with Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve contacts; create and update actions change contact records and require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
