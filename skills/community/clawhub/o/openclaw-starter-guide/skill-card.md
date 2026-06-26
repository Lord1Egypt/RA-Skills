## Description: <br>
Guides OpenClaw users through model provider selection, fallback chains, quota checks, multi-agent setup, and troubleshooting for a cost-conscious assistant deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooey](https://clawhub.ai/user/jooey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to choose providers, configure fallback model chains, manage API quotas and costs, and troubleshoot a multi-agent assistant setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced provider skills may introduce separate setup, trust, or operational requirements. <br>
Mitigation: Review each referenced provider skill before installing it. <br>
Risk: Provider API keys or account credentials could be exposed if shared in chat or logs. <br>
Mitigation: Keep API keys out of chat and store them through local configuration or secret-handling practices. <br>
Risk: Provider costs, privacy implications, and optional scheduled automation can create unintended spend or data exposure. <br>
Mitigation: Confirm provider costs and privacy implications, and add explicit limits before enabling scheduled or 24/7 automation. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Starter Guide on ClawHub](https://clawhub.ai/jooey/openclaw-starter-guide) <br>
- [MiniMax provider skill](https://clawhub.com/skills/add-minimax-provider) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes model-provider setup, fallback-chain guidance, quota-validation commands, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
