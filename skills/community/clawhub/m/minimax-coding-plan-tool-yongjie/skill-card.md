## Description:

MiniMax Token Plan tool for image generation, image understanding, text-to-speech, video generation, and web search through direct MiniMax API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call MiniMax Token Plan capabilities from OpenClaw workflows for web search, image analysis, image generation, and documented media-generation tasks that require a MiniMax/OpenClaw credential.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published documentation includes a full credential-like token and security evidence marks the release as suspicious.

Mitigation: Do not install this version as written; remove and rotate the embedded token, then configure only a user-owned MINIMAX_API_KEY.

Risk: Image-understanding requests can upload local image files to MiniMax when a file path is provided.

Mitigation: Review image paths and file contents before use, and avoid sending confidential or regulated images unless the deployment has approved data-handling controls.

Risk: The documentation describes video generation as asynchronous and notes that progress querying may not be supported through the Token Plan API.

Mitigation: Verify video-generation completion and retrieval behavior in the target environment before relying on it for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/minimax-coding-plan-tool-yongjie)

## Skill Output:

**Output Type(s):** [text, JSON, image URLs, audio, task status]

**Output Format:** [JSON responses with search results, image analysis text, image URLs, base64 audio data, or asynchronous task identifiers depending on the invoked tool.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and MINIMAX_API_KEY; local image paths can be encoded and sent to MiniMax for image-understanding requests.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
