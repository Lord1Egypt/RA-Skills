## Description:

Crypto research via Grok model real-time X/Twitter knowledge, forwarding the user's query as-is to the Grok API for token narrative, story, and sentiment research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arespollo](https://clawhub.ai/user/arespollo)

### License/Terms of Use:


## Use Case:

External users and crypto researchers use this skill to ask Grok-compatible models what X/Twitter discourse says about a token or project narrative. It is not intended for price analysis, on-chain data retrieval, or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts are sent to https://ai.a9.bot/v1 using A9_GROK_API_KEY.

Mitigation: Do not include wallet secrets, private strategies, unreleased project details, or unrelated sensitive text in prompts.

Risk: The skill is scoped for crypto narrative research and can produce misleading results if used for trading or price decisions.

Mitigation: Use it only for token narrative, story, sentiment, or CT-discourse research, and avoid invoking it for price analysis, on-chain data, or trade execution.

## Reference(s):

- [Grok-compatible API endpoint](https://ai.a9.bot/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Discord-ready Markdown response from Grok]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forwards the exact user research prompt to the external API and requests up to 8192 output tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
