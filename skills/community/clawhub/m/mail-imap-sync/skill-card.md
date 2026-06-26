## Description: <br>
Synchronizes configured IMAP mailboxes into local Markdown files using incremental UID-based fetching, date-window modes, and structured time-based storage for AI analysis and mail knowledge-base workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettersao](https://clawhub.ai/user/bettersao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to pull messages from Gmail or other IMAP-compatible mailboxes into local Markdown files for summarization, monitoring, reporting, and local AI knowledge-base ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synced mailbox contents are saved as local Markdown files and may contain sensitive personal or business data. <br>
Mitigation: Keep the emails directory private, restrict filesystem access, and delete saved mail when it is no longer needed. <br>
Risk: IMAP credentials are configured locally and should be treated as secrets. <br>
Mitigation: Use an app-specific IMAP password where supported, keep config.json private, and prefer a virtual environment or container for execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettersao/mail-imap-sync) <br>
- [Publisher profile](https://clawhub.ai/user/bettersao) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, text] <br>
**Output Format:** [Local Markdown email files plus terminal status text and JSON-like synced path summaries described by the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an emails directory organized by account and date, and updates state.json for incremental synchronization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
