## Description:

Search and browse Hacker News with API access to stories, comments, users, and hiring threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to search Hacker News, retrieve story and comment data, inspect users, and navigate hiring threads through public Hacker News and Algolia endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to public Hacker News and Algolia endpoints.

Mitigation: Avoid using private, confidential, or sensitive information in Hacker News search queries.

Risk: Results depend on public API availability, pagination, rate limits, and the freshness of indexed Hacker News data.

Mitigation: Paginate large result sets, handle unavailable or missing items, and verify important results against the returned story or comment data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/hacker-news)
- [HN API Reference](artifact/api.md)
- [HN Search Patterns](artifact/search.md)
- [Official Hacker News Firebase API](https://hacker-news.firebaseio.com/v0)
- [Algolia Hacker News Search API](https://hn.algolia.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with inline API endpoints, curl examples, and summarized Hacker News results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on public Hacker News and Algolia API availability, pagination, and query terms supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
