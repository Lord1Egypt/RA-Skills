## Description: <br>
Sync local .md data files to Google Sheets with content-hash deduplication for expenses, investments, and other key-value data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users maintaining local Markdown ledgers use this skill to configure append-only Google Sheets synchronization with service-account authentication and deduplication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured sync may append private expense or investment data to the wrong Google Sheet. <br>
Mitigation: Confirm the spreadsheet ID is the intended destination before scheduling or running the sync. <br>
Risk: The service-account credential may grant broader Google Sheets access than needed. <br>
Mitigation: Use a credential owned by the user and limit it to the minimum permissions required for the target spreadsheet. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python regex examples, API notes, and sync configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Append-only synchronization guidance; users must supply their own Google service-account credential and spreadsheet destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
