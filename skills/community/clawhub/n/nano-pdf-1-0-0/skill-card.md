## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to issue nano-pdf CLI commands that edit a specific PDF page from a natural-language instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an unpinned external package from PyPI.

Mitigation: Install only when the nano-pdf package source is trusted, and pin or review the package version according to the deployment process.

Risk: PDF edits may target the wrong page or produce inaccurate document changes.

Mitigation: Check page numbering and inspect the generated PDF before sharing or relying on it.

Risk: Sensitive documents may be processed by a local CLI dependency.

Mitigation: Use a restricted environment for sensitive PDFs and limit document access to the files needed for the edit.

## Reference(s):

- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/)
- [ClawHub skill page](https://clawhub.ai/kenswj/skills/nano-pdf-1-0-0)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent should inspect generated PDFs before sharing and may need to retry page numbering if output is off by one.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
