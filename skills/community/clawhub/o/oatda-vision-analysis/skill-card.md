## Description: <br>
Analyze images using vision-capable AI models through OATDA's unified API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send HTTPS or data URI images to OATDA's vision API for image descriptions, OCR, and analysis of screenshots, diagrams, charts, and photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, screenshots, OCR targets, prompts, and related request data are sent to OATDA and may be processed by downstream model providers. <br>
Mitigation: Use the skill only when sharing the selected image and prompt with OATDA is acceptable; avoid sensitive documents, secrets, regulated data, and private internal screenshots unless approved. <br>
Risk: The skill requires an OATDA API key for outbound API calls. <br>
Mitigation: Keep the API key revocable, avoid printing it, and verify only that it exists or show a short prefix when troubleshooting. <br>


## Reference(s): <br>
- [OATDA](https://oatda.com) <br>
- [OATDA image analysis API endpoint](https://oatda.com/api/v1/llm/image) <br>
- [ClawHub skill page](https://clawhub.ai/devcsde/oatda-vision-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model response text, token usage, and cost information returned by OATDA.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
