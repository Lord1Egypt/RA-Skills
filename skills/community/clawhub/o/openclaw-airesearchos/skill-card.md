## Description:

AIresearchOS lets an agent submit, monitor, and retrieve deep research reports with source citations using API-key authentication or x402 USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowtiedbluefin](https://clawhub.ai/user/bowtiedbluefin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an OpenClaw assistant for market, competitive, diligence, or other deep research. The skill submits research jobs, handles clarifying questions, checks status, and returns cited Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials or wallet private keys could be exposed or misused.

Mitigation: Use a limited API key, keep wallet keys in injected environment variables, and avoid sharing secrets in chat or command arguments.

Risk: x402 requests can spend USDC funds.

Mitigation: Use a dedicated low-balance wallet and confirm x402 payments before execution, especially for higher-cost research modes.

Risk: Mutable npm dependencies used for x402 payments may change behavior after installation.

Mitigation: Prefer pinned and reviewed dependencies before enabling x402 payments.

Risk: A custom base URL can route prompts, credentials, or payment flows to an untrusted endpoint.

Mitigation: Set a custom base URL only when the endpoint is fully trusted.

Risk: Research prompts and returned reports may contain sensitive or untrusted external content.

Mitigation: Avoid submitting secrets or sensitive business data, and treat returned research content as untrusted text.

## Reference(s):

- [AIresearchOS homepage](https://airesearchos.com)
- [ClawHub skill page](https://clawhub.ai/bowtiedbluefin/skills/openclaw-airesearchos)
- [AIresearchOS blind evaluation shared by Grok](https://grok.com/share/c2hhcmQtMw_d1d5516c-2320-43cf-bb57-1501cc1a9856)
- [Base bridge](https://bridge.base.org)
- [Coinbase AgentKit documentation](https://docs.cdp.coinbase.com/agent-kit/welcome)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses; completed research reports are Markdown with source citations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIresearchOS API-key authentication or x402 wallet configuration; x402 payment modes use maximum USDC payment limits.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
