## Description:

Provides professional Chinese official document formatting using specified fonts and styles for titles, red headings, body text, and alphanumeric characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and document automation developers use this skill to format uploaded Chinese official Word documents against configurable templates and GB/T 9704-2012-style typography rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and overwrite caller-selected local files without path containment or overwrite safeguards.

Mitigation: Run it in a dedicated working folder with explicit input and output paths, limited filesystem access, and confirmation before overwriting files.

Risk: Template names are used to select local DOCX templates and may be unsafe if package validation does not constrain basenames.

Mitigation: Validate template names as basenames, restrict template lookup to the intended templates directory, and reject path traversal or unexpected extensions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erich1566/skills/official-layout-pro)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Formatted DOCX file with JSON status and output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires caller-provided input and output paths, optional template name, document code, and issuing organization name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
