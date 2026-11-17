## Description:

Multimodal document deep analysis tool based on Zhipu GLM-OCR, GLM-4.7, and GLM-4.6V.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baokui](https://clawhub.ai/user/baokui)

### License/Terms of Use:


## Use Case:

Developers and document-processing teams use this skill to extract tables and charts from PDFs or images, convert tables to Markdown, crop visual elements, and generate GLM-based semantic analysis of document content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input documents, extracted tables, captions, and cropped images are sent to Zhipu GLM services.

Mitigation: Process only documents approved for that provider and avoid confidential or regulated content unless organizational policy allows it.

Risk: Generated analysis may be influenced by malicious or misleading text inside source documents.

Mitigation: Treat analysis as model output and review conclusions before using them in decisions or downstream workflows.

Risk: Intermediate JSON reports and cropped images may contain sensitive document content on disk.

Mitigation: Use a protected output directory and apply retention or cleanup controls appropriate for the processed documents.

Risk: Multi-page PDFs default to first-page processing, which can produce incomplete document analysis.

Mitigation: Extend or verify batch-page handling before relying on results for multi-page documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; writes intermediate JSON, final analysis JSON, and cropped image files to the configured output directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
