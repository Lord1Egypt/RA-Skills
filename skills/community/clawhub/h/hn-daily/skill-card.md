## Description:

Fetch and filter Hacker News top stories. Use when user asks for tech news, HN updates, daily news digest, or wants to set up automated HN fetching. Supports keyword filtering (AI, programming, startups) and caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osgood001](https://clawhub.ai/user/osgood001)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch Hacker News top stories, filter for technology-related topics, and produce a daily digest or JSON story list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill contacts the public Hacker News API.

Mitigation: Use it only where outbound access to hacker-news.firebaseio.com is acceptable, and configure HTTP_PROXY or HTTPS_PROXY when network routing must be controlled.

Risk: The script may write a local cache file under ~/.cache/hn-daily.

Mitigation: Review local caching requirements before use and run with --no-cache when fresh output or cache avoidance is needed.

Risk: Default human-readable output may include Chinese text.

Mitigation: Use --format json or adjust the script output strings when downstream consumers require a specific language.

## Reference(s):

- [Hacker News API Reference](references/hn_api.md)
- [Official Hacker News API](https://github.com/HackerNews/API)
- [ClawHub Skill Page](https://clawhub.ai/osgood001/skills/hn-daily)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-like text digest or JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache fetched story data locally for 4 hours under ~/.cache/hn-daily.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
