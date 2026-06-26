## Description: <br>
Maxhub Weibo helps agents query public Weibo posts, comments, reposts, user profiles, follower and following data, search results, hot topics, and rankings through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agents use this skill for Weibo social-data lookup, public-opinion monitoring, topic tracking, creator profiling, content propagation analysis, and competitive research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the MaxHub API key plus user-supplied Weibo IDs, links, keywords, and optional cookies or tokens to MaxHub. <br>
Mitigation: Install only when that transfer is acceptable, keep credentials out of prompts and logs, and avoid providing cookies or session credentials unless explicitly required and authorized. <br>
Risk: Aggregating follower lists, likes, comments, collections, and other public social data can still create privacy or legal-compliance concerns. <br>
Mitigation: Use the skill only for authorized data processing, minimize personal data, and review outputs before storage, sharing, or publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiewxx/maxhub-weibo) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [Post endpoints](references/post.md) <br>
- [User endpoints](references/user.md) <br>
- [Search endpoints](references/search.md) <br>
- [Comment endpoints](references/comments.md) <br>
- [Recipe index](references/recipes/_index.md) <br>
- [Parameter and field mappings](references/param-mappings.md) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API-derived summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify MaxHub as the data source, avoid exposing secrets, and explicitly note missing fields when upstream responses omit requested data.] <br>

## Skill Version(s): <br>
3.8.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
