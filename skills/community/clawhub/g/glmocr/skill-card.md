## Description: <br>
Extract text from images and PDFs using the GLM-OCR API, including tables, formulas, and handwriting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and document-processing users use this skill to extract Markdown text, tables, formulas, and layout details from images, screenshots, scanned documents, and PDFs through the GLM/Zhipu OCR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, PDFs, or document URLs are sent to the GLM/Zhipu OCR service for extraction. <br>
Mitigation: Use only for documents that policy permits sending to that provider, and avoid highly confidential or regulated content unless explicitly approved. <br>
Risk: The ZHIPU_API_KEY may be stored locally in the skill's .env file. <br>
Mitigation: Keep the .env file out of shared folders and version control, and protect the API key as a sensitive credential. <br>


## Reference(s): <br>
- [GLM-OCR skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr) <br>
- [GLM-OCR GitHub repository](https://github.com/zai-org/GLM-OCR) <br>
- [Output schema](references/output_schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glmocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON envelope containing extracted Markdown text, layout details, raw API response data, source metadata, and error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print results to stdout or save them to a JSON file; local image and PDF inputs are encoded and submitted to the fixed GLM/Zhipu OCR endpoint.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
