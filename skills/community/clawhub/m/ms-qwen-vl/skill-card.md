## Description:

Calls the ModelScope Qwen3-VL multimodal API through the OpenAI SDK to analyze images for description, OCR, visual question answering, object detection, and chart interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crocketc](https://clawhub.ai/user/crocketc)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to route local or URL-based image analysis tasks from Claude Code to ModelScope Qwen3-VL models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image content is sent to a remote ModelScope API and may include secrets, personal data, regulated records, or confidential business information.

Mitigation: Use only with approved ModelScope data handling, and do not submit sensitive images unless that use is explicitly authorized.

Risk: Dependencies are declared with lower bounds, so future package versions can change behavior.

Mitigation: Install in an isolated environment and pin or lock dependency versions before production use.

Risk: The documented .env setup path does not consistently match the script path that loads the API key.

Mitigation: Store the API key in the location read by the script or update the setup instructions and loader path so they match.

## Reference(s):

- [ModelScope API Guide](artifact/references/api-guide.md)
- [ModelScope Vision Model List](artifact/references/models.md)
- [ModelScope API Endpoint](https://api-inference.modelscope.cn/v1)
- [ModelScope Image-to-Text Models](https://modelscope.cn/models?task=image-to-text)
- [ClawHub Release Page](https://clawhub.ai/crocketc/skills/ms-qwen-vl)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Plain text responses with optional output files, Markdown instructions, shell commands, and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ModelScope API credentials and supports fast, precise, and custom model selection.]

## Skill Version(s):

0.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
