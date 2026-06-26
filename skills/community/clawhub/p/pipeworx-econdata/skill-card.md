## Description: <br>
US economic indicators from the Bureau of Labor Statistics, including unemployment, CPI, and employment by industry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query public BLS economic series, unemployment, CPI, and employment data for dashboards, trend analysis, and economic research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses mcp-remote@latest, which can change behavior when the package updates. <br>
Mitigation: Pin mcp-remote to a reviewed trusted version before production deployment. <br>
Risk: Queries are routed through a third-party Pipeworx gateway. <br>
Mitigation: Use the skill for public economic data lookups and avoid sending confidential business context through the gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-econdata) <br>
- [Pipeworx econdata homepage](https://pipeworx.io/packs/econdata) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; MCP tool calls return structured economic data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct example calls and uses the Pipeworx remote MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
