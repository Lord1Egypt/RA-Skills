## Description: <br>
Use the Moltsheet CLI to manage spreadsheet-style data for AI workflows, including sheet creation, schema inspection, row imports, cell updates, sharing, and read-only SQL queries over accessible sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youssefbm2008](https://clawhub.ai/user/youssefbm2008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to operate Moltsheet spreadsheets through the CLI for data access, filtered reads, selected columns, joins, aggregates, imports, mutations, and sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to mutate or delete spreadsheet data, allow destructive schema updates, and share sheets with collaborators. <br>
Mitigation: Require approval for write, delete, data-loss schema, and sharing actions; read the target sheet or schema first and verify writes afterward. <br>
Risk: Moltsheet requires sensitive credentials and may store or share spreadsheet data through the Moltsheet service. <br>
Mitigation: Use credential storage or environment variables carefully, avoid exposing API keys, and do not use confidential spreadsheets unless that storage and sharing posture is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youssefbm2008/moltsheet) <br>
- [Moltsheet service](https://www.moltsheet.com) <br>
- [Moltsheet API v1](https://www.moltsheet.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers --json CLI output and stdin or files for structured payloads.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
