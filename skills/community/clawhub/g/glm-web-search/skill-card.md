## Description: <br>
Enables an agent to configure and call the GLM web-search MCP server for online search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to set up GLM web search through mcporter, configure a BigModel API key, and run webSearchPrime queries for current web information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a GLM/BigModel API key in local OpenClaw configuration. <br>
Mitigation: Use a limited-use key, restrict local config file permissions, and rotate or delete the key when it is no longer needed. <br>
Risk: Search terms are sent to the external GLM web-search service. <br>
Mitigation: Avoid submitting highly sensitive personal, confidential, or proprietary text as search queries. <br>


## Reference(s): <br>
- [GLM Search MCP Server Documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server) <br>
- [BigModel GLM Coding](https://www.bigmodel.cn/glm-coding?ic=OOKF4KGGTW) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, mcporter commands, and search-query examples; search results are returned by the GLM MCP service.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
