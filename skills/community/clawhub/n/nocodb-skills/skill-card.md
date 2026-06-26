## Description: <br>
Access and manage NocoDB databases via v3 REST API. Use for managing workspaces, bases, tables, fields, views, records, and more. Supports filtering, sorting, pagination, linked records, attachments, and team management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkmchinese](https://clawhub.ai/user/jkmchinese) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent administer NocoDB workspaces, bases, tables, fields, views, records, filters, sorts, attachments, scripts, teams, and API tokens through the NocoDB v3 REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad NocoDB administration powers, including database, team, script, file-upload, and API-token operations without built-in safety checks. <br>
Mitigation: Use a dedicated least-privilege token against a verified NOCODB_URL and require explicit human approval before delete, bulk update, team, script, token, or attachment-upload commands. <br>
Risk: Database changes may be destructive or difficult to reverse. <br>
Mitigation: Back up important data before using mutating commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON payload examples, and CLI command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOCODB_TOKEN and optionally NOCODB_URL and NOCODB_VERBOSE.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
