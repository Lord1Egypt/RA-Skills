## Description: <br>
Analyze images and multi-frame sequences using OpenAI GPT vision models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze image content, extract visible text, compare multiple images, and summarize multi-frame visual sequences with OpenAI vision-capable GPT models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images selected for analysis may be sent to OpenAI for processing. <br>
Mitigation: Use only images appropriate for external processing; redact sensitive screenshots, IDs, credentials, customer data, medical or financial documents, source code, and confidential business content before analysis. <br>
Risk: Vision output can misread small, rotated, distorted, or non-Latin text and can be approximate for object counts or spatial details. <br>
Mitigation: Use high-detail analysis for OCR, preprocess difficult images when possible, and review extracted text or counts before relying on them. <br>
Risk: High-detail analysis of many images can increase token usage and cost. <br>
Mitigation: Choose low, high, or auto detail based on task requirements and monitor token usage during batch processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/jpg-ocr-stat-openai-vision) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and optional JSON analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model name, detail level, token usage, warnings, extracted text, object descriptions, image comparisons, and error details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
