## Description: <br>
image-deck helps an agent create full-image slide decks, PPT-style presentations, single slides, and carousel pages with GPT Image 2 through Codex built-in image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tseng71](https://clawhub.ai/user/tseng71) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an image-generation workflow for slide decks where each page is a complete raster slide with text and visuals generated together. It is best suited for presentation, PPT, carousel, and deck requests that do not require editable PowerPoint text boxes, tables, or charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates slides as complete raster images, so visible text, charts, and layout elements are not editable PowerPoint objects after generation. <br>
Mitigation: Use it only when image-based slides are acceptable; route to a normal editable presentation workflow when editable text boxes, precise tables, or exact chart data are required. <br>
Risk: Image-generation prompts and local work files may contain source material supplied by the user. <br>
Mitigation: Review the inline prompt groups before approval, choose the language explicitly, and avoid sensitive source material unless it is appropriate for the image-generation workflow and local logs. <br>
Risk: Generated in-image text may be inaccurate, unreadable, or mismatched to the selected content-density mode. <br>
Mitigation: Inspect generated slides and regenerate any page with text errors, low readability, style drift, or density mismatch instead of overlaying corrections locally. <br>


## Reference(s): <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tseng71/image-deck) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with prompt templates, review checklists, and optional shell commands for installation or packaging] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to produce slide-by-slide design documents, image-generation prompts, generated slide images, image-generation logs, and optionally assembled PPTX or PDF files.] <br>

## Skill Version(s): <br>
0.1.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
