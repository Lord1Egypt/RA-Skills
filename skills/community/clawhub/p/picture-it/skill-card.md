## Description:

Picture it! helps agents plan and run picture-it CLI workflows to generate, edit, composite, crop, and post-process images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geongeorge](https://clawhub.ai/user/geongeorge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and revise visual assets such as blog headers, social cards, thumbnails, posters, product comparisons, and edited photos from terminal-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI image operations upload user images to fal.ai and may expose sensitive visual data to an external processor.

Mitigation: Use local-only commands for sensitive images, and run generate/edit/remove-bg/upscale only when the user accepts fal.ai processing.

Risk: A global npm install without a pinned version can change behavior across installs.

Mitigation: Pin picture-it to a reviewed exact version and avoid sudo or administrator installs.

Risk: FAL-backed workflows can incur avoidable usage costs when image direction or pipeline steps are unclear.

Mitigation: Clarify the desired visual direction, present a few options, and plan the minimum required FAL calls before running commands.

## Reference(s):

- [Picture it! ClawHub skill page](https://clawhub.ai/geongeorge/skills/picture-it)
- [picture-it GitHub homepage](https://github.com/geongeorge/picture-it)
- [picture-it npm package](https://www.npmjs.com/package/picture-it)
- [fal.ai privacy policy](https://fal.ai/privacy)
- [Composition Guide](references/composition-guide.md)
- [Prompt Library](references/prompt-library.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and occasional JSON overlay examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image file paths from picture-it command stdout; AI operations require FAL_KEY and network access to fal.ai.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
