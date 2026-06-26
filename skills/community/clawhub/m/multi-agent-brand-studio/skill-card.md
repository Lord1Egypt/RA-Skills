## Description: <br>
Sets up Multi-Agent Brand Studio on OpenClaw for multi-brand social media operations, approval-gated publishing, brand-isolated workspaces, and multi-agent content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuan0808](https://clawhub.ai/user/kuan0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn OpenClaw into a persistent multi-brand social media operations workspace with specialized agents, shared memory, brand-specific context, and approval-gated publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup makes broad persistent OpenClaw workspace and configuration changes for a multi-agent brand operations environment. <br>
Mitigation: Review the dry-run output and intended agent, cron, and configuration changes before applying setup. <br>
Risk: Telegram bot and channel configuration can route operational updates and brand work to external chats or topics. <br>
Mitigation: Confirm bot tokens, chat IDs, topic IDs, and channel routing before enabling Telegram integration. <br>
Risk: Brand or client information may be stored in local memory, shared knowledge, and brand profile files. <br>
Mitigation: Set clear boundaries for sensitive information and review local memory files before storing confidential brand data. <br>
Risk: Publishing decisions may be ambiguous without explicit approval language. <br>
Mitigation: Use the approval workflow and require explicit owner approval before publishing or taking external actions. <br>
Risk: Uninstall or cleanup steps can remove QMD or memory data if followed without backups. <br>
Mitigation: Back up QMD and memory data before following deletion-oriented uninstall instructions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kuan0808/multi-agent-brand-studio) <br>
- [README](README.md) <br>
- [Architecture](references/architecture.md) <br>
- [Agent Roles](references/agent-roles.md) <br>
- [Memory System](references/memory-system.md) <br>
- [Approval Workflow](references/approval-workflow.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated workspace files, and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw workspace scaffolding, agent configuration, brand templates, cron definitions, and owner-facing setup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
