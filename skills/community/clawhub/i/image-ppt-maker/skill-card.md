## Description:

Turns presentation ideas into McKinsey-style outlines, consistent 16:9 slide images, a playable HTML deck, and duration-aware speaker scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmexhj](https://clawhub.ai/user/callmexhj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and presentation creators use this skill to turn a presentation brief into reviewed slide logic, generated 16:9 PPT-style images, a local HTML slideshow, and final spoken notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide content may be sent to image generation tools during the workflow.

Mitigation: Avoid sensitive or restricted content unless the user has approved that use and the image-generation environment is appropriate.

Risk: The workflow writes generated images and a playable HTML deck to local output directories.

Mitigation: Use a clean output directory and review generated files before sharing or publishing them.

Risk: Some prompts and player UI text are built around Chinese-language defaults.

Mitigation: Ask the agent to adapt the language when the deck or audience requires another locale.

## Reference(s):

- [Workflow](references/workflow.md)
- [McKinsey-Style Outline](references/mckinsey-outline.md)
- [Image-2 Prompt Rules](references/image-2-prompts.md)
- [Generate HTML Player](scripts/generate-html-player.mjs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown workflow outputs plus generated slide image files, prompt records, an HTML slideshow, and speaker notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one 16:9 image per approved slide and requires explicit approval gates before HTML assembly and final speaker notes.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
