## Description: <br>
将论文 PDF 批处理为中文精读总结报告的工作流技能，支持使用 pdfplumber 或可配置的 PaddleOCR 端点抽取文本，并通过可配置的大模型端点生成论文研读报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to turn one or more PDF papers into structured Chinese deep-reading reports with evidence excerpts, methods summaries, and reusable review tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected document content may be sent to configured OCR or LLM services. <br>
Mitigation: Review config.json before use, confirm each OCR and LLM endpoint with the user, and prefer trusted self-hosted or internal endpoints for sensitive papers. <br>
Risk: API keys or tokens can be exposed if stored directly or printed in logs. <br>
Mitigation: Use environment variable references for secrets when possible and keep log and exception output redacted. <br>
Risk: Broad input folders can include unintended PDFs for processing. <br>
Mitigation: Pass specific PDF files or narrow directories instead of broad document folders. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mxingchtongaelofficial2568/llm-paper-review-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report files plus console progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one *_研读报告.md file per input PDF; output quality and data exposure depend on the configured OCR and LLM endpoints.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
