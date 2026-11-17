## Description:

Global Energy Power Grid Data helps agents query World Bank energy indicators, including electricity access, renewable and fossil energy mix, per capita consumption, energy intensity, and clean cooking access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to retrieve country or region energy-access, energy-mix, energy-efficiency, and SDG 7 tracking data through AgentPMT-hosted remote tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote install or reinstall guidance can change installed agent components.

Mitigation: Prefer the OpenClaw install path or a pinned, reviewed version of any setup skill before production use.

Risk: The skill relies on AgentPMT-hosted paid remote calls for energy-data queries.

Mitigation: Confirm account, payment, and data-sharing posture before enabling the remote tool for an agent.

Risk: Running documented unpinned npx commands may expose sensitive local environments to changing remote packages.

Mitigation: Avoid those commands in environments with sensitive files, secrets, or elevated permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-energy-power-grid-data)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/energy-access-production)
- [Generated Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON]

**Output Format:** [Markdown instructions with JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines one remote action, query_energy_data, with country or region, energy type, energy mix, urban-rural gap, and time-period parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
