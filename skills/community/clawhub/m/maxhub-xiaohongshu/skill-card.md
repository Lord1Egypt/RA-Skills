## Description: <br>
Xiaohongshu (RED) public note and user data analysis skill that uses the MaxHub API to query note details, comments, user profiles, search, topics, products, recommendation feeds, and related public content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, content teams, ecommerce operators, and MCN teams use this skill to route Xiaohongshu research tasks through MaxHub for public note, comment, user, search, topic, product, and trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this skill as suspicious because it handles Xiaohongshu profile, favorites, group, and session-like data with broad routing and incomplete guardrails. <br>
Mitigation: Use it only for authorized Xiaohongshu data processing, require explicit Xiaohongshu or RED intent before calls, and review profile, favorites, commenters, and group lookups with extra care. <br>
Risk: The skill transmits API keys, user-supplied IDs, keywords, URLs, and optional cookies or tokens to MaxHub at https://www.aconfig.cn. <br>
Mitigation: Keep MAXHUB_API_KEY private, avoid providing Xiaohongshu cookies or session credentials, minimize personal data, and do not expose secrets in logs or prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-xiaohongshu) <br>
- [MaxHub website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Xiaohongshu Notes & Comments](references/note.md) <br>
- [Xiaohongshu User](references/user.md) <br>
- [Xiaohongshu Search & Discovery](references/search.md) <br>
- [Xiaohongshu Products & Topics](references/product.md) <br>
- [Param & Field Mapping Index](references/param-mappings.md) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Recipe Index](references/recipes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and summarized API response analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MAXHUB_API_KEY; requests are routed to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: release evidence, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
