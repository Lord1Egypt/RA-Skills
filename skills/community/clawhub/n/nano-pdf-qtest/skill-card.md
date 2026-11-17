## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinqdw](https://clawhub.ai/user/qinqdw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document workflow users use this skill to ask an agent for nano-pdf CLI commands and guidance that apply natural-language edits to a specific page in a PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The nano-pdf package is installed from the configured Python package index at use time.

Mitigation: Use a sandbox or least-privileged environment and prefer a pinned, reviewed nano-pdf version for sensitive workflows.

Risk: PDF edits may affect the wrong page or create unexpected document changes.

Mitigation: Review the output PDF before sharing it, and retry with the alternate page-number convention if the result appears off by one.

## Reference(s):

- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/)
- [ClawHub skill page](https://clawhub.ai/qinqdw/skills/nano-pdf-qtest)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume the nano-pdf CLI is installed and available on PATH.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
