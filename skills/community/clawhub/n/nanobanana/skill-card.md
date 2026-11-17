## Description:

Nano Banana 2 Pro helps agents generate images, edit images from an input file, and run multimodal or text chat through the configured Nano Banana API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxunjinmu](https://clawhub.ai/user/moxunjinmu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users can use this skill to call a Nano Banana-compatible image API for prompt-based image generation, image editing from a local input image, and text or multimodal chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and the configured bearer token are sent to the third-party endpoint claw.cjcook.site.

Mitigation: Install only if you trust that service operator; use a dedicated, revocable token and avoid sensitive or private images unless privacy and retention practices are verified.

Risk: The security verdict is suspicious because the skill lacks enough privacy and trust-boundary guidance for the external image service.

Mitigation: Review the configured service, token handling, and data-sharing expectations before deploying the skill in a sensitive workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moxunjinmu/skills/nanobanana)
- [Nano Banana API Endpoint](https://claw.cjcook.site/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, API Calls]

**Output Format:** [Console text with saved JPEG image files when image responses are returned]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated images to an output directory and may return text content from the API response.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
