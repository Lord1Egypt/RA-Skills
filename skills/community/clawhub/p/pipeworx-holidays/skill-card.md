## Description:

Public holidays for 100+ countries, including yearly lookups, checks for whether today is a holiday, and next upcoming holidays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operational teams use this skill to account for country-specific public holidays in scheduling, travel planning, payroll, and HR workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs a mutable npm MCP bridge locally.

Mitigation: Pin mcp-remote to a reviewed exact version before installation and review updates before changing the pinned version.

Risk: Holiday lookup requests are sent to a remote holiday service.

Mitigation: Use the skill only where that remote service is acceptable, and avoid including sensitive data in holiday lookup requests.

Risk: The locally executed bridge may have access to more filesystem or environment data than the task needs.

Mitigation: Run the skill with limited filesystem and environment access.

## Reference(s):

- [Pipeworx holidays ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-holidays)
- [Pipeworx holidays homepage](https://pipeworx.io/packs/holidays)
- [Pipeworx holidays MCP endpoint](https://gateway.pipeworx.io/holidays/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Holiday lookup results as text or JSON, with MCP setup configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a remote holiday service; setup uses a locally executed npm MCP bridge.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
