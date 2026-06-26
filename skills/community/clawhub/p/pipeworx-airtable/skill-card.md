## Description: <br>
Integrate with the Airtable API to list bases, fetch and filter records, get record details, create records, and retrieve base schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure access to a Pipeworx-hosted Airtable MCP server for reading Airtable bases, records, schemas, and creating new records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Airtable read and write access through an external Pipeworx gateway that may handle record contents, schemas, workspace metadata, and record creation requests. <br>
Mitigation: Review who operates the gateway and its data handling before installing; use dedicated least-privilege Airtable credentials limited to the intended bases. <br>
Risk: The skill can create Airtable records and retrieve broad base and schema data. <br>
Mitigation: Test with non-sensitive bases first, restrict connected account permissions, and avoid sensitive production workspaces unless the gateway has been approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-airtable) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippet and tool descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote Pipeworx Airtable MCP gateway; responses depend on connected Airtable account permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
