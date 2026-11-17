## Description:

image-deck helps agents create PowerPoint-style slide decks, single slides, and carousel presentations as full-slide raster images using Codex built-in image_gen (GPT Image 2), with planning, prompt review, sample approval, slide QA, and optional PPTX/PDF assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tseng71](https://clawhub.ai/user/tseng71)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-producing agents use this skill to plan and generate visual PPT, PowerPoint-style, slide deck, single-slide, and carousel deliverables where each page is a complete generated image. It is best suited for polished image-based presentations rather than editable charts, dense tables, or text-heavy slides that must remain editable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deck pages are raster images, so slide text, charts, and dense tables are not fully editable after generation.

Mitigation: Use this skill for visual slide decks and route exact editable charts, dense tables, or editable text requirements to a normal presentation workflow.

Risk: Prompt, research, and generation log files can contain source material from the user or generated deck plan.

Mitigation: Treat these files as local work artifacts, review them before sharing, and remove sensitive source material when it is no longer needed.

Risk: The optional PPTX slide-number helper has a reported XML input validation weakness for untrusted presentations or complex font names.

Mitigation: Run the helper only on trusted PPTX files and use simple font names until validation is tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tseng71/skills/image-deck)
- [Prompt Patterns](references/prompt-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown planning guidance and prompts, generated raster slide image files, and optional PPTX/PDF presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slide images contain visible text inside the raster image; PPTX output is image-based and is not fully editable except for optional native slide-number fields.]

## Skill Version(s):

0.1.32 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
