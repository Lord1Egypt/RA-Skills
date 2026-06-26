## Description: <br>
Create or update a pawr.link profile. $9 USDC self-service (instant) or $10 curated (AI-built, ~1 min). Free profile discovery API. All payments via x402 on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baseddesigner](https://clawhub.ai/user/baseddesigner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, update, and discover public pawr.link profiles for agents, including link lists, social embeds, token widgets, and machine-readable profile data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create and update examples can trigger paid x402 USDC actions and publish or modify public profile content. <br>
Mitigation: Before running paid examples, confirm the endpoint, username, wallet, profile content, and USDC price; prefer a dedicated wallet with limited funds or spending controls. <br>


## Reference(s): <br>
- [pawr.link](https://pawr.link) <br>
- [pawr.link ClawHub page](https://clawhub.ai/baseddesigner/pawr-link) <br>
- [x402](https://www.x402.org/) <br>
- [Bankr SDK documentation](https://docs.bankr.bot/) <br>
- [Clawlinker](https://pawr.link/clawlinker) <br>
- [Agent Card](https://pawr.link/.well-known/agent.json) <br>
- [LLM Context](https://pawr.link/llms.txt) <br>
- [PawrLinkRegistry](https://basescan.org/address/0x760399bCdc452f015793e0C52258F2Fb9D096905#writeContract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for command examples; some create and update flows require x402-compatible USDC payment on Base.] <br>

## Skill Version(s): <br>
4.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
