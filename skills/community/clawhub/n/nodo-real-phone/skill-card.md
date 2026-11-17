## Description:

Give your agent a real Android phone with its own number, in the cloud. Use when the user needs SMS verification codes on a real SIM (not VoIP), WhatsApp, Instagram or TikTok through the real apps instead of unofficial libraries, or any mobile-only app. Sets up Nodo over MCP; new workspaces get 5,000 free credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can connect an agent to a Nodo Android phone for tasks that require a real SIM, SMS access, or a mobile app. They can also configure scheduled Nodo workflows for recurring tasks, with approval before sending or posting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, verification codes, and account sessions placed on Nodo devices are handled by Nodo as a trusted custodian.

Mitigation: Before using sensitive accounts, review Nodo's privacy and deletion controls and specify which actions need approval.

Risk: Scheduled workflows can continue after the chat and local computer are closed, and usage can have ongoing costs.

Mitigation: Confirm the schedule, ongoing costs, how to stop workflows, and how to revoke sessions before enabling recurring tasks.

## Reference(s):

- [Nodo MCP setup guide](https://mcp.nodo.com/start.md)
- [Nodo](https://nodo.com)
- [ClawHub release page](https://clawhub.ai/otto-iron/skills/nodo-real-phone)

## Skill Output:

**Output Type(s):** [Configuration instructions, API calls, Guidance]

**Output Format:** [Natural-language guidance and MCP tool interactions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure a scheduled workflow for recurring tasks.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
