## Description:

Set up and manage an AI-curated daily tech brief from customizable sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zidooong](https://clawhub.ai/user/zidooong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to set up a personalized daily technology brief that fetches, deduplicates, filters, and summarizes items from X/Twitter, Hacker News, GitHub Trending, RSS feeds, Reddit, Product Hunt, Tavily, and related sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves reusable X/Twitter session cookies locally for authenticated scraping.

Mitigation: Use a dedicated browser profile, protect x_session.json, exclude it from version control, and revoke the X session if it is exposed.

Risk: The skill stores API keys in a local .env file.

Mitigation: Protect and exclude .env from version control, and rotate the keys if the file is exposed.

Risk: The skill can install recurring scraping and push jobs.

Mitigation: Review scheduled jobs before enabling them and disable the cron jobs when the brief is no longer needed.

Risk: Authenticated scraping may process personalized timeline content.

Mitigation: Install only if the user is comfortable with local automation accessing their personalized X/Twitter feed.

## Reference(s):

- [Multi-Source Feed homepage](https://github.com/zidooong/multi-source-feed)
- [ClawHub skill page](https://clawhub.ai/zidooong/skills/multi-source-feed)
- [Architecture documentation](artifact/docs/architecture.md)
- [Tavily](https://tavily.com)
- [Product Hunt API documentation](https://api.producthunt.com/v2/docs)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local feed JSON files, scheduled jobs, and memo markdown when the setup and runtime commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
