## Description:

Build Power Platform custom connectors for Independent Publisher and Verified Publisher certification, including Swagger 2.0 definitions, authentication, policy templates, custom code, webhook triggers, CLI deployment, and submission preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rwilson504](https://clawhub.ai/user/rwilson504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and connector publishers use this skill to create, check, and submit Power Platform custom connector assets for Microsoft certification. It helps produce connector definitions, configuration files, custom code examples, deployment commands, and certification-ready guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated connector files or deployment commands can affect real Power Platform environments and published connector submissions.

Mitigation: Review apiDefinition.swagger.json, apiProperties.json, readme.md, script.csx, and connector permissions before running authenticated create or update commands.

Risk: Connector configuration and examples may involve API keys, OAuth clients, client secrets, or other credentials.

Mitigation: Use secure connection parameters, avoid committing real secrets, and keep development tooling in an isolated environment with pinned versions where practical.

Risk: Custom code and regex-based transformations can introduce runtime failures or excessive processing time.

Mitigation: Review generated script.csx before deployment, add input limits or regex timeouts, and test custom code behavior before certification or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rwilson504/skills/power-platform-custom-connector)
- [Project homepage](https://github.com/rwilson504/agent-skills/tree/main/power-platform-custom-connector)
- [OpenAPI Extensions Reference](references/OPENAPI_EXTENSIONS.md)
- [Authentication Patterns Reference](references/AUTH_PATTERNS.md)
- [Policy Templates Reference](references/POLICY_TEMPLATES.md)
- [Custom Code Reference](references/CUSTOM_CODE.md)
- [Webhook Triggers Reference](references/WEBHOOK_TRIGGERS.md)
- [Certification and Submission Reference](references/CERTIFICATION.md)
- [Examples Reference](references/EXAMPLES.md)
- [Common Mistakes Reference](references/COMMON_MISTAKES.md)
- [Microsoft PowerPlatformConnectors repository](https://github.com/microsoft/PowerPlatformConnectors)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, C#, PowerShell, and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce connector file templates such as apiDefinition.swagger.json, apiProperties.json, readme.md, icon guidance, and script.csx examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
