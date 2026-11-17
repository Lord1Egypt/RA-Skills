## Description:

计量器具台账与检定证书的到期覆盖、校准周期勾稽、重复登记与合计行逐列复核（共 6 项），材料不足时不给结论，每条结论都引用原文行号与数字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, lab, and equipment-management staff use this skill during monthly metrology checks to compare instrument ledgers with calibration certificate text. It reports expiry coverage, certificate consistency, calibration-cycle arithmetic, duplicate registrations, totals-row errors, and missing or invalid fields when the supplied material is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat local ledger checks as certificate-authenticity or compliance approval.

Mitigation: Review the excluded checks before relying on results; the skill does not verify certificates online, confirm institutional authority, or replace compliance judgment.

Risk: Incomplete ledger or certificate text can produce misleading confidence if interpreted as a clean result.

Mitigation: Use the skill's insufficient_input status and missing-field guidance as a stop condition; do not treat it as evidence that no issues were found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/instrument-calibration-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing findings, summary counts, executed checks, withheld checks, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; requires pasted ledger and certificate text or a JSON payload with text, and may return insufficient_input instead of conclusions when material is incomplete.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
