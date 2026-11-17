## Description:

Monitors and fetches Hacker News stories through the official API, including top, new, best, Ask, Show, Jobs, item, user, and keyword search views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve and summarize current Hacker News stories, user profiles, and search results from the public Hacker News API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency drift or vulnerable transitive packages could affect the CLI runtime.

Mitigation: Update and pin dependencies before deployment, then rescan the release artifact.

Risk: Text returned by Hacker News can contain untrusted user-generated content that is printed in a terminal.

Mitigation: Sanitize story and profile text before display, especially when rendering HTML-derived fields.

Risk: Broad activation phrases could trigger this public-network helper outside an HN-specific workflow.

Mitigation: Use narrow Hacker News-specific activation phrases for agent routing.

## Reference(s):

- [HN Reader on ClawHub](https://clawhub.ai/runawaydevil/skills/hn-reader)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public-network requests to the Hacker News API; no authentication required.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
