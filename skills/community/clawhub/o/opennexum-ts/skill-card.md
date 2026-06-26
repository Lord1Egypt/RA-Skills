## Description: <br>
Contract-driven multi-agent orchestration with ACP. TypeScript CLI for spawning and tracking coding agents via OpenClaw sessions_spawn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayao99315](https://clawhub.ai/user/ayao99315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use OpenNexum TS to coordinate contract-driven AI coding workflows, generate OpenClaw ACP spawn payloads, track sessions, run evaluator loops, and manage task completion or retry state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project instruction files and runtime state can influence future agent behavior or task tracking. <br>
Mitigation: Review AGENTS.md, CLAUDE.md, nexum/active-tasks.json, and generated runtime files before running the workflow in an existing project. <br>
Risk: The artifact ships a Telegram notification target and can send workflow status to a configured chat. <br>
Mitigation: Remove or replace the shipped nexum/config.json notification target and use a dedicated low-scope Telegram bot token only after confirming the destination chat. <br>
Risk: Running nexum init or orchestration commands intentionally creates or updates task-state files in the project. <br>
Mitigation: Use the skill only in repositories where Nexum is expected to manage task files and agent workflow state, and review changes before committing. <br>


## Reference(s): <br>
- [OpenNexum TS ClawHub page](https://clawhub.ai/ayao99315/opennexum-ts) <br>
- [README.md](README.md) <br>
- [Contract Schema Reference](references/contract-schema.md) <br>
- [Orchestrator Guide](references/orchestrator-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, pnpm, and openclaw; optional Telegram notification environment variables are TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
