## Description:

Autonomer Goalz-Agent für den öffentlichen Goalz-MCP-Endpunkt, der selbstständig spielt, berichtet und einen Verein langfristig entwickelt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geby85](https://clawhub.ai/user/geby85)

### License/Terms of Use:


## Use Case:

External Goalz players and automation users can use this skill to let an agent manage a Goalz account through MCP, including account bootstrap, team management, recurring checks, in-game communication, and long-term club development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for recurring hands-off Goalz account control.

Mitigation: Install it only for accounts where autonomous recurring play is acceptable, and review the planned session cadence before use.

Risk: The skill can request and use a Telegram bot token.

Mitigation: Provide only a dedicated Telegram bot token, treat it as a secret, and rotate or revoke it if it is exposed or no longer needed.

Risk: The skill can send public or private in-game communication.

Mitigation: Prefer policy-protected communication tools and review communication behavior when tone, recipients, or public visibility matter.

Risk: The skill can make irreversible or consequential game and account changes without per-action approval.

Mitigation: Use it only if autonomous registration, club takeover, transfers, sponsor decisions, stadium orders, and other high-impact game actions are acceptable.

## Reference(s):

- [Goalz MCP endpoint](https://www.goalz.de/mcp)
- [Modes and safety](references/modes-and-safety.md)
- [Tool groups](references/tool-groups.md)
- [Playbooks](references/playbooks.md)
- [Degraded mode](references/degraded-mode.md)
- [ClawHub skill page](https://clawhub.ai/geby85/skills/goalz-de)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [German Markdown guidance with operational status updates and MCP-oriented action plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide recurring autonomous sessions, Goalz MCP tool use, Telegram token handling, and policy-aware in-game communication.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
