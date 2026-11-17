## Description:

Placed Career Tools helps agents call the Placed API for resume-job matching, cover letters, LinkedIn optimization, interview questions, salary insights, offer analysis, application tracking, and company research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and career-support agents use this skill to access Placed career tools with a Placed API key. It supports job-fit analysis, resume and cover-letter guidance, application tracking, salary negotiation, offer analysis, and company research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist a Placed API key in a plaintext shell-sourced credentials file.

Mitigation: Prefer a current-session environment variable or secure credential manager; if a file is used, restrict permissions and keep the token out of shared dotfiles and logs.

Risk: Career-related data, including resumes, job descriptions, salary details, and application notes, may be sent to the Placed API.

Mitigation: Use the skill only when the user accepts sending that data to Placed, and avoid unnecessary sensitive details.

Risk: Application tracker tools can modify or delete job application records.

Mitigation: Confirm status-changing actions with the user, especially delete_job_application, before allowing the API call to run.

## Reference(s):

- [Placed Career Tools API Reference](references/api-guide.md)
- [Placed Homepage](https://placed.exidian.tech)
- [Placed Career Tools on ClawHub](https://clawhub.ai/ajitsingh25/skills/placed-career-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and Placed API responses that may be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PLACED_API_KEY and sends career-related data to the Placed API.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
