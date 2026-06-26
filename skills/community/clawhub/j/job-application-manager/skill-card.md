## Description: <br>
Syncs job application emails from Gmail and updates statuses in a Notion or SQLite tracker, including offers, rejections, and interview invitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyuan99](https://clawhub.ai/user/chenyuan99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to keep an application tracker current by reading relevant Gmail threads, classifying application status, syncing Notion or SQLite records, and optionally creating interview calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads job-related Gmail content and may write sensitive application details to Notion or SQLite. <br>
Mitigation: Use narrow Gmail labels where possible and review the configured tracker backend, Notion database, and SQLite path before running syncs. <br>
Risk: Bulk re-enrichment or calendar creation can make many tracker or calendar changes. <br>
Mitigation: Confirm bulk operations and calendar event creation before execution, and review the generated per-application report after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyuan99/job-application-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tracker updates, summaries, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update Notion pages, a local SQLite database, profile.md configuration, and optional calendar events when the relevant integrations are available.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter version 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
