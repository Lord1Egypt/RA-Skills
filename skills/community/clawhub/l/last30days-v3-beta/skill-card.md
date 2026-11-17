## Description:

Researches topics across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, Perplexity, and other sources, then scores surfaced items by engagement and market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, researchers, and operators use this skill to collect recent public signals about a topic, synthesize a research report, maintain watchlists, generate briefings, and query accumulated findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied topics can flow into shell commands during research execution.

Mitigation: Review generated commands before execution and quote or sanitize topic arguments.

Risk: Search topics and related context may be sent to configured third-party research, search, and social data services.

Mitigation: Avoid sensitive topics and use dedicated API keys with least-privilege account access.

Risk: GitHub setup paths may send a GitHub token to ScrapeCreators.

Mitigation: Avoid setup --github unless that transfer is acceptable; prefer dedicated API keys or device authorization.

Risk: Research data, preferences, briefings, and settings can be stored on the local machine.

Mitigation: Review local storage locations and file permissions before using persistent watchlist, briefing, or store modes.

Risk: Optional dependency installation may modify the local environment.

Mitigation: Install yt-dlp manually using the user's preferred package manager and review setup actions before running them.

## Reference(s):

- [One-Shot Research Mode](references/research.md)
- [Watchlist Management](references/watchlist.md)
- [Morning Briefing](references/briefing.md)
- [History & Knowledge Query](references/history.md)
- [ClawHub skill page](https://clawhub.ai/mvanhorn/skills/last30days-v3-beta)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports, briefing summaries, watchlist status tables, and optional command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save raw research and accumulated findings locally when storage flags or watchlist modes are used.]

## Skill Version(s):

3.0.0-open (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
