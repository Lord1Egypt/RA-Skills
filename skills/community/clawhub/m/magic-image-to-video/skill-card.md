## Description:

Generate a video task based on user-provided text and images (supports image URLs and local file paths), and submit it to a remote video service using an API Key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leizhang-magiclight](https://clawhub.ai/user/leizhang-magiclight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create a video generation task from a text prompt and an image, then receive the task ID and final video link from the remote MagicLight service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to the remote MagicLight service.

Mitigation: Avoid confidential images, secrets, and sensitive prompt content unless the user has approved sharing them with MagicLight.

Risk: The client may fetch arbitrary remote image URLs from the agent environment.

Mitigation: Use trusted image URLs and avoid internal, private, or unreviewed URLs.

Risk: Local image files can be uploaded to remote endpoints.

Mitigation: Review local file paths before execution and avoid uploading sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leizhang-magiclight/skills/magic-image-to-video)
- [MagicLight API service](https://open.magiclight.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown chat responses with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAGIC_API_KEY and a user-provided image URL or local image path.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
