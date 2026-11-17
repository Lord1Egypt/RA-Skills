## Description:

Generates images from text prompts with MiniMax image-01 models and saves the results as local image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create generated images for UI mockups, icons, illustrations, diagrams, concept art, placeholders, documentation, and other visual assets from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an undisclosed hardcoded MiniMax credential and insecure secret-handling guidance.

Mitigation: Install only after the embedded credential is removed and rotated, and require users to provide their own key through MINIMAX_API_KEY.

Risk: Prompt text is sent to MiniMax during image generation.

Mitigation: Avoid sensitive prompt content unless the user is comfortable sending it to MiniMax.

Risk: The scripts write generated image files to local output paths.

Mitigation: Choose output paths carefully and review paths before running generation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/skills/minimax-image-gyh)
- [MiniMax Image Skill Reference](artifact/reference.md)
- [MiniMax Image Skill Usage Examples](artifact/examples.md)
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image files with terminal status text and saved file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt, model, size, aspect ratio, image count, and output path influence generation and local file output.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
