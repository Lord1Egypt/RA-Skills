## Description:

Supports Questrade browser trade preparation and monitoring with Yahoo Finance quote cross-checks, manual execution guardrails, and local checklist artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[witty-quotes25](https://clawhub.ai/user/witty-quotes25)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare, review, and monitor Questrade Web order tickets while keeping broker submission manual and sensitive account data local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated checklist may appear to prove that a live trade is safe or compliant.

Mitigation: Treat the checklist as a drafting aid and manually verify risk, buying power, quote freshness, symbol, side, quantity, and broker state before submitting in Questrade.

Risk: Live market data or broker-vs-reference price differences may be stale or misleading.

Mitigation: Refresh market data and block or revisit the workflow when data age or price drift exceeds the configured thresholds.

Risk: Sensitive brokerage identifiers or secrets could be exposed in prompts, files, or logs.

Mitigation: Keep credentials and MFA data user-side only, mask account identifiers by default, and include raw identifiers only with explicit local-only confirmation.

Risk: Ambiguous trade parameters can lead to the wrong order ticket.

Mitigation: Refuse missing or ambiguous symbol, side, quantity, order type, or price inputs and require human confirmation before broker submission.

## Reference(s):

- [OpenClaw.ai Policy Compliance](artifact/references/openclaw-policy-compliance.md)
- [Questrade Browser Playbook](artifact/references/questrade-browser-playbook.md)
- [Open Claw Questrade Data Contracts](artifact/references/data-contracts.md)
- [ClawHub Skill Page](https://clawhub.ai/witty-quotes25/skills/openclaw-questrade)
- [Publisher Profile](https://clawhub.ai/user/witty-quotes25)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown checklists, JSON or CSV market snapshots, and concise execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local by default; account identifiers are masked unless explicitly requested with local-only sensitive storage confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
