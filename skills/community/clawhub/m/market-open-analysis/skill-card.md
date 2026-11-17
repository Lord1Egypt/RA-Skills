## Description:

openpd automatically collects WTI crude oil and gold market data, analyzes overnight news, and sends a weekday opening-market forecast report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshengyyy](https://clawhub.ai/user/linshengyyy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate weekday collection of commodity prices and news, generate WTI crude oil and gold opening-market outlooks, and push reports through OpenClaw messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring weekday cron jobs can run automatically without further user interaction.

Mitigation: Review the exact cron entries before enabling the installer, use the status and uninstall commands to audit or remove them, and do not run the installer as root.

Risk: The skill sends generated market reports through OpenClaw messaging to a configured target and channel.

Mitigation: Confirm the delivery channel and recipient before allowing automated pushes, especially when using shared messaging workspaces.

Risk: API keys are configured in local source files by the provided setup flow.

Mitigation: Store API keys outside the skill source when possible, restrict file permissions, and rotate keys if they are copied into committed or shared files.

Risk: Opening-market predictions may be incorrect or delayed and should not be treated as investment advice.

Mitigation: Use the generated reports as informational summaries only and review the underlying market and news sources before making trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshengyyy/skills/market-open-analysis)
- [Artifact README](artifact/README.md)
- [API key configuration guide](artifact/API_KEY.example.md)
- [CommodityPriceAPI](https://commoditypriceapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON price snapshots, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided API keys and OpenClaw messaging configuration; scheduled runs write local data, logs, and reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
