## Description:

JobHound is a full-process job-search assistant for resume analysis, job discovery and scoring, tailored resumes, interview preparation, interview review, offer evaluation, salary negotiation, and application tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucrossmym1nd](https://clawhub.ai/user/ucrossmym1nd)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to plan and manage a job search from resume parsing through applications, interviews, and offer decisions. It is tailored for China campus recruiting and internships while also supporting other regions and role families.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains persistent plaintext job-search memory that can include sensitive career, salary, and interview notes.

Mitigation: Choose a controlled workspace before use, avoid storing unnecessary sensitive details, and review or delete memory files when they are no longer needed.

Risk: Generated HTML resumes may expose unintended personal details or active web content when shared.

Mitigation: Review generated resumes before sharing, sanitize the HTML, or export to a static PDF when appropriate.

## Reference(s):

- [A-G 评估矩阵](references/a-g-matrix.md)
- [STAR 故事银行模板](references/star-bank-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports, HTML resumes, local Markdown/YAML tracking files, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory, application tracking, profile, and output files in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
