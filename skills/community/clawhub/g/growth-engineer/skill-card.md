## Description: <br>
Growth Engineer supports mobile apps and agent runtimes including OpenClaw and Hermes by correlating analytics, crashes, billing, feedback, store signals, and repo context into proposal drafts that can flow into agent chat, GitHub issues, or draft pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wotaso-dev](https://clawhub.ai/user/wotaso-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to connect mobile-app growth, monetization, crash, feedback, store, and repository signals, then turn those signals into execution-ready recommendations, local issue drafts, GitHub issues, or draft pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure recurring automation and make host-level changes during setup or operation. <br>
Mitigation: Install it only in an intended workspace or VPS, review OpenClaw/Hermes cron and self-update settings before first run, and disable automation modes that are not needed. <br>
Risk: Configured delivery modes can create GitHub issues, draft pull requests, chat outbox entries, Slack messages, Discord messages, or webhook notifications. <br>
Mitigation: Keep GitHub artifact creation disabled unless explicitly desired, use least-privilege tokens, and verify destination settings before enabling unattended runs. <br>
Risk: Connectors rely on API tokens and private keys for analytics, billing, crash, store, repository, and notification services. <br>
Mitigation: Store secrets only in the host terminal environment or managed secret files, never in chat, repository config, generated proposals, issues, or pull request bodies. <br>
Risk: Command-mode connectors and project configuration can execute local commands as part of data collection. <br>
Mitigation: Use trusted project configs, prefer file-mode connectors when possible, and review connector commands before running against unfamiliar workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wotaso-dev/skills/growth-engineer) <br>
- [Growth Engineer Homepage](https://github.com/Wotaso/growth-engineer-skill) <br>
- [Setup And Scheduling](references/setup-and-scheduling.md) <br>
- [Required Secrets](references/required-secrets.md) <br>
- [Advanced Setup](references/advanced-setup.md) <br>
- [Input Schema](references/input-schema.md) <br>
- [Generated GitHub Issue Template](references/issue-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, shell command snippets, and generated issue or pull request proposal drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local config, state, outbox, issue drafts, charts, and proposal artifacts depending on configured connectors and delivery modes.] <br>

## Skill Version(s): <br>
1.0.208 (source: server release evidence, skill metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
