## Description:

Checks Chinese tax late-payment surcharge tables by recalculating rows, totals, duplicates, and missing fields, with each finding tied to source evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill during closing, reconciliation, or tax payment review to check late-payment surcharge tables for arithmetic consistency, total-row agreement, duplicates, and missing required fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker is limited to arithmetic and table-consistency checks and does not determine legal tax obligations, waivers, or authority-specific treatment.

Mitigation: Use the output as a reconciliation aid and confirm any tax-law interpretation or filing decision with the responsible tax authority or qualified reviewer.

Risk: The free edition explicitly omits some checks, including rate-deviation, negative surcharge, long-overdue, and high-ratio warnings.

Mitigation: Review the reported checks_not_run list before relying on the result, and run additional review steps when omitted checks matter.

Risk: Materials that lack recognizable table headers or required fields produce no conclusion rather than a clean result.

Mitigation: Provide a table with the required headers and treat insufficient-input output as a request for more data, not as evidence that no issue exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/late-fee-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [analysis, text, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON finding report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js checker; reports executed checks, omitted checks, findings, summary counts, and insufficiency guidance when inputs cannot support a conclusion.]

## Skill Version(s):

1.0.42 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
