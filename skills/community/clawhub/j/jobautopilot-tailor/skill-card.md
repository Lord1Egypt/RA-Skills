## Description: <br>
Tailors resumes and cover letters to specific job descriptions, using the user's source resume materials to produce job-specific markdown and .docx files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerronl](https://clawhub.ai/user/jerronl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-support agents use this skill to tailor truthful resumes and concise cover letters for shortlisted job postings, then prepare files for a downstream application-submission workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads resume files, job tracker content, and personal contact details, so misconfigured paths can expose more personal information than intended. <br>
Mitigation: Keep RESUME_DIR limited to career documents intended for processing and review the configured tracker and contact environment variables before running the skill. <br>
Risk: Generated resumes or cover letters may be malformed, incomplete, or unsuitable to send if the markdown structure or document conversion fails. <br>
Mitigation: Review generated markdown and .docx files, verify there are no leftover placeholders, and confirm the files open correctly before submitting them. <br>
Risk: The resume template is referenced by URL and may not be the expected file if the configured template source changes. <br>
Mitigation: Verify the resume template URL and use a trusted local template path before generating documents. <br>


## Reference(s): <br>
- [Jobautopilot Tailor on ClawHub](https://clawhub.ai/jerronl/jobautopilot-tailor) <br>
- [Sample resume template](https://github.com/jerronl/jobautopilot/raw/main/jobautopilot-tailor/scripts/sample_placeholders.docx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown drafts, .docx files, tracker status updates, and concise progress reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured resume, output, template, tracker, and contact-detail environment variables; generated documents should be reviewed before use.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
