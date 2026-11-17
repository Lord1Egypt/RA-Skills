## Description:

Interact with the Noya AI platform for crypto trading, prediction markets, token analysis, DCA strategies, and structured crypto data via curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noyadev00-gmailcom](https://clawhub.ai/user/noyadev00-gmailcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Noya's crypto data endpoints and interact with Noya's agent workflows for token analysis, portfolio checks, swaps, bridges, transfers, DCA strategies, and prediction markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto prompts, account-linked data, conversation context, or financial data may be shared with Noya or other agents.

Mitigation: Review the exact context and financial data before handoff or delegation workflows, avoid forwarding full summaries, and share only the minimum necessary information.

Risk: Generated user_context.json files may persist sensitive account or financial context on disk.

Mitigation: Delete any generated user_context.json file after use.

Risk: Long-lived API keys increase impact if exposed.

Mitigation: Use a short-lived NOYA_API_KEY where possible and revoke it promptly if compromised.

## Reference(s):

- [Noya homepage](https://agent.noya.ai)
- [Noya docs index](https://mcp.noya.ai/llms.txt)
- [Noya API reference](artifact/reference.md)
- [ClawHub skill page](https://clawhub.ai/noyadev00-gmailcom/skills/noya-agent-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call HTTPS APIs with curl and parse streamed or JSON responses with jq; conversational agent workflows can require NOYA_API_KEY.]

## Skill Version(s):

1.0.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
