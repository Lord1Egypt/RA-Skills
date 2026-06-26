## Description: <br>
Manages OpenClaw model configuration by adding, testing, listing, and assigning model providers in models.json and agent config files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw model providers, validate model access, test optional tool-calling and streaming support, and set default or agent-specific models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local model and agent configuration files can be permanently changed. <br>
Mitigation: Verify each config path and agent path before running add commands, review the proposed configuration, and keep backups before changing defaults. <br>
Risk: API keys may be stored in local model configuration and sent to any configured model endpoint during tests. <br>
Mitigation: Use only trusted HTTPS Base URLs, confirm the host before testing, and avoid entering credentials for untrusted providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YKaiXu/model-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and JSON configuration examples; helper scripts emit JSON or formatted text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may update local models.json and agent config.json files, and model tests send API keys to the configured Base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
