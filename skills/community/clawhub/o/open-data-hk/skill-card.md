## Description: <br>
Provides access to Hong Kong DATA.GOV.HK catalog data through tools for listing datasets, viewing dataset and category details, searching metadata, faceted exploration, and file-format filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data users use this skill to query Hong Kong open-data catalog metadata and retrieve dataset or category search results. It requires a XiaoBenYang API key and sends requests through that third-party service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dataset queries and the required API key are routed through a third-party XiaoBenYang service rather than a direct DATA.GOV.HK integration. <br>
Mitigation: Install only if comfortable trusting XiaoBenYang with the API key and queries; prefer direct DATA.GOV.HK access when official-source provenance is required. <br>
Risk: The skill stores the provided API key locally in a .env file. <br>
Mitigation: Use a dedicated key, avoid shared or synced directories, and treat the .env file as a local secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/open-data-hk) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries of JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a XiaoBenYang API key stored in .env or XBY_APIKEY; supports English, traditional Chinese, and simplified Chinese language options where tools expose them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
