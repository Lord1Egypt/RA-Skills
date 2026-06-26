## Description: <br>
Guides agents through configuring Kimi K2.5 (Kimi Code) as an Anthropic Messages API-compatible coding model for OpenClaw and Claude Code CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw or Claude Code CLI to route coding tasks to Kimi K2.5 through the Anthropic Messages API-compatible endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source code, and coding context may be sent to Kimi as an external model service. <br>
Mitigation: Use this skill only for projects where third-party model processing is allowed, and review data-sharing requirements before use. <br>
Risk: Real API keys may be exposed if copied into committed configuration, pasted source, screenshots, or logs. <br>
Mitigation: Store keys in local environment variables or a secret manager, and keep real keys out of source control and shared outputs. <br>
Risk: Incorrect endpoint or protocol configuration can fail requests or route traffic to the wrong Moonshot product. <br>
Mitigation: Use the Kimi Code endpoint with Anthropic Messages API settings, then verify the setup with a non-sensitive test task. <br>


## Reference(s): <br>
- [Kimi Code Console](https://www.kimi.com/code/console) <br>
- [Kimi Code API messages endpoint](https://api.kimi.com/coding/v1/messages) <br>
- [Chinese setup guide](references/SKILL_CN.md) <br>
- [ClawHub skill page](https://clawhub.ai/jack-yang-ai/kimi-code-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown with JSON, bash, curl, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholder API keys; users must supply their own Kimi API key and avoid committing secrets.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
