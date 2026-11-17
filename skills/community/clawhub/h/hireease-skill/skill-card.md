## Description:

Tailor a client resume for a matching new job, generate a PDF from the tailored LaTeX, and record the application in the HireEase portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibrahimsaleem](https://clawhub.ai/user/ibrahimsaleem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate a HireEase workflow that selects a client and job, tailors a resume, generates a PDF, and records the job application when explicitly confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-supplied API base URL could receive reusable HireEase credentials.

Mitigation: Restrict the API base URL to approved HireEase HTTPS origins before login and keep credentials in configured environment secrets.

Risk: Generated resumes may expose personal information through a public Google Drive link.

Mitigation: Review resume contents and Drive sharing settings before creating or submitting a public viewer link.

Risk: The workflow can create a real HireEase application record.

Mitigation: Require explicit confirmation before recording the application and stop after PDF generation when the user chooses not to submit for real.

## Reference(s):

- [HireEase Skill on ClawHub](https://clawhub.ai/ibrahimsaleem/skills/hireease-skill)
- [HireEase production base URL](https://hireease.me)
- [HireEase Render deployment base URL](https://hireease-s33h.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, files, API calls]

**Output Format:** [Markdown final summary with saved LaTeX and PDF file paths plus HireEase application details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a tailored LaTeX resume, generated PDF, and optional HireEase application record when the user confirms real submission.]

## Skill Version(s):

1.0.1 (source: artifact/skill.md frontmatter; release metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
