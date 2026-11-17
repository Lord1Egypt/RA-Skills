## Description:

Checks hospital and clinic medical-consumable worksheets for stock balance, stock amount, markup-rate, total-row, duplicate-row, blank-field, and negative-value issues, with each finding tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Hospital and clinic pricing, consumables accounting, and finance staff use this skill before monthly closing or pricing self-checks to recalculate worksheet arithmetic and identify rows that need review. It is limited to table-internal checks and does not determine local pricing-policy applicability, procurement-price correctness, physical inventory presence, or medical/clinical guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic findings as legal, medical, or official pricing-policy advice.

Mitigation: Use the skill only as a local worksheet arithmetic checker, and confirm pricing policy, procurement price, and clinical questions with authoritative files and qualified reviewers.

Risk: Hospital consumable worksheets may contain sensitive operational or pricing data.

Mitigation: Run the skill in a controlled local environment, share only the minimum necessary input, and verify deployment controls before processing sensitive worksheets.

Risk: The free version omits zero-rate markup judgment, below-cost charge judgment, three-part amount reconciliation, and impact-ranked adjustment lists.

Mitigation: Review the reported checks_not_run scope and use manual review or a fuller workflow for omitted compliance and impact analyses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/medical-consumable-markup-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient inputs return missing-field guidance without conclusions.]

## Skill Version(s):

1.0.47 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
