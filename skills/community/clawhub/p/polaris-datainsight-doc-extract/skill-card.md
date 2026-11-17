## Description:

Extract structured data from Office documents (DOCX, PPTX, XLSX, HWP, HWPX) using the Polaris AI DataInsight Doc Extract API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob-g-park](https://clawhub.ai/user/jacob-g-park)

### License/Terms of Use:

Apache-2.0 for the skill definition; Polaris AI DataInsight Terms of Service for service usage

## Use Case:

Developers and engineers use this skill to extract text, tables, charts, images, shapes, equations, headers, and footers from Office-format documents for document analysis, data migration, search, and RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Office document contents to a third-party Polaris DataInsight API under broad document-extraction trigger conditions.

Mitigation: Use only with documents you are authorized to process externally, and confirm the vendor's data handling, retention, regional processing, and API key controls before handling confidential, regulated, customer, employee, legal, or proprietary content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacob-g-park/skills/polaris-datainsight-doc-extract)
- [Polaris AI DataInsight](https://datainsight.polarisoffice.com)
- [Polaris DataInsight Doc Extract endpoint](https://datainsight-api.polarisoffice.com/api/v1/datainsight/doc-extract)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown with Python, curl, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced API returns a ZIP file containing unifiedSchema JSON.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
