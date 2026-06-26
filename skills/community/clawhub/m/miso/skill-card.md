## Description: <br>
MISO provides Telegram-native mission-control templates and helper commands for tracking OpenClaw multi-agent workflow progress, approvals, and completion status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShunsukeHayashi](https://clawhub.ai/user/ShunsukeHayashi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to make autonomous and multi-agent work visible in Telegram through standard mission states, progress messages, reactions, and approval gates. It is useful when parallel agent work needs concise status updates from the chat list and repeatable start, plan, status, and close workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mission details may be automatically posted to a fixed Telegram channel. <br>
Mitigation: Enable channel posting only for workspaces where mission names, agent counts, and key insights are safe for every channel member to see. <br>
Risk: The Telegram helper uses a hardcoded local bot-token configuration path and fixed chat identifiers. <br>
Mitigation: Replace these values with workspace-specific configuration before installation, and use a dedicated Telegram bot with only the permissions required. <br>
Risk: Local mission state stored in .miso-state.json may not match workspace retention or backup expectations. <br>
Mitigation: Define retention, backup, and cleanup behavior for local mission state before using the skill for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ShunsukeHayashi/miso) <br>
- [README](artifact/README.md) <br>
- [Mission Control specification](artifact/SKILL.md) <br>
- [Channel integration](artifact/CHANNEL-INTEGRATION.md) <br>
- [Design system](artifact/DESIGN-SYSTEM.md) <br>
- [Examples](artifact/examples/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown templates with optional JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Telegram mission status messages, slash-command workflows, channel notifications, and bot helper commands.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
