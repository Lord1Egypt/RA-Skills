## Description:

This skill uploads Instagram image posts through browser automation in an active OpenClaw browser session, including image upload, caption entry, optional collaborator tagging, and sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to prepare and publish Instagram image posts through an active OpenClaw browser session. It supports image upload, caption entry, collaborator tagging, and sharing when the user is already logged in to Instagram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content from a real logged-in Instagram account without a built-in final approval step.

Mitigation: Confirm the active Instagram account, selected images, caption, and collaborators before running the upload flow.

Risk: The browser session may be logged in to an unintended Instagram account.

Mitigation: Check the visible Instagram account in the browser before upload and use a dedicated browser profile for publishing workflows when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/insta-post)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown instructions with shell commands and JavaScript automation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script execution may return JSON status for upload success, uncertainty, or failure.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
