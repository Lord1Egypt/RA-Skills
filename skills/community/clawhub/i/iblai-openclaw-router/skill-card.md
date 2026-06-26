## Description: <br>
Cost-optimizing model router for OpenClaw that routes each request to a cheaper capable Claude model using weighted scoring, with optional OpenRouter support for OpenAI and Google models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neuralshift1](https://clawhub.ai/user/Neuralshift1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and configure a local model-routing proxy for background jobs, subagents, and other workloads where lower-cost model selection is useful. The skill helps route requests across configured model tiers while keeping routing on the user's OpenClaw server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent local system service. <br>
Mitigation: Review the install script and generated systemd unit before installing or enabling the service. <br>
Risk: The router handles API keys and may place the selected key in the service environment. <br>
Mitigation: Confirm which API key will be used and prefer a protected secret file or manual key setup over embedding secrets directly in the unit. <br>
Risk: Prompt text and routing decisions may be sensitive in operational logs. <br>
Mitigation: Set ROUTER_LOG=0 for sensitive workloads and review logging behavior before production use. <br>
Risk: Custom apiBaseUrl values can forward prompts and credentials to an external provider. <br>
Mitigation: Use only provider URLs that the operator trusts and has approved for the workload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Neuralshift1/iblai-openclaw-router) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API](https://openrouter.ai/api/v1) <br>
- [ibl.ai](https://ibl.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, verification, customization, and uninstall guidance for a local OpenClaw routing proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
