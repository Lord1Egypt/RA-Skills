## Description:

Use the Keevx API to convert images to videos with support for V and KL models, 720p/1080p/4K resolutions, audio generation, task creation, status queries, and batch image-to-video conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-xiling](https://clawhub.ai/user/baidu-xiling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to create videos from one or more images through the Keevx API, including local image upload, task creation, polling, and callback-based completion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected images, prompts, and generated-media requests to Keevx using the user's Keevx API key.

Mitigation: Use an environment variable or secrets manager for the API key, review Keevx handling and retention terms, and avoid uploading sensitive, private, proprietary, or unauthorized images unless those terms are acceptable.

Risk: Generated video and thumbnail URLs are retained for a limited time.

Mitigation: Download required generated media promptly and design downstream workflows to tolerate expired output URLs.

## Reference(s):

- [Keevx documentation](https://docs.keevx.com)
- [Keevx account and API key page](https://www.keevx.com/main/home)
- [ClawHub skill page](https://clawhub.ai/baidu-xiling/skills/keevx-image-to-video)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown with curl commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses KEEVX_API_KEY for authenticated Keevx API requests and may return task IDs, status values, video URLs, and thumbnail URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
