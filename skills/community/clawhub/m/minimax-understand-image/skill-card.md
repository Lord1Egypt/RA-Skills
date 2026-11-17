## Description:

Uses MiniMax MCP to analyze images, describe visual content, identify objects, text, and scenes, and answer prompts about an image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure MiniMax credentials and call the MiniMax MCP understand_image tool against local image paths or URLs for visual question answering and image descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run remote installer commands.

Mitigation: Review setup commands before execution and prefer installing uv through a trusted package manager.

Risk: The skill launches an unpinned third-party MCP package with access to credentials and inherited environment variables.

Mitigation: Pin the MCP package version where possible and limit which environment variables are passed to the subprocess.

Risk: Images and prompts are sent to a third-party MiniMax service.

Mitigation: Avoid using the skill with sensitive screenshots, documents, or photos unless that data sharing is approved.

Risk: Mirror-based package installs can change the trusted supply-chain path.

Mitigation: Use mirror-based installs only when the mirror is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/minimax-understand-image)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and formatted JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an image path or URL and a text prompt; the helper script times out requests after 120 seconds.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
