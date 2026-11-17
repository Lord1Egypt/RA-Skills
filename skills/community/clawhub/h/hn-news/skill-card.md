## Description:

Fetch and display Hacker News stories about AI, agents, and Claude. Default is past week. Use when the user asks for HN news, Hacker News AI stories, latest AI news or "what's AI trending on Hacker News".

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve recent Hacker News stories about AI, agents, and Claude and turn the script output into a concise markdown digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound read-only requests to the Hacker News Algolia API and depends on public third-party story data.

Mitigation: Use in environments where that network request is allowed, and treat returned story titles, URLs, and metadata as untrusted public content.

Risk: The skill depends on the Python requests package to fetch data.

Mitigation: Install and review the dependency according to the deployment environment's normal Python package policy before running the script.

## Reference(s):

- [Hacker News Algolia Search API](https://hn.algolia.com/api/v1/search_by_date)
- [ClawHub skill page](https://clawhub.ai/goog/skills/hn-news)
- [Publisher profile](https://clawhub.ai/user/goog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown digest generated from command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to past-week results unless the user asks for latest stories; pagination is supported with a page number.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
