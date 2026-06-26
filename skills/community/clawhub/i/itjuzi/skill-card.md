## Description: <br>
Generates investor-focused sector funding briefings, project observations, and active investor analysis using ITjuzi MCP financing and investor data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyentq-alt](https://clawhub.ai/user/skyentq-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, investors, and research teams use this skill to query ITjuzi MCP data and produce structured financing briefs for sectors, regions, funding rounds, and active investors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided ITjuzi API key for MCP queries. <br>
Mitigation: Use a scoped or revocable API key and store it in the MCP or client credential store rather than shared chats. <br>
Risk: Briefing conclusions can be misleading if MCP results are sparse, funding amounts are missing, or the query window is too narrow. <br>
Mitigation: Keep source fields in the briefing, label missing or undisclosed amounts, and note when the sample size is small. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skyentq-alt/itjuzi) <br>
- [ITjuzi MCP Endpoint](https://mcp.itjuzi.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Structured Markdown briefing with tables and concise bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided ITjuzi API keys and MCP query results; does not create chart files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
