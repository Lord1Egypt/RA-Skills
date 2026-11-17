## Description:

Kimi K2.5 Vision analyzes local image files with Kimi K2.5 through DashScope, reusing a DashScope API key from the environment or OpenClaw configuration when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowstart](https://clawhub.ai/user/flowstart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to analyze screenshots or image files with Kimi K2.5 when image understanding is requested or unavailable in the active model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images are sent to DashScope for analysis.

Mitigation: Install and use the skill only for images that are acceptable to transmit to DashScope.

Risk: A recovered DashScope API key can be exposed in terminal or agent logs.

Mitigation: Remove raw API-key printing and avoid shell-history based persistence guidance before routine use.

Risk: Broad activation could run image analysis when the user did not explicitly intend it.

Mitigation: Narrow activation to explicit user requests for image analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowstart/skills/openclaw-dashscope-kimi2-5-vision)
- [Ali Bailian API key console](https://bailian.console.aliyun.com/)
- [DashScope chat completions endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain text image-analysis response with CLI setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image-analysis results are returned as terminal text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
