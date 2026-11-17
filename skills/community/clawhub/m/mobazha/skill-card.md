## Description:

Entry point for Mobazha skills. Provides an overview of available skills and guides the AI agent to load the right one based on user intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this index skill to identify the appropriate Mobazha companion skill for deployment, onboarding, store connection, operations, content, or marketing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The index can route an agent toward companion skills that may involve server access, credentials, MCP store-management authority, install scripts, or external services.

Mitigation: Review each companion skill separately before use and require explicit user confirmation for high-impact actions.

Risk: Workflows connected to Mobazha stores may require user-provided credentials or service access.

Mitigation: Keep credentials within the active session, avoid logging or transmitting secrets, and confirm the intended connection before proceeding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengzie/skills/mobazha)
- [Mobazha Website](https://mobazha.org)
- [Mobazha Self-Host Guide](https://mobazha.org/self-host)
- [Mobazha Download Page](https://mobazha.org/download)
- [Mobazha SaaS Platform](https://app.mobazha.org)
- [Mobazha GitHub Organization](https://github.com/mobazha)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance and routing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [This index skill does not itself execute commands, access credentials, or persist data; higher-impact actions are delegated to separately reviewed companion skills.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
