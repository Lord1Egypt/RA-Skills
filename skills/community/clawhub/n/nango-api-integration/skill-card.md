## Description: <br>
Connect AI agents to 700+ external APIs using Nango for OAuth handling, authentication flows, and tool calling across external services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure Nango-backed API access, OAuth connections, provider credentials, and MCP-style integration patterns for services such as Google, Slack, GitHub, Salesforce, Stripe, Notion, Linear, and HubSpot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad credential-backed access to external APIs can expose data or perform write actions across connected services. <br>
Mitigation: Use least-privilege OAuth scopes, test accounts where possible, and require explicit approval before write, delete, financial, public-posting, CRM, or repository mutation actions. <br>
Risk: Nango and provider secrets could be exposed through prompts, logs, or generated examples. <br>
Mitigation: Keep NANGO_SECRET_KEY and provider keys in environment variables or secret stores, and avoid including credentials in prompts, logs, or shared outputs. <br>
Risk: Unused or stale provider connections may retain access after an agent workflow is complete. <br>
Mitigation: Review and revoke unused Nango or provider connections when they are no longer needed. <br>


## Reference(s): <br>
- [Nango Provider Reference](references/providers.md) <br>
- [Nango Documentation](https://docs.nango.dev) <br>
- [Nango Integration Catalog](https://nango.dev/integrations) <br>
- [Nango Dashboard](https://app.nango.dev) <br>
- [Nango GitHub Repository](https://github.com/NangoHQ/nango) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, TypeScript, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, provider examples, OAuth and API-key patterns, MCP configuration guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
