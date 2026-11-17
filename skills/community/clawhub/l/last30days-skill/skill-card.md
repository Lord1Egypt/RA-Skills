## Description:

Research any topic across Reddit, X, YouTube, and the web from the last 30 days, then synthesize findings into expert answers and copy-paste-ready prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsondevops](https://clawhub.ai/user/johnsondevops)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to research current discussions, recommendations, news, and prompt techniques, then receive concise synthesis or prompts for a target tool. The open variant can also track watchlists, generate briefings, and query accumulated research history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X search may read browser login cookies.

Mitigation: Prefer explicit API-key or manually supplied-token modes, review the cookie-auth dependency path, and enable X cookie auth only on machines where that access is acceptable.

Risk: Research topics and results may be written to local SQLite databases, briefing files, or temporary output.

Mitigation: Avoid sensitive topics on shared machines, restrict file permissions, and review output and temp-file handling before deployment.

Risk: Outbound search requests send topic strings to third-party providers.

Mitigation: Treat query text as data shared with the configured providers and disable optional providers that are not approved for the deployment.

Risk: Server security verdict is suspicious because of under-disclosed dependency and file-handling risks.

Mitigation: Audit bundled scripts and vendored dependencies, pin reviewed versions, and scan before installation or release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsondevops/skills/last30days-skill)
- [Project homepage](https://github.com/mvanhorn/last30days-skill)
- [One-Shot Research Mode](variants/open/references/research.md)
- [Watchlist Management](variants/open/references/watchlist.md)
- [Morning Briefing](variants/open/references/briefing.md)
- [History and Knowledge Query](variants/open/references/history.md)
- [Open Claw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured summaries and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local command invocations, source stats, citations by platform handle/subreddit/channel, and copy-paste-ready prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
