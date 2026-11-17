## Description:

Converts Markdown content into presentation slides with standard Markdown import, theme options, and PowerPoint-compatible export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and presentation authors use this skill to convert Markdown notes or outlines into slide decks for business reports, teaching materials, meetings, or talks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML fallback may preserve active embedded HTML from source Markdown.

Mitigation: Avoid converting untrusted Markdown when python-pptx is unavailable, or inspect the generated HTML before opening it in a browser.

Risk: The skill runs a local converter script over user-provided Markdown input.

Mitigation: Install and run it only in environments where local file conversion scripts are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/md-to-slides)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with command-line examples and generated PPTX or HTML presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates PowerPoint-compatible .pptx output when python-pptx is installed; otherwise writes an HTML presentation fallback.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
