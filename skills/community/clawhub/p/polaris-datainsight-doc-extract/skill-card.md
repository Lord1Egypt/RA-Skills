## Description: <br>
Extract structured data from Office documents (DOCX, PPTX, XLSX, HWP, HWPX) using the Polaris AI DataInsight Doc Extract API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacob-g-park](https://clawhub.ai/user/jacob-g-park) <br>

### License/Terms of Use: <br>
Apache-2.0 for the skill definition; Polaris DataInsight service terms apply to API usage. <br>


## Use Case: <br>
Developers and engineers use this skill to extract text, tables, charts, images, shapes, equations, headers, and footers from Office-format documents for document parsing, data analysis, RAG pipelines, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to Polaris DataInsight for processing, which can expose confidential, regulated, customer, or proprietary content to an external service. <br>
Mitigation: Use the skill only with documents your organization permits for Polaris DataInsight processing, and avoid confidential or regulated files unless that use is approved. <br>
Risk: The Polaris DataInsight API key could be exposed if pasted into chats, scripts, or logs. <br>
Mitigation: Store the API key in POLARIS_DATAINSIGHT_API_KEY and avoid hardcoding or sharing it in generated examples, logs, or chat transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacob-g-park/polaris-datainsight-doc-extract) <br>
- [Polaris DataInsight](https://datainsight.polarisoffice.com) <br>
- [Polaris DataInsight Doc Extract API endpoint](https://datainsight-api.polarisoffice.com/api/v1/datainsight/doc-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with Python and shell code blocks; API responses are ZIP files containing unifiedSchema JSON and table or chart CSV data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POLARIS_DATAINSIGHT_API_KEY and uploads selected documents to Polaris DataInsight for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
