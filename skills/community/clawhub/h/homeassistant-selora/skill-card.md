## Description:

Connects an agent to Home Assistant through Selora AI to inspect home status, control devices, and manage automations and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lafoush](https://clawhub.ai/user/lafoush)

### License/Terms of Use:

MIT-0

## Use Case:

Home Assistant users can ask their agent to check home status, control devices, diagnose problems, and create or update automations, dashboards, and other home settings through Selora AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device control and configuration changes can affect physical safety or disrupt the home.

Mitigation: Require explicit user approval before changes, and review proposed changes and risk assessments before high-impact actions.

Risk: Home state, history, and camera images can expose private household information.

Mitigation: Access cameras only on request and use OAuth or a scoped, least-privilege token rather than unnecessary admin access.

Risk: The optional troubleshooting command can execute a package version that has not been pinned.

Mitigation: Do not run the optional npx command unless the current package source is trusted.

## Reference(s):

- [Home Assistant skill release](https://clawhub.ai/lafoush/skills/homeassistant-selora)
- [Selora AI installation guide](https://selorahomes.com/docs/selora-ai/installation/)
- [Selora AI MCP tool reference](artifact/references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Conversational text or Markdown, with configuration examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report device states, camera observations, risk assessments, and results of user-approved home changes.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
