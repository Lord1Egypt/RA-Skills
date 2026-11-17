## Description:

Searches public Xiaohongshu content, note details, comments, and creator posts through the Guaikei service so agents can support content research, competitor analysis, KOL screening, and trend discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, market researchers, and analysts use this skill to collect public Xiaohongshu data for keyword research, note and comment analysis, creator monitoring, competitor analysis, and trend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, target URLs, and the GUAIKEI API token are sent to the Guaikei service.

Mitigation: Use the skill only when that data flow is acceptable; avoid sensitive targets and rotate the token if exposure is suspected.

Risk: Token-bearing URLs and collected Xiaohongshu data may be saved in generated logs.

Mitigation: Review or delete the logs directory after use, avoid shared or CI workspaces, and restrict access to generated output files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-explorer)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Structured JSON results with optional Markdown summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; outputs may include Xiaohongshu keywords, target URLs, public content metadata, comments, author details, and local log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
