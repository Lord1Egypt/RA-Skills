## Description:

银行保函台账逐项核对，包括保函金额与保证金比例复算、到期日复算、保函号唯一性、注销与状态自洽、到期未注销仍占额度，并为每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and credit-management staff use this skill to check bank guarantee ledgers for arithmetic mismatches, maturity-date errors, duplicate guarantee numbers, inconsistent cancellation status, and expired guarantees that still occupy credit capacity. It is intended for local review of ledger text and does not verify guarantee authenticity or provide legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks ledger consistency but does not verify whether a guarantee is genuine or whether legal, banking, or claim procedures are correct.

Mitigation: Use the output as a ledger-review aid and confirm guarantee authenticity, legal conclusions, and bank process decisions through authoritative business channels.

Risk: The free version explicitly withholds advanced checks such as release schedules, aggregate release totals, contract-overrun checks, and credit-limit comparisons.

Mitigation: Review the reported scope and checks_not_run fields before acting, and perform any withheld checks separately when they are material.

Risk: Incorrect, missing, or non-tabular input can prevent reliable conclusions.

Mitigation: Provide ledger text with the required header fields and treat insufficient-input responses as a request for more data, not as a pass result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/guarantee-letter-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON containing ledger findings, summary totals, scope, and source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over pasted ledger text; insufficient inputs return missing fields instead of conclusions.]

## Skill Version(s):

1.0.54 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
