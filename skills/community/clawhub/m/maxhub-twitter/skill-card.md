## Description: <br>
Maxhub Twitter helps agents query public Twitter/X social data through the MaxHub API for tweet details, comments, user profiles, followers, search timelines, trends, and related analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to research public Twitter/X activity, inspect user profiles and social graphs, follow trends, and assemble read-only social-data reports. It is suited for public-opinion monitoring, account profiling, topic propagation analysis, competitor research, and content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twitter/X handles, tweet IDs, links, search terms, and returned public social data are sent to MaxHub at https://www.aconfig.cn. <br>
Mitigation: Use the skill only for authorized data processing, minimize retained personal or social-graph data, and avoid unnecessary republication. <br>
Risk: The skill requires a MaxHub API key and may accept optional cookies or tokens. <br>
Mitigation: Use a dedicated API key, rotate it as needed, and do not provide production cookies or session tokens. <br>
Risk: Broad chained lookups can collect more public social data than the user intended. <br>
Mitigation: Confirm ambiguous requests before running broad chained lookups and keep outputs scoped to the requested task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-twitter) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [Content API Reference](references/content.md) <br>
- [User API Reference](references/user.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown text with curl command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MaxHub API requests; requires MAXHUB_API_KEY and transmits user-supplied IDs, keywords, URLs, and optional cookies or tokens to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
