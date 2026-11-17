## Description:

Extracts figure images from academic PDFs by analyzing page structure, locating captions, cropping clean figures, and validating image quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[438061781](https://clawhub.ai/user/438061781)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic writers use this skill to guide an agent through extracting clean figure images from PDF papers for documents, manuscripts, and related writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted figures may include captions, body text, or incomplete subfigures if crop boundaries are selected incorrectly.

Mitigation: Review every extracted image before use and adjust crop coordinates based on the PDF text-block and caption analysis.

Risk: The workflow processes local academic PDFs supplied to the agent.

Mitigation: Use intentionally provided PDF files only and confirm the document is appropriate for this extraction workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/438061781/skills/pdf-figure-extractor)

## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with Python code blocks and extraction checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for local PDF figure extraction, coordinate selection, image cropping, and manual quality review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
