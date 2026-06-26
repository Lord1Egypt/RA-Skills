## Description: <br>
Maxhub Bilibili lets agents query and analyze public Bilibili data through the MaxHub API, including videos, creators, search, comments, live rooms, subtitles, and collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, content analysts, and research teams use this skill to collect Bilibili public data, analyze videos and creators, inspect comments and live data, and build content research workflows through MaxHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, API keys, user-supplied identifiers, keywords, URLs, and optional cookies are sent to MaxHub as a third-party processor. <br>
Mitigation: Install only if this data flow is acceptable, minimize personal data, keep secrets out of logs and prompts, and use only authorized data processing workflows. <br>
Risk: VIP playback or cookie-assisted requests may expose account session credentials or higher-risk Bilibili access. <br>
Mitigation: Use a separate low-risk Bilibili cookie when needed, never provide a primary account session cookie, and require explicit confirmation before cookie-based or high-resolution member-only playback requests. <br>
Risk: Ambiguous requests can match multiple recipes or endpoints and lead to unintended lookups. <br>
Mitigation: Ask for clarification when recipe matching is ambiguous and use the documented recipe index, parameter mappings, and endpoint whitelist before making API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-bilibili) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [Agent decision tree](SKILL.md) <br>
- [Recipe index](references/recipes/_index.md) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; requests are sent to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: evidence release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
