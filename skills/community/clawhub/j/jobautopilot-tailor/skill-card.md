## Description:

Tailors a user's resume and cover letter to a specific job description, using the user's source resume materials and job tracker to produce Markdown drafts and polished DOCX files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerronl](https://clawhub.ai/user/jerronl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to tailor truthful resume and cover-letter materials for shortlisted jobs, convert them to DOCX, and update the job-search tracker for handoff to a submitter workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads resume materials, contact details, and job tracker entries that may contain sensitive personal information.

Mitigation: Use a dedicated resume folder and tracker with only the files needed for the workflow, and run the skill in a restricted environment when possible.

Risk: The skill generates application documents and updates tracker status, so incorrect tailoring or formatting could affect an application.

Mitigation: Review generated Markdown and DOCX files before sending them, and confirm tracker updates after each job.

Risk: The workflow depends on Python packages and local conversion scripts.

Mitigation: Pin dependencies and review the configured conversion script path before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerronl/skills/jobautopilot-tailor)
- [Jobautopilot Repository](https://github.com/jerronl/jobautopilot)
- [Sample DOCX Template](https://github.com/jerronl/jobautopilot/raw/main/jobautopilot-tailor/scripts/sample_placeholders.docx)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, DOCX files, tracker updates, shell commands, and concise status reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local resume, tracker, template, and contact-info environment variables; generated documents should be reviewed before use.]

## Skill Version(s):

1.3.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
