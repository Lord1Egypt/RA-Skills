## Description:

Generates Chinese retirement and inheritance risk assessment reports from structured interview notes, including family diagrams, P0-P3 risk prioritization, legal reference notes, tool-direction matrices, risk summaries, and follow-up agendas without recommending specific products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hukaiyi777](https://clawhub.ai/user/hukaiyi777)

### License/Terms of Use:

MIT-0

## Use Case:

External advisors and agents use this skill to turn structured retirement and inheritance interview notes into client-facing Chinese risk assessment reports. It is intended for report generation and follow-up planning, not product recommendation or individualized legal, tax, trust, underwriting, or insurance advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain sensitive personal, family, health, asset, or inheritance information.

Mitigation: Use a private working directory, require users to provide only necessary or redacted interview notes, and review the generated report before sharing it.

Risk: The report references legal, tax, trust, underwriting, insurance, and regulatory topics that can become outdated or require professional judgment.

Mitigation: Keep those sections framed as risk context, require human review for legal or product decisions, and verify current regulatory and institutional requirements before relying on the report.

Risk: The bundled local generator depends on Python packages for Word document and image creation.

Mitigation: Review and pin dependencies such as python-docx and pillow, install them from trusted sources, and avoid running the generator with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hukaiyi777/skills/hky-insure-risk-report)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Report template generator](artifact/assets/report_template.py)
- [Example report](artifact/demo/示例-养老与传承风险分析报告.docx)
- [Report preview image](artifact/images/report-preview.png)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated DOCX and PNG files when the bundled Python template is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured interview notes as input; the bundled local generator can produce a Word report and family diagram image.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
