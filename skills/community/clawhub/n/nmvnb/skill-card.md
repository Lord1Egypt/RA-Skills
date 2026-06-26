## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking available free models, configuring fallback routing for rate limits, and updating openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pz33y](https://clawhub.ai/user/pz33y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenRouter free models, choose a ranked primary model, and set fallback models to reduce cost and handle rate limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace identity is inconsistent: server metadata names the release SEEK while artifact files describe FreeRide. <br>
Mitigation: Verify that this is the expected FreeRide/OpenRouter package before installation or execution. <br>
Risk: The skill can persistently change OpenClaw's default model routing and fallback configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running FreeRide commands and review routing changes before restarting the gateway. <br>
Risk: The optional watcher can make ongoing OpenRouter health checks and automatic model rotations. <br>
Mitigation: Run freeride-watcher --daemon only when continuous checks and automatic rotation are intended. <br>
Risk: The skill depends on an OpenRouter API key. <br>
Mitigation: Keep OPENROUTER_API_KEY out of shared files and source control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pz33y/nmvnb) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run FreeRide CLI commands that update OpenClaw model routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files also declare 1.0.0, 1.0.1, and 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
