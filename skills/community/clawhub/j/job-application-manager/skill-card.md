## Description:

Syncs job application emails from Gmail and updates statuses in a Notion or SQLite tracker, detecting offers, rejections, interview invitations, and follow-up needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to keep a job application tracker current from Gmail activity, with optional writes to Notion, a local SQLite database, and Google Calendar interview events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive job-related Gmail threads and write extracted details to a tracker.

Mitigation: Use it only with explicit consent for Gmail access and tracker writes, and review the data it will sync before installation.

Risk: SQLite persistence can be unsafe when the database path is user-supplied, profile-loaded, or passed through shell interpolation.

Mitigation: Prefer the Notion backend or a fixed trusted SQLite path; validate and pass SQLite paths safely without shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyuan99/skills/job-application-manager)
- [Publisher profile](https://clawhub.ai/user/chenyuan99)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured tracker content, JSON-like API payloads, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read job-related Gmail threads and write extracted application details to Notion, SQLite, or Google Calendar when configured.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata; artifact frontmatter version 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
