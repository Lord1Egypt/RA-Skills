## Description:

Fetch and triage the latest unread RSS/news entries from a Miniflux instance via its REST API using an API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hartlco](https://clawhub.ai/user/hartlco)

### License/Terms of Use:


## Use Case:

Developers and users with Miniflux accounts use this skill to list unread RSS entries, inspect full article content, summarize selected entries, and explicitly mark selected entries as read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Miniflux API tokens could be exposed if configured or used unsafely.

Mitigation: Use an HTTPS Miniflux URL, prefer a limited-purpose token, avoid passing real tokens on the command line, and store local credentials with restrictive permissions.

Risk: Explicit mark-read commands can change feed state in the connected Miniflux account.

Mitigation: Only mark entries as read when the user explicitly requests specific IDs or a category, require the script's --confirm flag, and keep category operations bounded by a limit.

## Reference(s):

- [Miniflux API notes](references/miniflux-api-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown lists and summaries, with optional JSON output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include entry IDs, feed titles, links, article content, and explicit read-state update confirmations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
