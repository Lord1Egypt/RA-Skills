## Description: <br>
Reads Gmail messages across folders and labels with the gog CLI, including inbox checks, unread-message review, folder listing, Gmail search, and message retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coorops25](https://clawhub.ai/user/Coorops25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and personal Gmail users use this skill to ask an agent to check, search, summarize, and retrieve Gmail messages through the gog CLI. It is also packaged with broader email automation behaviors for organizing, analyzing, responding to, scheduling, and reporting on mail activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may do more than read Gmail, including moving, sending, exporting, monitoring, and externally processing sensitive email data. <br>
Mitigation: Install it only when broad Gmail automation is intended, limit Google scopes where possible, and keep recurring jobs or external notifications disabled unless explicitly needed. <br>
Risk: Bulk delete, archive, send, or export actions can affect many emails or expose message content. <br>
Mitigation: Require clear previews and explicit user confirmation before any bulk delete, archive, send, or export operation. <br>
Risk: User-provided email search text or message content could be unsafe if passed directly into shell commands. <br>
Mitigation: Avoid raw user text in shell commands and construct gog queries with careful quoting and validation. <br>
Risk: Local email logs may retain sensitive metadata or message content. <br>
Mitigation: Periodically review or delete local email logs and avoid storing message content unless the user explicitly requests it. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/Coorops25/gmailcleaner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured email summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON output from the gog CLI for agent-side parsing; result limits are controlled with --max.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
