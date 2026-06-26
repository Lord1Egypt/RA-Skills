## Description: <br>
Manage LinkedIn presence via the LinkedIn API. Create posts and articles, manage comments, handle media uploads, search ad targeting entities, and retrieve user profile and image data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage a connected LinkedIn account through ClawLink, including profile lookup, posting, comments, media retrieval, and ad targeting discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a connected LinkedIn account through ClawLink, including publishing comments or posts and deleting content. <br>
Mitigation: Review previews carefully and confirm only write or delete actions that match the intended target and effect. <br>
Risk: LinkedIn organization posting and ad targeting actions may fail or behave differently when the connected account lacks the required role, scope, or Marketing API access. <br>
Mitigation: Verify account permissions before using organization posting or ad targeting workflows, and report the real tool error if permission checks fail. <br>


## Reference(s): <br>
- [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/) <br>
- [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/linkedin-social) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected LinkedIn account through ClawLink; write and delete actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
