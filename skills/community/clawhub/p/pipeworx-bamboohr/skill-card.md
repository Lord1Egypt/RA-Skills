## Description: <br>
Provides agent access to BambooHR employee directory, profile, time-off, and employee file metadata through a Pipeworx MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized people-operations developers and internal automation teams use this skill to connect an agent to BambooHR data for employee lookup, directory access, time-off review, and employee file metadata retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive BambooHR employee directory, profile, time-off, and file metadata to an agent through a third-party gateway. <br>
Mitigation: Use only with authorization to expose BambooHR HR data, and confirm tenant, credential scopes, and access controls before enabling it. <br>
Risk: The evidence does not provide enough detail about scoping, privacy handling, audit logging, retention, or read-only behavior. <br>
Mitigation: Confirm read-only behavior, audit logging, retention policy, and third-party data handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-bamboohr) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures a BambooHR MCP endpoint at https://gateway.pipeworx.io/bamboohr/mcp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
