## Description: <br>
Explore and analyze LinkedIn companies by retrieving company profiles, employee directories, posts, job listings, job counts, and job details through KeyAPI MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lycici](https://clawhub.ai/user/lycici) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, sales researchers, recruiting researchers, and developers use this skill to gather LinkedIn company intelligence and synthesize company overview, hiring, content, people, and job-market findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled runner is broader than the advertised LinkedIn-only purpose. <br>
Mitigation: Run commands explicitly with --platform linkedin and review each tool name and JSON parameter before execution. <br>
Risk: The skill uses a KEYAPI_TOKEN and can load or persist credentials locally. <br>
Mitigation: Use a dedicated token, provide it through the environment when possible, and remove any .env file when it is no longer needed. <br>
Risk: Collected company, people, post, and job data can be stored in the local cache. <br>
Mitigation: Review cached files before sharing the workspace and delete .keyapi-cache/ when the collected data is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lycici/keyapi-linkedin-company-analysis) <br>
- [KeyAPI](https://keyapi.ai/) <br>
- [KeyAPI LinkedIn MCP server](https://mcp.keyapi.ai/linkedin/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and KEYAPI_TOKEN; caches retrieved API results locally under .keyapi-cache/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
