## Description: <br>
Look up real-estate listings, property details, price and tax history, market reports, saved homes, and photo galleries on homes.com via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and real-estate researchers use this skill to query homes.com listings, property records, saved homes, price and tax history, market reports, and photo galleries through an MCP server. It is intended for read-only real-estate lookup and comparison workflows, with saved-home and saved-search access requiring an authenticated homes.com browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP and fetchproxy extension can read homes.com pages through the user's active browser session, including saved homes or saved searches when requested. <br>
Mitigation: Install only when comfortable with that browser-session access, and avoid requesting account-specific saved-home or saved-search data unless it is needed. <br>
Risk: The skill depends on a separately installed npm package and Chrome extension that are not bundled in the skill artifact. <br>
Mitigation: Review the external homes-mcp package and fetchproxy extension before enabling them. <br>
Risk: homes.com does not publish a public consumer API, so extraction can be affected by site changes, authentication state, or WAF challenges. <br>
Mitigation: Treat returned listings and history as website-derived data, verify important results against homes.com directly, and resolve browser-session challenges before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/homes-mcp) <br>
- [homes-mcp npm package](https://www.npmjs.com/package/homes-mcp) <br>
- [homes-mcp repository listed in artifact](https://github.com/chrischall/homes-mcp) <br>
- [fetchproxy extension repository](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with setup snippets and MCP tool results summarized in text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only homes.com data; saved homes and saved searches require an authenticated browser session.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
