## Description:

HireMate is an AI recruiting assistant that generates job descriptions, screening criteria, interview questions, candidate scores, match analyses, salary reports, and interview evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keybryant](https://clawhub.ai/user/keybryant)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and recruiting operations teams use this skill to draft recruiting materials and produce advisory resume, candidate-fit, salary, and interview assessments. Outputs should support human review rather than replace hiring or compensation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive candidate data such as resumes, interview notes, strengths, concerns, locations, education, and experience.

Mitigation: Use redacted candidate data where possible and store any generated output files in approved, access-controlled locations.

Risk: Candidate scores, match analyses, interview recommendations, screening criteria, salary reports, and cultural-fit fields may affect hiring or compensation decisions without sufficient privacy, fairness, or scope guardrails.

Mitigation: Treat outputs as advisory, require human review, and validate screening, salary, language, cultural-fit, and hire/no-hire criteria against organizational policy and applicable law.

Risk: Salary benchmark outputs depend on bundled reference data that can become stale.

Mitigation: Verify compensation recommendations against current market data and update salary benchmarks on the cadence required by the hiring workflow.

## Reference(s):

- [Job description templates](references/jd_templates.json)
- [Interview questions database](references/interview_questions_db.json)
- [Salary benchmark data](references/salary_data.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, guidance]

**Output Format:** [Markdown or JSON reports written to stdout or an optional output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI scripts generate recruiting documents, scoring summaries, salary reports, and interview evaluation reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
