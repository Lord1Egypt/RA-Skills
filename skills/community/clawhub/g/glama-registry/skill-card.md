## Description: <br>
Glama Registry searches the Glama MCP registry for MCP servers that match a query string. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search for MCP servers by keyword and review the returned registry results. The skill requires a user-provided XiaoBenYang API key before it can call the upstream search endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves a XiaoBenYang API key in a local .env file. <br>
Mitigation: Keep .env out of source control, restrict local file access, and rotate the key if it is exposed. <br>
Risk: Dependency versions are lower-bounded but not pinned. <br>
Mitigation: Pin and review dependencies for controlled or reproducible deployments. <br>
Risk: Search results come from an upstream API and may be incomplete, unavailable, or stale. <br>
Mitigation: Review returned MCP server details before using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/glama-registry) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown summary of JSON-derived MCP registry search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XBY_APIKEY and returns success, raw results, and status message fields from the upstream API wrapper.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
