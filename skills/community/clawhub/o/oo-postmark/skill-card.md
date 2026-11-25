## Description:

Postmark (postmarkapp.com). Use this skill for ANY Postmark request — reading, creating, and updating data. Whenever a task involves Postmark, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Postmark server and message data, validate and manage templates, and send transactional email through a connected Postmark account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-dependency setup runs a remote CLI installer whose behavior has not been verified.

Mitigation: Review and independently verify the installer before allowing setup to run it.

Risk: Email sending and template changes can affect Postmark data and recipients.

Mitigation: Keep the skill's confirmation step and verify the exact action and payload before sending or changing templates.

## Reference(s):

- [Postmark](https://postmarkapp.com)
- [Postmark developer documentation](https://postmarkapp.com/developer)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Postmark skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-postmark)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Postmark data as JSON or concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send email or change templates require confirmation of the exact action and payload.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
