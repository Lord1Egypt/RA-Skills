## Description: <br>
Builds Microsoft Power Platform custom connectors for Independent Publisher and Verified Publisher certification, including Swagger 2.0 definitions, apiProperties configuration, authentication, policy templates, C# custom code, webhook triggers, dynamic values, Copilot Studio extensions, certification checklists, and pac connector CLI guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rwilson504](https://clawhub.ai/user/rwilson504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Power Platform makers, and connector publishers use this skill to create production-ready custom connector files, configure authentication and policy behavior, and prepare submissions for Microsoft Independent Publisher or Verified Publisher certification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can involve OAuth tokens, API keys, SAS URLs, and other sensitive connector credentials. <br>
Mitigation: Use placeholders in generated examples, avoid pasting production secrets into chat, pull requests, or committed files, and submit real secrets only through Microsoft-approved secure channels. <br>
Risk: Generated connector files, custom code, CLI commands, and webhook behavior can affect a real Power Platform environment. <br>
Mitigation: Review generated apiDefinition.swagger.json, apiProperties.json, script.csx, CLI commands, and webhook registration or cleanup behavior before deploying to production. <br>
Risk: SAS URLs or other temporary access links may remain valid longer than intended. <br>
Mitigation: Keep temporary access URLs short-lived and rotate or revoke them after connector validation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rwilson504/power-platform-custom-connector) <br>
- [Publisher Profile](https://clawhub.ai/user/rwilson504) <br>
- [Skill Homepage](https://github.com/rwilson504/agent-skills/tree/main/power-platform-custom-connector) <br>
- [PowerPlatformConnectors Repository](https://github.com/microsoft/PowerPlatformConnectors) <br>
- [OpenAPI Extensions Reference](references/OPENAPI_EXTENSIONS.md) <br>
- [Authentication Patterns Reference](references/AUTH_PATTERNS.md) <br>
- [Policy Templates Reference](references/POLICY_TEMPLATES.md) <br>
- [Custom Code Reference](references/CUSTOM_CODE.md) <br>
- [Webhook Triggers Reference](references/WEBHOOK_TRIGGERS.md) <br>
- [Certification and Submission Reference](references/CERTIFICATION.md) <br>
- [Examples Reference](references/EXAMPLES.md) <br>
- [Common Mistakes Reference](references/COMMON_MISTAKES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, C#, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce connector file templates such as apiDefinition.swagger.json, apiProperties.json, readme.md, icon guidance, and optional script.csx guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
