## Description:

Generate whiteboard-style presentations with Chinese-first slide content by using Nano Banana Pro images and PptxGenJS-based PPT assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamsky](https://clawhub.ai/user/dreamsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to plan and generate professional whiteboard-style PPT decks with Chinese primary text, generated slide images, and a 16:9 PowerPoint output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm dependency for PPT generation.

Mitigation: Pin pptxgenjs in package.json and use a lockfile for repeatable builds.

Risk: The skill is designed for Chinese-first slide content, which may not match every audience or locale.

Mitigation: Override the language requirement in the user request when another primary language is needed.

Risk: Generated slide images may contain unclear text or inconsistent whiteboard styling.

Mitigation: Review generated images before PPT assembly and regenerate slides with explicit resolution, readability, and style constraints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamsky/skills/ppt-with-nano-banana)
- [Publisher profile](https://clawhub.ai/user/dreamsky)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with prompt templates, JavaScript code blocks, shell commands, and file-organization guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generated slide images and PPT assembly; final presentation files depend on the user's local image generation and PptxGenJS workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
