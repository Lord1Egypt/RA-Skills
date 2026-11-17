## Description:

Autonomous Uniswap V3 monitoring on consensus-backed data with on-chain provenance verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerloom-bot](https://clawhub.ai/user/powerloom-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and DeFi operators use this skill to monitor Uniswap V3 pools, detect whale activity and token flows, and request Powerloom provenance checks for returned snapshot data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional wallet-funded signup and top-up flows can sign on-chain payments and require wallet credentials.

Mitigation: Prefer the free-key browser onboarding path; when wallet-funded payment is necessary, use a burner wallet with only the needed funds and verify recipient, amount, chain, token, and plan before confirming.

Risk: API keys, Telegram credentials, and wallet secrets can be exposed if pasted into chat or persisted in long-lived scheduler text.

Mitigation: Store secrets in a proper secret store where possible, avoid primary wallet keys, and remove POWERLOOM_EVM_PRIVATE_KEY after wallet-funded setup or top-up.

Risk: Non-interactive agent runs could otherwise broadcast irreversible transactions without a human pause.

Mitigation: Use dry-run review first; the provided spend scripts require CONFIRM in a TTY or an explicit --yes or one-shot confirmation variable before broadcast.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/powerloom-bot/skills/powerloom-bds-univ3)
- [Powerloom BDS metering](https://bds-metering.powerloom.io)
- [Browser signup and billing](https://bds-metering.powerloom.io/metering)
- [Hosted BDS MCP SSE endpoint](https://bds-mcp.powerloom.io/sse)
- [Powerloom BDS Uniswap V3 repository](https://github.com/powerloom/powerloom-bds-univ3)
- [Powerloom metering contract and service](https://github.com/powerloom/bds-agenthub-billing-metering)
- [bds-agent user guide](https://github.com/powerloom/bds-agent-py/blob/main/docs/USER_GUIDE.md)
- [Quickstart](references/01-quickstart.md)
- [BDS MCP tool catalog](references/02-tool-catalog.md)
- [Verification provenance](references/03-verification.md)
- [Credit budget](references/04-credit-budget.md)
- [Data market scope](references/05-data-market-scope.md)
- [Troubleshooting](references/06-troubleshooting.md)
- [Prompt patterns](references/07-prompt-patterns.md)
- [OpenClaw one-shot wallet-funded onboarding](references/08-openclaw-one-shot.md)
- [OpenClaw one-shot free-key onboarding](references/09-openclaw-one-shot-free-key.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Uniswap V3 monitoring summaries, alert text, API-key setup guidance, and provenance verification status.]

## Skill Version(s):

0.2.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
