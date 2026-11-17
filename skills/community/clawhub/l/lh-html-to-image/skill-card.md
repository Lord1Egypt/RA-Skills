## Description:

Converts HTML and CSS into PNG images by guiding an agent to create local HTML files and capture them with Chrome headless screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhedev](https://clawhub.ai/user/liuhedev)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to produce text-heavy visual assets such as covers, posters, info cards, quote cards, and comparison cards from controlled HTML/CSS layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to appear for general poster or image requests where HTML/CSS screenshot rendering is not intended.

Mitigation: Confirm that the task needs local HTML/CSS rendering before using the skill, and use an image generation tool instead for illustrations or photos.

Risk: The workflow creates local HTML files and runs Chrome headless to render screenshots.

Mitigation: Review generated HTML and file paths before execution, and run Chrome only against trusted local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhedev/skills/lh-html-to-image)
- [Project homepage](https://github.com/liuhedev/lh-openclaw-kit)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML, CSS, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML files and PNG screenshots using Chrome or Chromium headless execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
