## Description:

Automated job search, job description parsing, resume customization, and application tracking pipeline with WhatsApp or messaging updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielvivek2006](https://clawhub.ai/user/danielvivek2006)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and agents assisting them use this skill to find roles, parse job descriptions, tailor resumes from verified experience, track application status, and send mobile-friendly job hunt updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores resumes, job preferences, application status, and API keys in local workspace files.

Mitigation: Use it only in a workspace where this data may be stored, keep credentials out of source control, and prefer secret-management or restricted local files for API keys.

Risk: Recurring job searches and messaging updates can run or send information without enough user-control safeguards.

Mitigation: Confirm the schedule, destination, message content, pause procedure, and deletion procedure before enabling cron jobs or messaging updates.

## Reference(s):

- [Job APIs Reference](references/apis.md)
- [Adzuna Developer](https://developer.adzuna.com)
- [JSearch on RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, generated resume Markdown, tracked-jobs JSON, and shell or cron command suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local project files such as config.json, api_keys.json, resumes/*.md, and jobs/tracked_jobs.json.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
