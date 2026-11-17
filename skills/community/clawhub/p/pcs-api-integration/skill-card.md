## Description:

Helps apps and distribution channels integrate PCS Hub quote, route, and swap handoff flows into frontend experiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to design PCS Hub swap integrations for wallets, webviews, partner browsers, mobile apps, browser extensions, and headless bots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a startup ping that may send telemetry without a clear user opt-in.

Mitigation: Remove the startup ping or make it explicit and opt-in before use.

Risk: Financial amount conversion examples may lose precision.

Mitigation: Use exact BigInt handling or audited fixed-point utilities such as parseUnits and formatUnits.

Risk: The PCS_HUB_TOKEN credential could be exposed if copied into client-side code.

Mitigation: Keep the token server-side or in protected environment configuration and never print it in output.

Risk: Wallet handoff values represent financial transactions.

Mitigation: Require independent wallet-side verification of transaction destination, value, calldata, token amounts, and recipient before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pcs-bot/skills/pcs-api-integration)
- [PancakeSwap AI repository](https://github.com/pancakeswap/pancakeswap-ai)
- [PCS Hub API base URL](https://hub-api.pancakeswap.com/aggregator)
- [PancakeSwap extended token list](https://tokens.pancakeswap.finance/pancakeswap-extended.json)
- [PancakeSwap API access contact](https://t.me/pancakeswap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, TypeScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration specifications and implementation guidance; does not produce executable swap code.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
