## Description: <br>
Access and manage NocoDB databases via REST APIs, including bases, tables, fields, records, links, filters, sorts, attachments, and Enterprise workspace, view, script, team, and collaboration APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarkPhoenix2704](https://clawhub.ai/user/DarkPhoenix2704) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent configure, query, and administer NocoDB resources through a Bash CLI backed by the NocoDB REST API. It is suited for record management, schema updates, collaboration setup, and API-token workflows when the supplied token has the required plan and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The supplied NOCODB_TOKEN can grant broad authority over NocoDB data and administration. <br>
Mitigation: Use a least-privilege token and test against non-production bases before allowing access to production data. <br>
Risk: Delete, bulk update, membership, script, token, and file-upload commands can cause destructive or sensitive changes. <br>
Mitigation: Require explicit human confirmation and payload review before executing those commands. <br>
Risk: Attachment uploads can expose local files selected by the agent. <br>
Mitigation: Confirm file paths and intended records before upload commands are run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DarkPhoenix2704/nocodb-official) <br>
- [Artifact README](artifact/README.md) <br>
- [Agent Skills Open Standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require curl, jq, NOCODB_TOKEN, and optionally NOCODB_URL and NOCODB_VERBOSE.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
