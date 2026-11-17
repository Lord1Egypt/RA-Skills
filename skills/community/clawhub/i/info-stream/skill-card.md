## Description:

Daily News Collector helps an agent set up an automated daily news digest that collects, curates, caches, and distributes industry news through scheduled jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgy2020](https://clawhub.ai/user/lgy2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to configure an agent to collect, curate, cache, and distribute daily news digests for a chosen topic through scheduled collection and delivery tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled jobs may be created or run in an unexpected environment.

Mitigation: Confirm the intended cron schedule, execution environment, chat destination, and weekly news file location before enabling the collection and distribution jobs.

Risk: The Tavily API key could be exposed if stored directly in prompts, scripts, or shared files.

Mitigation: Store TAVILY_API_KEY only in an appropriate environment or secrets location and avoid embedding it in generated reports or repository files.

Risk: Private or sensitive search topics may be sent to an external search provider.

Mitigation: Use non-sensitive topics for automated searches unless the organization has approved the external provider and data handling requirements.

Risk: Overlapping collection runs may duplicate or overwrite a daily report.

Mitigation: Keep collection as the only write path, keep distribution read-only, and check for the current date header before writing.

Risk: Generated news summaries may be incomplete, stale, or misleading.

Mitigation: Prefer original sources, include clickable URLs for each story, and cross-reference important items before relying on the digest.

## Reference(s):

- [Daily News Collector on ClawHub](https://clawhub.ai/lgy2020/skills/info-stream)
- [Usage Guide](artifact/references/usage-guide.md)
- [Tavily API Setup](artifact/references/tavily-setup.md)
- [Information Source Reference](artifact/references/sources.md)
- [Tavily](https://tavily.com)
- [WebKit Blog](https://webkit.org/blog/)
- [V8 Blog](https://v8.dev/blog)
- [Mozilla Hacks](https://hacks.mozilla.org/)
- [Chromium Blog](https://blog.chromium.org/)
- [Hacker News](https://news.ycombinator.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cron schedules, weekly Markdown cache files, and Tavily API configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
