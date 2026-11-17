## Description:

Automatically fills and submits job applications by opening application pages, completing multi-step forms, uploading tailored resume and cover letter files, confirming submission, and updating a job tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerronl](https://clawhub.ai/user/jerronl)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to automate repetitive job application submission steps after a tailored resume is ready. It fills browser forms, uploads local application documents, handles common dropdown and required-field checks, and records applied, error, or wrong_url status in a tracker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may submit real job applications and upload local resume or cover letter documents.

Mitigation: Require explicit user approval for target jobs and uploaded files, verify the final application state before submit, and record failures or wrong URLs in the tracker.

Risk: Generated temporary shell scripts perform state-changing browser actions.

Mitigation: Use private temporary files, restrict permissions, validate the browser tab and URL before execution, and clean up scripts unconditionally after use.

Risk: Browser form values and application data can expose sensitive personal information to the agent context.

Mitigation: Avoid returning populated field values where possible, exclude credential, payment, and security fields, and keep personal data limited to approved environment variables and local resume files.

Risk: Unpinned runtime dependencies can change behavior over time.

Mitigation: Pin and review required dependencies such as python-docx before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerronl/skills/jobautopilot-submitter)
- [Project homepage](https://github.com/jerronl/jobautopilot)
- [ERRORS.md](artifact/ERRORS.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with bash, JavaScript, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate state-changing browser automation commands, file-upload actions, and tracker status updates during agent execution.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter states 1.3.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
