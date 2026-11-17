## Description:

Automates the Golden Hour Instagram engagement workflow by watching comments on a Reel or Post for a specified keyword and then sending a DM and public reply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to configure and run an Instagram comment-to-DM automation for a specified media item, keyword, message, and duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Instagram DMs and public replies automatically from a business account.

Mitigation: Use it only when this automation is intended, review the DM and reply text before running, and monitor the session.

Risk: The skill relies on a long-lived Instagram Graph API access token.

Mitigation: Use a least-privileged token, keep it out of source control, and rotate it if exposed.

Risk: The skill can send an extra OpenClaw webchat notification after a successful action.

Mitigation: Remove or disable that notification path if it is not intended for the deployment.

Risk: Token handling and social posting automation require careful review before installation.

Mitigation: Review the skill before deployment and prefer safer authorization-header handling where supported.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Instagram Graph API credentials, a target media ID, a trigger keyword, message text, and a polling duration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
