## Description: <br>
Search and browse Hacker News with API access to stories, comments, users, and hiring threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to retrieve and search public Hacker News stories, comments, user profiles, and hiring threads through the Firebase and Algolia APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make outbound requests to public Hacker News and Algolia endpoints, which can expose query terms to those services. <br>
Mitigation: Review queries before execution and avoid submitting private or sensitive information. <br>
Risk: Hacker News results can include deleted, dead, paginated, or null-url items. <br>
Mitigation: Check item status, handle text-only posts, and paginate deliberately before presenting results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/hacker-news) <br>
- [HN API Reference](api.md) <br>
- [HN Search Patterns](search.md) <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0) <br>
- [Hacker News Algolia API](https://hn.algolia.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline API endpoints, curl examples, and JSON field references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public API request patterns, pagination notes, and response-field guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
