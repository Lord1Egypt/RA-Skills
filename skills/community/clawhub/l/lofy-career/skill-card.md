## Description:

Lofy Career helps agents track job applications, tailor resumes to job descriptions, prepare for interviews with company research, draft follow-ups, and analyze job-search strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrey401](https://clawhub.ai/user/harrey401)

### License/Terms of Use:


## Use Case:

Job seekers and career-support agents use this skill to manage a job-search pipeline, adapt application materials, prepare for interviews, draft follow-ups, and review application-response patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive career and application data may be persisted in a job-application file.

Mitigation: Use the skill only in workspaces where persistent career data is acceptable, and review stored application data regularly.

Risk: Career conversations may trigger state-changing updates without clear confirmation.

Mitigation: Require explicit user confirmation before writing application-status, follow-up, interview, or offer updates.

Risk: The skill may read career-profile information while tailoring resumes or preparing interviews.

Mitigation: Keep profile/career.md limited to information the user is comfortable using for job-search assistance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, draft email text, resume bullet suggestions, and JSON application-tracking updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain data/applications.json and read profile/career.md when those files are available to the agent.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
