## Description: <br>
Provides a WebUI and command-line workflow for managing OpenClaw model providers, saving model configurations, and switching the active AI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peter-zx](https://clawhub.ai/user/peter-zx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain reusable AI model provider configurations, switch the active provider/model, and restart the local gateway when a switch is applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or store provider API keys while managing OpenClaw model settings. <br>
Mitigation: Use dedicated or revocable provider keys, avoid shared machines, redact keys from read responses, and rotate keys after testing. <br>
Risk: The local web API can read and write OpenClaw configuration, control the gateway, and change advanced agent or tool settings. <br>
Mitigation: Run only on a trusted local machine, restrict access to loopback, and add authentication or origin checks before exposing the service beyond localhost. <br>
Risk: Switching, deleting, restarting, or changing security-related settings can disrupt active sessions or alter the expected agent runtime. <br>
Mitigation: Require explicit confirmation before destructive or service-control actions and back up OpenClaw configuration before switching or deleting providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peter-zx/openclaw-tokenapi-qiehuan-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local WebUI, update OpenClaw configuration files, store provider credentials locally, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
