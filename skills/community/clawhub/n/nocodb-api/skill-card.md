## Description: <br>
Connects agents to NocoDB databases through REST API v3 for querying records, managing tables and views, handling linked records, filtering, sorting, and uploading attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dofbi](https://clawhub.ai/user/dofbi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with NocoDB Cloud or self-hosted NocoDB instances, including record CRUD, schema management, attachments, collaboration resources, and API tokens where permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A NocoDB API token may authorize broad database, schema, collaboration, token, script, or file-upload actions. <br>
Mitigation: Use a dedicated least-privilege token and avoid broad production or admin tokens unless the workflow requires them. <br>
Risk: Destructive, bulk, schema, member, team, script, token, and upload operations can materially change data or access. <br>
Mitigation: Require explicit approval before deletes, bulk updates, schema changes, member or team changes, script actions, token actions, or file uploads. <br>
Risk: An incorrect NOCODB_URL could send authenticated requests to the wrong NocoDB endpoint. <br>
Mitigation: Verify NOCODB_URL before use and do not print, log, or share NOCODB_TOKEN. <br>


## Reference(s): <br>
- [ClawHub NocoDB API release](https://clawhub.ai/dofbi/nocodb-api) <br>
- [NocoDB documentation](https://docs.nocodb.com/) <br>
- [NocoDB REST API documentation](https://docs.nocodb.com/developer-resources/rest-APIs/) <br>
- [NocoDB project](https://github.com/nocodb/nocodb) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with shell command examples; command results are JSON or tab-separated text depending on the operation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOCODB_TOKEN, NOCODB_URL, curl, and jq; some workspace, view, script, team, collaboration, and token operations require NocoDB Enterprise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
