## Description: <br>
OpenClaw Agent Skill helps agents answer OpenClaw setup, usage, troubleshooting, and development questions from bundled OpenClaw documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brabaflow](https://clawhub.ai/user/brabaflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get OpenClaw guidance, exact CLI and configuration examples, and citations into the bundled docs for gateway, channel, provider, plugin, deployment, and troubleshooting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled docs include high-impact setup, permission, persistence, and privacy examples that may affect local systems, chat channels, secrets, or backups if copied without review. <br>
Mitigation: Review generated commands and configuration before use, inspect remote installer scripts, protect secrets and backups, and use least-privilege channel and gateway settings. <br>
Risk: Approve-all permissions, heartbeat, memory, media upload, and auto-start proxy examples can broaden operational access when used in trusted environments without isolation. <br>
Mitigation: Avoid approve-all modes unless isolated, restrict allowed senders and tools, and test persistent or remote-access features in a controlled environment before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brabaflow/openclaw-agent-skill) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw quick start](https://docs.openclaw.ai/start/quickstart) <br>
- [OpenClaw security documentation](https://docs.openclaw.ai/security) <br>
- [OpenClaw CLI reference](https://docs.openclaw.ai/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with cited documentation sections and inline code blocks when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should cite the relevant bundled OpenClaw documentation section and avoid guessing when the docs do not cover a topic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
