## Description: <br>
Guides agents that have Linkup search or fetch access on query construction, search depth, output type selection, single-page fetching, and multi-step web retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shauryajain21](https://clawhub.ai/user/shauryajain21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill when performing web search, content extraction, company research, news retrieval, data enrichment, or real-time information gathering with Linkup tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad scraping guidance and includes LinkedIn comment and commenter-profile extraction examples without privacy guardrails. <br>
Mitigation: Constrain Linkup use to user-authorized, task-relevant sources; avoid bulk LinkedIn comment or profile collection unless there is a legitimate compliant need. <br>
Risk: Deep search can perform multi-step scraping and may retrieve more information than needed for simple lookups. <br>
Mitigation: Prefer narrower standard searches or single-page fetches when deep scraping is unnecessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shauryajain21/linkup-search) <br>
- [Linkup MCP server bundle](https://github.com/LinkupPlatform/linkup-mcp-server/releases/latest/download/linkup-mcp-server.mcpb) <br>
- [Linkup website](https://linkup.so) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may recommend Linkup search depth, output type, domain filters, date filters, and fetch settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
