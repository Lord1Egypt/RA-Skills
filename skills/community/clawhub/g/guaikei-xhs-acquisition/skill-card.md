## Description:

Searches public Xiaohongshu notes by keyword, retrieves note details and comments, and monitors public profile posts for structured content research and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and agent workflows use this skill to collect public Xiaohongshu search results, note details, comments, and public profile posts for topic research, trend monitoring, competitor analysis, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note URLs, profile URLs, and retrieved public data to the Guaikei API.

Mitigation: Install and run it only when that external data sharing is acceptable for the user, workspace, and task.

Risk: GUAIKEI_API_TOKEN and xsec_token-bearing URLs are sensitive and may appear in command inputs or generated logs.

Mitigation: Use private workspaces, restrict token access, avoid shared shells or logs, and clean the generated logs directory when needed.

Risk: The skill is limited to public Xiaohongshu data and may fail or return empty results for invalid, private, deleted, or unsupported links.

Mitigation: Validate inputs before execution, ask for full note or profile URLs when short links are ambiguous, and avoid fabricating analysis when results are empty or errors occur.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-acquisition)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON results from the command-line tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
