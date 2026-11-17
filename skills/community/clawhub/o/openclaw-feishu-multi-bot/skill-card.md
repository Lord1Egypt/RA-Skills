## Description:

Configures multiple Feishu/Lark bot identities for one OpenClaw instance so each agent can use its own Feishu app, name, avatar, and message routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonlin1212](https://clawhub.ai/user/simonlin1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to configure independent Feishu/Lark bot entry points for multiple agents, generate openclaw.json blocks, and troubleshoot routing, startup, and group-isolation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper accepts Feishu AppSecrets on the command line and prints generated configuration that includes secrets.

Mitigation: Do not pass real AppSecrets on shared systems, and do not paste generated output into logs, tickets, chats, or source control.

Risk: Unvalidated agent IDs can lead to unsafe or incorrect generated configuration.

Mitigation: Validate and sanitize agent IDs before running the helper, then inspect the generated JSON manually before merging it into openclaw.json.

Risk: Gateway restart or process-kill commands can disrupt active OpenClaw sessions.

Mitigation: Run health checks first, schedule restarts deliberately, and treat pkill or gateway restart commands as operationally disruptive.

## Reference(s):

- [Architecture: Multi-Bot Feishu Integration](references/architecture.md)
- [Build Guide: Feishu Multi-Bot Setup](references/build-guide.md)
- [Routing Deep Dive](references/routing-deep-dive.md)
- [Troubleshooting](references/troubleshooting.md)
- [Feishu Developer Console](https://open.feishu.cn/app)
- [Publisher Profile](https://clawhub.ai/user/simonlin1212)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated openclaw.json configuration blocks and operational restart commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
