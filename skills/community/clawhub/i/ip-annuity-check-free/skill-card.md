## Description:

知识产权年费与续展台账逐项核对，算下次缴费日、已缴合计与到期天数，查重复申请号、空缺、周期与日期倒挂，每条结论都带原文行号，不需要付款，也不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, intellectual-property, and finance teams use this skill to check copied IP annuity and renewal ledgers before payment or follow-up. It recalculates ledger-derived dates and fee totals, flags missing or inconsistent rows, and cites source line numbers for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the output as legal advice, official deadline monitoring, fee validation, or proof that renewal obligations have been satisfied.

Mitigation: Treat results as a ledger consistency check only and verify deadlines, legal status, fee standards, and renewal obligations against official records or qualified counsel.

Risk: The skill reads copied IP ledger data supplied by the user.

Mitigation: Run it only in a trusted local workspace and avoid supplying data that should not be processed by the current agent environment.

Risk: The free version intentionally omits checks such as overdue-payment schedules, 90/180-day planning tables, status/payment contradiction checks, duplicate charging checks, and agency-fee anomaly checks.

Mitigation: Review the listed withheld checks and do not interpret a clean free-version run as full annuity or renewal compliance coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ip-annuity-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, shell commands]

**Output Format:** [Human-readable Chinese text or JSON findings with source line numbers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with bundled Node.js scripts; materials must be supplied as JSON or copied ledger text with headers.]

## Skill Version(s):

1.0.20 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
