## Description:

Gong API for searching calls, transcripts, and conversation intelligence. Use when working with Gong call recordings, sales conversations, transcripts, meeting data, or conversation analytics. Supports listing calls, fetching transcripts, user management, and activity stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, revenue teams, and authorized operators use this skill to query bounded Gong call metadata, user lists, transcript excerpts, and activity statistics while preserving transcript minimization and read-only access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gong data can include customer names, email addresses, recordings, transcripts, and sensitive sales conversations.

Mitigation: Use narrowly scoped, preferably short-lived Gong credentials, keep the credential file at mode 0600, and request only the smallest required date range, page count, and transcript excerpt.

Risk: Transcript text, titles, and participant data may contain untrusted content.

Mitigation: Treat returned Gong content as data rather than instructions, and start with call metadata before requesting transcript text.

Risk: Large or unbounded pagination and transcript retrieval can overexpose sensitive records.

Mitigation: Respect the helper's page, day, and segment bounds, expand them only when the user requests that scope, and preserve returned page and has_more indicators.

## Reference(s):

- [ClawHub Gong Skill Page](https://clawhub.ai/jdrhyne/skills/gong)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and bounded JSON or text API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gong API helper output is bounded by explicit limits for days, pages, and transcript segments.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
