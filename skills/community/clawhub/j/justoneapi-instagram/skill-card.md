## Description:

Analyze Instagram workflows with JustOneAPI, including user profile, post details, user published posts, hashtag post search, and reels search across five API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Instagram profile, post, hashtag, and reels data through JustOneAPI when they have a valid token and concrete identifiers such as usernames, post shortcodes, hashtags, or pagination cursors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a JustOneAPI token that may be exposed through command history, logs, screenshots, or shared systems.

Mitigation: Use a narrowly scoped, revocable token and avoid pasting the token into chat, screenshots, or logged commands.

Risk: Instagram identifiers and returned profile, post, caption, media, and engagement data may be sensitive or subject to privacy and authorization obligations.

Mitigation: Query only authorized data and handle returned results according to applicable privacy, retention, and access-control requirements.

Risk: The server security verdict flags the release for review before installation.

Mitigation: Review the skill and its requested token handling before deployment, especially on shared or heavily logged systems.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and operation-specific Instagram identifiers such as username, code, hashtag, keyword, paginationToken, or endCursor.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
