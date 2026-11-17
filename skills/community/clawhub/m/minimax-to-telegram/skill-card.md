## Description:

Generate images, audio, and video using MiniMax MCP and send the generated media to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyin258](https://clawhub.ai/user/hoyin258)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to configure MiniMax MCP media generation and deliver generated images, audio, video, or music to Telegram chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned third-party npm and MCP tooling may change behavior or introduce package supply-chain risk.

Mitigation: Pin or verify mcporter and minimax-mcp before installation, and review the skill before deployment.

Risk: The MiniMax API key can grant access to paid or sensitive media-generation capabilities.

Mitigation: Use a least-privileged API key, store it in environment or configuration secrets, and avoid logging it.

Risk: Signed MiniMax media URLs include authentication query parameters and can expose generated media if shared too broadly.

Mitigation: Send complete signed URLs only to the intended Telegram destination, avoid posting them elsewhere, and regenerate expired links when needed.

Risk: Generated media sent to Telegram is accessible to Telegram and the selected recipients.

Mitigation: Confirm recipient chat IDs and avoid sending sensitive generated content unless Telegram and the recipients are acceptable disclosure paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoyin258/skills/minimax-to-telegram)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and Python-style code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers MiniMax MCP setup, media generation commands, Telegram delivery steps, timeout handling, and Cantonese audio parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
