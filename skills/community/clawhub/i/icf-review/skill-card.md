## Description: <br>
Reviews clinical trial informed consent forms for compliance, completeness, and ethical reasonableness against GCP, ICH-GCP, FDA, and Chinese regulatory expectations, then produces a structured Markdown review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenlcj](https://clawhub.ai/user/kenlcj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical research, IRB/EC, compliance, and study operations users use this skill to review informed consent forms against required consent elements and identify missing clauses, non-compliant wording, ethical risks, required revisions, and suggested improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release metadata includes unrelated wallet, purchase, crypto, and credential capability tags that could be mistaken for actual permissions. <br>
Mitigation: Confirm the install environment does not grant permissions based only on those tags and rely on the clean security verdict and source review before use. <br>
Risk: Informed consent forms may contain patient, subject, sponsor, or study-sensitive information. <br>
Mitigation: Process real consent documents only in environments approved by the user's organization and applicable clinical research privacy controls. <br>
Risk: The PDF conversion helper depends on a local markitdown installation and creates derived Markdown for review. <br>
Mitigation: Use a trusted local markitdown installation and review the converted Markdown before relying on the generated compliance report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenlcj/icf-review) <br>
- [FDA Informed Consent Guidance 2023](REFERENCES/FDA_Informed_Consent_Guidance_2023.md) <br>
- [ICF Elements Checklist](REFERENCES/ICF_Elements_Checklist.md) <br>
- [Sample ICF Report](EXAMPLES/Sample_ICF_Report.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with checklist tables, findings, risk notes, and revision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local shell workflow guidance for converting PDF consent forms to Markdown before review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
