## Description: <br>
One-click configuration for connecting OpenClaw to the aicodee.com MiniMax model relay service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outrice](https://clawhub.ai/user/outrice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a custom MiniMax provider by extracting the API base URL, API key, and model name from a message and applying them to OpenClaw settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes OpenClaw configuration and stores the supplied API key locally in plaintext. <br>
Mitigation: Review the target OpenClaw config path before running it, use a limited-scope or disposable API key, and keep a backup of existing provider settings. <br>
Risk: The skill changes the default OpenClaw model provider to the configured MiniMax relay. <br>
Mitigation: Confirm the intended provider name, model ID, and base URL before applying the configuration, and restore the prior default model if the relay is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/outrice/jisuai-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a Python configuration helper that updates OpenClaw provider settings when required API values are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
