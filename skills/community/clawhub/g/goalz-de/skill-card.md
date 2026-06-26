## Description: <br>
Goalz über MCP enables an autonomous Goalz agent to play through the public Goalz MCP endpoint, report progress, and manage a club toward long-term success. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geby85](https://clawhub.ai/user/geby85) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Goalz players or operators can use this skill to run an agent-managed club through the public Goalz MCP, including account bootstrap, team checks, match preparation, communication, scheduling, and autonomous game actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for unattended Goalz account management with broad messaging, scheduling, and irreversible game-action authority. <br>
Mitigation: Install only for intentional unattended use, check Goalz rules on automation, and set hard limits for scheduling, public posts, registration, club takeovers, transfers, bids, sponsor choices, stadium orders, and other irreversible actions. <br>
Risk: Telegram bot tokens and account credentials may be exposed or overused if reused outside this skill. <br>
Mitigation: Use a dedicated Goalz account and a fresh revocable Telegram bot token, and keep all tokens and credentials out of normal reports and public communication. <br>


## Reference(s): <br>
- [Modes and Safety](references/modes-and-safety.md) <br>
- [Tool Groups](references/tool-groups.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Degraded Mode](references/degraded-mode.md) <br>
- [Goalz MCP endpoint](https://www.goalz.de/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/geby85/goalz-de) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration] <br>
**Output Format:** [German Markdown status updates with MCP tool calls and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a Telegram bot token as a secret and may perform autonomous Goalz actions when enabled.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
