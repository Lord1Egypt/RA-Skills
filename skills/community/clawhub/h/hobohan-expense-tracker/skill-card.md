## Description: <br>
Log daily expenses via check-in prompts; dedup, categorize, sync to local ledger and Google Sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to collect daily spending check-ins, maintain a local markdown expense ledger, categorize entries, avoid duplicate records, and sync expense rows to Google Sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records private spending details and notes in persistent local ledger files and a Google Sheet. <br>
Mitigation: Use it only with ledgers and sheets you control, review entries before sync, and avoid recording unnecessary sensitive notes. <br>
Risk: The sync behavior depends on a service-account credential path and a specific Google Sheet destination. <br>
Mitigation: Confirm the sheet ID and credential belong to the intended account, limit the service account's permissions, and disable sync for local-only tracking. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown ledger entries and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local ledger files and Google Sheets sync guidance for expense tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
