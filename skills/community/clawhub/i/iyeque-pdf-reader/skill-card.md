## Description:

Extracts text, searches content, and inspects metadata in local PDF files with bounded page reads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can read selected PDFs, locate passages for evidence, and inspect document metadata before preparing summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted text may expose sensitive document contents to the agent workflow.

Mitigation: Select PDFs deliberately and handle extracted content according to its sensitivity.

Risk: The skill depends on PyMuPDF for parsing PDF files.

Mitigation: Review and maintain the dependency as part of normal package hygiene.

## Reference(s):

- [Pdf Reader on ClawHub](https://clawhub.ai/iyeque/skills/iyeque-pdf-reader)

## Skill Output:

**Output Type(s):** [Text, Metadata]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extraction includes pages read and text; search includes matching pages, counts, and bounded page context. Extraction and search read at most 500 pages per request by default.]

## Skill Version(s):

1.2.2 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
