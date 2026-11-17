## Description:

A local Chinese-language Node.js checker that runs 14 deterministic manufacturing and production worksheet checks per object directory and reports one conclusion line per object with source file and line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing cost accountants, production statisticians, workshop accountants, and finance managers use this skill during monthly cost close, production report review, inventory and fixed-asset checks, subcontracting settlement, outsourced processing review, and license or special-equipment inspection tracking. It checks supplied local worksheet directories and reports per-object findings with source file and line references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can be mistaken for audit, legal, business approval, or assurance review.

Mitigation: Use results as worksheet-checking assistance only; route findings through qualified audit, legal, finance, or operations reviewers before relying on them.

Risk: User-provided manufacturing worksheets may contain sensitive operational or financial data.

Mitigation: Run the local checker only on worksheet directories intended for analysis and avoid providing unrelated files.

Risk: The free release lists some checks as withheld or not executed.

Mitigation: Review the reported not-executed items before treating a result as complete for a business workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/manufacturing-ops-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON with per-object check results and cited source file and line findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-supplied local worksheet directories, does not write files, and reports withheld checks as not executed.]

## Skill Version(s):

1.0.25 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
