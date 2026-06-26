## Description: <br>
Nex Timetrack helps freelancers and agencies track billable time with live timers, manual entries, client and project rates, billing summaries, search, and CSV/JSON export using local SQLite storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, agencies, and agents supporting them use this skill to start and stop timers, log work manually, manage client and project rates, summarize billable hours, and export local records for invoicing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported files may include client names, emails, rates, hours, and notes. <br>
Mitigation: Review exported CSV or JSON files before sharing them and protect the local database and export directory as billing records. <br>
Risk: Custom export paths can write outside the skill's own folder and may overwrite user files. <br>
Mitigation: Use the default export location unless the destination path is known and safe. <br>
Risk: Deleting or editing entries can affect records used for billing. <br>
Mitigation: Back up the local SQLite database before destructive changes or before relying on it for invoicing. <br>


## Reference(s): <br>
- [Nex Timetrack ClawHub release](https://clawhub.ai/nexaiguy/nex-timetrack) <br>
- [Nex AI website](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and local CSV or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores time tracking data locally in SQLite and can export billing records to CSV or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
