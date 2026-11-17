## Description:

Generate and edit images with Google's Nano Banana 2 image model through Atlas Cloud or Google AI Studio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate new images, edit existing images, and create visual assets such as sprites, thumbnails, banners, logos, product photos, illustrations, and concept art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and selected images are sent to Atlas Cloud or Google AI Studio.

Mitigation: Use the skill only when those uploads are intended, and avoid confidential, regulated, or highly personal images unless they are approved for those services.

Risk: Atlas Cloud image editing can upload local files to temporary provider storage.

Mitigation: Confirm with the user before uploading local files and upload only files the user explicitly approves.

Risk: The skill requires Atlas Cloud or Google AI Studio API keys.

Mitigation: Provide keys through environment variables and avoid embedding credentials in prompts, files, or command examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/nano-banana-2-skill)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are downloaded to local output files; provider responses may also include text status messages.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
