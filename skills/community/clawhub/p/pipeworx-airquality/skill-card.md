## Description: <br>
Air Quality MCP - wraps air-quality-api.open-meteo.com for free, unauthenticated air quality data access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query air quality data through the Pipeworx MCP gateway and configure MCP clients for the airquality endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill shows commands that contact an external Pipeworx MCP gateway. <br>
Mitigation: Review endpoint URLs and request arguments before execution, and avoid sending sensitive or regulated data. <br>
Risk: Anonymous use is rate limited. <br>
Mitigation: Expect rate-limit failures during repeated calls and use the documented Pipeworx sign-up path when higher limits are needed. <br>


## Reference(s): <br>
- [Pipeworx Airquality Homepage](https://pipeworx.io/packs/airquality) <br>
- [Pipeworx Homepage](https://pipeworx.io) <br>
- [Pipeworx Airquality MCP Gateway](https://gateway.pipeworx.io/airquality/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-airquality) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls return JSON-RPC 2.0 responses; anonymous usage is rate limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
