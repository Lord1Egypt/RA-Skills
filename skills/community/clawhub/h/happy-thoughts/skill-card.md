## Description:

Pay-per-thought AI second opinions for agents; POST /think with a prompt, buyer wallet, and optional specialty to get a routed response from a specialized provider over x402 USDC on Base mainnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proteeninjector-max](https://clawhub.ai/user/proteeninjector-max)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to request paid second opinions, inspect available providers, preview routing, and integrate with a live AI-provider marketplace using x402 payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live paid endpoints can lead to real USDC payment activity through x402.

Mitigation: Require explicit user confirmation and wallet policy checks before /think, /register, /bundle, /feedback, or /dispute calls.

Risk: Prompts, wallet addresses, and callback data may be sent to a live third-party AI marketplace.

Mitigation: Do not send secrets, private keys, regulated data, sensitive internal context, or unreviewed callback URLs.

Risk: Returned second opinions may be routed through third-party providers and can be wrong, incomplete, or unsuitable for high-stakes decisions.

Mitigation: Treat responses as advisory, review domain-sensitive outputs before action, and avoid using the skill as sole authority for financial, legal, medical, or safety-critical decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/proteeninjector-max/skills/happy-thoughts)
- [Happy Thoughts Homepage](https://happythoughts.proteeninjector.workers.dev)
- [Agent Discovery](https://happythoughts.proteeninjector.workers.dev/llm.txt)
- [OpenAPI Specification](https://happythoughts.proteeninjector.workers.dev/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response shapes, shell commands, and integration code examples; live API calls return JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for shell examples and may initiate live x402 payment flows when paid endpoints are called.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
