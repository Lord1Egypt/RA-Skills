## Description:

Analyze Social Media workflows with JustOneAPI, including cross-Platform Search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run API-backed cross-platform social media searches across sources such as Weibo, WeChat, Zhihu, Douyin, Xiaohongshu, Bilibili, Kuaishou, and news. It is useful for trend research and monitoring with explicit keyword, platform, time-window, and pagination parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends social-media search terms and a JustOneAPI token to api.justoneapi.com.

Mitigation: Use a low-privilege, revocable token and avoid sensitive searches.

Risk: The API token can be exposed through command lines, command logs, or retained full request URLs.

Mitigation: Avoid sharing logs, limit token scope, and rotate the token if command output or URLs may have been retained.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-search)
- [Publisher profile](https://clawhub.ai/user/justoneapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; selected requests return API JSON from JustOneAPI.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
