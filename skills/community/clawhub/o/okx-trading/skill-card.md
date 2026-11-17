## Description:

Trade crypto on OKX with a strict human-in-the-loop confirmation gate for balances, prices, trade proposals, confirmed execution, DCA, grid strategies, snapshots, and PnL digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vm-development](https://clawhub.ai/user/vm-development)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to inspect OKX account and market data, prepare DCA or grid trading plans, and execute only explicitly confirmed OKX trades. It is intended for operators who can review trading proposals and manage exchange credentials, limits, and live-trading risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval and guardrail design may not reliably prevent unintended live orders.

Mitigation: Use demo mode first, keep live trading disabled until reviewed, require explicit confirmation for order placement, and set small per-trade and daily notional caps.

Risk: OKX credentials can authorize high-impact trading actions if over-scoped or exposed.

Mitigation: Use tightly scoped OKX API keys with no withdrawal permission, apply IP restrictions where available, and rotate keys after testing or suspected exposure.

Risk: Grid automation can restock or rescale within pre-authorized bounds and may amplify losses if limits are misconfigured.

Mitigation: Avoid live grid autonomy until the confirmation-token, guardrail recheck, and concurrency issues are fixed; when testing, configure conservative position caps, daily caps, and maximum rescales.

Risk: Unpinned dependencies can change trading behavior after installation.

Mitigation: Pin reviewed dependency versions before use and re-test OKX calls after dependency updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vm-development/skills/okx-trading)
- [ClawHub publisher profile](https://clawhub.ai/user/vm-development)
- [OKX account and API setup](https://www.okx.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts emit text or JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local pending proposal, strategy, notional, snapshot, and audit files; trading commands require OKX credentials and configured guardrail environment variables.]

## Skill Version(s):

0.3.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
