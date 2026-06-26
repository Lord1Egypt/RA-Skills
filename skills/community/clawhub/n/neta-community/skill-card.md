## Description: <br>
Neta API community skill for browsing interactive feeds, viewing collection details, interacting with content, and browsing content by tags and characters in a community context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiuhan](https://clawhub.ai/user/huxiuhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Neta community feeds, inspect works, query tags and characters, and perform community interactions such as likes, favorites, comments, follows, and unfollows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an account token to perform account-changing actions such as liking, favoriting, commenting, following, or unfollowing. <br>
Mitigation: Use read-only browsing by default and require explicit confirmation before any account-changing action. <br>
Risk: Feed responses, profile data, or debug logs may contain community or account information. <br>
Mitigation: Avoid saving responses or logs unless they can be protected and deleted. <br>


## Reference(s): <br>
- [Neta Community on ClawHub](https://clawhub.ai/huxiuhan/neta-community) <br>
- [huxiuhan publisher profile](https://clawhub.ai/user/huxiuhan) <br>
- [Best Practices for Interactive Feed](references/interactive-feed.md) <br>
- [Social Interaction Skills](references/social-interactive.md) <br>
- [Best Practices for Hashtag Research](references/hashtag-research.md) <br>
- [Best Practices for Character Search (Community)](references/character-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and API workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NETA_TOKEN and the Neta CLI for authenticated account actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
