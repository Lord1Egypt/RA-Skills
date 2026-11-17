## Description:

Recognizes and extracts tables from images and PDFs into Markdown using the ZhiPu GLM-OCR API, including complex tables, merged cells, and multi-page documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to extract tables from local or remote images and PDFs, convert table content to editable Markdown, and inspect layout details returned by GLM-OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or PDFs and the configured ZHIPU_API_KEY are sent to ZhiPu's GLM-OCR service.

Mitigation: Use the skill only when provider exposure is acceptable, avoid highly sensitive documents unless approved, and prefer skill-level key configuration when key sharing across Zhipu skills is not desired.

Risk: Raw upstream API responses may contain extra document details when debugging is enabled.

Mitigation: Keep raw response inclusion disabled by default and enable it only for explicit debugging needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaredforreal/skills/glmocr-table)
- [GLM-OCR table skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-table)
- [ZhiPu Layout Parsing API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90)
- [ZhiPu API key management](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown table text and JSON response objects, optionally saved to a result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; GLM_OCR_TIMEOUT can adjust API timeout; raw upstream responses are omitted unless explicitly requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
