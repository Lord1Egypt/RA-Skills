## Description: <br>
Official skill for recognizing handwritten text from images and PDFs using the ZhiPu GLM-OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to extract handwritten text from notes, letters, documents, formulas, labels, annotations, and mixed handwritten or printed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and PDFs selected for OCR are sent to ZhiPu's GLM-OCR service. <br>
Mitigation: Use the skill only for documents that are acceptable to process with ZhiPu, and avoid highly sensitive personal, legal, medical, financial, or confidential materials unless that provider relationship is approved. <br>
Risk: The skill requires a ZHIPU_API_KEY credential. <br>
Mitigation: Store the key in the configured environment and avoid exposing it in prompts, files, logs, or shared outputs. <br>
Risk: Including raw upstream responses may expose extra service-returned details during debugging. <br>
Mitigation: Keep raw responses disabled unless explicitly needed, and review any saved result JSON before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/glmocr-handwriting) <br>
- [GLM-OCR Handwriting Skill Homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-handwriting) <br>
- [ZhiPu Layout Parsing API Documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the CLI with extracted Markdown text; agent-facing responses are concise Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save result JSON to a file; raw upstream response is omitted unless explicitly requested or needed for debugging.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
