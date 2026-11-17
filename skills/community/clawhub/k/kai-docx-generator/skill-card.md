## Description:

Generate professional .docx documents from Markdown text or fill data into .docx templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document automation users, and agents use this skill to convert Markdown into styled Word documents, fill existing .docx templates with structured data, and validate generated .docx files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted DOCX templates may expose XML parsing or resource-exhaustion risks.

Mitigation: Use the skill in a sandbox or low-sensitivity workspace and avoid untrusted templates until XML parsing and ZIP limits are hardened.

Risk: Markdown image references may expose local-file or resource-exhaustion risks.

Mitigation: Review image references before generation, keep inputs from trusted sources, and rely on workspace path containment.

Risk: Unpinned dependencies can reduce reproducibility across installs.

Mitigation: Pin dependency versions before production use or controlled deployment.

## Reference(s):

- [Kai Docx Generator on ClawHub](https://clawhub.ai/kaisersong/skills/kai-docx-generator)
- [Style Presets Reference](references/style-presets.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands; generated outputs are .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Markdown-to-.docx conversion, template filling, strict placeholder checks, style presets, and document validation.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
