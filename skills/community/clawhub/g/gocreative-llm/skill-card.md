## Description:

LLM Gateway provides agent-facing text completions through GoCreative endpoints for Claude, GPT, and DeepSeek-style model tiers with pay-per-call USDC payment via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request AI text completions without direct provider keys, choose a cost and quality tier per task, and route prompts to pay-as-you-go model endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text is sent in URL paths, which can expose sensitive content through logs, browser history, proxies, or monitoring systems.

Mitigation: Use only non-sensitive prompts unless separate privacy assurances are in place, and avoid sending secrets, credentials, regulated data, or confidential customer material.

Risk: The skill can trigger automatic USDC payments through x402 without documented spending limits.

Mitigation: Configure wallet controls before use, including low balances, per-transaction approval, exact price and recipient checks, and task-level spending limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/gocreative-llm)
- [GoCreative API provider](https://api.gocreativeai.com)
- [GoCreative ask endpoint](https://api.gocreativeai.com/v1/ai/ask/{prompt})
- [GoCreative pro endpoint](https://api.gocreativeai.com/v1/ai/pro/{prompt})
- [GoCreative ultra endpoint](https://api.gocreativeai.com/v1/ai/ultra/{prompt})

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Plain text completions returned by HTTPS GET endpoints, with Markdown guidance for prompt routing and URL encoding.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires URL-encoded prompts in request paths and x402 wallet payment on Base.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
