## Description: <br>
Searches U.S. colleges by name and retrieves College Scorecard details such as tuition and admission rates through a Pipeworx-hosted MCP gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, advisors, researchers, and developers can use this skill to search U.S. colleges and retrieve public College Scorecard details while working in an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: College lookup queries are sent to a third-party Pipeworx-hosted MCP gateway. <br>
Mitigation: Use ordinary college search terms and avoid including unrelated personal or sensitive information in queries unless sharing it with that service is acceptable. <br>
Risk: Lookup results depend on the remote MCP gateway and the underlying College Scorecard data source. <br>
Mitigation: Confirm important tuition, admissions, or institutional details against authoritative college or Department of Education sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/b-gutman/pipeworx-college-scorecard) <br>
- [College Scorecard MCP gateway](https://gateway.pipeworx.io/college-scorecard/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text and JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to a Pipeworx-hosted MCP gateway; results depend on College Scorecard data and gateway availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
