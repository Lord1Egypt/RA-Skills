## Description:

Connect AI agents to external APIs through Nango, with guidance for OAuth, API-key authentication, MCP server use, and tool-calling patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to configure Nango-backed OAuth and API-key connections, explore provider capabilities, and adapt example agent tool patterns for services such as Google, Slack, GitHub, Notion, Stripe, and Salesforce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can receive broad access to connected third-party accounts and write-capable API patterns.

Mitigation: Use least-privilege Nango keys and provider scopes, and require explicit confirmation before sending messages, creating issues, updating records, or making other mutating API calls.

Risk: Secrets and provider credentials can be exposed through prompts, logs, or insecure configuration.

Mitigation: Keep Nango and provider credentials in environment variables or a secret store, and keep secrets out of prompts, generated code examples, and logs.

Risk: External SDKs and provider APIs can change behavior or permissions over time.

Mitigation: Pin SDK versions, test each target provider in a controlled environment, and review requested scopes before production use.

## Reference(s):

- [Nango Provider Reference](references/providers.md)
- [Nango Documentation](https://docs.nango.dev)
- [Nango Integration Catalog](https://nango.dev/integrations)
- [Nango GitHub Repository](https://github.com/NangoHQ/nango)
- [ClawHub Skill Page](https://clawhub.ai/engsathiago/skills/nango-api-integration)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python, TypeScript, shell, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example scripts for mocked provider calls and a connection tester that requires NANGO_SECRET_KEY for live checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
