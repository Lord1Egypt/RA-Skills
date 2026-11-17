## Description:

Generate and convert icons. Use when creating SVGs, building sprite sheets, converting ICO/PNG/SVG, or generating favicon sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate SVG icons, assemble sprite sheets, convert icon formats, resize assets, search built-in icon names, and create favicon sets for web and app projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe script inputs may lead to local command execution or writes outside the intended output directory.

Mitigation: Use only trusted icon names, sizes, colors, prefixes, output paths, and source files until the script validates numeric dimensions and constrains filenames to safe basenames.

Risk: Processing untrusted SVG or XML content may expose the agent environment to unsafe file content.

Mitigation: Process only trusted SVGs until SVG/XML sanitization is added; review generated files before using them in downstream projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/icon)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [Publisher homepage](https://bytesagain.com)
- [Feedback page](https://bytesagain.com/feedback/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts include SVG, PNG, ICO, sprite sheet SVG, web manifest JSON, and HTML snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes icon assets and favicon files to caller-selected output paths when its shell script is executed.]

## Skill Version(s):

3.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
