## Description:

Searches and analyzes public Douyin data for keyword results, creator posts, comments, and real-time hot lists; it is not for publishing, editing, downloading videos, or non-Douyin platforms.

This skill is for research and development only.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect and analyze public Douyin search results, creator posts, comments, and trending topics for content research, competitor monitoring, sentiment review, and hot-list tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords, Douyin URLs, IDs, and GUAIKEI_API_TOKEN are sent to Guaikei, and the token is treated as sensitive because this version places it in URLs.

Mitigation: Use the skill only for explicit Douyin research, provide the token through the environment, use a dedicated token, and rotate it if exposure is suspected.

Risk: The skill can write JSON result files under its logs directory.

Mitigation: Treat generated logs as potentially sensitive research data and delete them when they are no longer needed.

Risk: Invalid-token paths can display contact or marketing text despite the skill documentation saying they should not.

Mitigation: Review stderr before exposing output to end users and avoid forwarding unsolicited contact or marketing text.

Risk: Broad activation may run the skill for loosely related short-video research requests.

Mitigation: Invoke it only when the user explicitly needs Douyin public-data search, posts, comments, or hot-list analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-search-and-analyze)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Usage documentation](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Command JSON schemas](assets/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON results on stdout, logs on stderr, and optional local JSON result files under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; command outputs cover search, creator posts, comments, and hot-list results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
