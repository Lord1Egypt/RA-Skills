## Description: <br>
使用 Calculator Server MCP 进行加减法运算。当用户需要进行加法或减法计算时使用此 skill。Server 地址：http://192.168.71.7:8000/mcp，支持 add（加法）和 subtract（减法）两个工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dqatsh](https://clawhub.ai/user/dqatsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a Calculator Server MCP for simple addition and subtraction tasks. It is useful when an agent needs documented setup guidance, authentication requirements, and example calls for the add and subtract tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a bearer token to a private HTTP MCP endpoint. <br>
Mitigation: Use it only on a trusted protected network, scope the token to this calculator service, and prefer HTTPS or another protected transport before using real credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dqatsh/my-test-skill-4-xn) <br>
- [Publisher profile](https://clawhub.ai/user/dqatsh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the XINIUDATA_MCP_TOKEN environment variable to authenticate with the MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
