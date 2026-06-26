## Description: <br>
Optimize OpenClaw model configuration by declaring missing model capabilities such as vision input, context window, max output tokens, and reasoning support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yay2008](https://clawhub.ai/user/yay2008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw model settings and add missing capability declarations after configuring models or providers. It helps restore features such as image input, larger context windows, longer output, and reasoning mode when OpenClaw cannot infer them automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect model capability values can affect future OpenClaw sessions, including vision availability, truncation behavior, and reasoning mode. <br>
Mitigation: Review each proposed capability value with the user before applying it and prefer provider-specific limits when available. <br>
Risk: Editing the local OpenClaw configuration can overwrite working settings. <br>
Mitigation: Back up ~/.openclaw/openclaw.json to ~/.openclaw/openclaw.json.bak before modifying the configuration. <br>


## Reference(s): <br>
- [Common Model Capabilities Reference](artifact/references/model-capabilities.md) <br>
- [OpenClaw Model Optimizer on ClawHub](https://clawhub.ai/yay2008/openclaw-model-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-confirmed capability declarations and backup guidance for OpenClaw configuration changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
