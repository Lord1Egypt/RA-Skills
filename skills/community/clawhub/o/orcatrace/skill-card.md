## Description:

Polymarket intelligence for AI agents: real-time prediction-market signals, whale calibration, digest summaries, resolving-soon markets, and paid single-market research through OrcaTrace APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover OrcaTrace's free and paid Polymarket intelligence endpoints, inspect response shapes, and make x402-paid API calls when market analysis is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid examples can sign USDC payments from a wallet key.

Mitigation: Use a limited wallet, verify route price challenges, and require explicit approval before paid requests.

Risk: Prediction-market intelligence and LLM-synthesized analysis may be wrong, stale, or unsuitable for financial decisions.

Mitigation: Treat outputs as informational, check response createdAt provenance, and cross-check claims against primary market data before acting.

Risk: Free and paid endpoints call an external OrcaTrace API.

Mitigation: Install only when the agent is expected to contact OrcaTrace and keep network/payment permissions scoped to that task.

## Reference(s):

- [OrcaTrace Website](https://orcatrace.dev)
- [OrcaTrace API](https://api.orcatrace.dev)
- [OpenAPI Specification](https://api.orcatrace.dev/openapi.json)
- [Discovery Document](https://api.orcatrace.dev/discovery)
- [x402 Payment Manifest](https://api.orcatrace.dev/.well-known/x402)
- [A2A Agent Card](https://api.orcatrace.dev/.well-known/agent-card.json)
- [ClawHub Skill Page](https://clawhub.ai/jcislo/skills/orcatrace)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with curl commands, TypeScript examples, endpoint tables, and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide paid x402 calls using USDC on Base; free endpoints are available for shape testing before payment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
