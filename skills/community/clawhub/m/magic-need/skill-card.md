## Description: <br>
Magic Need captures missing tool, API, or data-source requests from AI agents, categorizes them, and stores them for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guim4dev](https://clawhub.ai/user/guim4dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to record tools, APIs, logs, metrics, or data sources an agent needed but could not access during a task. The recorded backlog helps teams review recurring gaps and prioritize integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Need descriptions may contain secrets, credentials, incident details, or sensitive operational context if users paste them into the local backlog. <br>
Mitigation: Do not record secrets, tokens, credentials, or sensitive incident details; review generated reports before sharing them through Slack, Discord, or other channels. <br>
Risk: The skill keeps a durable local backlog of agent-requested tools and data sources. <br>
Mitigation: Install it only when local persistence is desired and manage ~/.magic-need/needs.json according to the environment's data retention practices. <br>


## Reference(s): <br>
- [Magic Need on ClawHub](https://clawhub.ai/guim4dev/magic-need) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Sonary](https://www.sonary.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text confirmations, JSON-backed local records, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local need records to ~/.magic-need/needs.json and can generate grouped reports for review or notification workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
