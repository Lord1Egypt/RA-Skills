## Description:

Recognizes and extracts mathematical formulas from images and PDFs into LaTeX format using the ZhiPu GLM-OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, educators, and document-processing teams use this skill to extract formulas and surrounding text from formula images, scanned documents, PDFs, scientific papers, textbooks, and exams into Markdown or LaTeX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local images, PDFs, or remote document URLs are sent to ZhiPu's GLM-OCR service using the configured API key.

Mitigation: Use only documents approved for that provider and account setup, and avoid confidential documents unless the data handling path is approved.

Risk: A shared ZHIPU_API_KEY may be reused across ZhiPu skills when configured globally.

Mitigation: Use skill-level API-key configuration when the key should be scoped to this skill.

Risk: Raw upstream OCR responses may include additional document content when debugging output is enabled.

Mitigation: Leave raw response inclusion disabled unless debugging requires it, and review saved result files before sharing them.

## Reference(s):

- [GLM-OCR Formula skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-formula)
- [ZhiPu Layout Parsing API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90)
- [ClawHub skill release page](https://clawhub.ai/jaredforreal/skills/glmocr-formula)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses containing OCR status, extracted Markdown or LaTeX text, optional layout details, source metadata, and error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save JSON output to a file, pretty-print responses, and include raw upstream responses only when explicitly requested for debugging.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
