## Description: <br>
Uses the ModelScope Qwen3-VL multimodal API through an OpenAI SDK-compatible client to describe images, extract OCR text, answer visual questions, detect objects, and analyze charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crocketc](https://clawhub.ai/user/crocketc) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agent users use this skill to analyze local or URL-based images through ModelScope Qwen3-VL models for image description, OCR, visual question answering, object detection, and chart analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts selected by the user are sent to ModelScope for processing. <br>
Mitigation: Use the skill only with images and prompts that are appropriate to share with ModelScope. <br>
Risk: The ModelScope API key is required for operation and could be exposed if handled carelessly. <br>
Mitigation: Store the API key in a protected environment variable or .env file and avoid passing secrets on the command line. <br>
Risk: Runtime dependencies can introduce ordinary package maintenance risk. <br>
Mitigation: Install in a virtual environment and keep dependencies on patched current versions. <br>


## Reference(s): <br>
- [ModelScope API usage guide](references/api-guide.md) <br>
- [ModelScope vision model list](references/models.md) <br>
- [ModelScope multimodal models](https://modelscope.cn/models?task=image-to-text) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; API calls return text analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write returned analysis text to a file when the CLI output option is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
