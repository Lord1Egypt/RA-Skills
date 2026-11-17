## Description:

Generate AI videos via GoAI API for text-to-video and image-to-video requests, including Chinese-language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goai](https://clawhub.ai/user/goai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate AI video clips from text prompts or optional image references through the GoAI API. It preserves the user's original prompt language and returns both the saved media path and public media URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or compromised API endpoint could influence the server-provided task ID used in the downloaded video filename and overwrite unexpected local files.

Mitigation: Run the skill from a workspace where generated media files can be safely written, use the default GoAI endpoint unless another endpoint is intentionally trusted, and confine downloads to a dedicated output directory before routine use.

Risk: Local image references are uploaded to GoAI when image-to-video generation is requested.

Mitigation: Avoid passing sensitive local images unless the user is comfortable uploading them to GoAI.

## Reference(s):

- [GoAI homepage](https://mustgoai.com)
- [ClawHub skill page](https://clawhub.ai/goai/skills/goai-video-gen)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated media file paths and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On success, emits MEDIA, MEDIA_URL, RESULT_PATH, and RESULT_URL lines; generated media is saved as an MP4 file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
