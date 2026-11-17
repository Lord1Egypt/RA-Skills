## Description:

Automates job search on Indeed, analyzes fit, tailors resumes, applies through supported ATS platforms, and logs application outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abedmir31](https://clawhub.ai/user/abedmir31)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and their agents use this skill to search for matching roles, evaluate fit, tailor an existing resume without adding unsupported claims, submit applications through supported job platforms, and track results.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can auto-submit personal data to third-party job platforms.

Mitigation: Run it in review-only mode or require per-application approval, and limit submissions to intended companies and roles.

Risk: The skill text asks the agent to request passwords or verification codes through Discord when sessions expire.

Mitigation: Complete authentication only on the official job platform sites and do not share passwords or verification codes in Discord.

Risk: Local resume, configuration, and tracking files contain personal contact details and job-search history.

Mitigation: Restrict filesystem access to these files and remove unnecessary personal data before sharing or installing the skill.

Risk: Resume PDF generation compiles LaTeX from resume content.

Mitigation: Harden or sandbox the LaTeX pipeline before using untrusted or agent-generated resume content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abedmir31/skills/job-applications)
- [Publisher profile](https://clawhub.ai/user/abedmir31)
- [Resumake Template 1](https://resumake.io)
- [ShareLaTeX](https://sharelatex.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON tracking records, LaTeX source, and generated resume PDFs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce tailored resume files and application logs based on local candidate configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
