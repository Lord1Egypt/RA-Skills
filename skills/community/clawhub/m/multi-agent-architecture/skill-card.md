## Description: <br>
Architecture guide for running multiple specialized AI agents on a single OpenClaw server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and operate multiple specialized OpenClaw agents with isolated workspaces, Telegram routing, shared memory, monitoring, and backup practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent, provider, and Telegram credentials may be exposed if copied into chat, source control, shared memory, or backups. <br>
Mitigation: Keep tokens out of chat and git, restrict Telegram bots with allowedChatIds, and exclude secrets from shared memory and backups. <br>
Risk: Automatic restart or cron examples may affect running services if enabled without review. <br>
Mitigation: Review restart scripts and cron entries before enabling them, and limit automation to agents and services that require it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mosoonpi-ai/multi-agent-architecture) <br>
- [Publisher profile](https://clawhub.ai/user/mosoonpi-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational checklists, configuration examples, and monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
