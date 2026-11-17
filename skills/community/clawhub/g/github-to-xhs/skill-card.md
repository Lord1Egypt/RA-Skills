## Description:

Analyze a GitHub repository and generate Xiaohongshu (Little Red Book) infographic posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn GitHub repositories into social-media-ready Xiaohongshu content, including project analysis, visual outline strategies, image prompts, and HTML card layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository URL handling may allow unexpected paths or output locations.

Mitigation: Use only trusted GitHub URLs and review the generated file paths before running the bundled script.

Risk: Generated HTML can contain repository-derived content intended for publication.

Mitigation: Inspect generated HTML and social copy before opening, screenshotting, or sharing it.

Risk: The security verdict is suspicious due to unsafe URL handling and file-writing behavior.

Mitigation: Review or harden the bundled script before installing it in a shared or production agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laojun509/skills/github-to-xhs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, HTML, image-generation prompts, and archive packaging guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a repository-specific output directory with analysis, alternative outline strategies, prompt files, and a Xiaohongshu post HTML file.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
