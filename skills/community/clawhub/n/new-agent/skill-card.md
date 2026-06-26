## Description: <br>
Create OpenClaw agents and connect them to messaging channels including Telegram, Discord, Slack, Feishu, WhatsApp, Signal, and Google Chat, with single and batch setup modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create one or more OpenClaw agents, provision dedicated workspaces, connect supported messaging channels, and verify gateway bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live bot credentials may be included in chat prompts, manifests, or OpenClaw configuration. <br>
Mitigation: Start with test or scoped credentials, keep manifests and openclaw.json out of version control, restrict file permissions, and rotate any token exposed in prompts, logs, or shared files. <br>
Risk: Batch mode allows all created agents to interact through agent-to-agent tooling. <br>
Mitigation: Review the generated agentToAgent allow list after setup and remove any agent pairings that are not required. <br>
Risk: Gateway restarts and configuration writes can disrupt active messaging connections. <br>
Mitigation: Prefer batch setup for multiple agents, keep the automatic backup made before config changes, and verify bindings and channel status after restart. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joansongjr/new-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace files, update OpenClaw configuration, and restart the OpenClaw gateway when helper scripts are run.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
