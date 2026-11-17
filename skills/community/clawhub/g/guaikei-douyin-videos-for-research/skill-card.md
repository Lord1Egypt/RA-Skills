## Description:

Helps agents research public Douyin content by searching keywords, collecting creator posts, retrieving video comments, and checking real-time trending topics; it does not publish, edit, or download videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to gather public Douyin search results, creator posts, comments, and hot-list data for content research, competitor monitoring, sentiment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate on vague requests for short-video research.

Mitigation: Use it only for explicit Douyin research tasks and ask for clarification when the target platform or task is ambiguous.

Risk: Requests are sent to Guaikei with GUAIKEI_API_TOKEN, and the security summary notes token exposure risk in request URLs.

Mitigation: Set the token only through the environment, avoid sensitive investigation keywords, and rotate the token if request URLs may have been logged outside the user's control.

Risk: Generated JSON result files are stored locally in the skill's logs directory.

Mitigation: Review, protect, or delete generated log files after use, especially when searches or comments contain sensitive research topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-videos-for-research)
- [Guaikei website](https://www.guaikei.com)
- [Usage documentation](readme.md)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Command JSON Schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout, with JSON result files saved for search, post, and comment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and returns status, request metadata, runtime metadata, and Douyin public-content results.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
