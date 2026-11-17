## Description:

Manga Animation guides an agent through a checkpointed manga-video workflow from story idea to script, storyboard, character prompts, Ark-generated images, and image-to-video clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a574824551](https://clawhub.ai/user/a574824551)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and creative teams use this skill to turn a story idea or existing script into manga-animation production assets with review checkpoints before Ark image and video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story text, prompts, images, and generated media requests may be sent to Volcengine Ark.

Mitigation: Use the skill only when sending that content to Ark is acceptable, and review the script, storyboard, prompts, and media inputs before API calls.

Risk: API credentials may be exposed if pasted into scripts.

Mitigation: Set ARK_API_KEY through the environment and avoid storing keys directly in source files.

Risk: A storyboard.json reference_image path can cause a local image file to be uploaded during video generation.

Mitigation: Run video generation only on storyboard.json files you created or reviewed, and verify each reference_image path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a574824551/skills/polecomic)
- [Volcengine Ark console](https://console.volcengine.com/ark)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)
- [Script template](references/script-template.md)
- [Storyboard guide](references/storyboard-guide.md)
- [Character guide](references/character-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON storyboard files, Python command examples, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged review checkpoints and may update storyboard.json with generated image paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
