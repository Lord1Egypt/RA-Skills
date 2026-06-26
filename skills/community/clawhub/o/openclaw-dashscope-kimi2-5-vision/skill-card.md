## Description: <br>
Provides image recognition with Kimi K2.5 for Ali Bailian GLM users and can automatically read an existing DashScope API key from OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowstart](https://clawhub.ai/user/flowstart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to analyze local images or screenshots with a custom prompt when their current model does not provide media understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse DashScope or OpenClaw API keys and may print a recovered key in full. <br>
Mitigation: Use a dedicated API key for this skill, run it only in private terminals, and redact or patch any output path that prints the key before broader deployment. <br>
Risk: Selected images and prompts are uploaded to DashScope for recognition. <br>
Mitigation: Use the skill only with images and prompts that are appropriate to send to DashScope, and avoid private or regulated content unless approved for that service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flowstart/openclaw-dashscope-kimi2-5-vision) <br>
- [Ali Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope chat completions endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends selected image content and the user prompt to DashScope, then prints the model response.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
