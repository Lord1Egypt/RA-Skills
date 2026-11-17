## Description:

Checks platform settlement aging and in-transit fund tables by recalculating rows, reconciling totals, and detecting duplicate, blank, placeholder, or negative entries, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and settlement operations users can use this skill during monthly close, reconciliation, or inventory review to check platform settlement and in-transit fund tables. It helps recalculate stated amounts, compare detail rows against totals, and identify data gaps without making platform-rule or accounting-policy judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes financial settlement table contents supplied by the user.

Mitigation: Run it only in an approved local environment and avoid providing data that the operator is not permitted to process with this third-party skill.

Risk: The free edition does not perform every settlement-aging check and does not validate platform rules, fee policy, accounting treatment, bank records, ERP records, tax handling, or cash-flow modeling.

Mitigation: Review the listed free-version scope and withheld checks, and verify conclusions against platform exports, accounting policy, and source records before relying on the results.

Risk: A clean security scan does not guarantee that financial conclusions are complete or suitable for a specific business decision.

Mitigation: Treat the output as a reconciliation aid with source-row references, and have qualified finance personnel review exceptions and missing-data notices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/platform-settlement-aging-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON findings from a local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs on user-provided settlement table data; the free edition lists withheld checks and returns insufficient-input guidance rather than conclusions when required material is missing.]

## Skill Version(s):

1.0.51 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
