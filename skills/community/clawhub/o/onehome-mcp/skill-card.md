## Description: <br>
Search OneHome (CoreLogic) portal listings, get property details, photos, schools, saved searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real-estate buyers use this skill through an agent to search private OneHome portal listings shared by their agent, inspect property details, photos, schools, saved searches, and compare listings. It also supports local mortgage and affordability calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires private OneHome portal authentication and can access portal data shared by a real-estate agent. <br>
Mitigation: Install only when that access is expected, provide credentials through environment variables or a secret manager, and avoid pasting magic links or bearer tokens into chats or logs. <br>
Risk: Raw GraphQL requests can ask for fields beyond the structured listing tools. <br>
Mitigation: Use the raw GraphQL escape hatch only for fields needed for the user's real-estate task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/onehome-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool names, environment variable names, and JSON-like tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authentication setup guidance for OneHome tokens or magic links and notes when local calculator tools do not require network access.] <br>

## Skill Version(s): <br>
0.12.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
