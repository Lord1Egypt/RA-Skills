## Description:

Searches public Xiaohongshu notes by keyword, supports content-type, sort, and time filters, and returns note titles, authors, engagement data, comments, creator posts, and links for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content creators, and analysts use this skill to retrieve public Xiaohongshu keyword results, note details, comments, and creator post lists for content research, competitive monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Guaikei API token and Xiaohongshu query or link data are sent to www.guaikei.com, and the current token handling may expose the token in request URLs or logs.

Mitigation: Use a scoped, revocable GUAIKEI_API_TOKEN, rotate it if already used, and review request and local logs before and after installation.

Risk: Fetched public Xiaohongshu data is saved under the skill's logs directory.

Mitigation: Treat local logs as potentially sensitive work product and apply retention, access, and deletion practices appropriate for the user's organization.

Risk: The skill depends on a third-party API service for Xiaohongshu data retrieval.

Mitigation: Confirm data-sharing authorization and acceptable use for the Guaikei service before running commands with customer, campaign, or competitor research inputs.

## Reference(s):

- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei API Site](https://www.guaikei.com)
- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and saves fetched public data under the skill's logs directory.]

## Skill Version(s):

1.0.0 (source: frontmatter metadata, package.json, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
