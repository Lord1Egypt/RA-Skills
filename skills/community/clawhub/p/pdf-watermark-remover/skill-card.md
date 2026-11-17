## Description:

Remove image-based watermarks from PDF files by deleting drawing instructions from PDF content streams and removing XObject references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucrossmym1nd](https://clawhub.ai/user/ucrossmym1nd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document operators use this skill to remove image-based PDF watermarks and optional watermark links from local PDF files while preserving the rest of the document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits PDF content heuristically and may miss a watermark or affect unintended visual content if detection settings are inaccurate.

Mitigation: Keep the original PDF, tune position and size thresholds narrowly, and review the generated PDF before replacing any source document.

Risk: Optional link annotation removal can delete links beyond the intended watermark target if run without a specific domain filter.

Mitigation: Use --remove-links only with a known --link-domain value when the watermark link domain is known.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucrossmym1nd/skills/pdf-watermark-remover)
- [Publisher profile](https://clawhub.ai/user/ucrossmym1nd)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks and local PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and PyMuPDF; output PDFs should be reviewed before replacing originals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
