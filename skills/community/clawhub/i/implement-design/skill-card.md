## Description: <br>
Translates Figma designs into production-ready code with 1:1 visual fidelity using a connected Figma MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[springer63](https://clawhub.ai/user/springer63) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design engineers use this skill to implement UI from Figma URLs, fetch design context, screenshots, and assets through the Figma MCP server, and translate the result into project conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can access Figma design content through a connected MCP server. <br>
Mitigation: Use it only with Figma links or files the user is authorized to access. <br>
Risk: Generated UI code may differ from the source design or introduce implementation defects. <br>
Mitigation: Review generated changes and validate layout, typography, colors, assets, responsiveness, and accessibility against the Figma screenshot before deployment. <br>


## Reference(s): <br>
- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/) <br>
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/) <br>
- [Figma Variables and Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, command, and configuration changes as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Figma MCP server connection and a user-provided Figma URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
