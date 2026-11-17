## Description:

Automated job application assistant for job-email-apply skill only. Searches for jobs, composes personalised application emails with CV attached, sends via Gmail SMTP (with manual approval per email), and maintains a JSON tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to search job listings, draft tailored application emails, send approved Gmail SMTP messages with a CV attached, and maintain a local JSON application tracker. It is intended for explicit job-email-apply commands such as searching jobs, drafting applications, sending applications, checking the tracker, updating status, or checking inbox replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Gmail, CV, and application-tracker data.

Mitigation: Use a dedicated Gmail account and app password, keep CONFIG.md, SMTP-SECRET.txt, the CV, and Applications.json local and private, and revoke the app password if exposure is suspected.

Risk: Outbound applications could send incorrect personal claims, credentials, or unintended recipient data.

Mitigation: Review every drafted email before approval; the skill requires explicit confirmation, validates recipient and CV path, and checks that subject, body, and URLs do not contain credentials before sending.

Risk: Job listings, company pages, and incoming recruiter emails may contain untrusted instructions or misleading content.

Mitigation: Treat external content only as data for extraction, ignore embedded workflow changes, store minimal parsed excerpts, and mark ambiguous inbox replies as NEEDS_REVIEW.

Risk: Automatic tracker retention may remove older entries from the active Applications.json file.

Mitigation: Clarify the 180-day archive behavior before use and review applications_archive.json expectations if active-history retention matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z-hussein/skills/job-apply-automation)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Configuration template](references/config.md)
- [Email templates](references/email-templates.md)
- [Tracker commands](references/Tracker-commands.md)
- [Platform notes](references/Platform-notes.md)
- [Job profile template](references/job-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, drafted email text, JSON tracker updates, and setup shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outbound emails require explicit user approval before sending; application state is stored in Applications.json.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
