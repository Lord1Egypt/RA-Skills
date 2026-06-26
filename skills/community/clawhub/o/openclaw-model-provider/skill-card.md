## Description: <br>
Help users add custom model providers to OpenClaw by configuring model providers, default model selection, environment variables, and validation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksbbs](https://clawhub.ai/user/ksbbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add built-in or custom AI model providers, generate configuration snippets, apply them to OpenClaw settings, and validate provider availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real API keys could be exposed if users paste production credentials into chat or shared configuration. <br>
Mitigation: Use placeholders in generated examples and set real keys locally through environment variables or a secret manager. <br>
Risk: Incorrect model-provider settings could break or misroute OpenClaw requests. <br>
Mitigation: Review generated changes, keep a backup of ~/.openclaw/openclaw.json, and run OpenClaw validation commands before relying on the provider. <br>
Risk: Any configured provider may receive future OpenClaw prompts and context. <br>
Mitigation: Choose providers that meet the user's data-handling requirements before making them default. <br>


## Reference(s): <br>
- [OpenClaw model provider documentation](https://docs.openclaw.ai/zh-CN/concepts/model-providers) <br>
- [OpenClaw configuration reference](references/openclaw-config-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw configuration fragments, environment-variable names, backup commands, validation commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
