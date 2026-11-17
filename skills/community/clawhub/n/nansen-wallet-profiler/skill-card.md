## Description:

Wallet profiler — balance, PnL, labels, transactions, counterparties, related wallets, batch, trace, compare. Use when analysing a specific wallet address or comparing wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect blockchain wallet balances, PnL, labels, transactions, and counterparties, or to batch, trace, and compare wallet activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Name-based search extends the skill beyond profiling a supplied wallet address.

Mitigation: Review whether name searches are intended before use; use address-based commands when analyzing a known wallet.

Risk: Research calls, including calls in loops, can trigger x402 payments from the configured wallet under its existing authorization and spending policy.

Mitigation: Review payment policy and spending limits before running calls; keep trace width and loop size conservative.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, JSON, CSV]

**Output Format:** [CLI results as JSON, CSV, or human-readable tables, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet research results depend on the selected addresses, chain, and query options. Trace and repeated calls can incur payment under the configured wallet policy.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
