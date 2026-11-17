## Description:

Use the Keevx API to generate images from prompts and reference images with configurable mode, quality, aspect ratio, batch generation, and task status querying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-xiling](https://clawhub.ai/user/baidu-xiling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through creating images with Keevx from text prompts and optional reference images, including uploading local references, submitting generation tasks, polling status, and handling results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images are sent to the Keevx service.

Mitigation: Avoid sensitive, private, regulated, or confidential prompts and images unless Keevx's terms and data handling are acceptable for the use case.

Risk: Local reference images are uploaded to an external API before generation.

Mitigation: Review each local file before upload and limit reference images to content that is appropriate to share with Keevx.

Risk: Callback URLs receive asynchronous task completion data.

Mitigation: Use callback URLs only when the destination is trusted and expected to receive generated image metadata.

Risk: Generated image URLs are retained for 7 days according to the artifact guidance.

Mitigation: Download required outputs promptly and avoid relying on generated URLs as durable storage.

## Reference(s):

- [Keevx Documentation](https://docs.keevx.com)
- [Keevx Home](https://www.keevx.com/main/home)
- [Keevx API Base](https://api.keevx.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/baidu-xiling/skills/keevx-image-generate)
- [Publisher Profile](https://clawhub.ai/user/baidu-xiling)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Keevx API request examples, upload instructions, polling guidance, callback handling, and generated image result URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
