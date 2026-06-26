## Description: <br>
Image and video analysis powered by Isaac vision models, including visual Q&A, object detection, OCR, captioning, counting, and grounded spatial reasoning with boxes, points, and polygons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Subraiz](https://clawhub.ai/user/Subraiz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to analyze images or extracted video frames with Perceptron vision models for visual question answering, object detection, OCR, captioning, counting, structured outputs, and spatial annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, videos, URLs, and model outputs may be sent to the external Perceptron API for analysis. <br>
Mitigation: Use this skill only with content approved for external processing, and avoid private IDs, receipts, proprietary footage, medical or legal material, and confidential screens unless authorized. <br>
Risk: The skill requires a Perceptron API key. <br>
Mitigation: Store the API key in an environment variable or secret manager, and do not hardcode, commit, or log it. <br>
Risk: Detailed reasoning traces and model outputs may expose sensitive visual context. <br>
Mitigation: Avoid exposing raw reasoning traces or detailed model outputs in normal logs or user-facing interfaces. <br>


## Reference(s): <br>
- [Perceptron Skill Page](https://clawhub.ai/Subraiz/perceptron) <br>
- [Perceptron Documentation](https://docs.perceptron.inc/) <br>
- [Perceptron API Reference](https://docs.perceptron.inc/api-reference/endpoint/chat-completions) <br>
- [Capabilities Reference](references/capabilities.md) <br>
- [Prompting Reference](references/prompting.md) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; CLI output can be plain text, Markdown, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized spatial annotations such as boxes, points, polygons, and optional pixel-coordinate conversions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
