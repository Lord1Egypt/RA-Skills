## Description:

No-key web search for autonomous agents. One Jarvis call, paid per use with Base USDC x402; You.com routes first with automatic Exa fallback. Fixed maximum buyer price $0.012. No search-provider account or API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yl124915300-dot](https://clawhub.ai/user/yl124915300-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill when an agent needs current public-web search without provisioning You.com or Exa credentials. It guides the agent through a paid x402 Base USDC search flow with a fixed maximum buyer price of $0.012 per call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could authorize an unnecessary paid search.

Mitigation: Use the skill only for genuine current-web search needs and enforce the documented maximum of 12000 atomic USDC ($0.012) before funding.

Risk: Improper wallet handling could expose payment credentials or custody of funds.

Mitigation: Use only the buyer's own x402 wallet/client, never provide private keys or seed phrases to the skill, and validate the x402 v2 Base/USDC challenge before funding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yl124915300-dot/skills/jarvis-a2a-search-buyer)
- [Jarvis A2A router manifest](https://jarvis-orderflow-router.yl124915300.workers.dev/.well-known/jarvis-a2a-router.json)
- [x402 buyer integration examples](https://jarvis-orderflow-router.yl124915300.workers.dev/integrations/x402-buyers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Terminal search outcome is SUCCESS or FAILED; the documented maximum buyer price is 12000 atomic USDC ($0.012) per search.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
