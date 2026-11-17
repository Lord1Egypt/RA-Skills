## Description:

Converts Chinese math textbook screenshots or text with formulas into giscus and GitHub Discussion compatible Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuancaoyaohw](https://clawhub.ai/user/yuancaoyaohw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and technical writers use this skill to convert Chinese math screenshots or pasted formula text into Markdown that renders reliably in giscus and GitHub Discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File delivery can overwrite local content if an output path is chosen carelessly.

Mitigation: Confirm the destination path before writing converted Markdown and avoid overwriting existing files.

Risk: GitHub rendering checks can touch external repositories or discussions.

Mitigation: Run rendering checks only against content and repositories the user controls.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/yuancaoyaoHW/math-screenshot-to-giscus)
- [ClawHub skill release page](https://clawhub.ai/yuancaoyaohw/skills/math-screenshot-to-giscus)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown source with rendered preview guidance; file output may be used for complex formula conversions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on GitHub MathJax and giscus formatting, including double backslashes for LaTeX commands and alternatives for unsupported matrix environments.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
