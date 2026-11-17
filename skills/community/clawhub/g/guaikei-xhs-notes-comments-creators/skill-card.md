## Description:

Retrieves public Xiaohongshu note search results, note details, comments, and creator posts through Guaikei API-backed Node.js commands, returning structured JSON for content research and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, analysts, and creator-management teams use this skill to collect public Xiaohongshu data for topic research, competitor monitoring, KOL screening, trend tracking, and comment review. The skill prepares source data for downstream summaries, reports, and structured analysis rather than making final marketing decisions on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei API token, Xiaohongshu keywords, and Xiaohongshu URLs to the Guaikei service.

Mitigation: Install only when this data sharing is acceptable, use a scoped token where possible, and rotate the token if it may have been exposed.

Risk: Tokenized Xiaohongshu links and retrieved public content may be written to local JSON logs.

Mitigation: Treat the logs directory as sensitive, avoid committing logs, and delete or protect logs after analysis.

Risk: The artifact behavior places API credentials in request query strings.

Mitigation: Prefer a future version that sends credentials in headers or a request body and redacts token-like values from saved outputs.

Risk: The skill is limited to public Xiaohongshu data and may return empty or error results for private, deleted, unavailable, or misclassified links.

Mitigation: Confirm inputs are public and match the intended command type; use the JSON status and error fields before drawing conclusions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-notes-comments-creators)
- [Guaikei service site](https://www.guaikei.com)
- [Options Reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful command results are also saved as JSON log files under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
