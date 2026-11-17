## Description:

Proactive Claw is a proactive OpenClaw assistant that learns from calendar and feedback signals to suggest prep blocks, buffers, follow-ups, and scheduling adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googlarz](https://clawhub.ai/user/googlarz)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to review upcoming calendar events and receive locally driven suggestions for preparation time, buffers, follow-ups, and deep-work protection. It can run manually or in a local daemon loop, with approved changes applied to Google Calendar or Nextcloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar credentials and tokens are stored locally and could expose calendar access if the skill workspace is readable by others.

Mitigation: Keep the skill directory private to the local user account, and revoke Google OAuth access or rotate the Nextcloud app password after uninstalling or suspected exposure.

Risk: Nextcloud calendar access can be configured insecurely.

Mitigation: Use HTTPS-only Nextcloud URLs and prefer a dedicated low-privilege app password.

Risk: Calendar suggestions and approved edits may be incorrect or disruptive.

Mitigation: Use the default confirmation mode, review proposed prep blocks, buffers, and follow-ups before applying them, and start with a safe preview run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googlarz/skills/proactive-claw)
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/v3/)
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar)
- [Google OAuth token endpoint](https://oauth2.googleapis.com)
- [Google account app permissions](https://myaccount.google.com/permissions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar changes are suggested by default and applied only after user approval; local state and credentials are stored in the skill workspace.]

## Skill Version(s):

1.2.41 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
