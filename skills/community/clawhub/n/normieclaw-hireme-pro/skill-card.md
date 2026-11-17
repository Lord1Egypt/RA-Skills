## Description:

HireMe Pro helps job seekers build ATS-friendly resumes, tailor cover letters, score job matches, prepare for interviews, track applications, and export resume PDFs from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to turn career history and target job postings into tailored resumes, cover letters, interview prep notes, application tracking records, salary negotiation guidance, and exportable resume PDFs. Agents use it as a structured workflow for local resume data management and job-search coaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and application workflows can involve sensitive personal data such as contact details, employment history, salary targets, and interview notes.

Mitigation: Collect only the data needed for the task, keep resume data local where possible, avoid sending PII in web queries, and use restrictive local permissions and encrypted storage for real user data.

Risk: The optional dashboard kit is intended to store profile, resume, application, and activity data, and server security evidence identifies an access-control gap.

Mitigation: Do not deploy the dashboard with real data until all user/profile tables and storage policies have proper row-level access controls reviewed and tested.

Risk: PDF generation depends on Playwright and executes a bundled shell workflow over user-provided resume data and templates.

Mitigation: Pin and review Playwright before installation, run the script only from the skill directory, and use trusted templates and resume JSON inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-hireme-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Setup instructions](artifact/SETUP-PROMPT.md)
- [Security report](artifact/SECURITY.md)
- [Dashboard kit specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Chat guidance, Markdown documents, JSON resume and application data, HTML templates, and PDF files generated through the bundled shell workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF generation requires Python 3 and Playwright; the optional dashboard kit should be reviewed before deployment with real personal data.]

## Skill Version(s):

1.0.3 (source: server release metadata, created 2026-03-31; changelog notes security fixes for script confinement and setup traversal removal)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
