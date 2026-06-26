## Description: <br>
Maxhub Zhihu helps agents query and analyze public Zhihu user, content, search, hot-list, comment, article, and AI-search data through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, content researchers, marketing teams, and public-opinion analysts use this skill to retrieve and summarize Zhihu public content, user profiles, search results, comments, hot lists, and AI-search results. Agents use the bundled recipes and endpoint references to choose read-only MaxHub API calls and return sourced analysis or command guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zhihu keywords, user identifiers, URLs, and API credentials are transmitted to the MaxHub API service. <br>
Mitigation: Use the skill only when that third-party data transfer is acceptable, minimize submitted identifiers and keywords, and avoid unnecessary sensitive inputs. <br>
Risk: API keys, cookies, or session tokens could be exposed through prompts, logs, or shared outputs. <br>
Mitigation: Store MAXHUB_API_KEY in environment or agent configuration, do not print secrets, rotate keys periodically, and avoid primary account cookies or session tokens. <br>
Risk: Returned Zhihu comments, profiles, and social-graph data may include personal or sensitive user-generated content. <br>
Mitigation: Use the skill for authorized public-data analysis, minimize retained personal data, and review outputs before storing, sharing, or publishing them. <br>
Risk: Ambiguous prompts can trigger unintended user-profile or social-graph lookups. <br>
Mitigation: Clarify ambiguous requests before lookup and follow the recipe and endpoint whitelist references when selecting calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-zhihu) <br>
- [Publisher profile](https://clawhub.ai/user/xiewxx) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter mappings](references/param-mappings.md) <br>
- [Recipe index](references/recipes/_index.md) <br>
- [User endpoints reference](references/user.md) <br>
- [Search endpoints reference](references/search.md) <br>
- [Content endpoints reference](references/post.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise explanations, curl command examples, configuration snippets, and API-derived summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; requests send keywords, user-supplied identifiers, URLs, and optional cookies or tokens to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server evidence release, SKILL.md frontmatter, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
