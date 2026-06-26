## Description: <br>
Math.js MCP wraps the mathjs.org API for free, unauthenticated expression evaluation and unit conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add math expression evaluation and unit conversion through Pipeworx's Math.js MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Math expressions and unit-conversion inputs are sent to Pipeworx through the mcp-remote npm bridge. <br>
Mitigation: Avoid secrets, personal data, and sensitive business calculations; use only inputs appropriate for a third-party remote service. <br>
Risk: Using mcp-remote@latest can change bridge behavior over time. <br>
Mitigation: Pin the bridge version when reproducibility matters. <br>


## Reference(s): <br>
- [Pipeworx mathjs pack](https://pipeworx.io/packs/mathjs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and text results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Pipeworx remote MCP endpoint and the mcp-remote npm bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
