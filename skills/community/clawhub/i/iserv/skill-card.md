## Description:

HTTP client for IServ school platforms. Log in to an IServ instance (e.g. https://grabbe-dt.de) and fetch common student data like unread mail counts, calendar events, files/folders, tasks/exercises, announcements/news, and other IServ modules via HTTP endpoints. Includes best-effort file ops + exercise submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finnbusse](https://clawhub.ai/user/finnbusse)

### License/Terms of Use:


## Use Case:

Developers and users with authorized IServ accounts use this skill to access school-platform mail, calendar, file, messenger, exercise, and announcement workflows through a command-line HTTP client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live school-platform credentials and account-level access to mail, messenger, files, and exercises.

Mitigation: Install only when the IServ instance and publisher are trusted, provide credentials through environment variables, and use an HTTPS ISERV_BASE_URL.

Risk: Remote messaging, file mutation, and exercise submission commands can change user data on the configured IServ account.

Mitigation: Review command targets before execution and avoid destructive operations unless the destination, path, or submission has been personally verified.

Risk: Evidence reports unsafe URL and filename handling that can expose credentials or overwrite local files.

Mitigation: Treat downloads and submissions as risky until same-origin checks and safe filename handling are added.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment-provided IServ credentials; some commands can read or mutate remote mail, messenger, files, and exercises.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
