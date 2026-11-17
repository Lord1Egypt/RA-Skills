## Description:

This skill helps agents retrieve and analyze public Xiaohongshu notes, comments, keyword search results, and author posts, returning structured JSON for content research and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External content creators, brand marketers, market analysts, and agent developers use this skill to collect public Xiaohongshu data for trend monitoring, competitor analysis, KOL screening, comment analysis, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Xiaohongshu links, and returned public datasets are sent to the Guaikei API.

Mitigation: Use only when data sharing with the Guaikei API is authorized, and keep GUAIKEI_API_TOKEN private.

Risk: Saved JSON logs may contain research topics, monitored profiles, comments, and token-bearing Xiaohongshu URLs.

Mitigation: Restrict access in shared workspaces and periodically delete or secure the logs directory.

Risk: The skill is intended for public Xiaohongshu data and internal or team analysis, not private, hidden, login-only, or unlawfully redistributed data.

Mitigation: Run it only against public content and review intended use against applicable platform, organizational, and legal requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-note-comment-tool)
- [Guaikei API service](https://www.guaikei.com)
- [Parameter and command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON and save JSON logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, comment, and author profile inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
