## Description:

Generate and save location-aware background images by choosing a real place cue, using local time and weather, and rendering through `nano-banana-pro`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chadnewbry](https://clawhub.ai/user/chadnewbry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to create finished location-aware background images for apps, dashboards, wallpapers, and mockups with explicit output paths and style constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gemini API key and uses Nano Banana Pro as the renderer.

Mitigation: Install and run it only when you are comfortable providing that credential and using that rendering provider.

Risk: Prompt details or reference images may be sent to the image-generation provider to complete the render.

Mitigation: Avoid providing sensitive prompt content or reference images unless that provider use is acceptable.

Risk: Generated images are saved locally.

Mitigation: Choose output paths intentionally and review generated files before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chadnewbry/skills/location-aware-backgrounds)
- [OpenClaw homepage](https://clawhub.ai/chadnewbry/location-aware-backgrounds)
- [Prompt patterns](references/prompt-patterns.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [PNG image files with Markdown rationale, exact prompts, saved paths, and production recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Nano Banana Pro for rendering and saves generated images locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
