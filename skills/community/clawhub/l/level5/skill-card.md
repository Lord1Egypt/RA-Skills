## Description:

Budget Management for AI Agents - USDC billing gateway. Deposit USDC on Solana; pay for LLM compute per token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris-gilbert](https://clawhub.ai/user/chris-gilbert)

### License/Terms of Use:


## Use Case:

External developers and agent operators use Level5 to register and configure a USDC-funded LLM billing proxy for OpenAI, Anthropic, and OpenRouter-compatible clients. Agents can provide setup guidance, shell commands, SDK configuration examples, dashboard links, and balance-aware proxy usage after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and responses may be routed through the Level5 proxy service.

Mitigation: Install only when Level5 is approved for the intended data, and avoid using it for secrets or regulated data unless that approval exists.

Risk: Dashboard and proxy URLs include token-bearing account access information.

Mitigation: Treat dashboard and proxy URLs as sensitive credentials and avoid placing them in logs, tickets, screenshots, or shared chats.

## Reference(s):

- [Level5 homepage](https://level5.cloud)
- [Level5 agent service descriptor](https://level5.cloud/.well-known/agent-service.json)
- [ClawHub skill page](https://clawhub.ai/chris-gilbert/skills/level5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, JSON examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes registration, dashboard, balance, pricing, and proxy configuration guidance; network actions are described as requiring explicit user confirmation.]

## Skill Version(s):

1.6.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
