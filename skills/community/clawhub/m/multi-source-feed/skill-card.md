## Description: <br>
Set up and manage an AI-curated daily tech brief from customizable sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zidooong](https://clawhub.ai/user/zidooong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install, configure, and schedule a personalized daily technology brief from X/Twitter, Hacker News, GitHub Trending, RSS feeds, Reddit, Product Hunt, Tavily search, and related sources. It supports customizing source lists, reader preferences, memo format, and optional real-time X/Twitter highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a reusable logged-in X/Twitter browser session for scraping. <br>
Mitigation: Treat x_session.json as a secret, restrict access to the project directory, exclude the session file from backups and version control, and delete or revoke the session when the skill is no longer used. <br>
Risk: The skill sets up recurring local scraping jobs with weak safety controls. <br>
Mitigation: Review cron entries before enabling them, monitor local scrape logs, and disable scheduled jobs if scraping behavior or source access becomes undesirable. <br>
Risk: The skill uses API keys for selected sources. <br>
Mitigation: Store .env as a secret, avoid committing it, and rotate Tavily or Product Hunt credentials if they may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zidooong/multi-source-feed) <br>
- [Project homepage](https://github.com/zidooong/multi-source-feed) <br>
- [Tavily API](https://tavily.com) <br>
- [Product Hunt API documentation](https://api.producthunt.com/v2/docs) <br>
- [Architecture documentation](docs/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands, configuration edits, generated JSON feed files, and daily brief Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python setup, API keys for selected sources, and an X/Twitter browser session when X/Twitter sources are enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
