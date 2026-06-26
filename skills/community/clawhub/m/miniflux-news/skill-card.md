## Description: <br>
Fetch and triage the latest unread RSS/news entries from a Miniflux instance via its REST API using an API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hartlco](https://clawhub.ai/user/hartlco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to fetch unread Miniflux RSS entries, list recent items with links, inspect entry content, and summarize selected entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Miniflux API token to access a user's RSS account. <br>
Mitigation: Install only when the publisher is trusted, use HTTPS, prefer the narrowest token Miniflux supports, and protect the local config file. <br>
Risk: Mark-read operations can change account state. <br>
Mitigation: Run mark-read and mark-read-category only after checking the target IDs or category; the artifact requires explicit user intent and a --confirm flag. <br>


## Reference(s): <br>
- [Miniflux API notes](references/miniflux-api-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional JSON from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include entry IDs, titles, feed names, links, summaries, troubleshooting guidance, and explicit mark-read commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
