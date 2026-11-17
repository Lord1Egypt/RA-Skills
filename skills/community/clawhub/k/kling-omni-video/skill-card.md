## Description:

Generates or edits videos with the Kling Omni-Video API through a shell workflow for task submission, status polling, and video download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gayyzxyx](https://clawhub.ai/user/gayyzxyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create text-to-video, image-to-video, video editing, and video-reference generation requests for Kling Omni-Video. The skill produces the shell command workflow needed to submit the request, wait for completion, and save the resulting video file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe numeric option handling may allow invalid polling, timeout, or duration values to reach the shell workflow.

Mitigation: Validate numeric options before execution and reject non-numeric, negative, or out-of-range values.

Risk: A configurable API base URL can route API requests and bearer credentials to an unintended endpoint.

Mitigation: Restrict the API base URL to the intended HTTPS host before use and avoid overriding it in untrusted environments.

Risk: Prompts, image URLs, base64 images, and video URLs may be sent to the configured provider.

Mitigation: Do not submit private prompts, internal URLs, confidential images, or sensitive videos unless sharing them with the configured provider is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gayyzxyx/skills/kling-omni-video)
- [Publisher profile](https://clawhub.ai/user/gayyzxyx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HSAI_API_KEY, curl, and python3; the script may download an MP4 file after the remote task completes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
