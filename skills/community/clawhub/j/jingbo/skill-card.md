## Description: <br>
Provides Rain Classroom account and class query services, including user ID, teaching lists, class data, warning lists, today's teaching status, homework completion, and notice-read queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuetangop](https://clawhub.ai/user/xuetangop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and teaching support staff use this skill to connect an agent to Rain Classroom MCP tools for checking account identity, course lists, classroom statistics, student warnings, current-day teaching activity, homework completion, notice reading, and lesson reservations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a personal Rain Classroom secret that can authorize access to teaching account and class data. <br>
Mitigation: Install only after trusting the provider, configure clients to reference YUKETANG_SECRET instead of storing a raw bearer token, keep MCP config files out of commits, and rotate the secret if exposure is suspected. <br>
Risk: The shell installer silently sends an install-duration report. <br>
Mitigation: Review setup.sh before running it and use manual MCP configuration when silent reporting is not acceptable. <br>


## Reference(s): <br>
- [jingbo ClawHub Page](https://clawhub.ai/xuetangop/jingbo) <br>
- [Rain Classroom MCP API Reference](references/api_references.md) <br>
- [Rain Classroom Secret Setup](https://ykt-envning.rainclassroom.com/ai-workspace/open-claw-skill) <br>
- [Rain Classroom MCP Server](https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses should preserve returned wording, emoji, table headers, and course identifiers; the skill requires YUKETANG_SECRET for authenticated MCP access.] <br>

## Skill Version(s): <br>
1.0.327852 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
