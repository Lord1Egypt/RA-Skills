## Description:

Browse and search Hacker News, including top, new, best, Ask HN, Show HN, job posts, item details, comments, user profiles, Algolia search, and "Who is hiring?" threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to browse, search, and retrieve Hacker News stories, comments, user profiles, and hiring threads from public APIs without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script that makes unauthenticated network requests to Hacker News and Algolia.

Mitigation: Review the script before deployment and allow outbound requests only to the disclosed public APIs in restricted environments.

Risk: The script depends on curl, jq, and python3 and does not declare a formal permission boundary.

Mitigation: Install dependencies from trusted sources and run the skill in a least-privilege shell or sandbox when stricter controls are required.

## Reference(s):

- [Hacker News skill page](https://clawhub.ai/gchapim/skills/hackernews)
- [gchapim publisher profile](https://clawhub.ai/user/gchapim)
- [Hacker News API Reference](references/api.md)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/)
- [Algolia Hacker News Search API](https://hn.algolia.com/api/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Plain text or JSON from CLI commands, often summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports raw JSON output with --json; default output is human-readable terminal text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
