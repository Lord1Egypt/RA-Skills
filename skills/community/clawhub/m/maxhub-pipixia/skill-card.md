## Description: <br>
Maxhub Pipixia helps agents query and analyze Pipixia post, user, search, trend, hashtag, feed, and comment data through the MaxHub API, with one restricted view-count write capability requiring explicit user authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, content analysts, creators, and operations teams use this skill to retrieve Pipixia content and user data, track hot topics, inspect engagement, and assemble lightweight content research workflows. The restricted view-count endpoint should be used only after explicit confirmation and acceptance of platform terms-of-service risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Pipixia IDs, keywords, URLs, returned social data, and credentials to the third-party MaxHub API. <br>
Mitigation: Use a dedicated MaxHub API key, minimize personal data, and avoid exposing secrets in prompts, logs, or shared outputs. <br>
Risk: The restricted fetch_increase_post_view_count capability can increase a post's view count and may create platform terms-of-service risk. <br>
Mitigation: Do not enable or call the endpoint unless the user explicitly confirms the action, parameters, and acceptance of platform risk. <br>
Risk: Broad routing triggers and chained lookups can select multiple endpoints for related Pipixia analysis tasks. <br>
Mitigation: Use the documented recipe index, parameter mappings, and endpoint whitelist before calls; ask the user when intent or endpoint selection is ambiguous. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiewxx/maxhub-pipixia) <br>
- [Publisher profile](https://clawhub.ai/user/xiewxx) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter mappings](references/param-mappings.md) <br>
- [Recipe index](references/recipes/_index.md) <br>
- [Post API reference](references/post.md) <br>
- [User API reference](references/user.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API result summaries, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; sends user-supplied IDs, keywords, URLs, optional cookies or tokens, and API credentials to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
