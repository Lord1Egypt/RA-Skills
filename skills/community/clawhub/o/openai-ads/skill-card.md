## Description:

Autonomous AI Marketing & Ads Manager for OpenAI Ads via Habilis MCP Gateway (https://xvix.com.br). End-to-end campaign orchestration, chat_cards synthesis, catalog feeds, and performance telemetry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT

## Use Case:

Developers and marketing operators use this skill to configure an agent for OpenAI Ads campaign orchestration through the Habilis MCP Gateway, including campaign creation, chat_card creation, account checks, campaign listing, and performance insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable advertising credentials are sent through a third-party MCP gateway.

Mitigation: Use test or least-privilege ad accounts and avoid passing long-lived provider API keys through the remote gateway.

Risk: Campaign creation, activation, budgets, destination URLs, and creative changes can affect live ad spend.

Mitigation: Require manual approval before campaign creation, activation, budget changes, destination URL changes, and creative updates.

Risk: Conversion-tracking guidance can involve customer identifiers.

Mitigation: Complete privacy and legal review before using conversion-tracking workflows with customer identifiers.

## Reference(s):

- [Habilis MCP Gateway](https://xvix.com.br/api/mcp)
- [Habilis Developer Portal](https://xvix.com.br)
- [ChatGPT Ads & Chat Card Best Practices](references/chat_card_best_practices.md)
- [Stateless Client-Supplied Credentials Architecture](references/client-supplied-credentials.md)
- [ClawHub Skill Page](https://clawhub.ai/rafacpti23/skills/openai-ads)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup steps, MCP tool invocation guidance, ad creative guidance, and campaign analytics workflows.]

## Skill Version(s):

1.1.4 (source: server release evidence; artifact frontmatter and clawhub.json report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
