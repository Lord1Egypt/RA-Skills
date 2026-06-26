## Description: <br>
HireMate is an AI recruiting assistant for creating job descriptions, screening criteria, interview questions, candidate scores, match analyses, salary reports, and interview evaluations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keybryant](https://clawhub.ai/user/keybryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and HR operations staff use this skill to draft recruiting materials, generate structured interview content, compare candidates to job requirements, and prepare hiring-support reports. Candidate scores and recommendations should be treated as draft decision support requiring human HR and legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate scoring and recommendations can affect employment decisions and may rely on sensitive or insufficiently validated criteria. <br>
Mitigation: Use outputs only as draft decision support, require trained human HR and legal review, and document job-related criteria before applying scores. <br>
Risk: Resume text, interview notes, and candidate profiles may contain personal or sensitive information. <br>
Mitigation: Use only authorized candidate data, minimize or redact unnecessary personal details, and keep generated reports private. <br>
Risk: Cultural-fit, employment-gap, auto-reject, or no-hire recommendations may create fairness or compliance concerns. <br>
Mitigation: Remove or constrain those criteria unless they are job-related, consistently applied, documented, and compliant for the hiring context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keybryant/hiremate) <br>
- [Interview questions database](references/interview_questions_db.json) <br>
- [Job description templates](references/jd_templates.json) <br>
- [Salary benchmark data](references/salary_data.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON reports, with CLI command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some scripts can write generated markdown or JSON to an output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
