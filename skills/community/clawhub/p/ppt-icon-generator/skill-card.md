## Description:

Generate or search PNG transparent icons for PowerPoint presentations, including Iconify search, SVG-to-PNG conversion, and simple prompt-, shape-, or text-based icon generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to find, generate, convert, and verify transparent icon assets for PowerPoint slides and presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Icon searches and externally assisted prompt workflows may send search terms or prompt text to services such as Iconify, SimpleSVG, or Copilot.

Mitigation: Avoid sensitive presentation content in search queries or prompts, and use local shape or text generation when the request should stay local.

Risk: PNG generation or download can fall back to SVG output when conversion dependencies are unavailable.

Mitigation: Verify the final file format, size, and transparency with the verification script before using the asset in a presentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/ppt-icon-generator)
- [Iconify API](https://api.iconify.design/)
- [Copilot](https://copilot.microsoft.com)
- [SimpleSVG API](https://api.simplesvg.com/{prefix}/{name}.svg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG or SVG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are typically transparent icon assets sized by command-line options; PNG conversion can fall back to SVG when conversion dependencies are unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
