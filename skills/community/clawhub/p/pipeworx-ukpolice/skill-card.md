## Description: <br>
UK street-level crime data - reported crimes by location, police force directory, and case outcomes from data.police.uk <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, journalists, researchers, and developers use this skill to query UK street-level crime reports, police force directories, and case outcomes for location-based analysis or public-interest reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a remote MCP endpoint and curl/npx execution configured by the user. <br>
Mitigation: Install and run it only when the ClawHub skill page, artifact file, and Pipeworx endpoint match the expected UK Police Data capability. <br>
Risk: Crime and outcome data may influence neighborhood, travel, property, journalism, or research decisions. <br>
Mitigation: Treat outputs as public-data retrieval results and verify important conclusions against the underlying data source and reporting context before acting on them. <br>


## Reference(s): <br>
- [Pipeworx UK Police pack](https://pipeworx.io/packs/ukpolice) <br>
- [Pipeworx UK Police MCP endpoint](https://gateway.pipeworx.io/ukpolice/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-ukpolice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns crime category, location, outcome status, and unique ID from the remote MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
