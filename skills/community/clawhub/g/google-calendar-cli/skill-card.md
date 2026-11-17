## Description:

Google Calendar management via the gog CLI tool. Create, list, update, and delete calendar events with color support, OAuth authentication, and scripting capabilities. Use when working with Google Calendar events, scheduling meetings, checking availability, or managing calendar entries from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and calendar power users use this skill to manage Google Calendar events from an agent-assisted command-line workflow. It helps with listing events, creating or updating calendar entries, checking availability, using event colors, and scripting repeated calendar operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and uses a third-party Google Calendar CLI with OAuth access.

Mitigation: Verify that steipete/tap/gogcli is the intended CLI source and grant only the Google Calendar access needed for the task.

Risk: Automated create, update, or bulk-loop commands can modify real calendar data.

Mitigation: Test scripts on a non-critical calendar before using --no-input or bulk operations on important calendars.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install a third-party CLI, configure OAuth credentials, and create, update, list, or delete Google Calendar events.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
