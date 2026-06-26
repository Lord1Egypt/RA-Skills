## Description: <br>
Maxhub Threads lets an agent query public Threads posts, user profiles, comments, searches, timelines, and interaction data through the MaxHub API at https://www.aconfig.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media researchers, analysts, content teams, and developers use this skill to retrieve and summarize public Threads content, user profiles, comments, search results, and chained user or post activity for content research and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the MaxHub API key, Threads identifiers, search terms, URLs, and optional cookies or tokens to MaxHub at https://www.aconfig.cn. <br>
Mitigation: Use only authorized data, minimize personal data collection, avoid production account cookies or sessions, and keep secrets out of logs and prompts. <br>
Risk: Chained public Threads profile and activity lookups can support broad profiling or harassment if misused. <br>
Mitigation: Use explicit Threads-related prompts, avoid harassment or broad profiling, and limit collection to the task the user authorized. <br>
Risk: Results depend on third-party MaxHub API availability, authentication, permissions, and rate limits. <br>
Mitigation: Validate calls against the documented endpoint whitelist, stop on authentication or permission failures, and report unavailable or missing fields instead of fabricating data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-threads) <br>
- [Publisher profile](https://clawhub.ai/user/xiewxx) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Threads user reference](references/user.md) <br>
- [Threads content reference](references/content.md) <br>
- [Parameter and field mapping index](references/param-mappings.md) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Recipe index](references/recipes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown responses with curl command snippets and JSON-derived summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Threads data lookup through MaxHub; requires MAXHUB_API_KEY and transmits user-supplied identifiers, search terms, URLs, and optional cookies or tokens to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata, skill frontmatter, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
