## Description:

Marrow provides persistent agent memory for OpenClaw by surfacing past failures, logging decisions, and compounding useful patterns across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majinbuu0x9](https://clawhub.ai/user/majinbuu0x9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to make Marrow orientation, action logging, and history lookup part of the agent's default operating flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes Marrow an always-on external memory and logging layer for agent activity.

Mitigation: Install it only when persistent external memory is intended, and confirm privacy, retention, sharing, and import/export policies before use.

Risk: Logged actions could expose sensitive information if agents include secrets, credentials, PII, or sensitive file contents.

Mitigation: Keep logs limited to actions and outcomes, strip sensitive payloads, and avoid highly sensitive work unless explicit controls and approvals are in place.

Risk: Memory lookups and prior decisions can influence future task flow.

Mitigation: Review surfaced warnings and recommendations before acting, especially for unfamiliar, risky, or security-sensitive work.

## Reference(s):

- [Marrow MCP quick reference](references/marrow-api.md)
- [Marrow homepage](https://getmarrow.ai)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MARROW_API_KEY and an available @getmarrow/mcp server.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
