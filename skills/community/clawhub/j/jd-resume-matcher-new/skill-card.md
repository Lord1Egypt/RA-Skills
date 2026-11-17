## Description:

This prompt-only skill analyzes Chinese-language job descriptions and resumes to produce structured job-resume fit reports with deadline handling, red-line checks, evidence-based matching matrices, weighted scoring, gap recommendations, intent checks, and interview question predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moly-yan](https://clawhub.ai/user/moly-yan)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring teams, career advisors, and job seekers use this skill to compare a JD with one or more resumes and generate a structured Markdown assessment of fit, risks, scoring rationale, resume improvement opportunities, intent alignment, and likely interview follow-up questions. It can also provide lighter one-sided analysis when only a JD or only a resume is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JDs and resumes can contain personal, employment, compensation, or business-sensitive information.

Mitigation: Provide only materials that are appropriate to analyze in the active agent environment, and review generated reports before sharing them.

Risk: The skill may process file-based resumes or OCR text where extraction errors can affect dates, numbers, and evidence matching.

Mitigation: Verify extracted text and treat unclear fields conservatively before relying on scoring or red-line conclusions.

Risk: Job-resume fit conclusions can affect hiring or application decisions.

Mitigation: Use the report as decision support and review conclusions against the original JD and resume evidence, especially pending HR-confirmation items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moly-yan/skills/jd-resume-matcher-new)
- [ClawHub publisher profile](https://clawhub.ai/user/moly-yan)
- [Usage guide](artifact/USAGE.md)
- [Standard calibration example](artifact/references/example.md)
- [Boundary calibration example](artifact/references/example-boundary.md)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown report with tables, scoring rationale, recommendations, and interview-preparation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; analyzes user-provided JD and resume content without hidden execution, network access, or persistence beyond normal skill installation.]

## Skill Version(s):

1.4.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
