## Description:

waboxapp (waboxapp.com). Use this skill for ANY waboxapp request — reading, creating, and updating data. Whenever a task involves waboxapp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can check the status of a connected Waboxapp account and send WhatsApp text messages, links, images, or files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified remote code and may add agent skills without clearly explaining those changes.

Mitigation: Review and verify the CLI installation separately, inspect any added skills, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Sending a message or media changes the connected account's external state.

Mitigation: Confirm the connected account, recipient, and exact message or media before sending.

## Reference(s):

- [Waboxapp homepage](https://www.waboxapp.com)
- [Waboxapp API documentation](https://www.waboxapp.com/assets/doc/waboxapp-API-v3.pdf)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-waboxapp)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON connector responses summarized in user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads account status and sends text or media through the connected account.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
