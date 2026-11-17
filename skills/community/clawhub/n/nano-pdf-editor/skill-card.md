## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document editors use this skill to invoke the nano-pdf CLI for page-specific PDF edits described in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the current nano-pdf package resolved by uv rather than a reviewed fixed version.

Mitigation: Use a constrained environment and prefer a pinned or locked installation when stronger supply-chain control is required.

Risk: PDF edits may affect the wrong page if the installed nano-pdf version or configuration interprets page numbers differently.

Mitigation: Review the output PDF and retry with the alternate page-numbering convention if the edit appears off by one.

Risk: Sensitive PDFs may be modified or shared with incorrect edits.

Mitigation: Sanity-check edited PDFs before sharing them outside the editing workflow.

## Reference(s):

- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/)
- [Nano Pdf ClawHub skill page](https://clawhub.ai/utromaya-code/skills/nano-pdf-editor)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce modified PDF files when the nano-pdf CLI is executed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
