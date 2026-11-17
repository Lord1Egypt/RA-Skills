## Description:

Edit PDFs with natural-language instructions using the nano-pdf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v585](https://clawhub.ai/user/v585)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document editors use this skill to ask an agent to invoke nano-pdf for natural-language edits to specific PDF pages, then inspect the generated PDF before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned third-party CLI can introduce supply-chain exposure.

Mitigation: Use a sandbox or pin and review a trusted nano-pdf version before use.

Risk: PDF contents may pass through an external AI workflow.

Mitigation: Avoid sensitive documents unless the workflow is approved for that data.

Risk: Generated PDF edits may be incorrect or target the wrong page.

Mitigation: Review the output PDF and retry with the alternate page numbering convention if needed.

## Reference(s):

- [Nano Pdf Cn on ClawHub](https://clawhub.ai/v585/skills/nano-pdf-cn)
- [nano-pdf PyPI project](https://pypi.org/project/nano-pdf/)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nano-pdf command to be installed; generated PDFs should be reviewed before distribution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
