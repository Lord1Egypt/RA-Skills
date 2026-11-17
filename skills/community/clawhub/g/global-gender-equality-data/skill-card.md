## Description:

Global Gender Equality Data lets an agent query gender equality indicators for countries or regions through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request World Bank gender equality and women's empowerment indicators, compare gender gaps, and produce country or regional analyses aligned with SDG 5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates schema and example details to live remote instructions that can change after release.

Mitigation: Treat live instructions as untrusted unless they remain within the documented query_gender_data action and avoid requests for secrets or unrelated tool access.

Risk: The documented setup path includes unpinned npx installs for supporting AgentPMT setup skills.

Mitigation: Prefer the OpenClaw install path, or pin and inspect any npx-installed setup skills before use.

Risk: Using the skill requires AgentPMT-hosted calls, account setup, and credit usage.

Mitigation: Install and invoke it only when the operator accepts the AgentPMT account, remote-call, and credit-use requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-gender-equality-data)
- [AgentPMT Publisher Profile](https://clawhub.ai/user/agentpmt)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/gender-equality-women-s-empowerment)
- [Generated Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown instructions with JSON request examples and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls use the query_gender_data action with country_or_region required and optional gender_aspect, calculate_gaps, and time_period parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
