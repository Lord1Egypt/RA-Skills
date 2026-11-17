## Description:

Searches Xiaohongshu public notes by keyword, fetches note details and comments, and retrieves creator post lists for content research, competitor monitoring, KOL screening, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, analysts, and agent developers use this skill to retrieve structured public Xiaohongshu data for topic research, competitor monitoring, creator analysis, and comment insight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Guaikei token, Xiaohongshu URLs, keywords, and retrieved public-content data to guaikei.com.

Mitigation: Install only when this data transfer is acceptable; treat GUAIKEI_API_TOKEN as sensitive and avoid exposing it in shared output.

Risk: Retrieved social-media data is automatically saved locally and may include research history, commenter or author data, and xsec_token-bearing URLs.

Mitigation: Protect or delete saved result files and avoid sharing the logs/ directory without review.

Risk: The authoritative security verdict is suspicious because of token handling and local data persistence behavior.

Mitigation: Review the skill and its data-handling expectations before deployment, then run it in an environment appropriate for sensitive tokens and collected data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-rednote-insight)
- [Guaikei service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Files, Guidance]

**Output Format:** [Structured JSON on stdout, with optional concise summaries and saved JSON result files under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; supports keyword, note URL, creator profile URL, filter, sort, time range, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
