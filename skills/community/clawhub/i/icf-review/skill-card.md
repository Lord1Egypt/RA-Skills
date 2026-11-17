## Description:

临床试验知情同意书(ICF)全面审查 - 基于GCP/ICH-GCP/FDA/中国法规，对知情同意书进行合规性、完整性、伦理合理性审查，输出结构化审查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenlcj](https://clawhub.ai/user/kenlcj)

### License/Terms of Use:

MIT-0

## Use Case:

IRB/EC reviewers, clinical research teams, and compliance staff use this skill to check informed consent forms against GCP, ICH-GCP, FDA, China regulatory, and ethics requirements. It produces a structured Chinese-language review report with pass/fail checks, deficiencies, risk points, and revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incorrect, incomplete, or jurisdictionally inappropriate ICF review conclusions.

Mitigation: Use qualified human reviewers to verify all clinical, legal, IRB, and regulatory conclusions before decisions are made.

Risk: The workflow may be mistaken for final ethics committee, legal, medical, or regulatory approval.

Mitigation: Treat outputs as drafting and checking assistance only, not as final approval or professional advice.

Risk: The skill expects Chinese-language review output and may not match users expecting another language or local review format.

Mitigation: Confirm language, jurisdiction, and reporting format requirements before relying on the generated review report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenlcj/skills/icf-review)
- [FDA Informed Consent Guidance 2023](artifact/REFERENCES/FDA_Informed_Consent_Guidance_2023.md)
- [ICF Elements Checklist](artifact/REFERENCES/ICF_Elements_Checklist.md)
- [Sample ICF Report](artifact/EXAMPLES/Sample_ICF_Report.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown review report with checklist tables and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; conclusions require qualified human review before clinical-trial, ethics-committee, legal, medical, or regulatory decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
