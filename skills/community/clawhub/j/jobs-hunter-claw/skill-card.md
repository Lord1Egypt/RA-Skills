## Description:

Automate job discovery, application submission, status tracking, and activity logging using Google Sheets as the central data store for a job hunt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quantdeveloperusa](https://clawhub.ai/user/quantdeveloperusa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage a job-search pipeline in Google Sheets, including discovered roles, applications, interview status, recruiter follow-ups, and periodic reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe CLI input handling may allow job or search text to execute local code under the user's account.

Mitigation: Avoid untrusted recruiter or job-posting text until the input-handling issues are fixed, and review the skill before installing.

Risk: Google Sheets automation can expose or modify sensitive job-search data.

Mitigation: Use a dedicated Google account or least-privilege credentials and limit email or calendar automation to job-related labels and calendars.

Risk: Cron jobs and force-delete operations can make repeated or destructive spreadsheet changes.

Mitigation: Back up the spreadsheet and test with limited data before enabling cron automation or force-delete workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quantdeveloperusa/skills/jobs-hunter-claw)
- [Google Sheet Setup Guide](references/google-sheet-setup.md)
- [gog CLI](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and optional Google Apps Script code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Sheets, the gog CLI, bash, and a JOB_TRACKER_SPREADSHEET_ID environment variable.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
