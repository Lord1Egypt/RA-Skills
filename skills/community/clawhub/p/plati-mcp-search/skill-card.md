## Description: <br>
Finds low-price subscription offers from Plati through a local MCP server and returns filtered, reliable options with listing links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rybnikov](https://clawhub.ai/user/rybnikov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Plati marketplace listings for subscription offers, compare price, seller reliability, duration, and account type, and return a concise ranked list with links and filters used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external `plati-mcp-server` npm package and a local MCP server. <br>
Mitigation: Install only if the package and server source are trusted, and pin or review the package version where possible. <br>
Risk: Marketplace searches can expose private account details if users include them in queries. <br>
Mitigation: Do not include private account details or sensitive credentials in marketplace search terms. <br>
Risk: Subscription marketplace listings may have seller-specific terms or purchase conditions. <br>
Mitigation: Review seller terms and listing details before buying any subscription offer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rybnikov/plati-mcp-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls, configuration] <br>
**Output Format:** [Plain-text numbered list with listing links and a short summary line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Avoids markdown tables and code blocks in final user messages; states filters used by the agent.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
