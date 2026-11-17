## Description:

医疗废物交接登记表逐项核对，执行逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance, cashier, and operations staff use this skill during month-end closing, reconciliation, or inventory checks to verify medical-waste transfer ledgers for arithmetic consistency, required fields, duplicate form numbers, and missing source material.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete regulatory compliance determination.

Mitigation: Use it only for the disclosed table checks and review the listed withheld and out-of-scope checks before relying on results.

Risk: Incomplete or malformed records can prevent supported conclusions.

Mitigation: Preserve table headers and source rows, and treat an insufficient-input status as no conclusion rather than a clean result.

Risk: Medical-waste transfer records may contain sensitive operational or personal data.

Mitigation: Run the checker locally, share only necessary fields, and control access to input and output files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/medical-waste-transfer-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON findings, with Markdown usage guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Node.js checks and returns an insufficient-input status instead of a compliance conclusion when records are incomplete.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
