## Description: <br>
GLM Search Pro lets an agent run Zhipu GLM web searches through a preferred REST/cURL backend or an optional MCP backend with engine, recency, domain, result count, and detail-level controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bithostgits](https://clawhub.ai/user/bithostgits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web information, news, and online resources through Zhipu GLM search. It is useful when web access is needed from China without a VPN and when searches need configurable engines, recency, domain filtering, or response detail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Zhipu/GLM. <br>
Mitigation: Install and use the skill only when sending search queries to Zhipu/GLM is acceptable for the intended data and workflow. <br>
Risk: MCP mode can persist the Zhipu API key in a local mcporter configuration URL. <br>
Mitigation: Prefer cURL mode with ZHIPU_API_KEY in the runtime environment; use MCP setup only when local key persistence is acceptable and rotate the key if the config file may have been exposed. <br>


## Reference(s): <br>
- [GLM Search Pro API Notes](references/api-notes.md) <br>
- [Zhipu Web Search Documentation](https://docs.bigmodel.cn/cn/guide/tools/web-search) <br>
- [Zhipu MCP Search Server Documentation](https://docs.bigmodel.cn/cn/coding-plan/mcp/search-mcp-server) <br>
- [GLM Search Pro on ClawHub](https://clawhub.ai/bithostgits/glm-search-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search responses with command-line status and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; cURL mode sends the key in an Authorization header, while optional MCP mode stores the key in a local mcporter configuration URL.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
