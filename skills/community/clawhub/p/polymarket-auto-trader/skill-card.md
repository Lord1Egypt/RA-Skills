## Description:

Autonomous Polymarket prediction-market trading agent that scans markets, estimates probabilities with an LLM, sizes positions with Kelly criterion, and executes trades through the CLOB API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanthbellary](https://clawhub.ai/user/srikanthbellary)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to set up an automated Polymarket trading workflow with wallet approvals, market scanning, LLM-based probability estimates, position sizing, order execution, cron operation, and P&L tracking.

### Deployment Geography for Use:

Outside the United States where legally and contractually permitted

## Known Risks and Mitigations:

Risk: Autonomous real-money trading can lose funds through incorrect model estimates, market movement, bugs, or unattended execution.

Mitigation: Use a dedicated low-balance wallet, start with tiny amounts, add dry-run mode and explicit confirmations, and enforce loss limits before live cron operation.

Risk: Broad token approvals and private-key based wallet access grant persistent financial authority.

Mitigation: Use bounded allowances where possible, revoke approvals when not needed, secure or replace plaintext private-key storage, and restrict host access.

Risk: Jurisdiction and platform-access requirements may make use inappropriate from some locations.

Mitigation: Confirm legal and contractual eligibility before use and deploy only from permitted locations.

Risk: Unbounded market selection can trade unwanted or high-risk markets.

Mitigation: Add market allowlists, position caps, monitoring alerts, and manual review for newly selected markets.

## Reference(s):

- [Polymarket API Reference](references/polymarket-api.md)
- [Polymarket Contract Addresses](references/contract-addresses.md)
- [Publisher homepage](https://github.com/srikanthbellary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, Python scripts, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a live automated trading workflow that requires PRIVATE_KEY and LLM_API_KEY environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
