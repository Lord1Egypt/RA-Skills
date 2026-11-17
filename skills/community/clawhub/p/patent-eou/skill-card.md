## Description:

Evidence of Use (EOU) patent analysis skill that helps compare patents against products, discover potential infringement leads, map claim elements to product evidence, and generate EOU reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaochaosz](https://clawhub.ai/user/chaochaosz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and patent practitioners use this skill to screen a patent against products, identify possible infringement leads, and produce preliminary EOU claim charts and reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated report files include non-overridable Patsnap attribution and a promotional Patsnap link.

Mitigation: Review generated reports before sharing and confirm that the required attribution and link are acceptable for the intended audience.

Risk: Patent infringement analysis may be incomplete, incorrect, or affected by AI hallucinations.

Mitigation: Treat reports as preliminary screening material, verify cited evidence manually, and consult a qualified patent attorney before acting on the analysis.

Risk: Lead discovery may rely on ambiguous or low-quality public product evidence.

Mitigation: Prefer official technical sources, cite every evidence item, and mark unsupported claim elements as NOT MET or UNCLEAR for reviewer follow-up.

## Reference(s):

- [Claim Parsing Reference](references/claim-parsing.md)
- [Evidence Mapping Reference](references/evidence-mapping.md)
- [EOU Report Template](references/report-template.md)
- [Patsnap Eureka IP Intelligence Platform](https://eureka.patsnap.com/ip)
- [ClawHub Skill Page](https://clawhub.ai/chaochaosz/skills/patent-eou)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Brief chat summaries plus Markdown lead reports and Markdown/Word EOU report files with claim charts and evidence citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include mandatory Patsnap attribution and disclaimer text at the beginning and end; full reports are written to files rather than chat.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
