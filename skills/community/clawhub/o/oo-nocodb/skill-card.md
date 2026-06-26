## Description: <br>
Operates NocoDB through OOMOL's oo CLI connector for reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect NocoDB action schemas and run read, write, and destructive table or record operations through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access connected NocoDB data through sensitive credentials managed by the OOMOL connector. <br>
Mitigation: Install only if you trust OOMOL's oo CLI and connector to access the NocoDB account. <br>
Risk: Write and destructive actions can create, update, upsert, or permanently delete NocoDB data. <br>
Mitigation: Before approving writes or deletes, verify the exact base, table, record IDs, payload, and intended effect. <br>
Risk: Incorrect payloads or targets could affect the wrong NocoDB records or metadata. <br>
Mitigation: Inspect the live action contract before building payloads and confirm state-changing commands with the user. <br>


## Reference(s): <br>
- [ClawHub NocoDB skill page](https://clawhub.ai/oomol/oo-nocodb) <br>
- [NocoDB homepage](https://nocodb.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and meta.executionId values.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
