## Description:

Generate AI videos via Pixmind API (text-to-video and image-to-video).

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate videos from text prompts or animate reference images through the Pixmind API, then poll task status for generated video and cover URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Pixmind API key, prompts, task IDs, generation settings, and any reference image URLs to Pixmind's aihub-admin.aimix.pro gateway.

Mitigation: Use the skill only when you trust Pixmind with that data; avoid confidential prompts or private image URLs, and rotate the API key if exposure is suspected.

Risk: Video generation can fail when a model, resolution, aspect ratio, or duration is unsupported by the selected Pixmind model.

Mitigation: Use the documented supported model table and validate required parameters, especially Seedance resolution and Sora duration, before submitting a generation request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuyunzhishang/skills/pixmind-video)
- [Publisher profile](https://clawhub.ai/user/fuyunzhishang)
- [Pixmind](https://www.pixmind.io)
- [Pixmind API Platform dashboard](https://www.pixmind.io/api-platform/dashboard/keys)
- [Pixmind API gateway](https://aihub-admin.aimix.pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Pixmind task IDs plus generated video and cover URLs when tasks complete.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
