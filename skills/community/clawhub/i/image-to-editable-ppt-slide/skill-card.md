## Description:

Rebuild one or more reference images as visually matching editable PowerPoint slides using native shapes, text, fills, and layout instead of a flat screenshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benjaminlee](https://clawhub.ai/user/benjaminlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to convert reference images such as flowcharts, dashboards, infographics, process diagrams, and designed slides into editable PowerPoint decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to commit workspace changes automatically.

Mitigation: Use it in a clean workspace and require explicit approval of staged files before any git commit.

Risk: The workflow reads local reference material and writes local PPTX, JSON, and helper script files.

Mitigation: Run it only on files intended for conversion and review generated files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benjaminlee/skills/image-to-editable-ppt-slide)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and JSON snippets, shell commands, generated JSON specs, helper scripts, and editable PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PowerPoint decks should remain editable through native shapes, text boxes, fills, lines, and layout objects.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
