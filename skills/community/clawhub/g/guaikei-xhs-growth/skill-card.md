## Description:

Searches public Xiaohongshu notes, note details, comments, and creator posts, returning structured data for trend research, competitor analysis, KOL screening, and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content creators, and analysts use this skill to collect public Xiaohongshu data for content ideation, competitor monitoring, comment analysis, creator research, and trend discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN, search terms, and Xiaohongshu links to guaikei.com.

Mitigation: Use only when that data sharing is acceptable, scope the token to the intended use, and rotate the token if request data may have been exposed.

Risk: Xiaohongshu links can include xsec_token values that should be treated as sensitive.

Mitigation: Avoid sharing those URLs in shared workspaces, logs, tickets, or CI output, and redact them before redistribution.

Risk: The skill can save full retrieved results to local JSON log files.

Mitigation: Run it in a private workspace, restrict access to the logs directory, and delete retained outputs when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-growth)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API portal](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with Node.js CLI commands; successful executions return structured JSON and may save JSON result files locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, creator URL, sorting, time range, content type, and result limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package metadata report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
